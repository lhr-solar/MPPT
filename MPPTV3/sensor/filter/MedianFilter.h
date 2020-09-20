/**
 * Maximum Power Point Tracker Project
 * 
 * File: MedianFilter.h
 * Author: Matthew Yu
 * Organization: UT Solar Vehicles Team
 * Created on: September 19th, 2020
 * Last Modified: 9/19/20
 * 
 * File Discription: This header file implements the MedianFilter class, which
 * is a derived class from the parent Filter class.
 */
#pragma once
#include "filter.h"
#include <new>
#include <limits>

/**
 * Definition of a derived implementation for a Rolling Median filter.
 * 
 * The MedianFilter class create objects that can be used to smooth data
 * measurements provided in a stream format.
 */
class MedianFilter: public Filter{
    protected:
        double * _dataBuffer;
        int _numSamples;
        int _idx;

        double _getMedian(int startIdx, int endIdx) { 
            // naive solution is to sort the data and pick (_numSamples + 1) / 2
            // index
            return 0.0; // TODO: fix this
         }

    public:
        MedianFilter() { MedianFilter(10); } // default implementation
        /**
         * constructor for a MedianFilter object.
         * 
         * @param maxSamples (int)
         *      number of samples that the filter should hold at maximum at any
         *      one time.
         * @precondition maxSamples is a positive number.
         */
        MedianFilter(int maxSamples) : Filter(maxSamples) {
            // setup the data buffer
            _dataBuffer = new (std::nothrow) double [_maxSamples];
            _idx = 0;
            _numSamples = 0;
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
};
