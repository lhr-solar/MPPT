/**
 * Maximum Power Point Tracker Project
 * 
 * File: IC.h
 * Author: Afnan Mir
 * Organization: UT Solar Vehicles Team
 * Created on: June 7th, 2021
 * Last Modified: 06/07/2021
 * 
 * File Discription: This header file implements the Incremental Conductance class, which
 * is a derived class from the abstract LocalMPPTAlgorithm class.
 */
#pragma once
#include "LocalMPPTAlgorithm.h"

class IC: public LocalMPPTAlgorithm{
    public:
        IC(const PinName pin, StrideType type) : LocalMPPTAlgorithm(pin,type){
            arrCurrOld = 0.0;
        }

        const char* get_name() const{
            return "Incremental Conductance"
        }
        double getReferenceVoltage(double arrayVoltage, double arrayCurrent){
            double arrVolt = arrayVoltage;
            double arrCurr = arrayCurrent;
            double dI = arrCurr - arrCurrOld;
            double dV = arrVolt - arrVoltOld;

            double voltStride = stride.getStride(arrVolt, arrCurr);

            targetVoltage = arrayVoltage;
            if(abs(dI * arrVolt + arrCurr*dV) < error){
                continue;
            }else if(dI*arrVolt + arrCurr * dV > error){
                targetVoltage += voltStride;
            }else if(dI*arrVolt + arrCurr * dV < -error){
                targetVoltage -= voltStride;
            }
            arrVoltOld = arrVolt;
            arrCurrOld = arrCurr;
            arrPowOld = arrVolt * arrCurr;
            return targetVoltage;
        }
    
    private:
        const double error = 0.01;
        static double arrCurrOld;
        
}