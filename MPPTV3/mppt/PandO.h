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


class PandO: public Mppt {
    protected:
        /**
         * processes internal inputs and determines an optimal target voltage for
         * the DC-DC converter to run at.
         */
        void process() {
            static double arrVoltOld = 0.0;
            static double arrPowerOld = 0.0; 

            while (inputLock);
            inputLock = true;
            double arrVolt = arrayVoltage;
            double arrCurr = arrayCurrent;
            double battVolt = battVoltage;
            double battCurr = battCurrent;
            inputLock = false;

            // run the algorithm
            // generate the differences
            double arrVoltDiff = arrVolt - arrVoltOld;
            double arrPowerDiff = arrVolt * arrCurr - arrPowerOld;

            // get the voltage perturb stride
            double dVoltRef = calculate_perturb_amount(DEFAULT, arrVolt, arrCurr, 0.0, 0.0);
            // get the new array applied voltage
            double arrVoltNew = arrVolt;
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

            // adjust the target voltage
            PWLock = true;
            targetVoltage = arrVoltNew;
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
