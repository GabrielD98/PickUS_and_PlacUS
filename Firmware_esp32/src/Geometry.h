#ifndef GEOMETRY_H
#define GEOMETRY_H

#include <Arduino.h>
#include "../lib/data.hpp"
#include <cmath>

//Positions definitions (mm)
#define P_X_MAX 304.80
#define P_X_MIN 0
#define P_Y_MAX 306.39
#define P_Y_MIN 0
#define P_Z_MAX 0
#define P_Z_MIN -24

//Maximum speed (mm/s)
#define SPEED_MAX 1000.0

//Size definitions (mm)
#define GEAR_RADIUS 8.0

//Motor steps definitions (microsteps per steps)
#define STEPS_REVOLUTION 200
#define MICROSTEPPING_X 16
#define MICROSTEPPING_Y 16
#define MICROSTEPPING_Z 4
#define MICROSTEPPING_YAW 4

//Distance per revolution (mm)
#define MM_REVOLUTION 40.0
#define CAM_DIAMETER 24.0
#define CAM_RADIUS (CAM_DIAMETER / 2.0)

/**
 * @brief Ensures every targeted positions exceeding the limits are replaced with the closest limits.
 * 
 * @param targetPositions Initial target positions.
 * @return position_t Corrected target positions.
 */
position_t dimensionLimits(position_t targetPositions);

/**
 * @brief Converts a physical coordinate to a corresponding number of steps for each stepper, from origin in home position.
 * 
 * @param distance Coordinates relative to home position.
 * @return position_t Corresponding number of steps for each motor.
 */
position_t coordToStep(position_t distance);

/**
 * @brief Converts a number of steps to a corresponding physical coordinate for each stepper, from origin in home position.
 * 
 * @param step Number of steps relative to home position.
 * @return position_t Corresponding coordinates.
 */
position_t stepToCoord(position_t step);

/**
 * @brief Converts a physical velocity to a corresponding number of steps per seconds.
 * 
 * @param velocity Motor speed in mm/s.
 * @return velocity_t Corresponding number of steps/s.
 */
velocity_t velocityToStep(float velocity);

#endif