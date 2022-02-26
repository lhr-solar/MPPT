#pragma once
#include <chrono>
#include "mbed.h"

class Stride{
    public:
        Stride();
        Stride(int _strideType);
        virtual float getStride(float vArr,float cArr,float vBatt,float cBatt);
        void setUp(float _vmpp, float _error);
        const char* getStrideTypeName();
        int getStrideType();

    private:
        
    protected:
        int strideType;
        float vOld;
        float iOld;
        float pOld;
        float VMPP;
        float error;
        float minStride;
        float ERROR = 0.05;

};