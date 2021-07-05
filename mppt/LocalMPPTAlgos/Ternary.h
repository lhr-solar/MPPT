/**
 * Maximum Power Point Tracker Project
 * 
 * File: Ternary.h
 * Author: Afnan Mir
 * Organization: UT Solar Vehicles Team
 * Created on: June 12th, 2021
 * Last Modified: 06/12/2021
 * 
 * File Discription: This header file implements the Bisection Search class, which
 * is a derived class from the abstract LocalMPPTAlgorithm class.
 */

#pragma once
#include "LocalMPPTAlgorithm.h"

class Ternary : public LocalMPPTAlgorithm{
    Ternary(const PinName pin, StrideType type) : LocalMPPTAlgorithm(pin, type){
        l1 = leftBound;
        l2 = rightBound;
        powerL1 = 0;
        powerL2 = 0;
        cycle = 0;
    }

    const char* get_name() const{ return "Ternary Search"; }

    double getReferenceVoltage(double arrayVoltage, double arrayCurrent){
            targetVoltage = 0;
            double arrVolt = arrayVoltage;
            double arrCurr = arrayCurrent;
            if(cycle == 0){
                powerL2 = arrVolt * arrCurr;
                if(powerL1 > powerL2){
                    rightBound = l2;
                }else{
                    leftBound = l1;
                }
                l1 = (rightBound - leftBound) * q + leftBound;
                targetVoltage = l1;
                cycle = 1;
            }else if(cycle == 1){
                powerL1 = arrVolt * arrCurr;
                l2 = rightBound - (rightBound - leftBound)*q;
                targetVoltage = l2;
                cycle = 0;
            }
            return targetVoltage;
        }
    
    private:
        /** approxiamation of 1/3 */
        const double q = 0.33;
        /** Voltage value of left goal post */
        double l1;
        /** Voltage value of right goal post */
        double l2;
        /** Power value of left goal post */
        double powerL1;
        /** Power value of right goal post */
        double powerL2;
        /** Variable to keep track of cycle number of algorithm
        int cycle;

        
};
