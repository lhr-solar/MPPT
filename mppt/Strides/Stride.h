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
        /**
         * Constructor for a Stride object that will calculate the perturb amount for each cycle 
         */
        Stride();
        /**
         * Constructor for a Stride object that will calculate the perturb amount for each cycle 
         * @param Vmpp the observed maximum power point for optimal and adaptive stride
         * @param error the margin we have to be within of the MPP tp safely say we are at the MPP
         */
        Stride(double Vmpp, double error);
        /**
         * returns the perturb amount needed for the next cycle
         * @param arrayVoltage the current array voltage measured
         * @param arrayCurrent the current array current measured
         * @return the amount we need to perturb for the next cycle
         */
        double getStride(double arrayVoltage, double arrayCurrent);
        /**
         * returns the name of the stride
         * @return the name of the stride
         */
        const char* get_name() const;
        /**
         * Sets the value of the Vmpp instance field after the global context algorithm is done running.
         * @param vmpp the observed vmpp from the global algorithm
         */
        void setup(double vmpp);
    protected:
        /** This variable is used to track the battery voltage */ 
        double battVoltage;
        /** This variable is used to track the battery current*/
        double battCurrent;
        /** This variable is used to store the target voltage*/
        double targetVoltage;
        /** This variable is used as the stride value if we reach a point where the stride is insignificant*/
        double minStride;
        /** This variable is used to track the array voltage on the last cycle*/
        static double arrVoltOld;
        /** This variable is used to track the array power on the last cycle*/
        static double arrPowerOld;
        // bool inputLock;
        /** This variable is the margin of how close we need to be to the MPP in order to safely say we are at the maximum*/
        double error;
        /** This variable is the observed MPP used for Optimal and Adaptive strides*/
        double VMPP;
 };
