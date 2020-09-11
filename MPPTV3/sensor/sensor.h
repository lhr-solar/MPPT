/**
 * sensor.h
 */
#pragma once
#include "mbed.h"
#include <chrono>


class Sensor {
    protected:
        bool lock;
        float adcValue;
        AnalogIn sensor;
        Ticker tick;
        virtual void measure() = 0;

    public:
        Sensor(PinName pin) : sensor(pin) {
            adcValue = 0.0;
            lock = false;
        }
        void set_reference_voltage(float voltageReference);
        float get_value();
        void start(int interval);
        void stop();
};
