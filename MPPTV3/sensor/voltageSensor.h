/**
 * Maximum Power Point Tracker Project
 * 
 * File: voltageSensor.h
 * Author: Matthew Yu
 * Organization: UT Solar Vehicles Team
 * Created on: September 10th, 2020
 * Last Modified: 10/11/20
 * 
 * File Discription: This header file implements the VoltageSensor class, which
 * is a derived class from the abstract Sensor class.
 */
#pragma once
#include "sensor.h"


/**
 * Definition of a derived implementation for voltage sensors using the uC ADC.
 * 
 * The VoltageSensor class create objects that can be used to measure voltage
 * from analog in pins on the uC.
 */
class VoltageSensor: public Sensor{
    public:
        /**
         * constructor for a voltage sensor object.
         * 
         * @param pin (PinName)
         *      pin to attach AnalogIn (sensor ADC pin) to.
         */
        VoltageSensor(PinName pin) : Sensor(pin) {}

        /**
         * reads and processes the value obtained from the AnalogIn pin.
         */
        void measure() {
            float tempValue = sensor.read_voltage();
            // do some processing on the temporary value, maybe even some SW
            // filtering
            lock = true;
            adcValue = tempValue;
            lock = false;
        }
};