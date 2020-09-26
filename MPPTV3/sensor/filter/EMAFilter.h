/**
 * Maximum Power Point Tracker Project
 * 
 * File: EMAFilter.h
 * Author: Matthew Yu
 * Organization: UT Solar Vehicles Team
 * Created on: September 20th, 2020
 * Last Modified: 9/20/20
 * 
 * File Discription: This header file implements the EMAFilter class, which
 * is a derived class from the parent Filter class. EMA stands for Exponential
 * Moving Average.
 * 
 * Sources:
 * https://hackaday.com/2019/09/06/sensor-filters-for-coders/
 * https://www.norwegiancreations.com/2015/10/tutorial-potentiometers-with-arduino-and-filtering/
 * https://www.norwegiancreations.com/2016/08/double-exponential-moving-average-filter-speeding-up-the-ema/
 */
#pragma once
#include "filter.h"
#include <new>
#include <limits>
#include <bits/stdc++.h>
#include <cmath>
#include <stdio.h>

/**
 * Definition of a derived implementation for an Exponential Moving Average filter.
 * 
 * The EMAFilter class creates objects that can be used to smooth data
 * measurements provided in a stream format.
 */
class EMAFilter: public Filter{
    protected:
        double avg;
        double alpha;

    public:
        EMAFilter() { EMAFilter(10, 0.2); } // default implementation
        /**
         * constructor for a MedianFilter object.
         * 
         * @param maxSamples (int)
         *      number of samples that the filter should hold at maximum at any
         *      one time.
         * @param alpha (double)
         *  
         * @precondition maxSamples is a positive number.
         */
        EMAFilter(int maxSamples, double alpha) : Filter(maxSamples) {
            avg = 0;
            this->alpha = alpha;
        }

        /**
         * adds a sample to the filter and updates calculations.
         * 
         * @param sample (double)
         *      input sample to calculate filter with.
         */
        void addSample(double sample) { 
            avg = (1-alpha) * avg + alpha * sample;
        }

        /**
         * returns the filtered result of the input data.
         * 
         * @return double
         *      filter output.
         */
        double getResult() { 
            return avg;
        }

        /**
         * Deallocates constructs in the filter for shutdown.
         */
        void shutdown() {}
};

void TEST() {
    printf("Hello World Test\n");
    // setup
    EMAFilter filter(5, .2); // 5 sample buffer
    // add 20 samples, increasing linearly by 10, and then some noisy 100s every 5 cycles.
    for (int i = 0; i < 20; i++) {
        if (i%5 == 0) { filter.addSample(100); } 
        else { filter.addSample(i*10.0); }
    
        // read the filter output at every point
        printf("output:\t%f\n\n", filter.getResult());
    }
    // shutdown
    filter.shutdown();
}