/**
 * sensor.cpp
 */

#include "sensor.h"


void Sensor::set_reference_voltage(float voltageReference) {
    sensor.set_reference_voltage(voltageReference);
}


float Sensor::get_value() {
    while (lock);
    return adcValue;
}


void Sensor::start(int interval) {
    tick.attach(callback(this, &Sensor::measure), std::chrono::microseconds(interval));
}


void Sensor::stop() {
    tick.detach();
}
