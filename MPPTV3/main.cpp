/**
 * Maximum Power Point Tracker Project
 * 
 * File: main.cpp
 * Author: Matthew Yu
 * Organization: UT Solar Vehicles Team
 * Created on: September 10th, 2020
 * Last Modified: 10/11/20
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
#include "mppt/PandO.h"


void manage_pipeline();

// TODO: initialize CAN

// initialize LEDs
DigitalOut boardLED(LED1); // D13 i think
DigitalOut trackingLED(D11);
DigitalOut batteryFullLED(D12);

// initialize voltage and current sensors
VoltageSensor sensorArrayVoltage(PA_0);
VoltageSensor sensorBattVoltage(PA_0);
CurrentSensor sensorArrayCurrent(PA_0);
CurrentSensor sensorBattCurrent(PA_0);
// initialize MPPT
PandO mppt(PA_0);
// TODO: initialize DC-DC converter


int main(void) {
    // this running boolean can be shut down in various events.
    bool running = true;

    // TODO: startup CAN

    // startup sensor interrupts
    sensorArrayVoltage.start(200000); // 200 ms
    sensorBattVoltage.start(200000);
    sensorArrayCurrent.start(200000);
    sensorBattCurrent.start(200000);
    
    // startup MPPT
    mppt.enable_tracking(50000); // 50 ms
    
    // TODO: startup DC-DC converter
    
    // startup the rest of the pipeline to manage data movement
    Ticker pipeline;
    pipeline.attach(manage_pipeline, std::chrono::microseconds(25000)); // 25 ms

    // main process loop
    while (running) {
        // read in CAN bus buffer to see if we have any messages
        // send out CAN bus messages if needed
        // look for conditions that main cause failure
    }
    
    // shutdown sensor
    sensorArrayVoltage.stop();
    sensorBattVoltage.stop();
    sensorArrayCurrent.stop();
    sensorBattCurrent.stop();
    // TODO: shutdown DC-DC converter

    // shutdown MPPT
    mppt.disable_tracking();
    // shutdown pipeline
    pipeline.detach();
    // TODO: shutdown CAN
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
    mppt.set_inputs(vArr, cArr, vBatt, cBatt);
    // pipe MPPT output into the DC-DC converter
    double pulseWidth = mppt.get_pulse_width();
}
