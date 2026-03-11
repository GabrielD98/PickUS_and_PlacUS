#include <Arduino.h>
#include "../lib/data.hpp"
#include <cmath>

//Positions definitions (mm)
#define P_LIM_X 306.39
#define P_LIM_Y 304.80
#define P_LIM_Z 60.33
#define P_LIM_YAW 360

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
#define CAME_DIAMETER 28.58

Position dimensionLimits(Position targetPosition);
Position coordToStep(Position distance);
Position stepToCoord(Position step);
