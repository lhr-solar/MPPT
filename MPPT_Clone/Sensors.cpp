/*******************************************************************************
 * Sensors.cpp
 *
 * Sensor Reading functions
 * Fall 2017 MPPT using the Nucleo-L432KC (Pholociraptor)
 * 
 * Author: Samantha Guu
 * Team: Samuel Chiu, Madeline Drake, Kyle Grier, Rafael Ibanez, Chase Lansdale,
 *       Brooks Loper
 * Created on: November 12, 2017
 * Revised on: November 14, 2017
 ******************************************************************************/
 
#include "mbed.h"
#include "constants.h"

AnalogIn v_in(PA_6);
AnalogIn v_out(PA_5);
AnalogIn i_hall_in(PA_5);
AnalogIn i_hall_out(PA_4);

//new sensor 
AnalogIn sensor_in(A3);
AnalogIn sensor_out(A2);

// ****************************** ReadInCurrent ********************************
// This function reads in the raw input current and converts to actual current
// Inputs: none
// Outputs: input current (float)
// Errors: none 
// *****************************************************************************
float ReadInCurrent(void){
    //need to make sure that sensor_in() is in actual voltage
    int cnt;
    float total = 0;
    for(cnt = 0; cnt < NUM_SAMPLES_TO_AVERAGE_SENSOR; cnt++){
        total += (sensor_in.read()* AIN_MULT*4);
    }
    return (total/NUM_SAMPLES_TO_AVERAGE_SENSOR);
}

float readInCurrent(void){
    //need to make sure that sensor_in() is in actual voltage
    float inCurrent = i_hall_in.read() * AIN_MULT * I_IN_MULT - HALL_IN_NO_CURRENT;
    if(inCurrent < 0){
        return 0;
    }
    return inCurrent;
}
// ****************************** ReadOutCurrent *******************************
// This function reads in the raw output current and converts to actual current
// Inputs: none
// Outputs: output current (float)
// Errors: none 
// *****************************************************************************
float ReadOutCurrent(void){
    //need to make sure that sensor_in() is in actual voltage
    int cnt;
    float total = 0;
    for(cnt = 0; cnt < NUM_SAMPLES_TO_AVERAGE_SENSOR; cnt++){
        total += sensor_out.read()* AIN_MULT * 4;
    }
    return (total/NUM_SAMPLES_TO_AVERAGE_SENSOR);
}

float readOutCurrent(void){
    //need to make sure that sensor_in() is in actual voltage
    float outCurrent = i_hall_out.read() * AIN_MULT * I_OUT_MULT - HALL_OUT_NO_CURRENT;
    if(outCurrent < 0){
        return 0;
    }
    return outCurrent;
}

// ****************************** ReadInVoltage ********************************
// This function reads in the raw input voltage and converts to actual voltage
// Inputs: none
// Outputs: input voltage (float)
// Errors: none 
// *****************************************************************************
float ReadInVoltage(void){
    return (v_in.read() * AIN_MULT * V_IN_MULT);
}

// ****************************** ReadOutVoltage *******************************
// This function reads in the raw output voltage and converts to actual voltage
// Inputs: none
// Outputs: output voltage (float)
// Errors: none 
// *****************************************************************************
float ReadOutVoltage(void){

    //pc.printf("Out (battery) voltage: %f\n\r",v_out.read()*AIN_MULT*V_OUT_MULT*0.96);
    //wait(1);
    return (v_out.read() * AIN_MULT * V_OUT_MULT);
}