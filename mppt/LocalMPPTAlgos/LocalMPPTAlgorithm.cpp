/**
 * Maximum Power Point Tracker Project
 * 
 * File: LocalMPPTAlgorithm.cpp
 * Author: Afnan Mir
 * Organization: UT Solar Vehicles Team
 * Created on: June 5th, 2021
 * Last Modified: 06/05/2021
 * 
 * File Discription: This implementation file implements the LocalMPPTAlgorithm class, which
 * is the parent class of the Local MPPT algroithms.
 */
#define MAX_VOLTAGE 0.8
#pragma once
#include "LocalMPPTAlgorithm.h"
#include <chrono>

LocalMPPTAlgorithm::LocalMPPTAlgorithm(const PinName pin, StrideType type) : trackingLED(pin){
    targetVoltage = 0.0;
    arrayVoltage = 0.0;
    arrayCurrent = 0.0;
    battVoltage = 0.0;
    battCurrent = 0.0;
    leftBound = 0.0;
    rightBound = MAX_VOLTAGE;
    arrVoltOld = 0.0;
    arrPowOld = 0.0;
    if(type == FIXED){
        stride = new Stride()
    }else if(type == ADAPTIVE){
        stride = new AdaptiveStride()
    }else if(type == OPTIMAL){
        stride = new OptimalStride()
    }else if(type == BISECTION){
        stride = new BisectionStride();
    }
}

void LocalMPPTAlgorithm::enable_tracking(const int interval){

}


void LocalMPPTAlgorithm::disable_tracking(){

}

double LocalMPPTAlgorithm::get_target_voltage() const{
    return targetVoltage;
}

const char* LocalMPPTAlgorithm::get_stride_type() const{
    return stride.get_name();
}

void LocalMPPTAlgorithm::handler(double arrayVoltage, double arrayCurrent){
    return 0.0;
}

void LocalMPPTAlgorithm:: update_tracking_LED(){
    
}

