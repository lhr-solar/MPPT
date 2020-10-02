/**
 * PV Curve Tracer Project
 * 
 * File: serial.cpp
 * Author: Matthew Yu
 * Organization: UT Solar Vehicles Team
 * Created on: September 27th, 2020
 * Last Modified: 10/02/20
 * 
 * File Discription: This implementation file implements the serial class, which is an
 * concrete class that defines a clear read/write API for handling communication
 * across UART serial lines.
 */
#include "serial.h"


Serial::Serial(
    const PinName txPin, 
    const PinName rxPin, 
    const int bufferSize,
    const int baudRate) : serialPort(txPin, rxPin) {
    serialPort.set_baud(baudRate);
    serialPort.set_format(8, BufferedSerial::None, 1);
    buffer = new char[bufferSize];
    this->bufferSize = bufferSize;
    usedCapacity = 0;
    writeIdx = 0;
    readIdx = 0;
}

bool Serial::receiveData() {
    if (isBufferFull(readIdx, writeIdx)) return false;

    int freeCapacity = bufferSize - usedCapacity;

    /** Read into a temp buffer. */
    char *buf = new char[freeCapacity];
    int bytesRead = serialPort.read(buf, freeCapacity);

    /** Smartly put in the bytes into our buffer. */
    if (bytesRead >= 0) {
        for (int i = 0; i < bytesRead; i++) {
            buffer[writeIdx] = buf[i];
            writeIdx = (writeIdx + 1) % bufferSize;
        }
        usedCapacity += bytesRead;
        delete[] buf;
        return true;
    } else {
        delete[] buf;
        return false;
    }
}

bool Serial::sendData(char* buffer, int buffSize) {
    if (serialPort.write(buffer, buffSize) >= 0) return true;
    else return false;
}

bool Serial::isBufferFull(int _readIdx, int _writeIdx) const {
    if (_readIdx == (_writeIdx + 1) % bufferSize) return true;
    else return false;
}

bool Serial::isBufferEmpty(int _readIdx, int _writeIdx) const {
    if (_readIdx == _writeIdx) return true;
    else return false;
}

char * Serial::extractCommand() {
    bool found = false;
    int total = 0;
    int currIdx = readIdx;

    /** Walk around the buffer until we find the next ';'. */
    while (!isBufferEmpty(currIdx , writeIdx) && !found) {
        if (buffer[currIdx] == ';') {
            found = true;
        }
        currIdx = (currIdx + 1) % bufferSize;
        total++;
    }

    // if we found it, fill up the command string pointer
    if (found) {
        int idx = readIdx;
        total--; // go back a step to the ';'.
        usedCapacity -= total;
        char *msg = new char[total];
        for (int i = 0; i < total; i++) {
            msg[i] = buffer[idx];
            idx = (idx + 1) % bufferSize;
        }
        // update read pointer
        readIdx = currIdx;
        // append null
        msg[total] = '\0';
        return msg;
    } else {
        return nullptr;
    }
}

void Serial::purgeBuffer() {
    usedCapacity = 0;
}

void Serial::shutdown() {
    delete[] buffer;
}