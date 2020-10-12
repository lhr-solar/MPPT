/**
 * Maximum Power Point Tracker Project
 * 
 * File: Sensor.cpp
 * Author: Matthew Yu
 * Organization: UT Solar Vehicles Team
 * Created on: September 10th, 2020
 * Last Modified: 10/07/20
 * 
 * File Discription: This file implements functions defined for the Sensor
 * class.
 */
#include "Sensor.h"


Sensor::Sensor(const PinName pin) : sensor(pin), filter(10) {
    adcValue = 0.0;
    lock = false;
}

Sensor::Sensor(const PinName pin, const int numFilterSamples) : 
    sensor(pin), filter(numFilterSamples) {
    adcValue = 0.0;
    lock = false;
}

void Sensor::set_reference_voltage(const float voltageReference) {
    sensor.set_reference_voltage(voltageReference);
}

double Sensor::get_value() const {
    while (lock);
    return adcValue;
}

void Sensor::start(const int interval) {
    tick.attach(callback(this, &Sensor::measure), 
        std::chrono::microseconds(interval));
}

void Sensor::stop() {
    tick.detach();
    filter.shutdown();
}
