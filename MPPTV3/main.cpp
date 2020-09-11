/**
 * Maximum Power Point Tracker Project
 * 
 * Author: Matthew Yu
 * Organization: UT Solar Vehicles Team
 * Created on: September 10th, 2020
 * Last Modified: 10/20/20
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
This goes into our DC-DC Converter, which also needs to be maintained by the Nucleo.
The DC-DC converter shifts our pulse width input into a voltage output across the PV.

This is our basic feedback loop.
*/

#include "mbed.h"
#include "sensor/currentSensor.h"
#include "sensor/voltageSensor.h"
#include "mppt/PandO.h"

int main(void) {
    // this running boolean can be shut down in various events.
    bool running = true;

    // setup buffer
    // setup CAN bus

    // setup LEDs
    DigitalOut boardLED(LED1); // D13 i think
    DigitalOut trackingLED(D11);
    DigitalOut batteryFullLED(D12);

    // initialize voltage and current sensors
    VoltageSensor sensorArrayVoltage(PA_0);
    VoltageSensor sensorBattVoltage(PA_0);
    CurrentSensor sensorArrayCurrent(PA_0);
    CurrentSensor sensorBattCurrent(PA_0);
    // initialize MPPT algorithm
    PandO mppt(PA_0);

    // setup timer interrupts
    sensorArrayVoltage.start(200000); // 200 ms
    sensorBattVoltage.start(200000);
    sensorArrayCurrent.start(200000);
    sensorBattCurrent.start(200000);
    
    // setup MPPT polling - every trigger MPPT generates a pulse width that goes to the DC-DC converter that sets it
    mppt.enableTracking(50000); // 50 ms
    
    while (running) {
        // read in CAN bus buffer to see if we have any messages
        // send out CAN bus messages if needed
        // look for conditions that main cause failure
    }

    // detach tickers for sensors
    sensorArrayVoltage.stop();
    sensorBattVoltage.stop();
    sensorArrayCurrent.stop();
    sensorBattCurrent.stop();
    // detach ticker for MPPT
    mppt.disableTracking();
    // shutdown CAN
}