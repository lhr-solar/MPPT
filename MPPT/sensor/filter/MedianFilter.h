/**
 * Maximum Power Point Tracker Project
 * 
 * File: MedianFilter.h
 * Author: Matthew Yu
 * Organization: UT Solar Vehicles Team
 * Created on: September 19th, 2020
 * Last Modified: 9/26/20
 * 
 * File Discription: This header file implements the MedianFilter class, which
 * is a derived class from the parent Filter class.
 */
#pragma once
#include "filter.h"
#include <new>
#include <limits>
#include <bits/stdc++.h>
#include <cmath>
#include <stdio.h>


/**
 * Definition of a derived implementation for a Rolling Median filter.
 * 
 * The MedianFilter class creates objects that can be used to smooth data
 * measurements provided in a stream format.
 */
class MedianFilter: public Filter{
    public:
        MedianFilter() { MedianFilter(10); } // default implementation
        /**
         * Constructor for a MedianFilter object.
         * 
         * @param maxSamples Number of samples that the filter should 
         *      hold at maximum at any one time.
         * @precondition maxSamples is a positive number.
         */
        MedianFilter(const int maxSamples) : Filter(maxSamples) {
            // setup the data buffer
            _dataBuffer = new (std::nothrow) double [_maxSamples];
            _idx = 0;
            _numSamples = 0;
        }

        /**
         * Adds a sample to the filter and updates calculations.
         * 
         * @param[in] val Input value to calculate filter with.
         */
        void addSample(const double sample) { 
            // check for exception
            if (_dataBuffer == nullptr) { return; }
            
            // saturate counter at max samples
            if (_numSamples < _maxSamples) {
                _numSamples ++;
            }
        
            _dataBuffer[_idx] = sample;
            _idx = (_idx + 1) % _maxSamples;
        }

        /**
         * Returns the filtered result of the input data.
         * 
         * @return Filter output.
         */
        double getResult() const { 
            // check for exception
            if (_dataBuffer == nullptr) { return 0.0; }

            // get the range window
            int startIdx = (_idx - _numSamples + _maxSamples) % _maxSamples;
            int endIdx = startIdx + _numSamples;
            // find the median from that range window
            return _getMedian(startIdx, endIdx);
        }

        /**
         * Deallocates constructs in the filter for shutdown.
         */
        void shutdown() { delete[] _dataBuffer; }

    private:
        /**
         * Returns the median of the data buffer.
         * 
         * @param[in] startIdx Start index of the data buffer.
         * @param[in] endIdx End index of the data buffer.
         * @return Median of the data buffer.
         */
        double _getMedian(const int startIdx, const int endIdx) const { 
            // naive solution is to sort the data and pick the n/2 index
            double * tempBuffer = new (std::nothrow) double [_numSamples];
            if (tempBuffer != nullptr) {
                for (int i = 0; i < _numSamples; i++) {
                    tempBuffer[i] = _dataBuffer[(i + startIdx) % _maxSamples];
                }
                
                // sort the buffer
                std::sort(tempBuffer, tempBuffer + _numSamples);
                
                // get the correct index value
                double val = 0.0;
                if (_numSamples == 0) { 
                    return 0.0;
                } else if (_numSamples%2 == 0) {
                    // even, split the median between two values
                    val = (tempBuffer[_numSamples/2] + tempBuffer[_numSamples/2 - 1]) / 2.0;
                } else {
                    val = tempBuffer[(int) floor(_numSamples/2)];
                }
                
                delete[] tempBuffer;
                return val;
            } else {
                return 0.0;
            }
        }

    private:
        /** Data Buffer.  */
        double * _dataBuffer;

        /** Number of samples in the buffer. */
        int _numSamples;

        /** Current index in the buffer. */
        int _idx;

};

void TEST() {
    printf("Hello World Test\n");
    // setup
    MedianFilter filter(5); // 5 sample buffer
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
    // 20
    // 25
    // 30
    // 30
    // 40
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
    // 160
    // 170
}