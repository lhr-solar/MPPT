/**
 * Maximum Power Point Tracker Project
 * 
 * File: sensor.cpp
 * Author: Matthew Yu
 * Organization: UT Solar Vehicles Team
 * Created on: September 10th, 2020
 * Last Modified: 9/11/20
 * 
 * File Discription: This file implements functions defined for the Sensor
 * class.
 */
#include "sensor.h"

Sensor::Sensor(const PinName pin) : sensor(pin) {
    adcValue = 0.0;
    lock = false;
}

void Sensor::set_reference_voltage(const float voltageReference) {
    sensor.set_reference_voltage(voltageReference);
}

const double Sensor::get_value() {
    while (lock);
    return adcValue;
}

void Sensor::start(const int interval) {
    tick.attach(callback(this, &Sensor::measure), std::chrono::microseconds(interval));
}

void Sensor::stop() {
    tick.detach();
}
