#pragma once
#include <chrono>
#include "mbed.h"

class GlobalMPPTAlgorithm{
    public:
        GlobalMPPTAlgorithm();
        float getReferenceVoltage();
        const char* getGlobalAlgoType();
        const char* getLocalAlgoType();
        const char* getStrideType();
    
    private:
        
};