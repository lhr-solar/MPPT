/**
 * mppt.h
 */
#pragma once
#include "mbed.h"
#include <chrono>


class Mppt {
    protected:
        DigitalOut trackingLED;
        Ticker tick;

        bool tracking;

        bool PWLock;
        bool inputLock;

        double pulseWidth;

        float arrayVoltage;
        float arrayCurrent; 
        float battVoltage;
        float battCurrent;

        void updateTrackingLED();
        virtual void process() = 0;
    public:
        Mppt(PinName pin) : trackingLED(pin) {
            trackingLED = 0;
            
            tracking = false;
            
            PWLock = false;
            inputLock = false;

            pulseWidth = 0.0;

            arrayVoltage = 0.0;
            arrayCurrent = 0.0;
            battVoltage = 0.0;
            battCurrent = 0.0;
        }
        void setInputs(
            float arrayVoltage, 
            float arrayCurrent, 
            float battVoltage, 
            float battCurrent
        );
        double getPulseWidth();
        void enableTracking(int interval);
        void disableTracking();
};