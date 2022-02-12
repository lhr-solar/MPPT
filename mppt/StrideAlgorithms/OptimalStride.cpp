#pragma once
#include "Stride.h"
#include "math.h"

class OptimalStride: public Stride{
    OptimalStride() : Stride(2){

    }
    float getStride(float vArr, float cArr, float vBatt, float cBatt){
        float arrPower = vArr * cArr;
        minStride = error * error * VMPP/(2*(1 - error));
        float stride = abs(VMPP - vArr);
        vOld = vArr;
        iOld = cArr;
        pOld = arrPower;
        return stride + minStride;
    }

    const char* getStrideTypeName(){
        return "Optimal";
    }
};