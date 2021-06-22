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

 enum StrideType{
     FIXED,
     BISECTION,
     OPTIMAL,
     ADAPTIVE
 };

 class LocalMPPTAlgorithm{
     public:
        enum LocalMPPTAlgorithmTypes {PANDO, IC, FC, BISECTION, GOLDEN, TERNARY};

     public:
        LocalMPPTAlgorithm(const PinName pin, StrideType type);

        void setInputs(
            const double arrayVoltage,
            const double arrayCurrent,
            const double battVoltage,
            const double battCurrent
            );
        void enable_tracking(const int interval);

        void disable_tracking();

        double get_target_voltage() const;

        const char* get_name() const;

        const char* get_stride_type() const;

        void setup(double vmpp, double left, double right);

        virtual double getReferenceVoltage(double arrayVoltage, double arrayCurrent) = 0;


    protected:
        void update_tracking_LED();

     protected:
        StrideType strideType;
        Stride stride;
        double arrayVoltage;
        double arrayCurrent;
        double battVoltage;
        double battCurrent;
        double targetVoltage;
        // int semaphore;
        double leftBound;
        double rightBound;
        static double arrVoltOld;
        static double arrPowOld;
 };