/**
 * Maximum Power Point Tracker Project
 * 
 * File: SimulatedAnnealing.cpp
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
#include <math.h>
#define ALPHA 0.75 //ALPHA is the decay rate of the temperature
#define INIT_TEMP 25 //INIT_TEMP is the initial temperature of the simulated annealing
#define MIN_TEMP 0.4 //MIN_TEMP is the temperature to stop the simulated annealing


class SimulatedAnnealing : public GlobalAlgo{
    public:
        /**
         * Constructor for a Simulated Annealing object to find the global MPP
         * @param pin the pin of the LED
         * @param local the local algorithm to pair with simulated annealing
         * @param type the stride to pair with the local and global algorithm
         */
        SimulatedAnnealing(const PinName pin, LocalType local, StrideType type) : GlobalAlgo(pin, local, type){
            temperature = INIT_TEMP;
            cycle = 0;
            startLocal = true;
            kick = true;
        }
        const char* getName() const{ return "Simulated Annealing"; } 
    
    private:
        /** Current temperature of simulated annealing */
        double temperature;
        /** current cycle number */
        int cycle;
        /** whether or not local algorithm should start */
        bool startLocal;
        /** If on first cycle of local algorithm */
        bool kick;
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

        void reset(){
           temperature = INIT_TEMP;
           cycle = 0;
           startLocal = true;
           kick = true;
           targetVoltage = 0;
           pastHistoriesIndex = 0;
           pastHistoryAverage = 0;
           pastHistoryFull = false;
           runningHistoryAverage = 0;
           runningHistoryIndex = 0;
           runHistoryFull = false;
        }

        void handler(){
            if(!semaphore){
                return;
            }
            //take in the inputs
            semaphore = false;
            double arrVolt = arrayVoltage;
            double arrCurr = arrayCurrent;
            double battVolt = battVoltage;
            double battCurr = battCurrent;
            semaphore = true; 
            //Random search time
            if(temperature > MIN_TEMP){
                if(cycle == 0){
                    targetVoltage = round(((double) rand()/RAND_MAX)*MAX_VOLTAGE,2); //fix so that it does doubles
                    cycle += 1;
                    arrVoltOld = arrVolt;
                    arrPowOld = arrCurr * arrVolt;
                }else if(cycle == 1){
                    arrVoltOld = arrVolt;
                    arrPowOld = arrCurr * arrVolt;
                }else{
                    double arrPower = arrVolt * arrCurrent;
                    if(arrPower > arrPowOld){ //if current power is greater than set point, change set point to current power
                        arrPowOld = arrPower;
                        arrVoltOld = arrVolt;
                        targetVoltage = arrVolt;
                    }else{
                        double p_r = exp((arrPower - arrPowOld)/temperature); //if current power is less than current set point, accept the new point with a given probability function
                        double diceroll = (double) rand()/RAND_MAX;
                        if(diceroll < p_r){
                            arrVoltOld = arrVolt;
                            arrPowOld = arrPower;
                            targetVoltage = arrVolt;
                        }
                    }
                    if(cycle % 4 == 0){ //every four cycles decrease the temperature by a scale factor of ALPHA
                        temp = temp * ALPHA;
                    }
                    cycle += 1;
                    targetVoltage = round(((double) rand()/RAND_MAX)*MAX_VOLTAGE,2); //pick a new random value for voltage
                }
            }else{ //end of random search
                if(startLocal){
                    targetVoltage = arrVoltOld;
                    startLocal = false;
                }else if(kick){
                    targetVoltage = arrVolt + 0.02; //kick start the local algorithm
                    kick = false;
                    arrVoltOld = arrVolt;
                    arrPowOld = arrVolt * arrCurr;
                }else{
                    targetVoltage = localAlgo.getReferenceVoltage(arrVolt, arrCurr); //local stride keeps current point at or near maximum power point
                    bool needToReset = checkRestart(arrVolt, arrCurr);
                    if(needToReset){
                        reset();
                        return;
                    }
                //     if(!runningHistoryFull){ //while the running history is not full, fill it up
                //     runningHistory[runningHistoryIndex] = arrVolt * arrCurr; //add current power point to history
                //     runningHistoryIndex = runningHistoryIndex + 1;
                //     runningHistoryAverage += arrVolt * arrCurr;
                //     if(runningHistoryIndex == SIZE){ //check if full
                //         runHistoryFull = true;
                //         runningHistoryIndex = 0;
                //         runningHistoryAverage /= SIZE; //Update average so that it is actually the average
                //     }
                // }else{
                //     double pastAverage = runningHistoryAverage; //get the past average
                //     runningHistoryAverage -= runningHistory[runningHistoryIndex]/SIZE;//subtract the oldest value out from the averge
                //     runningHistoryAverage += (arrCurr * arrVolt)/SIZE; //add the newest value to the average
                //     runningHistory[runningHistoryIndex] = arrVolt * arrCurr; //add the newest value to the array
                //     runningHistoryIndex = (runningHistoryIndex + 1) % SIZE; //update index
                //     if(!pastHistoryFull){ //while the past histories is not full, fill it up
                //         pastHistories[pastHistoriesIndex] = runningHistoryAverage; //add newest running history to past histories
                //         pastHistoriesIndex++; //update index
                //         pastHistoryAverage += runningHistoryAverage;
                //         if(pastHistoriesIndex == SIZE){ //check if pastHistory is full now
                //             pastHistoryFull = true;
                //             pastHistoriesIndex = 0;
                //             pastHistoryAverage /= SIZE;
                //         }
                //     }else{
                //         double previousPast = pastHistoryAverage; //get the previous past history average
                //         //update the new pastHistoryAverage
                //         pastHistoryAverage -= pastHistories[pastHistoriesIndex]/SIZE;
                //         pastHistoryAverage += runningHistoryAverage/SIZE;
                //         //add the newest running history to the past histories array
                //         pastHistories[pastHistoriesIndex] = runningHistoryAverage;
                //         //update index
                //         pastHistoriesIndex = (pastHistoriesIndex + 1) % SIZE;
                //         //If the percent difference gets below a certain point, we need to restart the global algorithm bc conditions have changed drastically
                //         if(
                //             (pastHistories[(pastHistoriesIndex-1) % SIZE] - (pastHistories[(pastHistoriesIndex-2) % SIZE]))/
                //             pastHistories[(pastHistoriesIndex-1) % SIZE] <= -0.5
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
                    //make sure we are within the bounds of the current peak
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
        }
};
#undef ALPHA 0.75 
#undef INIT_TEMP 25 
#undef MIN_TEMP 0.4
