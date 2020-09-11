/**
 * PandO.h
 */
#pragma once
#include "mppt.h"


class PandO: public Mppt {
    protected:
        void process() {
            while (inputLock);
            inputLock = true;
            float arrVolt = arrayVoltage;
            float arrCurr = arrayCurrent;
            float battVolt = battVoltage;
            float battCurr = battCurrent;
            inputLock = false;
            // run the algorithm...
        }
    public:
        PandO(PinName pin) : Mppt(pin) {}

};
