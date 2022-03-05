#include "GlobalMPPTAlgorithm.h"
#include <algorithm>

#define SIZE 10

class VoltageSweep : public GlobalMPPTAlgorithm{
    public:
        VoltageSweep(int _localType, int _strideType, float stepSize) : GlobalMPPTAlgorithm(VOLTAGE_SWEEP,_localType, _strideType){
            step = stepSize;
            sweeping = true;
            increasing = true;
            voltagePeakIndex = 0;
            voltageTroughIndex = 1;
            powerPeakIndex = 0;
            maxPower = 0;
            step = stepSize;
            setup = true;
        }

        float sweep(float vArr, float cArr, float vBatt, float cBatt){
            float arrPower = vArr * cArr;
            float vRef = vArr;
            if(arrPower > pOld && increasing){
                voltagePeaks[voltagePeakIndex++] = vOld;
                powerPeaks[powerPeakIndex++] = pOld;
                if(pOld > maxPower){
                    maxPower = pOld;
                    maxPowerIndex = powerPeakIndex-1;
                    maxVoltage = vOld;
                    maxVoltageIndex = voltagePeakIndex - 1;
                }
                increasing = false;
            }else if(arrPower > pOld && !increasing){
                increasing = true;
                voltageTroughs[voltageTroughIndex] = vOld;
            }
            vRef += step;
            vOld = vArr;
            iOld = cArr;
            pOld = arrPower;
            return vRef;
        }

        float getLeftBound() {
            float leftBound;
            if(maxPowerIndex == 0){
                leftBound = voltagePeaks[maxPowerIndex]/2;
            }else{
                leftBound = max(voltageTroughs[maxPowerIndex],(voltagePeaks[maxPowerIndex] + voltagePeaks[maxPowerIndex - 1])/2);
            }
            return leftBound;
        }

        float getRightBound() {
            double rightBound;
            if(maxPowerIndex == powerPeakIndex - 1){
                rightBound = 100.0; // Subject to change
            }else{
                float trough = voltageTroughs[maxPowerIndex + 1] - 0.02;
                float average = (voltagePeaks[maxPowerIndex] + voltagePeaks[maxPowerIndex + 1])/2;
                rightBound = max(trough, average);
            }
            return rightBound;
        }

        float getReferenceVoltage(float vArr, float cArr, float vBatt, float cBatt){
            float vRef = vArr;
            if(sweeping && vArr < MAX_VOLTAGE){
                vRef = sweep(vArr, cArr, vBatt, cBatt);
            }else{
                float leftBound = getLeftBound();
                float rightBound = getRightBound();
                if(setup){
                    sweeping = false;
                    model.setup(maxVoltage, leftBound, rightBound);
                    setup = false;
                    return leftBound;
                }
                if(vArr == leftBound){
                    vRef = leftBound += 0.02;
                }else if(vRef != 0){
                    vRef = model.getReferenceVoltage(vArr, cArr, vBatt, cBatt);
                    if(vRef < leftBound){
                        vRef = leftBound;
                    }
                    if(vRef > rightBound){
                        vRef = rightBound;
                    }
                }
            }
            return vRef;
        }

        const char* getGlobalAlgoString(){
            return "Voltage Sweep";
        }


    protected:
        double step;
        double voltagePeaks[SIZE];
        double voltageTroughs[SIZE];
        double powerPeaks[SIZE];
        bool sweeping;
        bool increasing;
        double maxPower;
        double maxVoltage;
        int voltagePeakIndex;
        int voltageTroughIndex;
        int powerPeakIndex;
        bool setup;
        int maxPowerIndex;
        int maxVoltageIndex;
        
};