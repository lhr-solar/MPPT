/**
 * Maximum Power Point Tracker Project
 * 
 * File: mppt.cpp
 * Author: Matthew Yu
 * Organization: UT Solar Vehicles Team
 * Created on: September 10th, 2020
 * Last Modified: 09/26/20
 * 
 * File Discription: This file implements functions defined for the Mppt
 * class.
 */
#include "mppt.h"

/** Public Methods. */

Mppt::Mppt(const PinName pin) : trackingLED(pin) {
    trackingLED = 0;
    
    tracking = false;
    
    PWLock = false;
    inputLock = false;

    targetVoltage = 0.0;

    arrayVoltage = 0.0;
    arrayCurrent = 0.0;
    battVoltage = 0.0;
    battCurrent = 0.0;
}

void Mppt::set_inputs(
    const double arrayVoltage, 
    const double arrayCurrent, 
    const double battVoltage, 
    const double battCurrent) 
{
    while (inputLock);
    inputLock = true;
    this->arrayVoltage = arrayVoltage;
    this->arrayCurrent = arrayCurrent;
    this->battVoltage = battVoltage;
    this->battCurrent = battCurrent;
    inputLock = false;
}

void Mppt::enable_tracking(const int interval) {
    if (!tracking) {
        tick.attach(callback(this, &Mppt::handler), std::chrono::microseconds(interval));
        trackingLED = 1;
        tracking = true;
    }
}

void Mppt::disable_tracking() {
    tick.detach();
    trackingLED = 0;
    tracking = false;
}

const double Mppt::get_target_voltage() {
    while (PWLock);
    return targetVoltage;
}

/** Private Methods. */

const char* Mppt::get_name() { return "None"; }

void Mppt::handler() {}

void Mppt::update_tracking_LED() {
    if (tracking) {
        trackingLED = !trackingLED;
    }
}

const double Mppt::calculate_perturb_amount(
    const Mode mode, 
    const double arrayVoltage, 
    const double arrayCurrent, 
    const double irradiance, 
    const double temperature) 
{
    switch (mode) {
        ADAPTIVE:
            return 0.0;
        default:
        DEFAULT:
            // fixed stride
            return 0.1;
    }
}