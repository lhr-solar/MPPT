/**
 * Maximum Power Point Tracker Project
 * 
 * File: AdaptiveStride.h
 * Author: Afnan Mir
 * Organization: UT Solar Vehicles Team
 * Created on: June 5th, 2021
 * Last Modified: 06/05/2021
 * 
 * File Discription: This header file implements the AdaptiveStride class, which
 * is a derivative class of the Stride class.
 */
#pragma once
#include "Stride.h"
#include <math.h>

class AdaptiveStride: public Stride{
    public:
        AdaptiveStride(): Stride(){}
        AdaptiveStride(double Vmpp, double error): Stride(Vmpp, error){}
        double getStride(double arrayVoltage, double arrayCurrent){
            // inputLock = true;
            double arrVolt = arrayVoltage;
            double arrCurr = arrayCurrent;
            // inputLock = false;
            minStride = error*error*VMPP/(2*(1-error));
            double stride = 0;
            if(arrVolt < VMPP){
                stride = exp((VMPP - arrVolt)/3) - 1;
            }
            arrPowerOld = arrVolt * arrCurr;
            arrVoltOld = arrVolt;
            return stride + minStride;
        }const char* get_name() const{return "Adaptive Stride";}
};