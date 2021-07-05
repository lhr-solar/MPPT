/**
 * Maximum Power Point Tracker Project
 * 
 * File: GlobalMPPTAlgorithm.h
 * Author: Afnan Mir
 * Organization: UT Solar Vehicles Team
 * Created on: June 12th, 2021
 * Last Modified: 06/12/2021
 * 
 * File Discription: This header file implements the GlobalMPPTAlgorithm class, which
 * is the parent class of the Global MPPT algroithms.
 */

#pragma once
#include "mbed.h"
#include "../LocalMPPTAlgos/LocalMPPTAlgorithm.h"
#include "../LocalMPPTAlgos/Pando.h"
#include "../LocalMPPTAlgos/Ternary.h"
#include "../LocalMPPTAlgos/Bisection.h"
#include "../LocalMPPTAlgos/GoldenSearch.h"
#include "../LocalMPPTAlgos/IC.h"
#include "../LocalMPPTAlgos/FC.h"
#define MAX_VOLTAGE 0.8


class GlobalAlgo{
    public:
        // All types of local algorithms
        enum LocalType{
            PANDO,
            TERNARY,
            GOLDEN,
            BISECTION,
            IC,
            FC
        };

        /**
         * Constructor for a Global MPPT Algorithm to find the GMPP 
         * @param pin the pin of the LED
         * @param local the local algorithm to pair with the global algorithm
         * @param stride the stride to pair with the local and global algorithm
         */
        GlobalAlgo(const PinName pin, LocalType local, StrideType stride);
        /**
         * Sets the system to the current state of the array with the current voltage and current of the array and battery
         * @param arrayVoltage voltage of the array
         * @param arrayCurrent current of the array
         * @param battVoltage voltage of the battery
         * @param battCurrent current of the battery
         */
        void set_inputs(const double arrayVoltage, 
                   const double arrayCurrent, 
                   const double battVoltage,
                   const double battCurrent);
        /**
         * Sets up a timed interrupt to begin Mppt processing given an interval in uS.
         * Also starts the tracking LED.
         * 
         * @param[in] interval Interval for the interrupt to trigger, in microseconds
         */
        void enableTracking(const int interval);
        /**
         * Disables the timed interrupt and the DC-DC converter pulse stops iterating. 
         * Also turns off the tracking LED.
         */
        void disableTracking();
        /**
         * Returns the latest target voltage of the Mppt algorithm.
         * 
         * @note This method may stall until the lock on the variable is released, which
         * means the Mppt has uploaded the new value into it.
         * 
         * @return Target voltage.
         */
        double getTargetVoltage() const;
        /**
         * Returns the name of the MPPT algorithm.
         * 
         * @return Pointer to the name of the MPPT algorithm. Does not need 
         * to freed.
         */
        const char* getName() const;

    protected:
        /**
         * This method processes the input conditions of the array in order to calculate the next target voltage
         * for the DC-DC converter to run at. This is an abstract method that will be impplemented by derivative
         * classes
         */
        virtual void handler() = 0;
        /**
         * Toggles the tracking LED if we're currently running the MPPT.
         */
        void updateTrackingLED();
    protected:
        /** The local algorithm paired with the global algorithm*/
        LocalMPPTAlgorithm localAlgo;
        /**Past 10 measures of the current voltage the DC-DC converter is outputting*/
        double runningHistory[10];
        /** Past 10 averages of the running histories */
        double pastHistories[10];
        /**Semaphore flag that signals whether the system is currently taking in input from array or not */
        bool semaphore;
        /** The tracking LED for the MPPT */
        DigitalOut trackingLED;
        /** Timer for system */
        Ticker tick;
        bool tracking;
        bool PWSempahore;
        /** The voltage that the DC-DC converter should be running at */
        double targetVoltage;
        /** Current array voltage */
        double arrayVoltage;
        /** Current array current */
        double arrayCurrent;
        /** Current battery voltage */
        double battVoltage;
        /** Current battery current */
        double battCurrent;
        /** old array voltage */
        static double arrVoltOld;
        /** old array power */
        static double arrPowOld;
};
