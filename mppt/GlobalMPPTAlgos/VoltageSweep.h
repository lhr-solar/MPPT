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
    const char* getName() const{ return "Voltage Sweep"; }
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
        /** interval to increment while sweeping */
        double step;
        /** array to keep track of voltage values of all local peaks */
        double voltagePeaks[SIZE];
        /** array to keep track of voltage values of all local troughs */
        double voltageTroughs[SIZE];
        /** array to keep track of power values of all local peaks */
        double powerPeaks[SIZE];
        /** Whether or not we are currently in sweeping phase */
        bool sweeping;
        /** While sweeping, is the curve increasing at the moment */
        bool increasing;
        /** the maximum power detected from sweeping */
        double maxPower;
        /** index we are at for the voltage peak array */
        int voltagePeakIndex;
        /** index we are at for the voltage trough array */
        int voltageTroughIndex;
        /** index we are at for the power peak array */
        int powerPeakIndex;
        /** After sweeping one cycle must be used to setup for local algorithm */
        bool setup;
        /** index in voltage peak array of where max power is */
        int maxPowerIndex;
        /** left bound for local algorithm */
        double leftBound;
        /** right bound for local algorithm */
        double rightBound;
        /** index we are at for running history array */
        int runningHistoryIndex;
        /** index we are at for pastHistories array */
        int pastHistoriesIndex;
        /** whether 10 items have been entered into running history array */
        bool runHistoryFull;
        /** whether 10 items have been entered into past histories array */
        bool pastHistoryFull;
        /** current average of all values in running histories */
        double runningHistoryAverage;
        /** current average of all averages of past 10 running histories */
        double pastHistoryAverage;

        void addToRunning(double arrayVoltage, double arrayCurrent){
            runningHistory[runningHistoryIndex] = arrayVoltage * arrayCurrent;
            runningHistory = runningHistoryIndex + 1;
            runningHistoryAverage += arrayVoltage * arrayCurrent;
            if(runningHistoryIndex == SIZE){
                runHistoryFull = true;
                runningHistoryIndex = 0;
                runningHistoryAverage /= SIZE;
            }
        }

        void addToPastHistory(double average){
            pastHistories[pastHistoriesIndex] = average;
            pastHistoriesIndex++;
            if(pastHistoriesIndex == SIZE){
                pastHistoryFull = true;
                pastHistoriesIndex = 0;
                pastHistoryAverage /= SIZE;
            }
        }

        bool checkRestart(double arrayVoltage, double arrayCurrent){
            if(!runningHistoryFull){
                addToRunning(arrayVoltage, arrayCurrent);
                return false;
            }else{
                double pastAverage = runningHistoryAverage;
                runningHistoryAverage -= runningHistory[runningHistoryIndex]/SIZE;
                runningHistoryAverage += (arrCurr * arrVolt)/SIZE;
                runningHistory[runningHistoryIndex] = arrayVoltage * arrayCurrent;
                runningHistoryIndex = (runningHistoryIndex + 1) % SIZE;
                if(!pastHistoryFull){
                    addToPastHistory(runningHistoryAverage);
                    return false;
                }else{
                    pastHistories[pastHistoriesIndex] = runningHistoryAverage;
                    pastHistoriesIndex = (pastHistoriesIndex + 1) % 1;
                    if(
                        (pastHistories[(pastHistoriesIndex-1) % SIZE] - (pastHistories[(pastHistoriesIndex-2) % SIZE]))
                        /pastHistories[(pastHistoriesIndex-1) % SIZE] <= -0.5
                        ){
                            return true;
                        } else {
                            return false;
                        }
                }
            }
        }

        void reset(void){
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
                bool needToReset = checkRestart(arrVolt, arrCurr);
                if(needToReset){
                    reset();
                    return;
                }
                // if(!runHistoryFull){
                //     runningHistory[runningHistoryIndex] = arrVolt * arrCurr;
                //     runningHistoryIndex = runningHistoryIndex + 1;
                //     runningHistoryAverage += arrVolt * arrCurr;
                //     if(runningHistoryIndex == SIZE){
                //         runHistoryFull = true;
                //         runningHistoryIndex = 0;
                //         runningHistoryAverage /= SIZE;
                //     }
                // }else{
                //     double pastAverage = runningHistoryAverage;
                //     runningHistoryAverage -= runningHistory[runningHistoryIndex]/SIZE;
                //     runningHistoryAverage += (arrCurr * arrVolt)/SIZE;
                //     runningHistory[runningHistoryIndex] = arrVolt * arrCurr;
                //     runningHistoryIndex = (runningHistoryIndex + 1) % SIZE;
                //     if(!pastHistoryFull){
                //         pastHistories[pastHistoriesIndex] = runningHistoryAverage;
                //         pastHistoriesIndex++;
                //         pastHistoryAverage += runningHistoryAverage;
                //         if(pastHistoriesIndex == SIZE){
                //             pastHistoryFull = true;
                //             pastHistoriesIndex = 0;
                //             pastHistoryAverage /= SIZE;
                //         }
                //     }else{
                //         double previousPast = pastHistoryAverage;
                //         pastHistoryAverage -= pastHistories[pastHistoriesIndex]/SIZE;
                //         pastHistoryAverage += runningHistoryAverage/SIZE;
                //         pastHistories[pastHistoriesIndex] = runningHistoryAverage;
                //         pastHistoriesIndex = (pastHistoriesIndex + 1) % SIZE;
                //         if(
                //             (pastHistories[(pastHistoriesIndex-1) % SIZE] - (pastHistories[(pastHistoriesIndex-2) % SIZE]))
                //             /pastHistories[(pastHistoriesIndex-1) % SIZE] <= -0.5
                //             ){
                //             sweeping = true;
                //             setup = true;
                //             targetVoltage = 0;
                //             pastHistoriesIndex = 0;
                //             pastHistoryAverage = 0;
                //             pastHistoryFull = false;
                //             runningHistoryAverage = 0;
                //             runningHistoryIndex = 0;
                //             runHistoryFull = false;
                //             voltagePeakIndex = 0;
                //             powerPeakIndex = 0;
                //             increasing = true;
                //             maxPower = 0;
                //             maxPowerIndex = -1;
                //             voltageTroughs[0] = 0;
                //             voltageTroughIndex = 1;
                //         }
                //     }
                // }
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
#undef SIZE
