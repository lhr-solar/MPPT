#pragma once
#include "Stride.h"
#include "math.h"

class AdaptiveStride: public Stride{
    public:
        AdaptiveStride() : Stride(1){

        }
        float getStride(float vArr, float cArr, float vBatt, float cBatt){
            float arrPower = vArr * cArr;
            minStride = error * error * VMPP/(2*(1 - error));
            float stride = 0;
            if(vArr < VMPP){
                stride = exp((VMPP - vArr)/3) - 1;
            }
            vOld = vArr;
            iOld = cArr;
            pOld = arrPower;
            return minStride + stride;
        }

        const char* getStrideTypeName(){
            return "Adapative";
        }

};