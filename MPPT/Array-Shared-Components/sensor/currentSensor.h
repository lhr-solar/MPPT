/**
 * Maximum Power Point Tracker Project
 * 
 * File: currentSensor.h
 * Author: Matthew Yu
 * Organization: UT Solar Vehicles Team
 * Created on: September 10th, 2020
 * Last Modified: 09/26/20
 * 
 * File Discription: This header file implements the CurrentSensor class, which
 * is a derived class from the abstract Sensor class.
 */
#pragma once
#include "sensor.h"


/**
 * Definition of a derived implementation for current sensors using the uC ADC.
 * 
 * The CurrentSensor class create objects that can be used to measure current
 * (converted into voltage at the ADC) from analog in pins on the uC.
 */
class CurrentSensor: public Sensor {
    public:
        /**
         * Constructor for a current sensor object.
         * 
         * @param[in] pin (PinName)
         *      pin to attach AnalogIn (sensor ADC pin) to.
         */
        CurrentSensor(const PinName pin) : Sensor(pin) {}

        /**
         * Constructor for a current sensor object.
         * 
         * @param[in] pin Pin to attach AnalogIn (sensor ADC pin) to.
         * @param[in] numFilterSamples Number of samples in our filter window
         */
        CurrentSensor(const PinName pin, const int numFilterSamples) : 
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
