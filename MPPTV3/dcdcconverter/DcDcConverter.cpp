/**
 * Maximum Power Point Tracker Project
 * 
 * File: DcDcConverter.cpp
 * Author: Matthew Yu
 * Organization: UT Solar Vehicles Team
 * Created on: September 10th, 2020
 * Last Modified: 9/11/20
 * 
 * File Discription: This file manages the Dcdcconverter class, which manages
 * the conversion of power from the array to the power management system.
 * There is one exposed function here, which is to take in a pulse width.
 * The DC-DC Converter after starting then continually updates the rate of pulses
 * to the HW circuit based on this pulse width.
 */
#include "DcDcConverter.h"

void Dcdcconverter::signal() {
    while (PWLock);
    pwm.write((float) pulseWidth);
}

void Dcdcconverter::set_pulse_width(double arrVoltage) {
    this->arrVoltage = arrVoltage;

    // convert voltage into pulse width
    while (battVoltageLock);
    double pulseWidthRes = 0.0;
    if (this->battVoltage > 0.0) {
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
    tick.attach(callback(this, &Dcdcconverter::signal), std::chrono::microseconds(interval));
}

/**
 * disables the timed interrupt and the Mppt algorithm stops processing. Also
 * turns off the tracking LED.
 */
void Dcdcconverter::stop() {
    tick.detach();
}