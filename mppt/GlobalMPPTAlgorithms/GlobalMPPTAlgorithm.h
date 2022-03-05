#pragma once
#include <chrono>
#include "mbed.h"
#include "LocalMPPTAlgorithms/PandO.cpp"
#include "LocalMPPTAlgorithms/IncrementalConductance.cpp"
#include "LocalMPPTAlgorithms/FeedbackControl.cpp"
#include "LocalMPPTAlgorithms/Bisection.cpp"
#include "LocalMPPTAlgorithms/Golden.cpp"
#include "LocalMPPTAlgorithms/Ternary.cpp"
#define VOLTAGE_SWEEP 0
#define SIM_ANNEALING 1
#define PARTICLE_SWARM 2
#define TRAP_METHOD 3
#define FIREFLY 4

#define MAX_VOLTAGE 100


class GlobalMPPTAlgorithm{
    public:
        GlobalMPPTAlgorithm(int _globalAlgoType, int _strideType, int _localAlgoType);
        float getReferenceVoltage(float vArr, float cArr, float vBatt, float cBatt);
        int getGlobalAlgoType();
        int getLocalAlgoType();
        const char*getStrideType();
        const char* getGlobalAlgoString();
        const char* getLocalAlgoString();
        float getLeftBound();
        float getRightBound();
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
