/**
 * Maximum Power Point Tracker Project
 * 
 * File: Bisection.h
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

class Bisection : public LocalMPPTAlgorithm{
    public:
        Bisection(const PinName pin, StrideType type) : LocalMPPTAlgorithm(pin, type){
            cycle = 0;
        }

        const char* get_name() const{
            return "Golden Search";
        }
    
    private:
        int cycle;
        const double error = 0.01;
        void handler(double arrayVoltage, double arrayCurrent){
            targetVoltage = 0;
            double arrVolt = arrayVoltage;
            double arrCurr = arrayCurrent;
            if(cycle == 0){
                targetVoltage = (leftBound + rightBound)/2;
                cycle = 1;
                arrVoltOld = leftBound;
                arrPowOld = arrVolt * arrCurr;
            }else if(cycle == 1){
                double pNew = arrVolt * arrCurr;
                double dP_dV = 0;
                if(arrVolt - arrVoltOld != 0){ //Prevent divide by 0 errors
                    dP_dV = (pNew - arrPowOld)/(arrVolt - arrVoltOld);
                }
                if(abs(dP_dV) < error){
                    targetVoltage = arrVolt;
                }else if(dP_dV > 0){
                    leftBound = arrVolt;
                    targetVoltage = (leftBound + rightBound)/2;
                }else{
                    rightBound = arrVolt;
                    targetVoltage = (leftBound + rightBound)/2;
                }
                arrVoltOld = arrVolt;
                arrPowOld = pNew;
            }
        }
};