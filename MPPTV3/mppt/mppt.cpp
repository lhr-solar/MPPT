/**
 * mppt.cpp
 */

#include "mppt.h"


void Mppt::updateTrackingLED() {
    if (tracking) {
        trackingLED = !trackingLED;
    }
}


void Mppt::setInputs(float arrayVoltage, float arrayCurrent, float battVoltage, float battCurrent) {
    while (inputLock);
    inputLock = true;
    this->arrayVoltage = arrayVoltage;
    this->arrayCurrent = arrayCurrent;
    this->battVoltage = battVoltage;
    this->battCurrent = battCurrent;
    inputLock = false;
}


double Mppt::getPulseWidth() {
    while (PWLock);
    return pulseWidth;
}


void Mppt::enableTracking(int interval) {
    tick.attach(callback(this, &Mppt::process), std::chrono::microseconds(interval));
    trackingLED = 1;
    tracking = true;
}


void Mppt::disableTracking() {
    tick.detach();
    trackingLED = 0;
    tracking = false;
}