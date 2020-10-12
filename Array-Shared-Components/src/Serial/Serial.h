/**
 * PV Curve Tracer Project
 * 
 * File: Serial.h
 * Author: Matthew Yu
 * Organization: UT Solar Vehicles Team
 * Created on: September 27th, 2020
 * Last Modified: 10/07/20
 * 
 * File Discription: This header file describes the serial class, which is an
 * concrete class that defines a clear read/write API for handling communication
 * across UART serial lines.
 */
#pragma once
#include "mbed.h"


/**
 * Definition of an implementation of serial communication using the mbed BufferedSerial
 * class.
 * 
 * The Serial class sets up a the serial communication and manages a buffer to
 * read and translate messages from the PC via USB. Implementation details are
 * taken from prog1.ino.
 */
class Serial {
    public:
        /** 
         * Constructor for a serial object.
         * 
         * @param[in] txPin Transceiver pin.
         * @param[in] rxPin Receiver pin.
         * @param[in] bufferSize Size of the buffer.
         * @param[in] baudRate Baudrate of the connection.
         */
        explicit Serial(
            const PinName txPin, 
            const PinName rxPin, 
            const int bufferSize, 
            const int baudRate
        );

        /**
         * Looks to fill the buffer from serial.
         * 
         * @return True if data was read, false if error.
         */
        bool receiveData();

        /**
         * Looks to send data across serial to the client.
         * 
         * @param[in] buffer Pointer to the buffer to write.
         * @param[in] buffSize Size of the buffer to write.
         * @return True if data was sent, false if error.
         */
        bool sendData(char* buffer, int buffSize);

        /**
         * Returns whether the internal buffer is full and cannot read any more.
         * 
         * @param[in] _readIdx Read pointer of the buffer.
         * @param[in] _writeIdx Write pointer of the buffer.
         * @return True if buffer is full, false elsewise.
         */
        bool isBufferFull(int _readIdx, int _writeIdx) const;

        /**
         * Returns whether the internal buffer is empty and cannot read any more.
         * 
         * @param[in] _readIdx Read pointer of the buffer.
         * @param[in] _writeIdx Write pointer of the buffer.
         * @return True if buffer is empty, false elsewise.
         */
        bool isBufferEmpty(int _readIdx, int _writeIdx) const;

        /**
         * Attempts to read a complete command from the buffer, adjusting
         * internal pointers as required.
         * 
         * @return Pointer to our command string. Must be freed by the user.
         */
        char * extractCommand();

        /**
         * Purges the buffer for more serial input. Happens in case we get
         * corrupted data in the buffer and it gets filled up.
         */
        void purgeBuffer();

        /**
         * Deallocates relevant structures.
         */
        void shutdown();

    private:
        BufferedSerial serialPort;

        /** Pointer to a buffer object that holds data. */
        char *buffer;

        /** Maximum size of the buffer. */
        int bufferSize;

        /** Buffer indicator. */
        int usedCapacity;

        /** Indices for writing/reading from a circular char buffer. */
        int writeIdx;
        int readIdx;

};