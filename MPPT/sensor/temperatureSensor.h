/**
 * Maximum Power Point Tracker Project
 * 
 * File: temperatureSensor.h
 * Author: Matthew Yu
 * Organization: UT Solar Vehicles Team
 * Created on: September 10th, 2020
 * Last Modified: 09/26/20
 * 
 * File Discription: This header file implements the TemperatureSensor class, which
 * is a derived class from the abstract Sensor class.
 */
#pragma once
#include "sensor.h"


/**
 * Definition of a derived implementation for temperature sensors using the uC ADC.
 * 
 * The TemperatureSensor class create objects that can be used to measure voltage
 * from analog in pins on the uC.
 */
class TemperatureSensor: public Sensor{
    public:
        /**
         * Constructor for a temperature sensor object.
         * 
         * @param[in] pin Pin to attach AnalogIn (sensor ADC pin) to.
         */
        TemperatureSensor(const PinName pin) : Sensor(pin) {}

        /**
         * Constructor for a temperature sensor object.
         * 
         * @param pin Pin to attach AnalogIn (sensor ADC pin) to.
         * @param numFilterSamples Number of samples in our filter window
         */
        TemperatureSensor(const PinName pin, const int numFilterSamples) : 
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