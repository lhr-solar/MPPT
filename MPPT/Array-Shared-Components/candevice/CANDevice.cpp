/**
 * Maximum Power Point Tracker Project
 * 
 * File: CANDevice.cpp
 * Author: Matthew Yu
 * Organization: UT Solar Vehicles Team
 * Created on: September 10th, 2020
 * Last Modified: 9/26/20
 * 
 * File Discription: This file manages the CAN class, abstracting away
 * implementation logic to send and receive messages via the CAN lines and
 * providing an easy interface.
 */
#include "CANDevice.h"


/** Public Methods. */

CANDevice::CANDevice(
    const PinName pinRx, 
    const PinName pinTx) : can(pinRx, pinTx, CAN_BUS_BAUD) 
{
    bufferLock = false;
    getIdx = 0;
    putIdx = 0;
}

char* CANDevice::getMessage() {
    if (bufferLock) return new char[1]();

    CANMessage canMsg = mailbox[getIdx];
    char * msg = new char[canMsg.len];
    std::strcpy(msg, reinterpret_cast <char *>(canMsg.data));

    getIdx = (getIdx + 1) % CAN_BUS_SIZE;
    return msg;
}

void CANDevice::start(const int interval) {
    tick.attach(callback(this, &CANDevice::handler), 
        std::chrono::microseconds(interval));
}

void CANDevice::stop() {
    tick.detach();
}

/** Private Methods. */

void CANDevice::handler() {
    // turn LED on
    bufferLock = true;
    // if bus buffer is free, read a new byte
    if (((putIdx + 1) % CAN_BUS_SIZE) != getIdx) {
        can.read(mailbox[putIdx]);
        // check to see if id matches our accepted list
        if (checkID(mailbox[putIdx].id)) {
            // if we have a valid message we move to the next mailbox slot
            putIdx = (putIdx + 1) % CAN_BUS_SIZE;
        }
    }
    bufferLock = false;
}

bool CANDevice::checkID(const int id) {
    switch (id) {
        case MPPT_CAN_ID:
            return true;
        default:
            return false;
    }
}