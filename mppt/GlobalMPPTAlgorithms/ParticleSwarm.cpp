#include "GlobalMPPTAlgorithm.h"
#include <math.h>

class Particle{
    public:
        Particle(){
            xPosition = 0;
            velocity = 0;
        }

        Particle(float xPos, float vel){
            xPosition = xPos;
            velocity = vel;
        }

        void changeXPos(float vel){
            xPosition += vel;
        }

        void changeVelocity(float v){
            velocity = v;
        }

        float getPBest(){
            return personalBest;
        }

        float getVoltBest(){
            return personalBestVoltage;
        }

        float getXPos(){
            return xPosition;
        }

        float getVelocity(){
            return velocity;
        }

        void changePBest(float newBest, float newBestVolt){
            personalBest = newBest;
            personalBestVoltage = newBestVolt;
        }
    private:
        float xPosition;
        float velocity;
        float personalBest;
        float personalBestVoltage;
};

class ParticleSwarm : GlobalMPPTAlgorithm{
    public:
        ParticleSwarm(int _localType, int _strideType):GlobalMPPTAlgorithm(PARTICLE_SWARM, _localType, _strideType){
            gBest = 0.0;
            gBestVolt = 0.0;
            goForward = true;
            setup = true;
            startLocal = true;
            kick = true;
            cycle = -1;
            totalCycle = 0;
            for(int i=0;i<NUM_AGENTS;i++){
                float percent = ((float) rand()/(RAND_MAX));
                float intervalRange = (float)MAX_VOLTAGE/NUM_AGENTS;
                float start = i*(intervalRange);
                float position = intervalRange*percent + start;
            }
        }
    private:
        const static int NUM_AGENTS = 4;
        const float C1 = 0.02;
        const float C2 = 0.5;
        const float W = 0.35;
        float gBest;
        float gBestVolt;
        Particle agents[NUM_AGENTS];
        bool goForward;
        bool setup;
        bool startLocal;
        bool kick;
        int totalCycle;
        int cycle;
};