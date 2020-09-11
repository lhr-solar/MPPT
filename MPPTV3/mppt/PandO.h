/**
 * Maximum Power Point Tracker Project
 * 
 * File: PandO.h
 * Author: Matthew Yu
 * Organization: UT Solar Vehicles Team
 * Created on: September 10th, 2020
 * Last Modified: 10/11/20
 * 
 * File Discription: This header file implements the PandO class, which
 * is a derived class from the abstract Mppt class.
 */
#pragma once
#include "mppt.h"
#include "string"
using std::string;


class PandO: public Mppt {
    protected:
        /**
         * processes internal inputs and determines an optimal pulse width for
         * the DC-DC converter to run at.
         */
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
        /**
         * constructor for a PandO object.
         * 
         * @param pin (PinName)
         *      pin to attach DigitalOut (tracking LED) to.
         */
        PandO(PinName pin) : Mppt(pin) {}

        /**
         * returns the name of the MPPT algorithm being run.
         * 
         * @return PandO (string)
         */
        string get_name() { return "PandO"; }

};
