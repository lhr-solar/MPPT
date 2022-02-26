#include "LocalMPPTAlgorithm.h"
#include "math.h"

class Golden: public LocalMPPTAlgorithm{
    public:
        Golden(int _strideType) : LocalMPPTAlgorithm(GOLDEN, _strideType){
            cycle = 0;
            l1 = leftBound;
            l2 = rightBound;

            powerL1 = 0;
            powerL2 = 0;
        }

        float getReferenceVoltage(float vArr, float cArr, float vBatt, float cBatt) override{
            float vRef = 0;

            if(cycle == 0){
                l1 = rightBound - (rightBound - leftBound)*phi;
                vRef = l1;
                cycle = 1;
            }else if(cycle == 1){
                powerL1 = vArr * cArr;
                l2 = (rightBound - leftBound)*phi + leftBound;
                vRef = l2;
                cycle = 2;
            }else{
                if(cycle == 2){
                    powerL2 = vArr * cArr;
                }else if(cycle == 3){
                    powerL1 = vArr*cArr;
                }

                if(powerL1 > powerL2){
                    rightBound = l2;
                    l2 = l1;
                    powerL2 = powerL1;
                    l1 = (rightBound - (rightBound - leftBound)*phi);
                    vRef = l1;
                    cycle = 3;
                }else{
                    leftBound = l1;
                    l1 = l2;
                    powerL1 = powerL2;
                    l2 = (rightBound - leftBound) * phi + leftBound;
                    vRef = l2;
                    cycle = 2;
                }
            }
            return vRef;
        }

        const char* getLocalAlgoType(){
            return "Golden";
        }
    private:
        double phi = (sqrt(5) + 1)/2 - 1;
        int cycle;
        float l1;
        float l2;
        float powerL1;
        float powerL2;
};