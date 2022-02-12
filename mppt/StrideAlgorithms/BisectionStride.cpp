#pragma once
#include "Stride.h"

class BisectionStride: public Stride{
    public:
        BisectionStride(): Stride(3){
            slopeMultiplier = 0.01;
            minPowDiff = 0.01;
            minVoltDiff = 0.01;
        }
        float getStride(float vArr, float cArr, float vBatt, float cBatt){
            float arrPower = vArr * cArr;
            float vDiff = vArr - vOld;
            float pDiff = arrPower - pOld;
            float stride = 0;
            if(abs(pDiff) >= minPowDiff && abs(vDiff) >= minVoltDiff){
                float slope = pDiff/vDiff;
                if(slope < 0){
                    stride = (vArr + vOld)/2 - vOld;
                }else if(slope > 0){
                    stride = slope * slopeMultiplier;
                }
            }
            vOld = vArr;
            pOld = arrPower;
            iOld = cArr;
            return max(minStride, abs(stride));
        }

    private:
        float slopeMultiplier;
        float minPowDiff;
        float minVoltDiff;
};