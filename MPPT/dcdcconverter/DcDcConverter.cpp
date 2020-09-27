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

Dcdcconverter::Dcdcconverter(PinName pin) : pwm(pin) {            
    PWLock = false;
    battVoltageLock = false;
    pulseWidth = 0.0;
    arrVoltage = 0.0;
    battVoltage = 0.01;
}

void Dcdcconverter::set_pulse_width(double arrVoltage) {
    this->arrVoltage = arrVoltage;

    // Okay since this isn't an interrupt. Plus the relevant lock code is very short.
    while (battVoltageLock);
    
    // convert voltage into pulse width
    double pulseWidthRes = 0.0;
    if (this->arrVoltage > 0.0) {
        pulseWidthRes = 1 - this->battVoltage / this->arrVoltage;
    }

    PWLock = true;
    this->pulseWidth = pulseWidthRes;
    PWLock = false;
}

void Dcdcconverter::set_batt_voltage(double battVoltage) {
    battVoltageLock = true;
    this->battVoltage = battVoltage;
    battVoltageLock = false;
}

double Dcdcconverter::get_pulse_width() {
    while (PWLock);
    return pulseWidth;
}

void Dcdcconverter::start(int interval) {
    tick.attach(callback(this, &Dcdcconverter::handler), std::chrono::microseconds(interval));
}

void Dcdcconverter::stop() {
    tick.detach();
}

/** Private Methods. */

void Dcdcconverter::handler() {
    if (PWLock) return;
    pwm.write((float) pulseWidth);
}
