#include "GlobalMPPTAlgorithm.h"
class Trapezium : public GlobalMPPTAlgorithm{
    public:
        Trapezium(int _localType, int _strideType) : GlobalMPPTAlgorithm(3, _localType, _strideType){
            pRef = 0;
            aRef = 0;
            vRef = 0;
            aOld = 0;
            findingtrapezoids = true;
            startLocal = true;
            kick = true;
            // areas = {0};
            pointer = 0;
            DV = .05;
            pOld = 0;
            vOld = 0;
        }
        float getReferenceVoltage(float vArr, float cArr, float vBatt, float cBatt){
            float vRef = vArr;
            float arrPower = vArr * cArr;
            if (findingtrapezoids == true){
                float currentarea = ((DV * .5)*(arrPower + pOld));
                areas[pointer] = currentarea;
                pointer++;
                float DA = currentarea - aOld;
                float DP = arrPower - pOld;
                if (DA > 0){
                    aRef = currentarea;
                    pRef = pOld;
                    this->vRef = vOld;
                    if (currentarea >= aRef && arrPower >= pRef){
                        pRef = arrPower;
                        this->vRef = vArr;
                    }
                }
                else{
                    if(currentarea >= aRef && arrPower >= pRef){
                        pRef = arrPower;
                        this->vRef = vArr;
                    }
                    this->vRef = vRef + DV;
                    vOld = vArr;
                    pOld = arrPower;
                    aOld = currentarea;

                }
                if(vRef > MAX_VOLTAGE){
                    findingtrapezoids = false;
                    return this->vRef;
                }
                return vRef;
            }
            else{
                if (startLocal == true){
                    vRef = this->vRef;
                    startLocal = false;
                    model.setup(this->vRef, 0 , MAX_VOLTAGE);
                }
                else if(kick == true){
                    vRef = vArr + .02;
                    kick = false;
                    vOld = vArr;
                    pOld = cArr * vArr;
                    //model.stridemodel.vold = arrvoltage
                    // model.stridemodel.pold = pold;
                    iOld = cArr;
                }
                else{
                    vRef = model.getReferenceVoltage(vArr,cArr,vBatt, cBatt);
                    //needsChange = checkenvironmentalchanges(irradiance)
                    // if(needsChange == true){
                    //     vRef = 0;
                    //     pRef = 0;
                    //     aRef = 0;
                    //     aOld = 0;
                    //     findingtrapezoids = true;
                    //     startLocal = true;
                    //     kick = true;
                    //     //runninghistory.clear()
                    //     return vRef
                    // }
                    return vRef;
                }
            }
            return vRef;
        }
    private:
        float pRef;
        float aRef;
        float vRef;
        float aOld;
        bool findingtrapezoids;
        bool startLocal;
        bool kick;
        float areas[100] = {0};
        int pointer;
        float DV;
        
};


