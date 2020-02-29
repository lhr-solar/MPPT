/* MotionSensor Base Class
 * Copyright (c) 2014-2015 ARM Limited
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

#ifndef MOTIONSENSOR_H
#define MOTIONSENSOR_H

#include "stdint.h"

/** motion_data_counts_t struct
 */
typedef struct {
    int16_t x;      /*!< x-axis counts */
    int16_t y;      /*!< y-axis counts */
    int16_t z;      /*!< z-axis counts */
} motion_data_counts_t;

/** motion_data_units_t struct
 */
typedef struct {
    float x;        /*!< x-axis counts */
    float y;        /*!< y-axis counts */
    float z;        /*!< z-axis counts */
} motion_data_units_t;


/** Motion Sensor Base Class
    Useful for accessing data in a common way
 */
class MotionSensor
{
public:

    /** Enable the sensor for operation
     */
    virtual void enable(void) const = 0;

    /** disable the sensors operation
     */
    virtual void disable(void) const = 0;

    /** Set the sensor sample rate
        @param frequency The desires sample frequency
        @return The amount of error in Hz between desired and actual frequency
     */
    virtual uint32_t sampleRate(uint32_t frequency) const = 0;

    /** Tells of new data is ready
        @return The amount of data samples ready to be read from a device
     */
    virtual uint32_t dataReady(void) const = 0;

    /** Get the x data in counts
        @param x A referene to the variable to put the data in, 0 denotes not used
        @return The x data in counts
     */
    virtual int16_t getX(int16_t &x) const = 0;

    /** Get the y data in counts
        @param y A referene to the variable to put the data in, 0 denotes not used
        @return The y data in counts
     */
    virtual int16_t getY(int16_t &y) const = 0;

    /** Get the z data in counts
        @param z A referene to the variable to put the data in, 0 denotes not used
        @return The z data in counts
     */
    virtual int16_t getZ(int16_t &z) const = 0;

    /** Get the x data in units
        @param x A referene to the variable to put the data in, 0 denotes not used
        @return The x data in units
     */
    virtual float getX(float &x) const = 0;

    /** Get the y data in units
        @param y A referene to the variable to put the data in, 0 denotes not used
        @return The y data in units
     */
    virtual float getY(float &y) const = 0;

    /** Get the z data in units
        @param z A referene to the variable to put the data in, 0 denotes not used
        @return The z data in units
     */
    virtual float getZ(float &z) const = 0;

    /** Get the x,y,z data in counts
        @param xyz A referene to the variable to put the data in, 0 denotes not used
     */
    virtual void getAxis(motion_data_counts_t &xyz) const = 0;

    /** Get the x,y,z data in units
        @param xyz A referene to the variable to put the data in, 0 denotes not used
     */
    virtual void getAxis(motion_data_units_t &xyz) const = 0;
};

#endif
