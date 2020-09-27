/**
 * Maximum Power Point Tracker Project
 * 
 * File: DcDcConverter.h
 * Author: Matthew Yu
 * Organization: UT Solar Vehicles Team
 * Created on: September 11th, 2020
 * Last Modified: 09/26/20
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
    public:
        /**
         * Constructor for a Dcdcconverter object.
         * 
         * @param[in] pin Pin to attach AnalogOut (pwm pin) to.
         */
        Dcdcconverter(const PinName pin);

        /**
         * Sets the pulse width of the DC-DC converter.
         * 
         * @param[in] arrVoltage Array voltage expectation from the MPPT.
         */
        void set_pulse_width(const double arrVoltage);

        /**
         * Sets the load voltage for the DC-DC converter.
         * 
         * @param[in] battVoltage Battery voltage measurement of the MPPT.
         */
        void set_batt_voltage(const double battVoltage);

        /**
         * Sets the limit for what the minimum battery voltage should be.
         * To limit power flow into the battery in the case of overheating,
         * etc, the DC-DC converter sets the battery side voltage to above 
         * the existing battery voltage measurement. This results in wasted
         * energy not reaching the battery since the current is lowered bu. This
         * wasted energy is converted into heat, which may be bad for the MPPT
         * or Array. Experimental feature.
         * 
         * @param battVoltageLim Lowest voltage we should get the battery side
         *      voltage to. This is only in effect if the battery voltage 
         *      measurement is lower than the limit voltage.
         */
        void set_batt_voltage_limit(const double battVoltageLim);

        /**
         * Sets the load voltage for the DC-DC converter.
         * 
         * @return Get the pulse width of the dc-dc converter.
         */
        double get_pulse_width() const;

        /**
         * Starts interrupt execution of the private handler function given the 
         * interval.
         * 
         * @param[in] interval Time, in microseconds, between each function call.
         */
        void start(const int interval);
        
        /**
         * Stops interrupt execution of the private handler function given the interval.
         */
        void stop();

    private:
        /**
         * Writes the pulse width to the pwm output to set the array.
         */
        void handler();

    private:
        AnalogOut pwm;
        Ticker tick;

        /** Locks to prevent read/modification of shared resources. */
        bool PWLock;
        bool battVoltageLock;
        bool battVoltageLimLock;

        /** Pulse width result value for the DC-DC converter. */
        double pulseWidth;
        double arrVoltage;
        double battVoltage;

        /** Limiter value for the battery voltage. */
        double battVoltageLim;

};