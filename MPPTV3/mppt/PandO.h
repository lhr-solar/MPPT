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
            static float arrVoltOld = 0.0;
            static float arrPowerOld = 0.0; 

            while (inputLock);
            inputLock = true;
            float arrVolt = arrayVoltage;
            float arrCurr = arrayCurrent;
            float battVolt = battVoltage;
            float battCurr = battCurrent;
            inputLock = false;

            // run the algorithm
            // generate the differences
            float arrVoltDiff = arrVolt - arrVoltOld;
            float arrPowerDiff = arrVolt * arrCurr - arrPowerOld;

            // get the voltage perturb stride
            double dVoltRef = calculate_perturb_amount(DEFAULT, arrVolt, arrCurr, 0.0, 0.0);
            // get the new array applied voltage
            float arrVoltNew = arrVolt;
            if (arrPowerDiff > 0.0) {
                if (arrVoltDiff > 0.0) {
                    arrVoltNew += dVoltRef;
                } else {
                    arrVoltNew -= dVoltRef;
                }
            } else {
                if (arrVoltDiff > 0.0) {
                    arrVoltNew -= dVoltRef;
                } else {
                    arrVoltNew += dVoltRef;
                }
            }

            // adjust the pulse width
            double pulseWidthClone = convert_into_pulse_width(arrVoltNew);
            PWLock = true;
            pulseWidth = pulseWidthClone;
            PWLock = false;

            // assign old variables
            arrVoltOld = arrVolt;
            arrPowerOld = arrVolt * arrCurr;
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
