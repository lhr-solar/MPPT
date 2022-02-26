#pragma once
#include <chrono>
#include "mbed.h"
#include "StrideAlgorithms/Stride.h"
#include "StrideAlgorithms/AdaptiveStride.cpp"
#include "StrideAlgorithms/BisectionStride.cpp"
#include "StrideAlgorithms/FixedStride.cpp"
#include "StrideAlgorithms/OptimalStride.cpp"
 
#define FIXED_STRIDE 1.0
#define PANDO 0
#define BISECTION 1
#define GOLDEN 2
#define IC 3
#define FC 4
#define TERNARY 5
 
 
 
class LocalMPPTAlgorithm{
    public:
        LocalMPPTAlgorithm();
        LocalMPPTAlgorithm(int localAlgoType, int stride);
        virtual float getReferenceVoltage(float vArr, float cArr, float vBatt, float cBatt);
        void setup(float _VMPP, float leftBound, float rightBound);
        const char* getLocalAlgoType();
        const char* getStrideType();
        int getLocalAlgorithm();
 
    protected:
        float pOld;
        float iOld;
        float vOld;
        float leftBound;
        float rightBound;
        int _localMPPTType;
        Stride stride;
};
