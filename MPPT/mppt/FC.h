/**
 * Maximum Power Point Tracker Project
 * 
 * File: FC.h
 * Author: Matthew Yu
 * Organization: UT Solar Vehicles Team
 * Created on: September 27th, 2020
 * Last Modified: 09/27/20
 * 
 * File Discription: This header file implements the FC class, which
 * is a derived class from the abstract Mppt class.
 */
#pragma once
#include "mppt.h"


class FC: public Mppt {
    public:
        /**
         * Constructor for a FC object.
         * 
         * @param[in] pin Pin to attach DigitalOut (tracking LED) to.
         */
        FC(PinName pin) : Mppt(pin) {}

        /**
         * Returns the name of the MPPT algorithm.
         * 
         * @return Pointer to the name of the MPPT algorithm. Does not need 
         * to freed.
         */
        const char* get_name() const { return "FC"; }

    private:
        /**
         * Processes internal inputs and determines an optimal target voltage
         * for the DC-DC converter to run at.
         */
        void handler() {
            static double arrVoltOld = 0.0;
            static double arrPowerOld = 0.0; 

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
            double arrPowerDiff = arrVolt * arrCurr - arrPowerOld;

            // get the voltage perturb stride
            double dVoltRef = calculate_perturb_amount(DEFAULT, arrVolt, arrCurr, 0.0, 0.0);
            // get the new array applied voltage
            double arrVoltNew = arrVolt;
            // if voltage does not change we don't update our calc.
            if (arrVoltDiff != 0) {
                if (arrPowerDiff/arrVoltDiff) {
                    arrVoltNew += dVoltRef;
                } else {
                    arrVoltNew -= dVoltRef;
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
};
