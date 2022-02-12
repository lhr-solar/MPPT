#include "Stride.h"

class FixedStride: public Stride{
    public:
        FixedStride(float fStep) : Stride(0){
            fixedStep = fStep;
        }

        float getStride(float vArr, float cArr, float vBatt, float cBatt){
            float arrPower = vArr * cArr;
            float vDiff = vArr - vOld;
            float pDiff = arrPower - pOld;
            float vRef = vArr;
            if(pDiff >= 0){
                if(vDiff >= 0.0){
                    vRef += fixedStep;
                }else{
                    vRef -= fixedStep;
                }
            }else{
                if(vDiff >= 0.0){
                    vRef -= fixedStep;
                }else{
                    vRef += fixedStep;
                }
            }
            vOld = vArr;
            iOld = cArr;
            pOld = arrPower;
            return vRef;
        }

        const char* getStrideType(){
            return "Fixed";
        }

    private:
        float fixedStep;
};