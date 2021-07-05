/**
 * Maximum Power Point Tracker Project
 * 
 * File: FC.h
 * Author: Afnan Mir
 * Organization: UT Solar Vehicles Team
 * Created on: June 7th, 2021
 * Last Modified: 06/07/2021
 * 
 * File Discription: This header file implements the dP/dV feedback class, which
 * is a derived class from the abstract LocalMPPTAlgorithm class.
 */
#pragma once
#include "LocalMPPTAlgorithm.h"
#include <math.h>

class GoldenSearch : public LocalMPPTAlgorithm{
    public:
        GoldenSearch(const PinName pin, StrideType type) : LocalMPPTAlgorithm(pin, type){
            cycle = 0;
            powerL1 = 0;
            powerL2 = 0;
            l1 = leftBound;
            l2 = rightBound;
        }
        const char* get_name() const{ return "Golden Search"; }
        double getReferenceVoltage(double arrayVoltage, double arrayCurrent){
            targetVoltage = 0;
            if(cycle == 0){
                l1 = rightBound - (rightBound - leftBound) * phi;
                targetVoltage = l1;
                cycle = 1;
            }else if(cycle == 1){
                powerL1 = arrayVoltage * arrayCurrent;
                l2 = (rightBound - leftBound)*phi + leftBound;
                targetVoltage = l2;
                cycle = 2;
            }else{
                if(cycle == 2){
                    powerL2 = arrayVoltage * arrayCurrent;
                }else if(cycle == 3){
                    powerL1 = arrayVoltage * arrayCurrent;
                }
                if(powerL1 > powerL2){
                    rightBound = l2;
                    l2 = l1;
                    powerL1 = powerL2;
                    l1 = rightBound - (rightBound - leftBound)*phi;
                    targetVoltage = l1;
                    cycle = 3;
                }else{
                    leftBound = l1;
                    l1 = l2;
                    powerL1 = powerL2;
                    l2 = (rightBound - leftBound)*phi + leftBound;
                    targetVoltage = l2;
                    cycle = 2;
                }
            }
            return targetVoltage;
        }
    private:
        /** constant value used to calculate the goal posts and target voltage*/
        const double phi = (sqrt(5) + 1)/2 - 1;
        /** variable to track the cycle number of algorithm */
        int cycle;
        /** Power of the left goal post*/
        double powerL1;
        /** power of right goal post*/
        double powerL2;
        /** Voltage of left goal post */
        double l1;
        /** Voltage of right goal post */
        double l2;
};
