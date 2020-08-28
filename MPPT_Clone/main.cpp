/*******************************************************************************
 * Maximum Power Point Tracker Project for EE 464H
 *
 * Perturb and Observe Algorithm (Revised for discrete pulsewidth incrementor)
 * 
 * Author: Juan Cortez, Angus Ranson
 * Team: Angus Ranson, Muhammad Bukhari, Rana Madkour, Josh Frazor, Zach Pavlich
 * Created on: September 14, 2015 at 14:26
 * Revised on: December 5, 2015 at 18:08
 *
 * Edited by: Kyle Grier, Samantha Guu
 * New Team: Samuel Chiu, Madeline Drake, Kyle Grier, Samantha Guu, 
 *           Rafael Ibanez, Chase Lansdale, Cobie Loper
 * New Team Mentor: Dr. Gary Hallock
 * Last Revised: November 14, 2017
 *
 * GitHub Repository: https://github.com/juancortez-ut/mppt
 *
 * Dependent Hardware: 
 *   - Microcontroller: Freescale FRDM-K64F
 *   - CAN_BUS: CAN-BUS Shield v.1.2 by SEEED Studios
 *
 * Dependent Libraries:
 *   - mbed Library: https://developer.mbed.org/users/mbed_official/code/mbed/
 *   - SEEEED_CAN_LIBRARY: /mppt/FRDM-K64F/CAN_BUS/SEEED_CAN/SEEED_CAN_LIBRARY
 *
 * FRDM-K64F Pinout: https://os.mbed.com/platforms/FRDM-K64F/#board-pinout
 *
 * Signal     | FRDM-K64F Pin   | Purpose
 * -----------------------------------------------------------------------
 * PwmOut     | PTC10           | Output PWM Signal to Boost Converter
 * DigitalOut | LED1            | Heartbeat LED
 * AnalogIn   | PTB3            | Input Hall Sensor
 * AnalogIn   | PTB11           | Output Hall Sensor
 * AnalogIn   | PTB2            | Input Voltage
 * AnalogIn   | PTB10           | Output Voltage
 * RawSerial  | USBTX, USBRX    | Serial Communication
 * 
 * Program Description: This program is written for the Freescale FRDM-K64F uC.
 * The description of the P&O algorithm is found below, in the comment section
 *   titled, 'Perturb & Observe Algorithm'.
 *
 *****************************************************************************************************/

/**
*                                   Perturb & Observe Algorithm
*
* The most widely used algorithm is the P&O algorithm. The P&O algorithm perturbs the duty cycle
* which controls the power converter, in this way it takes steps over the p-v characteristic to 
* find the MPPT. This perturbation causes a new operating point with a different output power. In 
* case this output power is larger than the previous output power, this point is set as the new 
* operating point. In case it is lower, the same power point is adjusted to a lower or higher working 
* voltage, depending on the previous step direction. (http://bit.ly/1L73nzE)
*
*
* Pulse Width (PW) is the elapsed time between the rising and falling edges of a single pulse.
* 
* Pulse Repetition Interval (PRI) is the time between sequential pulses.
*
* Pulse Repetition Frequency (PRF) is the reciprocal of PRI. The basic unit of measure for PRF
* is hertz (Hz). 
*
* Duty Cycle describes the "On Time" for a pulsed signal. We can report duty cycle in units of time, 
* but usually as a percentage. To calculate a signals' duty cycle, we need to know the signal's pulse
* width and repetition frequency.
*
**/
#include "stdlib.h"
#include "mbed.h"
#include "constants.h"
#include "Sensors.h"
#include "PandO.h"
#include "IncrementalVoltage.h"

//#include "CAN_lib.h"
#include "CAN.h"
#include "FastPWM.h"
//Define Constants
#define true                 1
#define false                0

#define MESSAGE_LENGTH       8
#define READING_COUNT        6

#define BUFFER_SIZE 50

#define CAN_RX_PIN PD_0
#define CAN_TX_PIN PD_1
#define MPPT_CAN_ID 100

#define SERIAL_BAUD 115200

#define BATTERY_FULL 135
#define BATTERY_MIN 75
#define ARRAY_MIN 5

DigitalOut myled(LED1);
DigitalOut trackingOn(D11);
DigitalOut batteryFull(D12);

volatile char message[BUFFER_SIZE];
volatile char nextChar;

void getMessage();
void processNewMessage();

volatile uint32_t algorithm = 2;
volatile uint32_t lastAlgorithm = 2;
volatile double lastPWM = 28;
volatile bool newMessage = false;
volatile bool changedFlag = false;

void processNewCanMessage();

#define CAN_BUS_SIZE 200
#define CAN_BUS_BAUD 25000
CAN canBus(D10, D2, CAN_BUS_BAUD); // D10, D2
void canBusHandler(void); 
CANMessage canMessage;
CANMessage newCanMessage;
int canGetIndex = 0;
int canPutIndex = 0;
CANMessage mailBox[CAN_BUS_SIZE];

#define PAUSE_COMMAND "0"
#define RESUME_COMMAND "1"
#define P_AND_O_COMMAND "2"
#define INCREMENTAL_CONDUCTANCE_COMMAND "3"
#define FUZZY_LOGIC_COMMAND   "4"
#define DUTY_CYCLE_COMMAND    "5"
#define CURRENT_IN_COMMAND    "6"
#define CURRENT_OUT_COMMAND   "7"
#define VOLTAGE_IN_COMMAND    "8" 
#define VOLTAGE_OUT_COMMAND   "9"
#define POWER_IN_COMMAND     "10"
#define POWER_OUT_COMMAND    "11"
#define CURRENT_ALGO_COMMAND "12"
#define DUMMY_COMMAND        "13"

#define PAUSE_COMMAND_INT 0
#define RESUME_COMMAND_INT 1
#define P_AND_O_COMMAND_INT 2
#define INCREMENTAL_CONDUCTANCE_COMMAND_INT 3
#define FUZZY_LOGIC_COMMAND_INT 4
#define DUTY_CYCLE_COMMAND_INT 5
#define CURRENT_IN_COMMAND_INT 6
#define CURRENT_OUT_COMMAND_INT 7
#define VOLTAGE_IN_COMMAND_INT 8 
#define VOLTAGE_OUT_COMMAND_INT 9
#define POWER_IN_COMMAND_INT 10
#define POWER_OUT_COMMAND_INT 11
#define CURRENT_ALGO_COMMAND_INT 12
#define DUMMY_COMMAND_INT        13

DigitalOut canTestHeartBeat(LED3);

// A Ticker is used to call a function at a recurring interval
// void Attach(T *tptr, void(T::*mptr)(void), float t)
// Attach a member function to be called by the Ticker, specifying time in secs

Ticker ticker;
Ticker ticker2;
Ticker ticker3;
static FastPWM mypwm(DEFAULT_PWM_PIN);     // Controls the PWM 

void setupAlgorithm();
void testCanFunc();

int frameCount;

int main(void)
{   
    trackingOn = 1;
    pc.attach(&getMessage, Serial::RxIrq);
    canBus.attach(&canBusHandler, CAN::RxIrq);
    batteryFull = 0;
    changedFlag = 1;
    trackingOn = 1;
    setupAlgorithm();
    __enable_irq();
    while(1)
    {
        if(newMessage == true)
        {   
            __disable_irq();
            processNewMessage();
            newMessage = false;
            __enable_irq();
        }
        
        if(changedFlag == true)
        {
            __disable_irq();
            setupAlgorithm();
            changedFlag = false;
            __enable_irq();
        }
        
        if(canGetIndex != canPutIndex)
        {
            __disable_irq();
            processNewCanMessage();
            __enable_irq();    
        }
        
        float output = ReadOutVoltage();
        float input = ReadInVoltage();
        if(output < BATTERY_MIN) {frameCount++;}
        else{frameCount = 0;}
        if(((output >= BATTERY_FULL) || (output < BATTERY_MIN) || (input < ARRAY_MIN)) && (algorithm != 0) && frameCount >= 3) 
        {
            trackingOn = 0;
            if(ReadOutVoltage() >= BATTERY_FULL) {batteryFull = 1;}
            lastAlgorithm = algorithm;
            algorithm = 0;
            changedFlag = true;
            pc.printf("Output voltage: %f\n", output);
            pc.printf("Input voltage: %f\n", input);
            pc.printf("Pausing for Safety Reasons\n\r");
        }

    }
}

void testCanFunc()
{
    char *data = "hello";
    canBus.write(CANMessage(1337, (char*)data, 8));
}

void setupAlgorithm()
{
    if(algorithm == 1)
    {
        algorithm = lastAlgorithm;
    }
        
    if(algorithm == 0)
    {
        ticker.detach();
        mypwm.pulsewidth_us(0);
    }
    
    if(algorithm == 2)
    {
        PandO_Init();
        mypwm.pulsewidth_us(lastPWM);
        ticker.attach(&perturb_and_observe, SAMPLE_PERIOD);
    }
    
    if(algorithm == 3)
    {
        incrementalInit();
        mypwm.pulsewidth_us(lastPWM);
        ticker.attach(&incremental_conductance, SAMPLE_PERIOD); //Incremental conductance
    }
    
}

void getMessage()
{
    myled = 1;

    int index = 0;
    nextChar = 'a';
    while(nextChar != '\n')    
    {
                nextChar = pc.getc();
                if (index < BUFFER_SIZE-1 && nextChar != '\n') 
                {
                    message[index++] = nextChar;
                }
    }
    message[index] = '\0';
    newMessage = true;

    myled = 0;
}

void processNewMessage()
{   
    if(strcmp((char*)message, "Pause") == 0) 
    {
        if(algorithm != 0)
        {
            changedFlag = true;
            trackingOn = 0;
            lastAlgorithm = algorithm;
            algorithm = 0;
            lastPWM = mypwm.read();
            pc.printf("Pausing\n\r");
        }
        else{pc.printf("Already Paused\n\r");}
        return;
    }
    else if(strcmp((char*)message, "Resume") == 0)
    {
        
        if(algorithm == 0)
        {
            changedFlag = true;
            trackingOn = 1;
            algorithm = lastAlgorithm;
            pc.printf("Resuming\n\r");
        }
        else{pc.printf("Already Resumed\n\r");}
        return;
    }     
    else if(strcmp((char*)message, "PandO") == 0)
    {
        if(algorithm != 2)
        {
            changedFlag = true;
            algorithm = 2;
            pc.printf("Switching algorithm to Preturb and Observe\n\r");
        }
        else{pc.printf("Already running Preturb and Observe\n\r");}
        return;
    }     
    else if(strcmp((char*)message, "IncrementalConductance") == 0)
    {
        if(algorithm != 3)
        {
            changedFlag = true;
            algorithm = 3;
            pc.printf("Switching algorithm to Incremental Conductance\n\r");
        }
        else{pc.printf("Already running incremental conductance\n\r");}
        return;
    }    
    else if(strcmp((char*)message, "FuzzyLogic") == 0)
    {
        if(algorithm != 4)
        {
            changedFlag = true;
            algorithm = 4;
            pc.printf("Switching algorithm to Fuzzy Logic\n\r");
        }
        else{pc.printf("Already running Fuzzy Logic\n\r");}
    }
    else if(strcmp((char*)message, "CurrentAlgo") == 0)
    {
        if(algorithm == 0){pc.printf("Current Algorithm: Paused\n\r");}
        else if(algorithm == 1){pc.printf("Current Algorithm: Paused\n\r");}
        else if(algorithm == 2){pc.printf("Current Algorithm: PandO\n\r");}
        else if(algorithm == 3){pc.printf("Current Algorithm: Incremental Voltage\n\r");}
        else if(algorithm == 4){pc.printf("Current Algorithm: FuzzyLogic\n\r");}
    }
    else if(strcmp((char*)message, "DutyCycle") == 0)
    {
        pc.printf("Duty Cycle: %f us\n\r", currentDutyCycle);
    }
    else if(strcmp((char*)message, "VoltageIn") == 0)
    {
        pc.printf("Voltage In: %fV\n\r", ReadInVoltage());
    }
    else if(strcmp((char*)message, "VoltageOut") == 0)
    {
        pc.printf("Voltage Out: %fV\n\r", ReadOutVoltage());
    }
    else if(strcmp((char*)message, "CurrentIn") == 0)
    {
        pc.printf("Current In: %fA\n\r", ReadInCurrent());
    }
    else if(strcmp((char*)message, "CurrentOut") == 0)
    {
        pc.printf("Current Out: %fA\n\r", ReadOutCurrent());
    }
    else if(strcmp((char*)message, "PowerIn") == 0)
    {
        pc.printf("Power In: %fW\n\r", ReadInVoltage() * ReadInCurrent());
    }
    else if(strcmp((char*)message, "PowerOut") == 0)
    {
        pc.printf("Power Out: %fW\n\r", ReadOutVoltage() * ReadOutCurrent());
    }
    else
    {     
        pc.printf("Unknown Command\n\r");
    }
}

void canBusHandler()
{
    myled = 1;
    if(((canPutIndex + 1) % CAN_BUS_SIZE) != canGetIndex)
    {
        canBus.read(newCanMessage);
        mailBox[canPutIndex] = newCanMessage;
        canPutIndex = (canPutIndex + 1) % CAN_BUS_SIZE;
    }
    myled = 0;
}

void processNewCanMessage()
{
    canMessage = mailBox[canGetIndex];
    canGetIndex = (canGetIndex + 1) % CAN_BUS_SIZE;
    if(canMessage.id != MPPT_CAN_ID){return;}
    
    if(strcmp((char*)canMessage.data, "BLINK") == 0)
    {
        if(canTestHeartBeat == 0) {canTestHeartBeat = 1;}
        else{canTestHeartBeat = 0;}
    }
    else if(strcmp((char*)canMessage.data, PAUSE_COMMAND) == 0)
    {
        
        if(algorithm != 0)
        {
            lastAlgorithm = algorithm;
            algorithm = 0;
            changedFlag = true;
            char* data = "1";
            int id = MPPT_CAN_ID + PAUSE_COMMAND_INT;
            canBus.write(CANMessage(id, data, 2));
        }
        else
        {
            char* data = "0";
            canBus.write(CANMessage(MPPT_CAN_ID + PAUSE_COMMAND_INT, data, 2));
        }
        return;
    }
    else if(strcmp((char*)canMessage.data, RESUME_COMMAND) == 0)
    {
        if(algorithm == 0)
        {
            algorithm = lastAlgorithm;
            changedFlag = true;
            char* data = "1";
            canBus.write(CANMessage(MPPT_CAN_ID + RESUME_COMMAND_INT, data, 2));
        }
        else
        {
            char* data = "0";
            canBus.write(CANMessage(MPPT_CAN_ID + RESUME_COMMAND_INT, data, 2));
        }
        return;
    }
    else if(strcmp((char*)canMessage.data, P_AND_O_COMMAND) == 0)
    {
        if(algorithm != 2)
        {
            lastAlgorithm = algorithm;
            algorithm = 2;
            changedFlag = true;
            char *data = "1";
            canBus.write(CANMessage(MPPT_CAN_ID + P_AND_O_COMMAND_INT, data, 8));
        }
        else
        {
            char *data = "0";
            canBus.write(CANMessage(MPPT_CAN_ID + P_AND_O_COMMAND_INT, data, 8)); 
        }
        return;
    }
    else if(strcmp((char*)canMessage.data, INCREMENTAL_CONDUCTANCE_COMMAND) == 0)
    {
        if(algorithm != 3)
        {
            lastAlgorithm = algorithm;
            algorithm = 3;
            changedFlag = true;
            char *data = "1";
            canBus.write(CANMessage(MPPT_CAN_ID + INCREMENTAL_CONDUCTANCE_COMMAND_INT, data, 2));
        }
        else
        {
            char *data = "0";
            canBus.write(CANMessage(MPPT_CAN_ID + INCREMENTAL_CONDUCTANCE_COMMAND_INT, data, 2)); 
        }
        return;
    }
    else if(strcmp((char*)canMessage.data, FUZZY_LOGIC_COMMAND) == 0)
    {
        if(algorithm != 4)
        {
            lastAlgorithm = algorithm;
            changedFlag = true;
            algorithm = 4;
            char *data = "1";
            canBus.write(CANMessage(MPPT_CAN_ID + FUZZY_LOGIC_COMMAND_INT, data, 2));
        }
        else
        {
            char *data = "0";
            canBus.write(CANMessage(MPPT_CAN_ID + FUZZY_LOGIC_COMMAND_INT, data, 2)); 
        }
        return;
    }
    else if(strcmp((char*)canMessage.data, CURRENT_ALGO_COMMAND) == 0)
    { 
        int data[2];
        data[0] = algorithm;
        canBus.write(CANMessage(MPPT_CAN_ID + CURRENT_ALGO_COMMAND_INT, (char*)data, 8));
    }
    else if(strcmp((char*)canMessage.data, DUTY_CYCLE_COMMAND) == 0)
    {
         int data[2]; 
         data[0] = (int)currentDutyCycle;
         canBus.write(CANMessage(MPPT_CAN_ID + DUTY_CYCLE_COMMAND_INT, (char*)data, 4));
         return;
    }
    else if(strcmp((char*)canMessage.data, VOLTAGE_IN_COMMAND) == 0)
    {
         int data[2]; 
         data[0] = ReadInVoltage();
         canBus.write(CANMessage(MPPT_CAN_ID + VOLTAGE_IN_COMMAND_INT, (char*)data, 4));
         return;
    }
    else if(strcmp((char*)canMessage.data, VOLTAGE_OUT_COMMAND) == 0)
    {
         int data[2]; 
         data[0] = ReadOutVoltage();
         canBus.write(CANMessage(MPPT_CAN_ID + VOLTAGE_OUT_COMMAND_INT, (char*)data, 4));
         return;
    }
    else if(strcmp((char*)canMessage.data, CURRENT_IN_COMMAND) == 0)
    {
         int data[2]; 
         data[0] = ReadInCurrent();
         canBus.write(CANMessage(MPPT_CAN_ID + CURRENT_IN_COMMAND_INT, (char*)data, 4));
         return;
    }
    else if(strcmp((char*)canMessage.data, CURRENT_OUT_COMMAND) == 0)
    {
         int data[2]; 
         data[0] = ReadOutCurrent();
         canBus.write(CANMessage(MPPT_CAN_ID + CURRENT_OUT_COMMAND_INT, (char*)data, 4));
         return;
    }
    else if(strcmp((char*)canMessage.data, POWER_IN_COMMAND) == 0)
    {
         int data[2]; 
         data[0] = ReadInVoltage() * ReadInCurrent();
         canBus.write(CANMessage(MPPT_CAN_ID + POWER_IN_COMMAND_INT, (char*)data, 4));
         return;
    }
    else if(strcmp((char*)canMessage.data, POWER_OUT_COMMAND) == 0)
    {
         int data[2]; 
         data[0] = ReadOutVoltage() * ReadOutCurrent();
         canBus.write(CANMessage(MPPT_CAN_ID + POWER_OUT_COMMAND_INT, (char*)data, 4));
        return;
    }
    else if(strcmp((char*)canMessage.data, DUMMY_COMMAND) == 0)
    {
        char data[4] = "Dum";
        canBus.write(CANMessage(MPPT_CAN_ID + DUMMY_COMMAND_INT, data, 4));
        return;
    }
}