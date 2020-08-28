/*******************************************************************************
 * constants.h
 *
 * Static constants for the entire program
 * Fall 2017 MPPT using the Nucleo-L432KC (Pholociraptor)
 * 
 * Author: Samantha Guu
 * Team: Samuel Chiu, Madeline Drake, Kyle Grier, Rafael Ibanez, Chase Lansdale,
 *       Brooks Loper
 * Created on: November 12, 2017
 * Revised on: November 14, 2017
 ******************************************************************************/
 
#ifndef __constants_h__
#define __constants_h__

#include "mbed.h"

#define SERIAL_BAUD 115200
extern Serial pc;

extern double currentDutyCycle;

// general program settings
static const bool useTime = false;          // turn on if want to time 1 sample
static const bool staticPerturb = true;     // true = constant perturb amt
                                            // false = calculated perturb amt
// main.cpp
static const double PRINT_PERIOD = 2;       // how fast we are printing info (secs)
static const double SAMPLE_PERIOD = 0.05;   // how fast we are doing P&O (secs)
//     for increment-on-switch-press subprogram
static int STATIC_INCREMENTOR = 50;         // added/subtracted from pulseWidth

// Sensors.cpp
static const double V_IN_MULT = 54.28;         //Fall2019 Changes: 54->52.3
static const double V_OUT_MULT = 54.28;        // = 56
static const double I_IN_MULT = 5;
static const double I_OUT_MULT = 5;
static const double HALL_IN_NO_CURRENT = 2.5;
static const double HALL_OUT_NO_CURRENT = 2.5;
static const double AIN_MULT = 3.3;

//new sensor constants
//linear regresstion fit
static const float Beta1 = 0.6137;
static const float Beta0 = 0.0016;
static const int NUM_SAMPLES_TO_AVERAGE_SENSOR = 7; 

// General to all algorithms
#define DEFAULT_PWM_PIN PA_1
static const double PWM_PERIOD_us = 40;     // 25 kHz switching
static const double PWM_PULSEWIDTH_us = 10; // initial duty cycle setting of 10us/40us -> 25%
static const int MAX_PULSE_WIDTH = 2800;
static const int MIN_PULSE_WIDTH = 500;
static float runtime = 0;

static const int MAX_BATTERY_VOLTAGE = 130;
static const int MIN_BATTERY_VOLTAGE = 5;

static float lastPowerInMeasured    = 0;
static float lastPowerOutMeasured   = 0;
static float lastVoltageInMeasured  = 0;
static float lastVoltageOutMeasured = 0;
static float lastCurrentInMeasured  = 0;
static float lastCurrentOutMeasured = 0; 

// PandO.cpp
static const int NUM_SAMPLES_TO_AVERAGE = 10;          // number of samples to average between each perturbation
static const float SCALING_FACTOR = 50;     // scales how much we perturb by
                                        

#endif