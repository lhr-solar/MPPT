/**
 * Maximum Power Point Tracker Project
 * 
 * File: currentSensor.h
 * Author: Matthew Yu
 * Organization: UT Solar Vehicles Team
 * Created on: September 10th, 2020
 * Last Modified: 10/11/20
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
         * constructor for a current sensor object.
         * 
         * @param pin (PinName)
         *      pin to attach AnalogIn (sensor ADC pin) to.
         */
        CurrentSensor(PinName pin) : Sensor(pin) {}

        /**
         * reads and processes the value obtained from the AnalogIn pin.
         */
        void measure() {
            double tempValue = sensor.read_voltage();
            // do some processing on the temporary value, maybe even some SW filtering
            lock = true;
            adcValue = tempValue;
            lock = false;
        }
};
