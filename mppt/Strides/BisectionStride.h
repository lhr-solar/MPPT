/**
 * Maximum Power Point Tracker Project
 * 
 * File: BisectionStride.h
 * Author: Afnan Mir
 * Organization: UT Solar Vehicles Team
 * Created on: June 5th, 2021
 * Last Modified: 06/05/2021
 * 
 * File Discription: This header file implements the BisectionStride class, which
 * is a derivative class of the Stride class.
 */
#pragma once
#include "Stride.h"

class BisectionStride: public Stride{
    public:
        BisectionStride(double slopeMult): Stride(){
            slopeMultiplier = slopeMult;
            minPowDiff = 0.01;
            minVoltDiff = 0.001;
        }
        BisectionStride(double slopeMult, double Vmpp, double error): Stride(Vmpp, error){
            slopeMultiplier = slopeMult;
            minPowDiff = 0.01;
            minVoltDiff = 0.001;
        }
        double getStride(double arrayVoltage, double arrayCurrent){
            // inputLock = true;
            double arrVolt = arrayVoltage;
            double arrCurr = arrayCurrent;
            // inputLock = false;

            double arrVoltDiff = arrVolt - arrVoltOld;
            double arrPowerDiff = arrVolt*arrCurr - arrPowerOld;
            double arrVoltNew = arrVolt;
            double stride = 0;
            if(abs(arrPowerDiff) >= minPowDiff && abs(arrVoltDiff) >= minVoltDiff){
                double slope = arrPowerDiff/arrVoltDiff;
                if(slope < 0){
                    stride = (arrVolt + arrVoltOld)/2 - arrVoltOld;
                }else{
                    stride = slope * slopeMultiplier;
                }
            }
            arrVoltOld = arrVolt;
            arrPowerOld = arrVolt*arrCurr;
            if(stride < minStride){
                return minStride;
            }else{
                return stride;
            }
        }
        const char* get_name() const{ return "Bisection Stride"; }
    
    private:
        /** This variable is used to multiply by the slope to help calculate the perturb amount */
        double slopeMultiplier;
        /** This is the difference in power needed at minimum in order to calculate the stride. If the difference is less, then use minStride*/
        double minPowDiff;
        /** This is the difference in voltage needed at minimum in order to calculate the stride. If the difference is less, then use minStride*/
        double minVoltDiff;
        /** function used to calculate absolute value of a double */
        double abs(double d){
            if(d < 0){
                return d*-1;
            }
            return d;
        }
};
