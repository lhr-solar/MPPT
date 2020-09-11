/**
 * Maximum Power Point Tracker Project
 * 
 * File: mppt.cpp
 * Author: Matthew Yu
 * Organization: UT Solar Vehicles Team
 * Created on: September 10th, 2020
 * Last Modified: 10/11/20
 * 
 * File Discription: This file implements functions defined for the Mppt
 * class.
 */
#include "mppt.h"

/**
 * toggles the tracking LED if we're currently running the MPPT.
 */
void Mppt::update_tracking_LED() {
    if (tracking) {
        trackingLED = !trackingLED;
    }
}

/**
 * sets the inputs for the MPPT algorithm to process at the next interrupt.
 * 
 * @param arrayVoltage (float)
 *      array voltage
 * @param arrayCurrent (float)
 *      array current
 * @param battVoltage (float)
 *      battery voltage
 * @param battCurrent (float)
 *      battery current
 */
void Mppt::set_inputs(float arrayVoltage, float arrayCurrent, float battVoltage, float battCurrent) {
    while (inputLock);
    inputLock = true;
    this->arrayVoltage = arrayVoltage;
    this->arrayCurrent = arrayCurrent;
    this->battVoltage = battVoltage;
    this->battCurrent = battCurrent;
    inputLock = false;
}

/**
 * returns the latest pulse width output of the Mppt algorithm.
 * 
 * @note This method may stall until the lock on the variable is released, which
 * means the Mppt has uploaded the new value into it.
 * 
 * @return pulse width value (double)
 */
double Mppt::get_pulse_width() {
    while (PWLock);
    return pulseWidth;
}

/**
 * sets up a timed interrupt to begin Mppt processing given an interval in uS.
 * Also starts the tracking LED.
 * 
 * @param interval (int)
 *      interval for the interrupt to trigger, in microseconds
 */
void Mppt::enable_tracking(int interval) {
    tick.attach(callback(this, &Mppt::process), std::chrono::microseconds(interval));
    trackingLED = 1;
    tracking = true;
}

/**
 * disables the timed interrupt and the Mppt algorithm stops iterating. Also
 * turns off the tracking LED.
 */
void Mppt::disable_tracking() {
    tick.detach();
    trackingLED = 0;
    tracking = false;
}