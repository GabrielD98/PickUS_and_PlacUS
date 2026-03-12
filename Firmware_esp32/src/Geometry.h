#include <Arduino.h>
#include "../lib/data.hpp"
#include <cmath>

#ifndef GEOMETRY_H
#define GEOMETRY_H

//Positions definitions (mm)
#define P_X_MAX 306.39
#define P_X_MIN 0
#define P_Y_MAX 304.80
#define P_Y_MIN 0
#define P_Z_MAX 0 // 60.33
#define P_Z_MIN -24
#define P_YAW_MAX 360
#define P_YAW_MIN 0

//Size definitions (mm)
#define GEAR_RADIUS 8

//Motor steps definitions 
#define STEPS_REVOLUTION 200
#define MICROSTEPPING_X 16
#define MICROSTEPPING_Y 16
#define MICROSTEPPING_Z 1
#define MICROSTEPPING_YAW 4

//Distance per revolution
#define MM_REVOLUTION 2*PI*GEAR_RADIUS
#define CAM_DIAMETER 24 // (mm) // 28.58  

position_t dimensionLimits(position_t targetPosition);
position_t mmToStep(position_t distance);
position_t stepToMm(position_t step);

#endif