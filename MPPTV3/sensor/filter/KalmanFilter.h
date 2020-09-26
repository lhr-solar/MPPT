/**
 * Maximum Power Point Tracker Project
 * 
 * File: SMAFilter.h
 * Author: Matthew Yu
 * Organization: UT Solar Vehicles Team
 * Created on: September 20th, 2020
 * Last Modified: 9/20/20
 * 
 * File Discription: This header file implements the KalmanFilter class, which
 * is a derived class from the parent Filter class.
 * 
 * Source: https://www.kalmanfilter.net/kalman1d.html
 */
#pragma once
#include "filter.h"
#include <new>
#include <stdio.h>


/**
 * Definition of a derived implementation for a Kalman filter.
 * 
 * The KalmanFilter class creates objects that can be used to smooth data
 * measurements provided in a stream format.
 */
class KalmanFilter: public Filter{
    protected:
        double estimate; // guess
        double eu; // estimate uncertainty (variance)
        double mu; // measurement uncertainty
        double q; // process noise variance

    public:
        KalmanFilter() { KalmanFilter(10, 10.0, 225, 25, 0.15); } // default implementation
        
        /**
         * constructor for a KalmanFilter object.
         * 
         * @param maxSamples (int)
         *      number of samples that the filter should hold at maximum at any
         *      one time.
         * @precondition maxSamples is a positive number.
         */
        KalmanFilter(int maxSamples) : Filter(maxSamples) {
            estimate = 10.0;
            eu = 225;
            mu = 25;
            q = 0.15;
        }

        /**
         * constructor for a KalmanFilter object.
         * 
         * @param maxSamples (int)
         *      number of samples that the filter should hold at maximum at any
         *      one time.
         * @param initialEstimate (double)
         *      Initial guess of a sensor sample value. A best guess would be at
         *      STC (i.e. Temp sensor: 25.0 C, 128 cell subarray - .65V each:
         *      85.0 V, 5.5 A from a subarray)
         * @param estimateUncertainty (double)
         *      estimate uncertainty variance. Play around with this value.
         *      Decreases over time by itself after initialization.
         * @param measurementUncertainty (double)
         *      Uncertainty of the input measurement. Typically listed on the
         *      datasheet but may need to be determined for custom builds (i.e.
         *      RTD to ADC).
         * @param processNoiseVariance (double)
         *      Measurement of how good we think our model is. Recommended range
         *      is 0.15 to 0.001. Play around with this value.
         * @precondition maxSamples is a positive number.
         */
        KalmanFilter(
            int maxSamples, 
            double initialEstimate,
            double estimateUncertainty,
            double measurementUncertainty,
            double processNoiseVariance
        ) : Filter(maxSamples) {
            estimate = initialEstimate;
            eu = estimateUncertainty;
            mu = measurementUncertainty;
            q = processNoiseVariance;
        }

        /**
         * adds a sample to the filter and updates calculations.
         * 
         * @param sample (double)
         *      input sample to calculate filter with.
         */
        void addSample(double sample) { 
            // Kalman Gain
            double K = eu / (eu + mu);
            // estimate update (state update)
            estimate = estimate + K * (sample - estimate);
            // estimate uncertainty
            eu = (1-K) * eu;

            // predict estimate
            estimate = estimate;
            // predict estimate uncertainty
            eu = eu + q;
        }

        /**
         * returns the filtered result of the input data.
         * 
         * @return double
         *      filter output.
         */
        double getResult() { 
            return estimate;
        }

        /**
         * Deallocates constructs in the filter for shutdown.
         */
        void shutdown() {}
};


void TEST() {
    printf("Hello World Test\n");
    // setup
    KalmanFilter filter(5); // 5 sample buffer
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