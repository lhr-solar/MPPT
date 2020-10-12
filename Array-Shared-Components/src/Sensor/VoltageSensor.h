/**
 * Maximum Power Point Tracker Project
 * 
 * File: VoltageSensor.h
 * Author: Matthew Yu
 * Organization: UT Solar Vehicles Team
 * Created on: September 10th, 2020
 * Last Modified: 10/07/20
 * 
 * File Discription: This header file implements the VoltageSensor class, which
 * is a derived class from the abstract Sensor class.
 */
#pragma once
#include "Sensor.h"


/**
 * Definition of a derived implementation for voltage sensors using the uC ADC.
 * 
 * The VoltageSensor class create objects that can be used to measure voltage
 * from analog in pins on the uC.
 */
class VoltageSensor: public Sensor{
    public:
        /**
         * Constructor for a voltage sensor object.
         * 
         * @param[in] pin Pin to attach AnalogIn (sensor ADC pin) to.
         */
        VoltageSensor(const PinName pin) : Sensor(pin) {}

        /**
         * Constructor for a voltage sensor object.
         * 
         * @param[in] pin Pin to attach AnalogIn (sensor ADC pin) to.
         * @param[in] numFilterSamples Number of samples in our filter window
         */
        VoltageSensor(const PinName pin, const int numFilterSamples) : 
            Sensor(pin, numFilterSamples) {}

        /**
         * Measures the sensor ADC input and converts it and filters it.
         */
        void measure() {
            double tempValue = sensor.read_voltage();
            // TODO: do some processing to convert it into a meaningful vaue

            // filter it
            filter.addSample(tempValue);
            tempValue = filter.getResult();

            lock = true;
            adcValue = tempValue;
            lock = false;
        }
};