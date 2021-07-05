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

class FC: public LocalMPPTAlgorithm{
    public:
        FC(const PinName pin, StrideType type) : LocalMPPTAlgorithm(pin, type){
            
        }
        const char* get_name() const{ return "FC"; }
        double getReferenceVoltage(double arrayVoltage, double arrayCurrent){
            double arrVolt = arrayVoltage;
            double arrCurr = arrayCurrent;
            double arrPow = arrVolt*arrCurr;
            double dP = arrPow - arrPowOld;
            double dV = arrVoltage - arrVoltOld;
            double voltStride = stride.getStride(arrVolt,arrCurr);
            if(dV == 0){
                targetVoltage+= 0.005;
            }else if(abs(dP/dV) < error){
                continue;
            }else{
                if(dP/dV > 0){
                    targetVoltage += voltStride;
                }else{
                    targetVoltage -= voltStride;
                }
            }
            arrVoltOld = arrVolt;
            arrPowOld = arrPow;
            return targetVoltage;
        }
    
    private:
        /** If power difference is less than this, we just use minStride*/
        const double error = 0.05;
        
}
