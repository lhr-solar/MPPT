/**
 * Maximum Power Point Tracker Project
 * 
 * File: sensor.h
 * Author: Matthew Yu
 * Organization: UT Solar Vehicles Team
 * Created on: September 10th, 2020
 * Last Modified: 9/20/20
 * 
 * File Discription: This header file describes the Sensor class, which is an
 * abstract parent class that defines and implements most of the shared methods
 * among its children.
 */
#pragma once
#include "mbed.h"
#include <chrono>
#include "filter/filter.h"


/**
 * Definition of a base implementation for sensors using the uC ADC.
 * 
 * The Sensor class is extended by children such as VoltageSensor and
 * CurrentSensor. It implements shared API for developers to control when a
 * sensor should record data from the ADC, and provides an interface to grab the
 * latest value and to write implementation code to tune the output value.
 */
class Sensor {
    protected:
        AnalogIn sensor;
        Filter filter;
        Ticker tick;

        // lock to prevent read/modification of shared resources
        bool lock;

        // adc output result value.
        double adcValue;

        virtual void measure() = 0;

    public:
        /**
         * constructor for a sensor object.
         * By default, we'll have a pass through filter object. This can be
         * swapped out for a SMAFilter or another child object class.
         * 
         * @param pin (PinName)
         *      pin to attach AnalogIn (sensor ADC pin) to.
         * 
         * @note default to a sample width of 10.
         */
        Sensor(PinName pin) : sensor(pin), filter(10) {
            adcValue = 0.0;
            lock = false;
        }
        /**
         * constructor for a sensor object.
         * By default, we'll have a pass through filter object. This can be
         * swapped out for a SMAFilter or another child object class.
         * 
         * @param pin (PinName)
         *      pin to attach AnalogIn (sensor ADC pin) to.
         * @param numFilterSamples (int)
         *      number of samples in our filter window
         */
        Sensor(PinName pin, int numFilterSamples) : sensor(pin), filter(numFilterSamples) {
            adcValue = 0.0;
            lock = false;
        }

        void set_reference_voltage(float voltageReference);

        double get_value();

        void start(int interval);

        void stop();
};
