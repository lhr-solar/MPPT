/**
 * Maximum Power Point Tracker Project
 * 
 * File: DcDcConverter.cpp
 * Author: Matthew Yu
 * Organization: UT Solar Vehicles Team
 * Created on: September 10th, 2020
 * Last Modified: 09/26/20
 * 
 * File Discription: This file manages the Dcdcconverter class, which manages
 * the conversion of power from the array to the power management system.
 * There is one exposed function here, which is to take in a pulse width.
 * The DC-DC Converter after starting then continually updates the rate of pulses
 * to the HW circuit based on this pulse width.
 */
#include "DcDcConverter.h"


/** Public Methods. */

Dcdcconverter::Dcdcconverter(const PinName pin) : pwm(pin) {            
    PWLock = false;
    battVoltageLock = false;
    battVoltageLimLock = false;
    pulseWidth = 0.0;
    arrVoltage = 0.0;
    battVoltage = 0.0;
    battVoltageLim = 1000.0; // something out of range of possible battery voltage
}

void Dcdcconverter::set_pulse_width(const double arrVoltage) {
    this->arrVoltage = arrVoltage;

    // Okay since this isn't an interrupt. Plus the relevant lock code is very short.
    while (battVoltageLock || battVoltageLimLock);
    
    // convert voltage into pulse width
    double pulseWidthRes = 0.0;
    if (this->arrVoltage > 0.0) {
        if (this->battVoltage < this->battVoltageLim) {
            pulseWidthRes = 1 - this->battVoltage / this->arrVoltage;
        } else {
            pulseWidthRes = 1 - this->battVoltageLim / this->arrVoltage;
        }
    }

    PWLock = true;
    this->pulseWidth = pulseWidthRes;
    PWLock = false;
}

void Dcdcconverter::set_batt_voltage(const double battVoltage) {
    battVoltageLock = true;
    this->battVoltage = battVoltage;
    battVoltageLock = false;
}

void Dcdcconverter::set_batt_voltage_limit(const double battVoltageLim) {
    battVoltageLimLock = true;
    this->battVoltageLim = battVoltageLim;
    battVoltageLimLock = false;
}

double Dcdcconverter::get_pulse_width() const {
    while (PWLock);
    return pulseWidth;
}

void Dcdcconverter::start(const int interval) {
    tick.attach(callback(this, &Dcdcconverter::handler), std::chrono::microseconds(interval));
}

void Dcdcconverter::stop(){
    tick.detach();
}

/** Private Methods. */

void Dcdcconverter::handler() {
    if (PWLock) return;
    pwm.write((float) pulseWidth);
}
