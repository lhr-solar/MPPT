/**
 * Maximum Power Point Tracker Project
 * 
 * File: CAN.h
 * Author: Matthew Yu
 * Organization: UT Solar Vehicles Team
 * Created on: September 12th, 2020
 * Last Modified: 10/12/20
 * 
 * File Discription: This file manages the CAN class, abstracting away
 * implementation logic to send and receive messages via the CAN lines and
 * providing an easy interface.
 */
#pragma once
#include "mbed.h"
#include <chrono>

#define MPPT_CAN_ID 100
#define CAN_BUS_SIZE 200
#define CAN_BUS_BAUD 25000


/**
 * Definition of an implementation for the CAN abstraction layer.
 * 
 * The CANDevice implements methods to control the transmission of messages 
 * between the device and other CAN lines. It receives and sends messages 
 * given to it.
 */
class CANDevice {
    protected:
        CAN can;
        CANMessage msg;
        CANMessage mailbox[CAN_BUS_SIZE];
        Ticker tick;

        bool bufferLock;

        int getIdx;

        void handler();

    public:
        /**
         * constructor for a CANDevice object.
         * 
         * @param pinRx (PinName)
         *      rx pin to attach CAN (pin) to.
         * @param pinTx (PinName)
         *      tx pin to attach cAN (pin) to.
         * @param freq (int)
         *      
         */
        CANDevice(PinName pinRx, PinName pinTx) : can(pinRx, pinTx, CAN_BUS_BAUD) {            
            bufferLock = false;
            getIdx = 0;
        }

        char* getMessage();

        void start(int interval);
        
        void stop();
};

