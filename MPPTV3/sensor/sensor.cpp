/**
 * Maximum Power Point Tracker Project
 * 
 * File: sensor.cpp
 * Author: Matthew Yu
 * Organization: UT Solar Vehicles Team
 * Created on: September 10th, 2020
 * Last Modified: 10/11/20
 * 
 * File Discription: This file implements functions defined for the Sensor
 * class.
 */
#include "sensor.h"

/**
 * sets the reference voltage for the AnalogIn data member. You can read more
 * about it here:
 * https://os.mbed.com/docs/mbed-os/v6.2/mbed-os-api-doxy/classmbed_1_1_analog_in.html#a9f0645e8673d582b544afba07253a424
 * 
 * @param voltageReference (float)
 *      reference voltage for the AnalogIn data member.
 */
void Sensor::set_reference_voltage(float voltageReference) {
    sensor.set_reference_voltage(voltageReference);
}

/**
 * returns the latest value of the sensor, scaled appropriately
 * 
 * @note This method may stall until the lock on the variable is released, which
 * means the sensor has uploaded the new value into it.
 * 
 * @return sensor value (double)
 */
double Sensor::get_value() {
    while (lock);
    return adcValue;
}

/**
 * sets up a timed interrupt to begin measuring from the sensor given an
 * interval in uS.
 * 
 * @param interval (int)
 *      interval for the interrupt to trigger, in microseconds
 */
void Sensor::start(int interval) {
    tick.attach(callback(this, &Sensor::measure), std::chrono::microseconds(interval));
}

/**
 * disables the timed interrupt and the sensor stops sensing.
 */
void Sensor::stop() {
    tick.detach();
}
