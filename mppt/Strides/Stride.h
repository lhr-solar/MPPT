/**
 * Maximum Power Point Tracker Project
 * 
 * File: Stride.h
 * Author: Afnan Mir
 * Organization: UT Solar Vehicles Team
 * Created on: June 5th, 2021
 * Last Modified: 06/05/2021
 * 
 * File Discription: This header file implements the Stride class, which
 * is the parent class of the stride algroithms.
 */
 #pragma once
 
 class Stride{
     public:
        Stride();
        Stride(double Vmpp, double error);
        double getStride(double arrayVoltage, double arrayCurrent);
        const char* get_name() const;
    protected: 
        double battVoltage;
        double battCurrent;
        double targetVoltage;
        double minStride;
        static double arrVoltOld;
        static double arrPowerOld;
        // bool inputLock;
        double error;
        double VMPP;
 };