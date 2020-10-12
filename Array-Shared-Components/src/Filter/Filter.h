/**
 * Maximum Power Point Tracker Project
 * 
 * File: Filter.h
 * Author: Matthew Yu
 * Organization: UT Solar Vehicles Team
 * Created on: September 19th, 2020
 * Last Modified: 10/07/20
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
    public:
        Filter(); // default implementation

        /**
         * constructor for a filter object.
         * 
         * @param[in] maxSamples Number of samples that the filter should hold at 
         *      maximum at any one time.
         */
        Filter(const int maxSamples);

        /**
         * Adds a sample to the filter and updates calculations.
         * 
         * @param[in] val Input value to calculate filter with.
         */
        void addSample(const double val);

        /**
         * Returns the filtered result of the input data.
         * 
         * @return Filter output.
         */
        double getResult() const;

        /**
         * Deallocates constructs in the filter for shutdown.
         */
        void shutdown();
    
    protected:
        /** Maximum number of samples that can be held. */
        int _maxSamples;

        /** Current value of the filter output. */
        double currentVal;
};

