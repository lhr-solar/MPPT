#include "LocalMPPTAlgorithm.h"

class Ternary : public LocalMPPTAlgorithm{
    public:
        Ternary(int _strideType) : LocalMPPTAlgorithm(TERNARY, _strideType){
            cycle = 0;
            l1 = 0;
            l2 = 0;
            powerL1 = 0;
            powerL2 = 0;
            q = 0.33;
        }

        float getReferenceVoltage(float vArr, float cArr, float vBatt, float cBatt) override{
            float vRef = 0;
            if(cycle == 0){
                powerL2 = vArr*cArr;
                if(powerL1 > powerL2){
                    rightBound = l2;
                }else{
                    leftBound = l1;
                }
                l1 = (rightBound - leftBound)*q + leftBound;
                vRef = l1;
                cycle = 1;
            }else if(cycle == 1){
                powerL1 = vArr * cArr;
                l2 = rightBound - (rightBound - leftBound)*q;
                vRef = l2;
                cycle = 0;
            }
            return vRef;
        }

        const char* getLocalAlgoType(){
            return "Ternary";
        }
    private:
        int cycle;
        float l1;
        float l2;
        float powerL1;
        float powerL2;
        float q;
};