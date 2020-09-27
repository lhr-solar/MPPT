/**
 * Maximum Power Point Tracker Project
 * 
 * File: IC.h
 * Author: Matthew Yu
 * Organization: UT Solar Vehicles Team
 * Created on: September 10th, 2020
 * Last Modified: 09/26/20
 * 
 * File Discription: This header file implements the IC class, which
 * is a derived class from the abstract Mppt class.
 */
#pragma once
#include "mppt.h"


class IC: public Mppt {
    public:
        /**
         * Constructor for a IC object.
         * 
         * @param[in] pin Pin to attach DigitalOut (tracking LED) to.
         */
        IC(PinName pin) : Mppt(pin) {}

        /**
         * Returns the name of the MPPT algorithm.
         * 
         * @return Pointer to the name of the MPPT algorithm. Does not need 
         * to freed.
         */
        const char* get_name() { return "IC"; }

    private:
        /**
         * Processes internal inputs and determines an optimal target voltage
         * for the DC-DC converter to run at.
         */
        void process() {
            static double arrVoltOld = 0.0;
            static double arrCurrOld = 0.0; 

            if (inputLock) return;

            inputLock = true;
            double arrVolt = arrayVoltage;
            double arrCurr = arrayCurrent;
            double battVolt = battVoltage;
            double battCurr = battCurrent;
            inputLock = false;

            // run the algorithm
            // generate the differences
            double arrVoltDiff = arrVolt - arrVoltOld;
            double arrCurrDiff = arrCurr - arrCurrOld;

            // get the voltage perturb stride
            double dVoltRef = calculate_perturb_amount(DEFAULT, arrVolt, arrCurr, 0.0, 0.0);
            // get the new array applied voltage
            double arrVoltNew = arrVolt;
            if (arrVoltDiff == 0.0) {
                if (arrCurrDiff > 0.0) {
                    arrVoltNew -= dVoltRef;
                } else if (arrCurrDiff < 0.0) {
                    arrVoltNew += dVoltRef;
                }
            } else {
                if (-arrCurr * arrVoltDiff > arrCurrDiff * arrVolt) {
                    arrVoltNew += dVoltRef;
                } else if (-arrCurr * arrVoltDiff < arrCurrDiff * arrVolt) {
                    arrVoltNew -= dVoltRef;
                }
            }

            // adjust the target voltage
            PWLock = true;
            targetVoltage = arrVoltNew;
            PWLock = false;

            // assign old variables
            arrVoltOld = arrVolt;
            arrCurrOld = arrCurr;
        }
};
