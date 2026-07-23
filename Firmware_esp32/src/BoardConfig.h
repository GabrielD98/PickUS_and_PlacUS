/**
 * @file boardconfig.h
 * @author PickusAndPlacus
 * @brief Hardware abstraction layer defining GPIO pin assignments.
 * @version 1.0
 * @date 17/04/2026
 */

#ifndef BOARDCONFIG_H
#define BOARDCONFIG_H

// --- Stepper motor pins ---
#define PIN_DX_DIR 4        /// Direction pin for X-axis stepper (Driver DX)
#define PIN_DX_STEP 5       /// Step pulse pin for X-axis stepper
#define PIN_DX_EN 9         /// Enable pin for X-axis stepper (Active LOW)

#define PIN_DY_DIR 15       /// Direction pin for Y-axis stepper (Driver DY)
#define PIN_DY_STEP 7       /// Step pulse pin for Y-axis stepper
#define PIN_DY_EN 9         /// Enable pin for Y-axis stepper (Active LOW)

#define PIN_DZ_DIR 17        /// Direction pin for Z-axis stepper (Driver DZ)
#define PIN_DZ_STEP 18      /// Step pulse pin for Z-axis stepper
#define PIN_DZ_EN 9         /// Enable pin for Z-axis stepper (Active LOW)

#define PIN_DYAW_DIR 10     /// Direction pin for YAW-axis stepper (Driver DYAW)
#define PIN_DYAW_STEP 11    /// Step pulse pin for YAW-axis stepper
#define PIN_DYAW_EN 9       /// Enable pin for YAW-axis stepper (Active LOW)

// --- Switches ---
#define PIN_PUMP 12         /// Vacuum pump pin
#define PIN_VALVE1 13       /// Solenoid valve pin
#define PIN_VALVE2 14       /// Solenoid valve pin
#define PIN_LIMSWITCH_X 6   /// Limit switch pin for X-axis origin
#define PIN_LIMSWITCH_Y 16  /// Limit switch pin for Y-axis origin
#define PIN_LIMSWITCH_Z 8   /// Limit switch pin for Z-axis origin

// --- Communication --- //Currently not used but are for expension
// #define PIN_CANIC_TX 47
// #define PIN_CANIC_RX 48

// --- Sensors ---
#define PIN_PSENSOR1_CLK 2   /// Pressure sensor clock pin
#define PIN_PSENSOR1_DATA 1  /// Pressure sensor output pin
#define PIN_PSENSOR2_CLK 42  /// Pressure sensor clock pin
#define PIN_PSENSOR2_DATA 41 /// Pressure sensor output pin

// --- LED ---
#define PIN_LED1 3

// --- Hardware counts / limits ---
#define MAX_TOOLHEAD 2      // Number of toolheads supported

#endif