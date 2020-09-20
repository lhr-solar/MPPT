/**
 * Maximum Power Point Tracker Project
 * 
 * File: filter.h
 * Author: Matthew Yu
 * Organization: UT Solar Vehicles Team
 * Created on: September 19th, 2020
 * Last Modified: 9/19/20
 * 
 * File Discription: This header file describes the Filter class, which is an
 * abstract parent class that defines and implements most of the shared methods
 * among its children.
 */
#pragma once


/**
 * Definition of a base implementation of filters that plug into the sensor
 * class.
 * 
 * The Filter class is extended by children such as MovingAvgFilter and
 * KalmanFilter. It implements a shared API for developers to input
 * measurements, tune the filter, and to retrieve an output value.
 * The parent Filter class simply is a passthrough filter and no analysis is
 * applied.
 */
class Filter {
    protected:
        int _maxSamples;

        double currentVal;
    public:
        Filter() { Filter(10); } // default implementation
        /**
         * constructor for a filter object.
         * 
         * @param maxSamples (int)
         *      number of samples that the filter should hold at maximum at any
         *      one time.
         */
        Filter(int maxSamples) {
            _maxSamples = maxSamples;
            currentVal = 0;
        }

        /**
         * adds a sample to the filter and updates calculations.
         * 
         * @param val (double)
         *      input value to calculate filter with.
         */
        void addSample(double val) { currentVal = val; }

        /**
         * returns the filtered result of the input data.
         * 
         * @return double
         *      filter output.
         */
        double getResult() { return currentVal; }

        /**
         * Deallocates constructs in the filter for shutdown.
         */
        void shutdown() { return; }
};