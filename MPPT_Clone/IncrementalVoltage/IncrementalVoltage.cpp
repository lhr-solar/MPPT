#include "mbed.h"
#include "FastPWM.h"
#include "math.h"

#include "constants.h"
#include "Sensors.h"
#include "IncrementalVoltage.h"

#define true                 1
#define false                0

static int pulseWidthInMilliSeconds;
static double pwMicroSeconds;
static FastPWM mypwm(DEFAULT_PWM_PIN);

double lastI = 0;
double lastV = 0;
double deltaI = 0;
double deltaV = 0;
static bool changed = false;

double Isamples[NUM_SAMPLES_TO_AVERAGE];
double Vsamples[NUM_SAMPLES_TO_AVERAGE];

double getIncrementalPulseWidth()
{
    return (double)pulseWidthInMilliSeconds/100;
} 

void incrementalInit()
{
    mypwm.period_us(PWM_PERIOD_us); 
    // set the PWM pulsewidth, in us (double), keeping the period the same
    mypwm.pulsewidth_us(PWM_PULSEWIDTH_us);
    pulseWidthInMilliSeconds = 100*PWM_PULSEWIDTH_us;
    currentDutyCycle = pulseWidthInMilliSeconds / PWM_PULSEWIDTH_us;
    
    lastI = 0;
    lastV = 0;
    deltaI = 0;
    deltaV = 0;
    changed = false;
}


void incremental_conductance()
{
    //take samples for current and voltage
    //takeSamples();
    //double currentV = calcAverage(Vsamples);
    //double currentI = calcAverage(Isamples);
    double currentI = ReadOutCurrent();
    double currentV = ReadOutVoltage();
    deltaI = currentI - lastI; 
    deltaV = currentV - lastV;
    double currentInI = ReadInCurrent();
    double currentInV = ReadInVoltage();
    
    lastPowerInMeasured = currentInI * currentInV;
    lastPowerOutMeasured = currentI * currentV;
    lastVoltageInMeasured = currentInV;
    lastVoltageOutMeasured = currentV;
    lastCurrentInMeasured = currentInI;
    lastCurrentOutMeasured = currentI;
    
    int multiplier = calcMultiplier(currentI, currentV); //find multiplier by comparing dI / dV = -I / V, if < go right, if > go left, else stay still 
    if(multiplier != 0) {changed = true;}
    pulseWidthInMilliSeconds += multiplier * deltaV;
    limitIncrementalPulseWidth();
    if(changed)
    {
        changed = false;
        pwMicroSeconds = (double)pulseWidthInMilliSeconds/100;
        currentDutyCycle = pulseWidthInMilliSeconds / PWM_PULSEWIDTH_us;
        mypwm.pulsewidth_us(pwMicroSeconds);  //update new pwm using control logic
    }
    lastI = currentI; //update old values and debug info
    lastV = currentV;
}

void takeSamples()
{
    //might implement in order to take multiple samples to average readings inbetween adjustments
}

double calcAverage(double *samples)
{
    double averageReading = 0;
    for(int i = 0; i < NUM_SAMPLES_TO_AVERAGE; i++)
    {
        averageReading += samples[i];
    }
    averageReading /= float(NUM_SAMPLES_TO_AVERAGE);
    return averageReading; 
}

void limitIncrementalPulseWidth()
{
    if(pulseWidthInMilliSeconds >= MAX_PULSE_WIDTH) {pulseWidthInMilliSeconds = MAX_PULSE_WIDTH;}
    else if(pulseWidthInMilliSeconds < MIN_PULSE_WIDTH) {pulseWidthInMilliSeconds = MIN_PULSE_WIDTH;}
}


int calcMultiplier(double currentI, double currentV)
{

    if(deltaV)
    {
        double deltaP = currentI * currentV - deltaI * deltaV;
        double result = deltaP / deltaV;
        if(result > 0) {return 1;}
        else if(result < 0) {return -1;}
        else{return 0;}
    }
    else
    {
        if(deltaI > 0) {return 1;}
        else if(deltaI < 0) {return -1;}
        else{return 0;}
    }
}

