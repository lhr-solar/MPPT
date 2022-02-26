#include "LocalMPPTAlgorithm.h"

class Bisection: public LocalMPPTAlgorithm{
    public:
        Bisection(int _strideType) : LocalMPPTAlgorithm(BISECTION, _strideType){
            error = 0.1;
            cycle = 0;
        };

        float getReferenceVoltage(float vArr, float cArr, float vBatt, float cBatt) override{
            float vRef = 0;
            if(cycle == 0){
                vRef = (leftBound + rightBound)/2;
                cycle = 1;
                vOld = leftBound;
                pOld = vArr * cArr;
            }else if(cycle == 1){
                float arrPower = vArr * cArr;
                float dP_dV = 0;
                if(vArr - vOld != 0){
                    dP_dV = (arrPower - pOld)/(vArr - vOld);
                }
                if(abs(dP_dV) < error){
                    vRef = vArr;
                }else if(dP_dV > 0){
                    leftBound = vArr;
                    vRef = (leftBound + rightBound)/2;
                }else{
                    rightBound = vArr;
                    vRef = (leftBound + rightBound)/2;
                }
                vOld = vArr;
                pOld = arrPower;
            }
            return vRef;
        }

        const char* getLocalAlgoType(){
            return "Bisection";
        }


    private:
        float error;
        int cycle;

};