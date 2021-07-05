/**
 * Maximum Power Point Tracker Project
 * 
 * File: LocalMPPTAlgorithm.h
 * Author: Afnan Mir
 * Organization: UT Solar Vehicles Team
 * Created on: June 5th, 2021
 * Last Modified: 06/05/2021
 * 
 * File Discription: This header file implements the LocalMPPTAlgorithm class, which
 * is the parent class of the Local MPPT algroithms.
 */
 #pragma once
 #include "mbed.h"
 #include "../Strides/Stride.h"
 #include "../Strides/BisectionStride.h"
 #include "../Strides/AdaptiveStride.h"
 #include "../Strides/OptimalStride.h"



 class LocalMPPTAlgorithm{
     public:
         enum StrideType{
            FIXED,
            BISECTION,
            OPTIMAL,
            ADAPTIVE
        };
        enum LocalMPPTAlgorithmTypes {PANDO, IC, FC, BISECTION, GOLDEN, TERNARY};

     public:
        /**
         * Constructor for a Local MPPT Algorithm Object to determine the target voltage after the global context algorithm
         * has finished
         * @param pin the pin for the LED
         * @param type the Stride to pair with the local algorithm
         */
        LocalMPPTAlgorithm(const PinName pin, StrideType type);

        void setInputs(
            const double arrayVoltage,
            const double arrayCurrent,
            const double battVoltage,
            const double battCurrent
            );
        void enable_tracking(const int interval);

        void disable_tracking();
        
        /**
         * function that returns the value of the target voltage for next cycle
         * @return the target voltage for the next cycle.
         */
        double get_target_voltage() const;
        
        /**
         * Returns the name of the Local MPPT Algorithm used
         * @return the name of the Local MPPT Algorithm
         */
        const char* get_name() const;
        
        /**
         * returns the name of the stride paired with the local algorithm
         * @return the name of the stride paired with the local algorithm
         */
        const char* get_stride_type() const;

        /**
         * Sets the vmpp for the adaptive and optimal stride, and left and right bounds for D&C algorithms
         * @param vmpp the observerd MPP from the global algorithm
         * @param left the left bound for local algorithm
         * @param right the right bound for the local algorithm
         */
        void setup(double vmpp, double left, double right);
        /**
         * returns the new value of the target voltage for the MPPT.
         * @param arrayVoltage last measured array voltage
         * @param arrayCurrent last measured array current
         * @return the new target voltage for MPPT.
         */
        virtual double getReferenceVoltage(double arrayVoltage, double arrayCurrent) = 0;
    protected:
        void update_tracking_LED();

     protected:
        /** The type of stride for the local algorithm to use*/
        StrideType strideType;
        /** The type of stride for the local algorithm to use*/
        Stride stride;
        /** Variable to store the measured array voltage at the time */
        double arrayVoltage;
        /** Variable to store the measured array current at the time */
        double arrayCurrent;
        /** This variable is used to track the battery voltage */
        double battVoltage;
        /** This variable is used to track the battery current*/
        double battCurrent;
        /** This variable is used to store the target voltage*/
        double targetVoltage;
        // int semaphore;
        /** value that the local algorithm should not go lower than*/
        double leftBound;
        /** value that local algorithm should not go higher than */
        double rightBound;
        /** This variable is used to track the array voltage on the last cycle*/
        static double arrVoltOld;
        /** This variable is used to track the array power on the last cycle*/
        static double arrPowOld;
 };
