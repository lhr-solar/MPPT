#include "LocalMPPTAlgorithm.h"

class Bisection: public LocalMPPTAlgorithm{
    public:
        Bisection() : LocalMPPTAlgorithm(BISECTION, 0){};
    private:
        float error = 0.01;
        int cycle;

};