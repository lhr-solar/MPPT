/**
 * Maximum Power Point Tracker Project
 * 
 * File: Stride.c
 * Author: Afnan Mir
 * Organization: UT Solar Vehicles Team
 * Created on: June 5th, 2021
 * Last Modified: 06/05/2021
 * 
 * File Discription: This cpp file implements the Stride class, which
 * is the parent class of the stride algroithms.
 */

#include "Stride.h"

Stride::Stride(){
    targetVoltage = 0.0;
    battVoltage = 0.0;
    battCurrent = 0.0;
    minStride = 0.01;
    arrVoltOld = 0.0;
    arrPowerOld = 0.0;
    inputLock = false;
    error = 0.05;
    VMPP = 0.621;
}
Stride::Stride(double Vmpp, double error){
    targetVoltage = 0.0;
    battVoltage = 0.0;
    battCurrent = 0.0;
    minStride = 0.01;
    arrVoltOld = 0.0;
    arrPowerOld = 0.0;
    inputLock = false;
    error = error;
    VMPP = Vmpp;
}


double Stride::getStride(double arrayVoltage, double arrayCurrent){
    return minStride;
}
const char*Stride::get_name() const{return "Fixed";}