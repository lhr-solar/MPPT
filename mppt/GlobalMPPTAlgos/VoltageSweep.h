/**
 * Maximum Power Point Tracker Project
 * 
 * File: VoltageSweep.cpp
 * Author: Afnan Mir
 * Organization: UT Solar Vehicles Team
 * Created on: June 14th, 2021
 * Last Modified: 06/14/2021
 * 
 * File Discription: This cpp file implements the VoltageSweep class, which
 * is a derivative class of the Global MPPT algroithms class.
 */

#pragma once
#include "GlobalMPPTAlgorithm.h"
#define SIZE 10

class VoltageSweep: public GlobalAlgo{
    VoltageSweep(const PinName pin, LocalType local, StrideType type,double step) : GlobalAlgo(pin,local,type){
        for(int i=0;i<SIZE;i++){
            voltagePeaks[i] = -1;
            powerPeaks[i] = -1;
            if(i == 0){
                voltageTroughs[i] = 0;
            }else{
                voltageTroughs[i] = -1
            }
        }
        sweeping = true;
        increasing = true;
        voltagePeakIndex = 0;
        voltageTroughIndex = 1;
        powerPeakIndex = 0;
        maxPower = 0;
        this->step = step;
        setup = true;
        runningHistoryIndex = 0;
        pastHistoriesIndex=0;
        runHistoryFull=0;
        pastHistoryFull=0;
        runningHistoryAverage=0;
        pastHistoryAverage = 0;
    }
    const char* getName() const{
        return "Voltage Sweep";
    }
    double getLeftBound(){
        double leftBound;
        if(maxPowerIndex == 0){
            leftBound = voltagePeaks[maxPowerIndex]/2;
        }else{
            leftBound = max(voltageTroughs[maxPowerIndex],(voltagePeaks[maxPowerIndex] + voltagePeaks[maxPowerIndex-1])/2);
        }
        return leftBound;
    }
    double getRightBound(){
        double rightBound;
        if(maxPowerIndex == powerPeaksIndex - 1){
            rightBound = MAX_VOLTAGE;
        }else{
            double trough = voltageTroughs[maxPowerIndex+1]-0.02;
            double average = (voltagePeaks[maxPowerIndex] + voltagePeaks[maxPowerIndex-1])/2
        }
        return rightBound;
    }
    
    private:
        double step;
        double voltagePeaks[SIZE];
        double voltageTroughs[SIZE];
        double powerPeaks[SIZE];
        bool sweeping;
        bool increasing;
        double maxPower;
        int voltagePeakIndex;
        int voltageTroughIndex;
        int powerPeakIndex;
        bool setup;
        int maxPowerIndex;
        double leftBound;
        double rightBound;
        int runningHistoryIndex;
        int pastHistoriesIndex;
        bool runHistoryFull;
        bool pastHistoryFull;
        double runningHistoryAverage;
        double pastHistoryAverage;
        void handler(){
            if(!semaphore){
                return;
            }
            semaphore = false;
            double arrVolt = arrayVoltage;
            double arrCurr = arrayCurrent;
            double battVolt = battVoltage;
            double battCurr = battCurrent;
            semaphore = true;
            if(sweeping){
                double arrPower = arrVolt * arrCurr;
                targetVoltage = arrVolt;
                if(arrPower < arrPowOld && increasing){
                    voltagePeaks[voltagePeakIndex] = arrVoltOld;
                    powerPeaks[powerPeakIndex] = arrPowOld;
                    voltagePeakIndex++;
                    powerPeakIndex++;
                    increasing = false;
                    if(maxPower < arrPowOld){
                        maxPower = arrPowOld;
                        maxPowerIndex = powerPeakIndex-1;
                    }
                }else if(arrPower >= arrPowOld && !increasing){
                    increasing = true;
                    voltageTroughs[voltageTroughIndex] = arrVoltOld;
                    voltageTroughIndex++;
                }
                targetVoltage += step;
                if(targetVoltage >= MAX_VOLTAGE){
                    sweeping = false;
                }
                arrVoltOld = arrVolt;
                arrPowOld = arrPower;
            }else{
                leftBound = getLeftBound();
                rightBound = getRightBound();
                if(setup){
                    sweeping = false;
                    maxVoltage = voltagePeaks[maxPowerIndex];
                    localAlgo.setup(maxPower,leftBound,rightBound);
                    setup = false;
                }
                if(!runningHistoryFull){
                    runningHistory[runningHistoryIndex] = arrVolt * arrCurr;
                    runningHistoryIndex = runningHistoryIndex + 1;
                    runningHistoryAverage += arrVolt * arrCurr;
                    if(runningHistoryIndex == SIZE){
                        runHistoryFull = true;
                        runningHistoryIndex = 0;
                        runningHistoryAverage /= SIZE;
                    }
                }else{
                    double pastAverage = runningHistoryAverage;
                    runningHistoryAverage -= runningHistory[runningHistoryIndex]/SIZE;
                    runningHistoryAverage += (arrCurr * arrVolt)/SIZE;
                    runningHistory[runningHistoryIndex] = arrVolt * arrCurr;
                    runningHistoryIndex = (runningHistoryIndex + 1) % SIZE;
                    if(!pastHistoryFull){
                        pastHistories[pastHistoriesIndex] = runningHistoryAverage;
                        pastHistoriesIndex++;
                        pastHistoryAverage += runningHistoryAverage;
                        if(pastHistoriesIndex == SIZE){
                            pastHistoryFull = true;
                            pastHistoriesIndex = 0;
                            pastHistoryAverage /= SIZE;
                        }
                    }else{
                        double previousPast = pastHistoryAverage;
                        pastHistoryAverage -= pastHistories[pastHistoriesIndex]/SIZE;
                        pastHistoryAverage += runningHistoryAverage/SIZE;
                        pastHistories[pastHistoriesIndex] = runningHistoryAverage;
                        pastHistoriesIndex = (pastHistoriesIndex + 1) % SIZE;
                        if((pastHistories[(pastHistoriesIndex-1) % SIZE] - (pastHistories[(pastHistoriesIndex-2) % SIZE]))/pastHistories[(pastHistoriesIndex-1) % SIZE] <= -0.5){
                            sweeping = true;
                            setup = true;
                            targetVoltage = 0;
                            pastHistoriesIndex = 0;
                            pastHistoryAverage = 0;
                            pastHistoryFull = false;
                            runningHistoryAverage = 0;
                            runningHistoryIndex = 0;
                            runHistoryFull = false;
                            voltagePeakIndex = 0;
                            powerPeakIndex = 0;
                            increasing = true;
                            maxPower = 0;
                            maxPowerIndex = -1;
                            voltageTroughs[0] = 0;
                            voltageTroughIndex = 1;
                        }
                    }
                }
                if(arrVolt >= MAX_VOLTAGE){
                    targetVoltage = getLeftBound();
                }else if(arrVolt == leftBound){
                    targetVoltage = leftBound + 0.02
                }else if(targetVoltage != 0){
                    targetVoltage = localAlgo.handler(arrVolt,arrCurr);
                    if(targetVoltage < leftBound){
                        targetVoltage = leftBound;
                    }
                    if(targetVoltage > rightBound){
                        targetVoltage = rightBound;
                    }
                }
                arrVoltOld = arrVolt;
                arrPowOld = arrVolt*arrCurr;
            }
        }
};