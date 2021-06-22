/**
 * Maximum Power Point Tracker Project
 * 
 * File: Pando.h
 * Author: Afnan Mir
 * Organization: UT Solar Vehicles Team
 * Created on: June 7th, 2021
 * Last Modified: 06/07/2021
 * 
 * File Discription: This header file implements the PandO class, which
 * is a derived class from the abstract LocalMPPTAlgorithm class.
 */
#pragma once
#include "LocalMPPTAlgorithm.h"

class Pando: public LocalMPPTAlgorithm{
    public:
        Pando(const PinName pin, StrideType type) : LocalMPPTAlgorithm(pin,type){}

        const char* get_name() const{
            return "PandO";
        }

        double getReferenceVoltage(double arrayVoltage, double arrayCurrent){
            double arrVolt = arrayVoltage;
            double arrCurr = arrayCurrent;
            double arrVoltDiff = arrVolt - arrVoltOld;
            double arrPowerDiff = arrVolt*arrCurr - arrPowOld;

            double dVoltRef = stride.getStride(arrVolt,arrCurr);

            double arrVoltNew = arrVolt;

            if(arrPowerDiff > 0.0){
                if(arrVoltDiff > 0.0){
                    arrVoltNew += dVoltRef;
                }else{
                    arrVoltNew -= dVoltRef;
                }
            }else{
                if(arrVoltDiff > 0.0){
                    arrVoltNew -= dVoltRef;
                }else{
                    arrVoltNew += dVoltRef;
                }
            }
            targetVoltage = arrVoltNew;
            arrVoltOld = arrVolt;
            arrPowOld = arrVolt * arrCurr;
            return targetVoltage;
        }
       
};
