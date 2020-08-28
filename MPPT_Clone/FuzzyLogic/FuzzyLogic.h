#ifndef FUZZYLOGIC_H
#define FUZZYLOGIC_H

#include "constants.h"

void fuzzyInit();
void fuzzy_logic_control();
double calcFuzzyMultiplier(double currentE, double deltaE);
void limitFuzzyPulseWidth();

#endif