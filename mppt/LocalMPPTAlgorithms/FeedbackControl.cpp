#include "LocalMPPTAlgorithm.h"

class FeedbackControl: public LocalMPPTAlgorithm{
    public:
        FeedbackControl() : LocalMPPTAlgorithm(FC, 0){}

        float getReferenceVoltage(float vArr, float cArr, float vBatt, float cBatt){
            float arrPower = vArr * cArr;
            float dP = arrPower - pOld;
            float dV = vArr - vOld;
            float step = stride.getStride(vArr, cArr, vBatt, cBatt);
            float vRef = vArr;
            if(dV == 0){
                vRef += 0.05;
            }else if(abs(dP/dV) < error){

            }else{
                if(dP/dV > 0){
                    vRef += step;
                }else{
                    vRef -= step;
                }
            }
            vOld = vArr;
            iOld = cArr;
            pOld = arrPower;
            return vRef;
        }

        const char* getLocalAlgoType(){
            return "Feedback Control";
        }
    private:
        float error = 0.05;
};