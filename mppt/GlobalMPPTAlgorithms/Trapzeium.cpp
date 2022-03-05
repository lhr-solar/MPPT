#include "GlobalMPPTAlgorithm.h"
/** Using the composite trapezoidal rule,
* the algorithm divides the region under the 
*  Power-Voltage function into trapezoids.
* Comparing the areas of the different trapezoids and power output, 
* the algorithm determines
* the new voltage output reference point.
* If the trapezoid area and power output increases, 
* the algorithm determines that the power and 
* voltage output reference point should increase and 
* vice versa as the trapezoid area decreases. 
* If the trapezoid area increases, but the power output decreases, 
* the reference points stay the same. 
* At points where the area doesn’t increase or decrease and 
* the power output increases or decreases, the reference points change.
* At the voltage intervals where the trapezoid area decreases or 
* stays constant, the local algorithm can then be used to determine 
* a more efficient voltage around the maximum.
*/
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
        /**
        * Returns the new output voltage value
        * @param vArr the last array input voltage. 
        * @param cARR the last array current input. 
        * @param vBatt the last battery voltage input. 
        * @param cBatt the last battery current input.
        * @return vRef, the new voltage output reference point.
        */
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


