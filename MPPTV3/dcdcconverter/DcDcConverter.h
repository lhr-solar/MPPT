/**
 * Maximum Power Point Tracker Project
 * 
 * File: DcDcConverter.h
 * Author: Matthew Yu
 * Organization: UT Solar Vehicles Team
 * Created on: September 11th, 2020
 * Last Modified: 10/11/20
 * 
 * File Discription: This file defines functions defined for the
 * Dcdcconverter class.
 */
#pragma once
#include "mbed.h"
#include <chrono>

/**
 * Definition of an implementation for the DC-DC converter.
 * 
 * The Dcdcconverter implements methods to control the PWM of the DC-DC
 * Converter HW unit. Given a pulse width, it'll continuously toggle two NMos
 * switches 
 */
class Dcdcconverter {
    protected:
        AnalogOut pwm;
        Ticker tick;

        // locks to prevent read/modification of shared resources
        bool PWLock;
        bool battVoltageLock;

        // pulse width result value for the DC-DC converter.
        double pulseWidth;
        double arrVoltage;
        double battVoltage;
    
        void signal();

    public:
        /**
         * constructor for a Dcdcconverter object.
         * 
         * @param pin (PinName)
         *      pin to attach AnalogOut (pwm pin) to.
         */
        Dcdcconverter(PinName pin) : pwm(pin) {            
            PWLock = false;
            battVoltageLock = false;
            pulseWidth = 0.0;
            arrVoltage = 0.0;
            battVoltage = 0.01;
        }

        void set_pulse_width(double arrVoltage);

        void set_batt_voltage(double battVoltage);

        double get_pulse_width();

        void start(int interval);
        
        void stop();
};