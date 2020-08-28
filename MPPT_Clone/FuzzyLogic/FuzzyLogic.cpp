#include "mbed.h"
#include "FuzzyLogic.h"

#include "FastPWM.h"
#include "math.h"
#include "Sensors.h"
#include "constants.h"

#define true                 1
#define false                0

static int pulseWidthInMilliSeconds;
static double pwMicroSeconds;
static FastPWM mypwm(DEFAULT_PWM_PIN);
bool pwmChange = false;

static double lastVoltage = 0;
static double lastPower = 0;
static double lastE = 0;
static int mulitplier = 1;

double NB = -1.0;
double NM = -.70;
double NS = -.35;
double PS = .35;
double PM = .70;
double PB = 1.0;

double bigThresh = 100;
double mediumThresh = 10;

void fuzzyInit()
{
    mypwm.period_us(PWM_PERIOD_us); // set the PWM pulsewidth, in us (double), keeping the period the same
    mypwm.pulsewidth_us(PWM_PULSEWIDTH_us);
    pulseWidthInMilliSeconds = 100*PWM_PULSEWIDTH_us;
    
    lastVoltage = 0;
    lastPower = 0;
    lastE = 0;
    pwmChange = false;
}

void fuzzy_logic_control()
{
    double currentVoltage = ReadOutVoltage();
    double currentI = ReadOutCurrent();
    double deltaPower = (currentVoltage * currentI) - lastPower;
    double deltaV = currentVoltage - lastVoltage;
    double currentE = deltaPower / deltaV;
    double deltaE = currentE - lastE;
    
    double inCurrent = ReadInCurrent();
    double inVoltage = ReadInVoltage();
    
    double multiplier = calcFuzzyMultiplier(currentE, deltaE);
    if(mulitplier != 0) {pwmChange = true;}
    pulseWidthInMilliSeconds += (int)(multiplier * STATIC_INCREMENTOR);
    limitFuzzyPulseWidth();
    if(pwmChange)
    {
        pwmChange = false;
        pwMicroSeconds = (double)pulseWidthInMilliSeconds/100;
        mypwm.pulsewidth_us(pwMicroSeconds);  //update new pwm using control logic
    }
    
    lastVoltage = currentVoltage;
    lastPower = currentVoltage * currentI;
    lastE = currentE;
    
    lastPowerInMeasured = inCurrent * inVoltage;
    lastPowerOutMeasured = currentVoltage * currentI;
    lastVoltageInMeasured = inVoltage;
    lastVoltageOutMeasured = currentVoltage;
    lastCurrentInMeasured = inCurrent;
    lastCurrentOutMeasured = currentI;
}

double calcFuzzyMultiplier(double currentE, double deltaE)
{
    if(currentE == 0)
    {
     if(deltaE == 0) {return 0;}
     else if(deltaE >  bigThresh) {return PB;}
     else if(deltaE > mediumThresh && deltaE <= bigThresh) {return PM;}
     else if(deltaE > 0 && deltaE <= mediumThresh) {return PS;}
     else if(deltaE < (-1 * bigThresh)) {return NB;}
     else if(deltaE < (-1 * mediumThresh) && deltaE > (-1 * bigThresh)) {return NM;}
     else{return NS;}
    }
    else if(currentE >  bigThresh)
    {
     if(deltaE == 0) {return PB;}
     else if(deltaE >  bigThresh) {return PB;}
     else if(deltaE > mediumThresh && deltaE <= bigThresh) {return PB;}
     else if(deltaE > 0 && deltaE <= mediumThresh) {return PB;}
     else if(deltaE < (-1 * bigThresh)) {return 0;}
     else if(deltaE < (-1 * mediumThresh) && deltaE > (-1 * bigThresh)) {return PS;}
     else{return PM;}
    }
    else if(currentE > mediumThresh && currentE <= bigThresh)
    {
     if(deltaE == 0) {return PM;}
     else if(deltaE >  bigThresh) {return PB;}
     else if(deltaE > mediumThresh && deltaE <= bigThresh) {return PB;}
     else if(deltaE > 0 && deltaE <= mediumThresh) {return PB;}
     else if(deltaE < (-1 * bigThresh)) {return NS;}
     else if(deltaE < (-1 * mediumThresh) && deltaE > (-1 * bigThresh)) {return 0;}
     else{return PS;}        
    }
    else if(currentE > 0 && currentE <= mediumThresh)
    {
     if(deltaE == 0) {return PS;}
     else if(deltaE >  bigThresh) {return PB;}
     else if(deltaE > mediumThresh && deltaE <= bigThresh) {return PB;}
     else if(deltaE > 0 && deltaE <= mediumThresh) {return PM;}
     else if(deltaE < (-1 * bigThresh)) {return NM;}
     else if(deltaE < (-1 * mediumThresh) && deltaE > (-1 * bigThresh)) {return NS;}
     else{return 0;}        
    }
    else if(currentE < (-1 * bigThresh))
    {
     if(deltaE == 0) {return NB;}
     else if(deltaE >  bigThresh) {return 0;}
     else if(deltaE > mediumThresh && deltaE <= bigThresh) {return NS;}
     else if(deltaE > 0 && deltaE <= mediumThresh) {return NM;}
     else if(deltaE < (-1 * bigThresh)) {return NB;}
     else if(deltaE < (-1 * mediumThresh) && deltaE > (-1 * bigThresh)) {return NB;}
     else{return NB;}        
    }
    else if(currentE < (-1 * mediumThresh) && currentE > (-1 * bigThresh))
    {
     if(deltaE == 0) {return NM;}
     else if(deltaE >  bigThresh) {return PS;}
     else if(deltaE > mediumThresh && deltaE <= bigThresh) {return 0;}
     else if(deltaE > 0 && deltaE <= mediumThresh) {return NS;}
     else if(deltaE < (-1 * bigThresh)) {return NB;}
     else if(deltaE < (-1 * mediumThresh) && deltaE > (-1 * bigThresh)) {return NB;}
     else{return NB;}        
    }
    else
    {
     if(deltaE == 0) {return NS;}
     else if(deltaE >  bigThresh) {return PM;}
     else if(deltaE > mediumThresh && deltaE <= bigThresh) {return PS;}
     else if(deltaE > 0 && deltaE <= mediumThresh) {return 0;}
     else if(deltaE < (-1 * bigThresh)) {return NB;}
     else if(deltaE < (-1 * mediumThresh) && deltaE > (-1 * bigThresh)) {return NB;}
     else{return NM;}        
    }    
}

void limitFuzzyPulseWidth()
{
    if(pulseWidthInMilliSeconds < MIN_PULSE_WIDTH) {pulseWidthInMilliSeconds = MIN_PULSE_WIDTH;}
    else if(pulseWidthInMilliSeconds > MAX_PULSE_WIDTH) {pulseWidthInMilliSeconds = MAX_PULSE_WIDTH;}
}