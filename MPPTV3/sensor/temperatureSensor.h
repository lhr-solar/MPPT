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
         * Constructor for a voltage sensor object.
         * 
         * @param[in] pin Pin to attach AnalogIn (sensor ADC pin) to.
         */
        TemperatureSensor(const PinName pin) : Sensor(pin) {}

        /**
         * Measures the sensor ADC input and converts it and filters it.
         */
        void handler() {
            double tempValue = sensor.read_voltage();
            // do some processing on the temporary value, maybe even some SW
            // filtering
            lock = true;
            adcValue = tempValue;
            lock = false;
        }
};