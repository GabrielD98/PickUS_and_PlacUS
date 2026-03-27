/**
 * @file boardconfig.h
 * @author PickusAndPlacus
 * @brief Hardware abstraction layer defining GPIO pin assignments
 * @version
 * @date
 */

#ifndef BOARDCONFIG_H
#define BOARDCONFIG_H

// --- Stepper motor pins ---
#define PIN_DX_DIR 6        /// Direction pin for X-axis stepper (Driver DX)
#define PIN_DX_STEP 7       /// Step pulse pin for X-axis stepper
#define PIN_DX_EN 15        /// Enable pin for X-axis stepper (Active LOW)

#define PIN_DY_DIR 16       /// Direction pin for Y-axis stepper (Driver DY)
#define PIN_DY_STEP 17      /// Step pulse pin for Y-axis stepper
#define PIN_DY_EN 18        /// Enable pin for Y-axis stepper (Active LOW)

#define PIN_DZ_DIR 3        /// Direction pin for Z-axis stepper (Driver DZ)
#define PIN_DZ_STEP 46      /// Step pulse pin for Z-axis stepper
#define PIN_DZ_EN 11        /// Enable pin for Z-axis stepper (Active LOW)

#define PIN_DYAW_DIR 12     /// Direction pin for YAW-axis stepper (Driver DYAW)
#define PIN_DYAW_STEP 13    /// Step pulse pin for YAW-axis stepper
#define PIN_DYAW_EN 14      /// Enable pin for YAW-axis stepper (Active LOW)

// --- Actuators ---
#define PIN_PUMP 5          /// Vacuum pump pin
#define PIN_VALVE 4         /// Solenoid valve pin

// --- Communication ---
// #define PIN_I2C_SDA 8
// #define PIN_I2C_SCA 9
// #define PIN_CANIC_TX 47
// #define PIN_CANIC_RX 48

// --- Sensors ---
#define PIN_LIMSWITCH_X 35  /// Limit switch pin for X-axis origin
#define PIN_LIMSWITCH_Y 36  /// Limit switch pin for Y-axis origin
#define PIN_LIMSWITCH_Z 37  /// Limit switch pin for Z-axis origin

#define PIN_PSENSOR_CLK 2   /// Pressure sensor clock pin
#define PIN_PSENSOR_DATA 1  /// Pressure sensor output pin

#endif