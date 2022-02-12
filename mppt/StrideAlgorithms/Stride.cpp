#include "Stride.h"

Stride::Stride(int _strideType){
    strideType = _strideType;
    vOld = 0.0;
    iOld = 0.0;
    pOld = 0.0;
    VMPP = 0.621;
}

void Stride::setUp(float _VMPP, float _error){
    VMPP = _VMPP;
    error = _error;
}

// float Stride::getReferenceVoltage(float vArr,float cArr,float vBatt,float cBatt){
//     return vArr;
// }

const char* Stride::getStrideTypeName(){
    return "Default";
}

int Stride::getStrideType(){
    return strideType;
}

