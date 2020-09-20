/**
 * Maximum Power Point Tracker Project
 * 
 * File: SMAFilter.h
 * Author: Matthew Yu
 * Organization: UT Solar Vehicles Team
 * Created on: September 19th, 2020
 * Last Modified: 9/19/20
 * 
 * File Discription: This header file implements the SMAFilter class, which
 * is a derived class from the parent Filter class. SMA stands for Simple Moving
 * Average.
 */
#pragma once
#include "filter.h"
#include <new>
#include <stdio.h>


/**
 * Definition of a derived implementation for a SMA filter.
 * 
 * The SMAFilter class creates objects that can be used to smooth data
 * measurements provided in a stream format.
 */
class SMAFilter: public Filter{
    protected:
        double * _dataBuffer;
        int _numSamples;
        int _idx;
        double _sum;

    public:
        SMAFilter() { SMAFilter(10); } // default implementation
        /**
         * constructor for a SMAFilter object.
         * 
         * @param maxSamples (int)
         *      number of samples that the filter should hold at maximum at any
         *      one time.
         * @precondition maxSamples is a positive number.
         */
        SMAFilter(int maxSamples) : Filter(maxSamples) {
            // setup the data buffer
            _dataBuffer = new (std::nothrow) double [_maxSamples];
            _idx = 0;
            _numSamples = 0;
            _sum = 0;
        }

        /**
         * adds a sample to the filter and updates calculations.
         * 
         * @param sample (double)
         *      input sample to calculate filter with.
         */
        void addSample(double sample) { 
            // check for exception
            if (_dataBuffer == nullptr) { return; }
            
            // saturate counter at max samples
            if (_numSamples < _maxSamples) {
                _numSamples ++;
                _sum += sample;
            } else {
                // add the new value but remove the value at the 
                // current index we're overwriting
                _sum += sample - _dataBuffer[_idx];
            }
        
            _dataBuffer[_idx] = sample;
            _idx = (_idx + 1) % _maxSamples;
        }

        /**
         * returns the filtered result of the input data.
         * 
         * @return double
         *      filter output.
         */
        double getResult() { 
            // check for exception
            if (_dataBuffer == nullptr) { return 0.0; }

            return _sum / _numSamples;
            printf("Hello world");
        }

        /**
         * Deallocates constructs in the filter for shutdown.
         */
        void shutdown() { delete[] _dataBuffer; }
};


void TEST() {
    printf("Hello World Test\n");
    // setup
    SMAFilter filter(5); // 5 sample buffer
    // add 20 samples, increasing linearly by 10, and then some noisy 100s every 5 cycles.
    for (int i = 0; i < 20; i++) {
        if (i%5 == 0) { filter.addSample(100); } 
        else { filter.addSample(i*10.0); }
    
        // read the filter output at every point
        printf("output:\t%f\n\n", filter.getResult());
    }
    // shutdown
    filter.shutdown();


    // Assert the following at each run
    // 100
    // 55
    // 43.33
    // 40
    // 40
    // 40
    // 50
    // 60
    // 70
    // 80
    // 80
    // 90
    // 100
    // 110
    // 120
    // 120
    // 130
    // 140
    // 150
    // 160
}