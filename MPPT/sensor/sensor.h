/**
 * Maximum Power Point Tracker Project
 * 
 * File: sensor.h
 * Author: Matthew Yu
 * Organization: UT Solar Vehicles Team
 * Created on: September 10th, 2020
 * Last Modified: 09/26/20
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
        Sensor(PinName pin);

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
        Sensor(PinName pin, int numFilterSamples);

        /**
         * Sets the reference voltage for the AnalogIn data member. You can read more
         * about it here:
         * https://os.mbed.com/docs/mbed-os/v6.2/mbed-os-api-doxy/classmbed_1_1_analog_in.html#a9f0645e8673d582b544afba07253a424
         * 
         * @param[in] voltageReference Reference voltage for the AnalogIn data member.
         */
        void set_reference_voltage(const float voltageReference);

        /**
         * Returns the latest value of the sensor, scaled appropriately.
         * 
         * @note This method may stall until the lock on the variable is released, which
         * means the sensor has uploaded the new value into it.
         * 
         * @return Sensor value.
         */
        const double get_value();

        /**
         * Starts interrupt execution of the private handler function given the 
         * interval.
         * 
         * @param[in] interval Time, in microseconds, between each function call.
         */
        void start(const int interval);

        /**
         * Stops interrupt execution of the private handler function given the interval.
         * constructor for a sensor object.
         * By default, we'll have a pass through filter object. This can be
         * swapped out for a SMAFilter or another child object class.
         * 
         * @param pin (PinName)
         *      pin to attach AnalogIn (sensor ADC pin) to.
         * 
         * @note default to a sample width of 10.
         */
        void stop();

    protected:
        AnalogIn sensor;
        Filter filter;
        Ticker tick;

        /** Lock to prevent read/modification of shared resources. */
        bool lock;

        /** ADC output result value. */
        double adcValue;

        virtual void measure() = 0;
};
