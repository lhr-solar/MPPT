/**
 * Maximum Power Point Tracker Project
 * 
 * File: GlobalMPPTAlgorithm.cpp
 * Author: Afnan Mir
 * Organization: UT Solar Vehicles Team
 * Created on: June 12th, 2021
 * Last Modified: 06/12/2021
 * 
 * File Discription: This cpp file implements the GlobalMPPTAlgorithm class, which
 * is the parent class of the Global MPPT algroithms.
 */

#include "GlobalMPPTAlgorithm.h"

GlobalMPPTAlgorithm::GlobalMPPTAlgorithm(const PinName pin, LocalType local, StrideType type) : trackingLed(pin){
    trackingLED = 0;
    arrVoltOld = 0;
    arrPowOld = 0;
    targetVoltage = 0.0;
    arrayVoltage = 0.0;
    arrayCurrent = 0.0;
    battVoltage = 0.0;
    battCurrent = 0.0;
    switch (local){
        case PANDO:
            localAlgo = new Pando(pin,type);
            break;
        case GOLDEN:
            localAlgo = new GoldenSearch(pin,type);
            break;
        case BISECTION:
            localAlgo = new Bisection(pin,type);
            break;
        case TERNARY:
            localAlgo = new Ternary(pin,type);
            break;
        case IC:
            localAlgo = new IC(pin,type);
            break;
        case FC:
            localAlgo = new FC(pin,type);
            break;
        default:
            localAlgo = new Pando(pin,type);
            break;
    }
}


void GlobalMPPTAlgorithm::set_inputs(const double arrayVoltage, 
        const double arrayCurrent, 
        const double battVoltage,
        const double battCurrent){
            while(!semaphore);
            semaphore = false;
            this->arrayVoltage = arrayVoltage;
            this->arrayCurrent = arrayCurrent;
            this->battVoltage = batt;
            this->battCurrent = battCurrent;
            sempahore = true;
        }

void GlobalMPPTAlgorithm::enable_tracking(const int interval){

}


void GlobalMPPTAlgorithm::disable_tracking(){

}

double GlobalMPPTAlgorithm::get_target_voltage() const{
    return targetVoltage;
}

const char* GlobalMPPTAlgorithm::get_stride_type() const{
    return localAlgo.get_stride_type();
}
