/**
 * Maximum Power Point Tracker Project
 * 
 * File: CAN.cpp
 * Author: Matthew Yu
 * Organization: UT Solar Vehicles Team
 * Created on: September 10th, 2020
 * Last Modified: 9/11/20
 * 
 * File Discription: This file manages the CAN class, abstracting away
 * implementation logic to send and receive messages via the CAN lines and
 * providing an easy interface.
 */
#include "CAN.h"

void CANDevice::handler() {
    static int putIdx = 0;
    // turn LED on
    bufferLock = true;
    // if bus buffer is free, read a new byte
    if (((putIdx + 1) % CAN_BUS_SIZE) != getIdx) {
        can.read(msg);
        mailbox[putIdx] = msg;
        putIdx = (putIdx + 1) % CAN_BUS_SIZE;
    }
    bufferLock = false;
}

/**
 * returns a pointer to the current message from the mailbox.
 * Upon calling the getMessage() function again, previous pointers now point to 
 * a new value and should be invalidated.
 *
 * @return char*
 *      current message to be read from the CAN mailbox.
 */
char* CANDevice::getMessage() {
    static char* currentMessage = nullptr;
    
    // dealloc the previous message, if any
    if (currentMessage == nullptr) {
        delete[] currentMessage;
    }
    
    while (bufferLock);
    CANMessage canMsg = mailbox[getIdx];
    getIdx = (getIdx + 1) % CAN_BUS_SIZE;
    if (canMsg.id != MPPT_CAN_ID) { 
        currentMessage = new char[2] {};
    } else {
        // TODO: test to see if we read complete messages
        char* msg = new char[messageLen] {};
        for (int i = 0; i < messageLen; i++) {
            msg[i] = canMsg.data[i];
        }
        currentMessage = msg;
    }

    return currentMessage;
}

void CANDevice::start(int interval) {
    tick.attach(callback(this, &CANDevice::handler), std::chrono::microseconds(interval));
}

void CANDevice::stop() {
    tick.detach();
}