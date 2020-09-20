/**
 * Maximum Power Point Tracker Project
 * 
 * File: mppt.cpp
 * Author: Matthew Yu
 * Organization: UT Solar Vehicles Team
 * Created on: September 10th, 2020
 * Last Modified: 9/11/20
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
 * placeholder process function which is inherited and implemented by children classes.
 */
void Mppt::process() {}


/**
 * determines the amount to travel from the current array voltage position to
 * reach the mppt.
 * TODO: implement the adaptive and default modes according to
 * TODO: sim/src/mppt_algorithms/mppt.py -> calc_perturb_amt()
 * 
 * @param arrayVoltage (double)
 *      array voltage
 * @param arrayCurrent (double)
 *      array current
 * @param irradiance (double)
 *      array irradiance
 * @param temperature (double)
 *      array temperature
 * 
 * @return expected voltage applied over the array (double)
 */
double Mppt::calculate_perturb_amount(Mode mode, double arrayVoltage, double arrayCurrent, double irradiance, double temperature) {
    switch (mode) {
        ADAPTIVE:
            return 0.0;
        default:
        DEFAULT:
            // fixed stride
            return 0.1;
    }
}

/**
 * sets the inputs for the MPPT algorithm to process at the next interrupt.
 * 
 * @param arrayVoltage (double)
 *      array voltage
 * @param arrayCurrent (double)
 *      array current
 * @param battVoltage (double)
 *      battery voltage
 * @param battCurrent (double)
 *      battery current
 */
void Mppt::set_inputs(double arrayVoltage, double arrayCurrent, double battVoltage, double battCurrent) {
    while (inputLock);
    inputLock = true;
    this->arrayVoltage = arrayVoltage;
    this->arrayCurrent = arrayCurrent;
    this->battVoltage = battVoltage;
    this->battCurrent = battCurrent;
    inputLock = false;
}

/**
 * returns the latest target voltage of the Mppt algorithm.
 * 
 * @note This method may stall until the lock on the variable is released, which
 * means the Mppt has uploaded the new value into it.
 * 
 * @return target voltage (double)
 */
double Mppt::get_target_voltage() {
    while (PWLock);
    return targetVoltage;
}

/**
 * sets up a timed interrupt to begin Mppt processing given an interval in uS.
 * Also starts the tracking LED.
 * 
 * @param interval (int)
 *      interval for the interrupt to trigger, in microseconds
 * 
 * @note: the interval should be at least 1% of the 
 */
void Mppt::enable_tracking(int interval) {
    if (!tracking) {
        tick.attach(callback(this, &Mppt::process), std::chrono::microseconds(interval));
        trackingLED = 1;
        tracking = true;
    }
}

/**
 * disables the timed interrupt and the Dc-dc converter pulse stops iterating. Also
 * turns off the tracking LED.
 */
void Mppt::disable_tracking() {
    tick.detach();
    trackingLED = 0;
    tracking = false;
}

/**
 * returns the name of the mppt algorithm.
 */
string Mppt::get_name() { return "None"; }