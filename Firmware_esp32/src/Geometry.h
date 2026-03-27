/**
 * @file geometry.h
 * @author PickusAndPlacus
 * @brief Physical parameters to delimit the machine's workspace
 * and convert distances to step count.
 * @version
 * @date
 */

#ifndef GEOMETRY_H
#define GEOMETRY_H

#include <Arduino.h>
#include "../lib/data.hpp"
#include <cmath>

// Physical travel limits of the machine.
#define P_X_MAX 304.80      /// Maximum X travel (mm)
#define P_X_MIN 0           /// Minimum X travel (mm)
#define P_Y_MAX 306.39      /// Maximum Y travel (mm)
#define P_Y_MIN 0           /// Minimum Y travel (mm)
#define P_Z_MAX 0           /// Z zero position (retracted)
#define P_Z_MIN -24         /// Z maximum descent (mm)
#define P_YAW_MAX 360       /// Maximum YAW travel (degrees)
#define P_YAW_MIN 0         /// Minimum YAW travel (degrees)

#define SPEED_MAX 1000.0    /// Maximum speed for every steppers (mm/s)

// Mechanical properties used for step conversion.
#define STEPS_REVOLUTION 200                /// (steps)
#define MM_REVOLUTION 40.0                  /// (mm)
#define GEAR_RADIUS 8.0                     /// X, Y and Z-axis gears radius (mm)
#define CAM_DIAMETER 24.0                   /// (mm)
#define CAM_RADIUS (CAM_DIAMETER / 2.0)     /// (mm)

// Microstepping resolution
#define MICROSTEPPING_X 16                  /// Microsteps per motor step for the X-axis
#define MICROSTEPPING_Y 16                  /// Microsteps per motor step for the Y-axis
#define MICROSTEPPING_Z 4                   /// Microsteps per motor step for the Z-axis
#define MICROSTEPPING_YAW 4                 /// Microsteps per motor step for the YAW-axis


/**
 * @brief Clips target positions to the machine's physical workspace.
 * @param targetPositions Raw input target coordinates from UI.
 * @return position_t Coordinates restricted to defined workspace ranges.
 */
position_t dimensionLimits(position_t targetPositions);

/**
 * @brief Converts physical coordinates to motor steps.
 * @param distance Physical coordinates relative to home.
 * @return position_t Calculated step count for each axis.
 */
position_t coordToStep(position_t distance);

/**
 * @brief Converts motor steps to physical coordinates for each axis.
 * @param step Number of steps relative to home position.
 * @return position_t Physical toolhead position.
 */
position_t stepToCoord(position_t step);

/**
 * @brief Converts a physical velocity (mm/s) to a corresponding number of steps per seconds.
 * @param velocity Speed (mm/s).
 * @return velocity_t Corresponding number of steps per second for each motor.
 */
velocity_t velocityToStep(float velocity);

#endif