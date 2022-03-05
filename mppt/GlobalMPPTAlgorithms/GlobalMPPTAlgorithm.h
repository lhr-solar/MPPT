#pragma once
#include <chrono>
#include "mbed.h"
#include "LocalMPPTAlgorithms/PandO.cpp"
#include "LocalMPPTAlgorithms/IncrementalConductance.cpp"
#include "LocalMPPTAlgorithms/FeedbackControl.cpp"
#include "LocalMPPTAlgorithms/Bisection.cpp"

#define MAX_VOLTAGE 100
class GlobalMPPTAlgorithm{
    public:
        GlobalMPPTAlgorithm(int _globalAlgoType, int _strideType, int _localAlgoType);
        float getReferenceVoltage(float vArr, float cArr, float vBatt, float cBatt);
        int getGlobalAlgoType();
        int getLocalAlgoType();
        const char*getStrideType();
        float* getBounds();
        bool checkEnvironmentChanges(float irradiance);
    
    protected:
        float vOld;
        float iOld;
        float pOld;
        int _globalMPPTType;
        LocalMPPTAlgorithm model;
        float runningHistory[10];
        float pastHistories[10];
};
