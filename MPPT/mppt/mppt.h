/**
 * Maximum Power Point Tracker Project
 * 
 * File: mppt.h
 * Author: Matthew Yu
 * Organization: UT Solar Vehicles Team
 * Created on: September 10th, 2020
 * Last Modified: 09/26/20
 * 
 * File Discription: This header file describes the Mppt class, which is an
 * abstract parent class that defines and implements most of the shared methods
 * among its children.
 */
#pragma once
#include <chrono>
#include "mbed.h"


enum Mode {
    DEFAULT,
    ADAPTIVE
};

/**
 * Definition of a base implementation for mppt algorithms.
 * 
 * The Mppt class is extended by children such as PandO and
 * IncrementalVoltage. It implements shared API for developers to control when
 * and how the MPPT should calculate the best pulse width for the DC-DC
 * converter to use.
 */
class Mppt {
    public:
        /**
         * Constructor for a MPPT object.
         * 
         * @param[in] pin Pin to attach DigitalOut (tracking LED) to.
         */
        Mppt(const PinName pin);

        /**
         * Sets the inputs for the MPPT algorithm to process at the next interrupt.
         * 
         * @param[in] arrayVoltage Array voltage
         * @param[in] arrayCurrent Array current
         * @param[in] battVoltage Battery voltage
         * @param[in] battCurrent Battery current
         */
        void set_inputs(
            const double arrayVoltage, 
            const double arrayCurrent, 
            const double battVoltage, 
            const double battCurrent
        );

        /**
         * Sets up a timed interrupt to begin Mppt processing given an interval in uS.
         * Also starts the tracking LED.
         * 
         * @param[in] interval Interval for the interrupt to trigger, in microseconds
         */
        void enable_tracking(const int interval);
        
        /**
         * Disables the timed interrupt and the DC-DC converter pulse stops iterating. 
         * Also turns off the tracking LED.
         */
        void disable_tracking();

        /**
         * Returns the latest target voltage of the Mppt algorithm.
         * 
         * @note This method may stall until the lock on the variable is released, which
         * means the Mppt has uploaded the new value into it.
         * 
         * @return Target voltage.
         */
        const double get_target_voltage();

        /**
         * Returns the name of the MPPT algorithm.
         * 
         * @return Pointer to the name of the MPPT algorithm. Does not need 
         * to freed.
         */
        const char* get_name();

    protected:
        /**
         * Processes internal inputs and determines an optimal target voltage
         * for the DC-DC converter to run at. Inherited and implemented by its children.
         */
        void handler();

        /**
         * Toggles the tracking LED if we're currently running the MPPT.
         */
        void update_tracking_LED();

        /**
         * Determines the amount to travel from the current array voltage position to
         * reach the mppt.
         * TODO: implement the adaptive and default modes according to
         * TODO: sim/src/mppt_algorithms/mppt.py -> calc_perturb_amt()
         * 
         * @param[in] arrayVoltage Array voltage
         * @param[in] arrayCurrent Array current
         * @param[in] battVoltage Battery voltage
         * @param[in] battCurrent Battery current
         * 
         * @return Expected voltage applied over the array.
         */
        const double calculate_perturb_amount(
            const Mode mode,
            const double arrayVoltage, 
            const double arrayCurrent, 
            const double irradiance, 
            const double temperature
        );

    protected:
        DigitalOut trackingLED;
        Ticker tick;

        /** Indicator of whether the MPPT is currently tracking or not. */
        bool tracking;

        /** Locks to prevent read/modification of shared resources. */
        bool PWLock;
        bool inputLock;

        /** Target voltage value for the DC-DC converter. */
        double targetVoltage;

        /** Input conditions for the MPPT to process. */
        double arrayVoltage;
        double arrayCurrent; 
        double battVoltage;
        double battCurrent;
};