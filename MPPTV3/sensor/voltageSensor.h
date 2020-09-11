/**
 * voltageSensor.cpp
 */
#pragma once
#include "sensor.h"


class VoltageSensor: public Sensor{
    public:
        VoltageSensor(PinName pin) : Sensor(pin) {}
        void measure() {
            float tempValue = sensor.read_voltage();
            // do some processing on the temporary value, maybe even some SW filtering
            lock = true;
            adcValue = tempValue;
            lock = false;
        }
};