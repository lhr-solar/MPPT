#include "LocalMPPTAlgorithm.h"
 
class PandO: public LocalMPPTAlgorithm{
    public:
        PandO(int _strideType) : LocalMPPTAlgorithm(PANDO, _strideType){};
 
        float getReferenceVoltage(float vArr, float cArr, float vBatt, float cBatt){
            float arrPower = vArr * cArr;
            float dV = vArr - vOld;
            float dP = arrPower - pOld;
            float step = stride.getStride(vArr, cArr, vBatt, cBatt);
            float vRef = vArr;
            if(dP > 0){
                if (dV > 0){
                    vRef += step;
                }else{
                    vRef -= step;
                }
            }else{
                if(dV > 0){
                    vRef -= step;
                }else{
                    vRef += step;
                }
            }
            vOld = vArr;
            iOld = cArr;
            pOld = arrPower;
            return vRef;
        }
 
        const char* getLocalAlgoType(){
            return "PandO";
        }
 
};
