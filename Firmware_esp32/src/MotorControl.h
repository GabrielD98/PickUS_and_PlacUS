#include <Arduino.h>
#include <AccelStepper.h>
#include <MultiStepper.h>

#ifndef MOTORCONTROL_H
#define MOTORCONTROL_H

#define PIN_DX_STEP 4
#define PIN_DX_DIR 5
#define PIN_DX_EN 6

#define PIN_DY_STEP 7
#define PIN_DY_DIR 15
#define PIN_DY_EN 16

// #define PIN_DZ_STEP 17
// #define PIN_DZ_DIR 18
// #define PIN_DZ_EN 10

// #define PIN_DYAW_STEP 11
// #define PIN_DYAW_DIR 12
// #define PIN_DYAW_EN 46


//Speed is set to be between 1 and how many times loop can be called per second
//Positions will be absolute or relative?
void gantryMove(MultiStepper& gantry, AccelStepper& motor1, AccelStepper& motor2, long positions[2], int speed);

void goHome(MultiStepper& gantry, AccelStepper& motor1, AccelStepper& motor2);

// void MoveToPos(AccelStepper& motor, int speed, int acceleration, int position);

#endif