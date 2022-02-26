#include "LocalMPPTAlgorithm.h"



LocalMPPTAlgorithm::LocalMPPTAlgorithm(int _localAlgoType, int _strideType){
    _localMPPTType = _localAlgoType;
    if(_strideType == 0){
        stride = FixedStride(FIXED_STRIDE);
    }else if(_strideType == 1){
        stride = AdaptiveStride();
    }else if(_strideType == 2){
        stride = OptimalStride();
    }else if(_strideType == 3){
        stride = BisectionStride();
    }else{
        stride = FixedStride(FIXED_STRIDE);
    }
    vOld = 0.0;
    iOld = 0.0;
    pOld = 0.0;
}

void LocalMPPTAlgorithm::setup(float _VMPP, float _leftBound, float _rightBound){
    leftBound = _leftBound;
    rightBound = _rightBound;
    stride.setUp(_VMPP, 0.05);
}

const char* LocalMPPTAlgorithm::getLocalAlgoType(){
    return "Default";
}

const char* LocalMPPTAlgorithm::getStrideType(){
    return stride.getStrideTypeName();
}

int LocalMPPTAlgorithm::getLocalAlgorithm(){
    return _localMPPTType;
}
