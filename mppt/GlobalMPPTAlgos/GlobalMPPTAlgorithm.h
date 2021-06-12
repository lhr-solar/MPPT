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
enum LocalType{
    PANDO,
    TERNARY,
    GOLDEN,
    BISECTION,
    IC,
    FC
};

class GlobalAlgo{
    public:

        GlobalAlgo(const PinName pin, LocalType local, StrideType stride);

        set_inputs(const double arrayVoltage, 
        const double arrayCurrent, 
        const double battVoltage,
        const double battCurrent);
        void enableTracking(const int interval);
        void disableTracking();
        double getTargetVoltage() const;
        const char* getName() const;

    protected:
        virtual void handler() = 0;

        void updateTrackingLED();



    protected:
        LocalMPPTAlgorithm localAlgo;
        double runningHistory[10];
        double pastHistories[10];
        bool semaphore;
        DigitalOut trackingLED;
        Ticker tick;
        bool tracking;
        bool PWSempahore;
        double targetVoltage;
        double arrayVoltage;
        double arrayCurrent;
        double battVoltage;
        double battCurrent;
        static double arrVoltOld;
        static double arrPowOld;
}