/**
 * Maximum Power Point Tracker Project
 * 
 * File: main.cpp
 * Author: Matthew Yu
 * Organization: UT Solar Vehicles Team
 * Created on: September 10th, 2020
 * Last Modified: 9/26/20
 * 
 * Program Discription: This program is meant to run on the STM32 L432KC Nucleo
 * uC that controls the MPPT board. It manages the power parameters of the
 * subarray, seeking to optimize power transfer to the BMS (Battery Management
 * System).
 * 
 * This program is designed to test and use various MPPT algorithms. These are
 * further described in their respective files in the mppt/ folder.
 */

/*
A couple of things here. Our MPPT takes in the following inputs:
- Voltage Sensor (Array Side)
- Current Sensor (Array Side)
- Voltage Sensor (Battery Side)
- Current Sensor (Battery Side)

At the moment, we don't really need to touch the battery side of things for now.

The MPPT provides the following output:
- Pulse Width as a function of output voltage. 

This goes into our DC-DC Converter, which also needs to be maintained by the
Nucleo. The DC-DC converter shifts our pulse width input into a voltage output
across the PV.

This is our basic feedback loop.
*/

#include <chrono>
#include "mbed.h"
#include "sensor/currentSensor.h"
#include "sensor/voltageSensor.h"
#include "mppt/mppt.h"
#include "mppt/PandO.h"
#include "mppt/IC.h"
#include "mppt/FC.h"
#include "CAN/CAN.h"
#include "dcdcconverter/DcDcConverter.h"

#define CAN_INT_PERIOD 50000        // 50 ms
#define SENSOR_INT_PERIOD 200000    // 200 ms
#define MPPT_INT_PERIOD 50000       // 50 ms
#define DC_DC_INT_PERIOD 50000      // 50 ms
#define PIPELINE_PERIOD 25000       // 25 ms

void manage_pipeline();

// initialize CAN
CANDevice can(PA_0, PA_0);

// initialize LEDs
DigitalOut boardLED(LED1); // D13 I think
DigitalOut trackingLED(D11);
DigitalOut batteryFullLED(D12);

// initialize voltage and current sensors
VoltageSensor sensorArrayVoltage(PA_0);
VoltageSensor sensorBattVoltage(PA_0);
CurrentSensor sensorArrayCurrent(PA_0);
CurrentSensor sensorBattCurrent(PA_0);
// initialize MPPT
PandO pando(PA_0);
IC ic(PA_0);
FC fc(PA_0);
Mppt* mppt;
// initialize DC-DC converter
Dcdcconverter converter(PA_0);

int main(void) {
    // this running boolean can be shut down in various events.
    bool running = true;

    // startup CAN
    can.start(CAN_INT_PERIOD);
    // startup sensor interrupts
    sensorArrayVoltage.start(SENSOR_INT_PERIOD);
    sensorBattVoltage.start(SENSOR_INT_PERIOD);
    sensorArrayCurrent.start(SENSOR_INT_PERIOD);
    sensorBattCurrent.start(SENSOR_INT_PERIOD);
    // startup MPPT - we assign the reference to the derived class to avoid possible object slicing
    mppt = &pando;
    mppt->enable_tracking(MPPT_INT_PERIOD);
    // startup DC-DC converter
    converter.start(DC_DC_INT_PERIOD);

    // main process loop
    while (running) {
        // read in CAN bus buffer to see if we have any messages
        char* msg = can.getMessage();
        if (strcmp(msg, "") != 0) {
            // check for start and stop commands
            if (strcmp(msg, "MPPT_START") == 0) {
                mppt->enable_tracking(MPPT_INT_PERIOD);
            } else if (strcmp(msg, "MPPT_STOP") == 0) {
                mppt->disable_tracking();
            }

            // TESTING
            // check for algorithm change 
            else if (strcmp(msg, "MPPT_PANDO") == 0) {
                // shut down current algorithm
                mppt->disable_tracking();
                // swap reference
                mppt = &pando;
                // start up new algorithm
                mppt->enable_tracking(MPPT_INT_PERIOD);
            } else if (strcmp(msg, "MPPT_IC") == 0) {
                // shut down current algorithm
                mppt->disable_tracking();
                // swap reference
                mppt = &ic;
                // start up new algorithm
                mppt->enable_tracking(MPPT_INT_PERIOD);
            } else if (strcmp(msg, "MPPT_FC") == 0) {
                // shut down current algorithm
                mppt->disable_tracking();
                // swap reference
                mppt = &fc;
                // start up new algorithm
                mppt->enable_tracking(MPPT_INT_PERIOD);
            }
        }
        // TODO: send out CAN bus messages if needed
        // TODO: look for conditions that may cause failure

        // free the allocated CAN message.
        delete[] msg;

        // run the pipeline
        manage_pipeline();
    }
    
    // shutdown sensor
    sensorArrayVoltage.stop();
    sensorBattVoltage.stop();
    sensorArrayCurrent.stop();
    sensorBattCurrent.stop();
    // shutdown DC-DC converter
    converter.stop();
    // shutdown MPPT
    mppt->disable_tracking();
    // shutdown CAN
    can.stop();
}

/**
 * manage_pipeline routes data changes from each step in the pipeline (sensor ->
 * mppt -> dc-dc converter).
 */
void manage_pipeline() {
    // grab the sensor data
    float vArr = sensorArrayVoltage.get_value();
    float vBatt = sensorBattVoltage.get_value();
    float cArr = sensorArrayCurrent.get_value();
    float cBatt = sensorBattCurrent.get_value();
    // pipe it into the MPPT
    mppt->set_inputs(vArr, cArr, vBatt, cBatt);
    // pipe MPPT output into the DC-DC converter
    double targetVoltage = mppt->get_target_voltage();
    converter.set_pulse_width(targetVoltage);
}
