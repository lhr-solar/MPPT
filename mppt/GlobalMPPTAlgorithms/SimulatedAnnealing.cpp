#include "GlobalMPPTAlgorithm.h"
#include <math.h>

class SimulatedAnnealing : GlobalMPPTAlgorithm{
    public:
        SimulatedAnnealing(int _localType, int _strideType) : GlobalMPPTAlgorithm(SIM_ANNEALING,_localType, _strideType){
            cycle = 0;
            temperature = INIT_TEMP;
            startLocal = true;
            kick = true;
        }

        float getReferenceVoltage(float vArr, float cArr, float vBatt, float cBatt){
            float vRef = vArr;
            if(temperature > 0.2){
                if(cycle == 0){
                    vRef = round(100*((double) rand()/RAND_MAX)*MAX_VOLTAGE)/100.0; 
                    cycle++;
                    vOld = vArr;
                    iOld = cArr;
                    pOld = vArr * cArr;
                }else if(cycle == 1){
                    vOld = vArr;
                    iOld = cArr;
                    pOld = vArr * cArr;
                    cycle++;
                }else{
                    float arrPower = vArr * cArr;
                    if(arrPower > pOld){
                        vOld = vArr;
                        pOld = arrPower;
                        iOld = cArr;
                        vRef = vArr;
                    }else{
                        float p_r = exp(arrPower - pOld/(float) temperature);
                        float diceRoll = (float)rand()/RAND_MAX;
                        if(diceRoll < p_r){
                            vOld = vArr;
                            pOld = arrPower;
                            iOld = cArr;
                            vRef = vArr;
                        }
                    }
                    if(cycle % 4 == 0){
                        temperature = temperature * ALPHA;
                        round(100*((double) rand()/RAND_MAX)*MAX_VOLTAGE)/100.0;
                    }
                    cycle += 1;
                    vRef = round(100*((double) rand()/RAND_MAX)*MAX_VOLTAGE)/100.0;
                }
            }else{
                if(startLocal){
                    vRef = vOld;
                    startLocal = false;
                    model.setup(vOld, 0, MAX_VOLTAGE);
                }else if(kick){
                    vRef = vArr + 0.02;
                    kick = false;
                    vOld = vArr;
                    pOld = cArr * vArr;
                    iOld = cArr;
                }else{
                    vRef = model.getReferenceVoltage(vArr, cArr, vBatt, cBatt);
                }
            }
            return vRef;
        }
    private:
        const float ALPHA = 0.8;
        const float MIN_TEMP = 0.3;
        const float INIT_TEMP = 25;
        const int K = 15;
        int cycle;
        bool startLocal;
        bool kick;
        float temperature;
};