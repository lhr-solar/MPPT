#pragma once
#include <chrono>
#include "mbed.h"

class LocalMPPTAlgorithm{
    LocalMPPTAlgorithm();
    float getReferenceVoltage();
    const char* getLocalAlgoType();
    const char* getStrideType();

    private:
        
};