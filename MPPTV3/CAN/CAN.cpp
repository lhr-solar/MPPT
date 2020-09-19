/**
 * Maximum Power Point Tracker Project
 * 
 * File: CAN.cpp
 * Author: Matthew Yu
 * Organization: UT Solar Vehicles Team
 * Created on: September 10th, 2020
 * Last Modified: 10/11/20
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

char* CANDevice::getMessage() {
    while (bufferLock);
    CANMessage canMsg = mailbox[getIdx];
    getIdx = (getIdx + 1) % CAN_BUS_SIZE;
    if (canMsg.id != MPPT_CAN_ID) { return ""; }

    return (char*) canMsg.data;
}

void CANDevice::start(int interval) {
    tick.attach(callback(this, &CANDevice::handler), std::chrono::microseconds(interval));
}

void CANDevice::stop() {
    tick.detach();
}