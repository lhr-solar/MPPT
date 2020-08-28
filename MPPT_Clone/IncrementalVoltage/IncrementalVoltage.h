#ifndef INCREMENTALVOLTAGE_H
#define INCREMENTALVOLTAGE_H

#include "constants.h"

void takeSamples();
double calcAverage(double *samples);
int calcMultiplier(double currentI, double currentV);
void limitPulseWidth();

void incrementalInit();

void limitIncrementalPulseWidth();
void incremental_conductance();

double getIncrementalPulseWidth();

#endif