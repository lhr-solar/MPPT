/**
 * Maximum Power Point Tracker Project
 * 
 * File: CAN.h
 * Author: Matthew Yu
 * Organization: UT Solar Vehicles Team
 * Created on: September 12th, 2020
 * Last Modified: 09/26/20
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
    public:
        /**
         * Constructor for a CANDevice object.
         * 
         * @param[in] pinRx RX pin to attach CAN (pin) to.
         * @param[in] pinTx TX pin to attach cAN (pin) to.
         */
        CANDevice(
            const PinName pinRx, 
            const PinName pinTx) : can(pinRx, pinTx, CAN_BUS_BAUD);

        /**
         * Grabs a CAN message from the internal buffer, if any.
         * 
         * @return Pointer to a CAN Message as a char array. 
         * @note Must be freed.
         */
        char* getMessage();

        /**
         * Starts interrupt execution of the private handler function given the 
         * interval.
         * 
         * @param[in] interval Time, in microseconds, between each function call.
         */
        void start(const int interval);
        
        /**
         * Stops interrupt execution of the private handler function given the interval.
         */
        void stop();

    private:
        /**
         * Reads a CANmessage and puts it into the mailbox.
         */
        void handler();

    private:
        CAN can;
        CANMessage msg;
        CANMessage mailbox[CAN_BUS_SIZE];
        Ticker tick;

        /** Lock for the mailbox. I hope you have a key. */
        bool bufferLock;

        /** Indices for traversing the mailbox. */
        int getIdx;
        int putIdx
};

