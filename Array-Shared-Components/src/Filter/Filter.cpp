#include "Filter.h"


Filter::Filter() : currentVal(0) { Filter(10); }

Filter::Filter(const int maxSamples) : currentVal(0) {
    _maxSamples = maxSamples;
    currentVal = 0;
}

void Filter::addSample(const double val) { currentVal = val; }

double Filter::getResult() const { return currentVal; }

void Filter::shutdown() { return; }

