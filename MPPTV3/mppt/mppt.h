/**
 * Maximum Power Point Tracker Project
 * 
 * File: mppt.h
 * Author: Matthew Yu
 * Organization: UT Solar Vehicles Team
 * Created on: September 10th, 2020
 * Last Modified: 10/11/20
 * 
 * File Discription: This header file describes the Mppt class, which is an
 * abstract parent class that defines and implements most of the shared methods
 * among its children.
 */
#pragma once
#include <chrono>
#include "mbed.h"
#include "string"
using std::string;

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
    protected:
        DigitalOut trackingLED;
        Ticker tick;

        // indicator of whether the MPPT is currently tracking or not
        bool tracking;

        // locks to prevent read/modification of shared resources
        bool PWLock;
        bool inputLock;

        // target voltage value for the DC-DC converter.
        double targetVoltage;

        // input conditions for the MPPT to process
        double arrayVoltage;
        double arrayCurrent; 
        double battVoltage;
        double battCurrent;

        void update_tracking_LED();

        void process();

        double calculate_perturb_amount(
            Mode mode,
            double arrayVoltage, 
            double arrayCurrent, 
            double irradiance, 
            double temperature
        );
    
    public:
        /**
         * constructor for a Mppt object.
         * 
         * @param pin (PinName)
         *      pin to attach DigitalOut (tracking LED) to.
         */
        Mppt(PinName pin) : trackingLED(pin) {
            trackingLED = 0;
            
            tracking = false;
            
            PWLock = false;
            inputLock = false;

            targetVoltage = 0.0;

            arrayVoltage = 0.0;
            arrayCurrent = 0.0;
            battVoltage = 0.0;
            battCurrent = 0.0;
        }

        void set_inputs(
            double arrayVoltage, 
            double arrayCurrent, 
            double battVoltage, 
            double battCurrent
        );

        double get_target_voltage();

        void enable_tracking(int interval);
        
        void disable_tracking();

        string get_name();
};