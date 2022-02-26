#include "LocalMPPTAlgorithm.h"

class IncrementalConductance: public LocalMPPTAlgorithm{
    public:
        IncrementalConductance() : LocalMPPTAlgorithm(IC, 0){}
        float getReferenceVoltage(float vArr, float cArr, float vBatt, float cBatt){
            float dI = cArr - iOld;
            float dV = vArr - vOld;
            float step = stride.getStride(vArr, cArr, vBatt, cBatt);
            float vRef = vArr;
            if(abs(dI*vArr + cArr*dV) < error){
                
            }else if(dI*vArr + cArr*dV > error){
                vRef += step;
            }else if(dI * vArr + cArr * dV < -error){
                vRef -= step;
            }
            iOld = cArr;
            vOld = vArr;
            pOld = vArr * cArr;
            return vRef;
        }

        const char* getLocalAlgoType(){
            return "Incremental Conductance";
        }
    private:
        float error = 0.05;
};