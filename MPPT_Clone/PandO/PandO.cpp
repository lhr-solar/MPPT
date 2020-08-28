/*******************************************************************************
 * PandO.cpp
 *
 * P&O Algorithm functions
 * Fall 2017 MPPT using the Nucleo-L432KC (Pholociraptor)
 * 
 * Author: Samantha Guu
 * Team: Samuel Chiu, Madeline Drake, Kyle Grier, Rafael Ibanez, Chase Lansdale,
 *       Brooks Loper
 * Created on: November 12, 2017
 * Revised on: November 14, 2017
 ******************************************************************************/
 
#include "mbed.h"
#include "FastPWM.h"
#include "math.h"

#include "constants.h"
#include "Sensors.h"
#include "PandO.h"

#define true                 1
#define false                0

// tracking
static int trackingOn = true;  //controls whether tracking updates PWM

// timing sections of code
Timer timer;


// Variables for calculations and measurements
static float voltageIn = 0;
static float currentIn = 0;
static float voltageOut = 0;
static float currentOut = 0;
static float lastPower = 0;     // Last Power Measurment
static float lastVoltage = 0;   // Last Voltage Measurment
static float inPower;
static float outPower;
double samples_power[NUM_SAMPLES_TO_AVERAGE];
double samples_voltage[NUM_SAMPLES_TO_AVERAGE];
int sample_idx = 0;


// PWM Related Variables
int pulseWidth;                 // Holds the current pulsewidth in us
double pw = 28;
int direction = 0;             // Direction of our adjustment of the pulse width. If direction is 0 then perturb +, o/w -
int incrementor;                // How much we are preturbing our Pulse Width with each adjustment in the desired direction
static FastPWM mypwm(DEFAULT_PWM_PIN);     // Controls the PWM 

DigitalOut myBat(PB_4);
DigitalOut myTrack(PB_5);

double getPandOPulseWidth()
{
    return pw;
}

// *********************** toggleHeartbeat ******************************************
// This function toggles an LED to show that the program is running
// Inputs: none
// Outputs: none
// Errors: none
// *****************************************************************************
void toggleHeartbeat(){
}
    
// *********************** PandO_Init ******************************************
// This function initializes anything needed the for P&O algo
// Inputs: none
// Outputs: none
// Errors: none
// *****************************************************************************
void PandO_Init()
{
    if(useTime) {timer.start();}
    
    mypwm.period_us(PWM_PERIOD_us);           // Set the PWM period, in us (double), keeping the duty cycle the same
    mypwm.pulsewidth_us(PWM_PULSEWIDTH_us);   // Set the PWM pulsewidth, in us (double), keeping the period the same
    pulseWidth = 100 * PWM_PULSEWIDTH_us;
    currentDutyCycle = pulseWidth;
    incrementor = STATIC_INCREMENTOR;

}
    
// *********************** averageSamples **************************************
// This subroutine calculates the average value of an array
// Inputs: pointer to an array of doubles
// Outputs: average of the array (double)
// Errors: none
// *****************************************************************************
double averageSamples(double *samples)
{
    double avg = 0;
    for(int i = 0; i < NUM_SAMPLES_TO_AVERAGE; i++)
    {
        avg += samples[i];
    }
    avg = avg / NUM_SAMPLES_TO_AVERAGE;
    return avg;
}
    
// *********************** pulseWidthErrorHandling *****************************
// This function restricts the pulseWidth values
// Inputs: Sensor Readings inVoltage, outVoltage
//         (uses pulseWidth global variable)
// Outputs: none (changes pulseWidth global variable)
// Errors: none
// *****************************************************************************
void pulseWidthErrorHandling()
{
    if(pulseWidth > MAX_PULSE_WIDTH){ pulseWidth = MAX_PULSE_WIDTH;}
    else if(pulseWidth < 0) {pulseWidth = 0;}
}

void updateTrackingStatus(float inVoltage, float outVoltage)
{
    if(outVoltage >= MAX_BATTERY_VOLTAGE)    // output voltage should be kept less than max voltage for battery
    {
        pulseWidth -= incrementor;
        trackingOn = false;
    }
    else if(inVoltage < MIN_BATTERY_VOLTAGE) // disable tracking if the input is disconnected
    {
        trackingOn = false;
    }
    else                                     // safe to engage tracking
    {
        trackingOn = true;
    }   
    updateTrackingLED();
}

void updateTrackingLED()
{
   // if(trackingOn) {trackingOnLED = 1;}
   // else {trackingOnLED = 00;}
}

// ****************************** calc_perturb_amt *****************************
// This function calculates how much to perturb by (for VARIABLE P&O)
// Inputs: Sensor Readings (inCurrent, outCurrent, inVoltage, outVoltage)
// Outputs: none (changes incrementor global variable)
// Errors: none 
// *****************************************************************************
void calc_perturb_amt(float deltaV, float deltaP){
    
    float logfxn = fabsf(log10(fabsf(deltaP) / fabsf(deltaV)));
    if((int) ((SCALING_FACTOR * logfxn) + 0.5) == 0 ||
       (int) ((SCALING_FACTOR * logfxn) + 0.5) > 100) // code "snubber"...ish
    {        
        logfxn = 1;                                            // always have an increment that's not 0 or nan
    }
    
    incrementor = (int) ((SCALING_FACTOR * logfxn) + 0.5);
}

// ****************************** perturb **************************************
// This function handles the perturb part of the algorithm
//  - determines direction to perturb in
//  - perturbs by a constant value (incrementor)
// Inputs: Sensor Readings (inCurrent, outCurrent, inVoltage, outVoltage)
// Outputs: none (changes pulseWidth global variable)
// Errors: none (This function does not care about errors - call 
//               pulseWidthErrorHandling right after this function to do checks)
// *****************************************************************************
void perturb(float newPower){
    if(trackingOn != true){
        return;
    }

    float deltaPower = newPower - lastPower;

    // 2) Based on change in power/voltage, determine perturb direction
    if(deltaPower < 0)
    {
        direction = -1;
    }
    else if(deltaPower >= 0)
    {
        direction = 1;
    }

    // 4) Save new power/voltage for next iteration
    
    // 5) Calculate the new pulsewidth based on perturb direction
    pulseWidth += incrementor * direction;
    
    pc.printf("New power: %f  ", newPower);
    pc.printf("Old power: %f  ", lastPower);
    pc.printf("Delta: %f  ", deltaPower);
    pc.printf("Direction: %d  ", direction);
    pc.printf("New Pulse Width: %f\n\r", pulseWidth);
        lastPower = newPower;
    
}

// ******************************* setPWM **************************************
// This function sets the PWM based on previously calculated pulseWidth
// Inputs: none (uses pulseWidth global variable)
// Outputs: none (changes pw global variable)
// Errors: none
// *****************************************************************************
void setPWM(){
    pw = (double)pulseWidth/100;
    // set PWM pulsewidth, specified in usec (double), keeping period same
    mypwm.pulsewidth_us(pw);
    currentDutyCycle = pulseWidth;
}

// ************************** perturb_and_observe ******************************
// This function directs the flow of the Perturb and Observe algorithm
// Inputs: none (reads in 4 sensor values in subroutines)
// Outputs: none (changes global variable pulseWidth)
// Errors: none (pulseWidth error checks in pulseWidthErrorHandling subroutine)
// *****************************************************************************
int pAndOCounter = 0;
double avgPower = 0;
void perturb_and_observe(void){
    toggleHeartbeat();

    /* Actual reading values */
    currentIn = ReadInCurrent();
    double voltageIn = ReadInVoltage();
    double voltageOut = ReadOutVoltage();
    
    pAndOCounter++;
    
    if (pAndOCounter == NUM_SAMPLES_TO_AVERAGE_SENSOR){         //Perturbing every 5th to get average of power measurements
        avgPower = avgPower/5;
        pAndOCounter = 0;
        
        perturb(avgPower);      //Change header, changed to avgPower instead of newPower
        pulseWidthErrorHandling();
        updateTrackingStatus(voltageIn, voltageOut);
        setPWM();
        avgPower = 0;
    }
    else {
        double newPower = voltageIn * currentIn;
        avgPower += newPower;
    }

 }