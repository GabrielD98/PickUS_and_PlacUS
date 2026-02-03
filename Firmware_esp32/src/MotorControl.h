#include <Arduino.h>
#include <AccelStepper.h>
#include <MultiStepper.h>

#include "BoardConfig.h"
#define NMOTOR 2

#ifndef MOTORCONTROL_H
#define MOTORCONTROL_H

//Speed is set to be between 1 and how many times loop can be called per second
//Positions will be absolute or relative?
void gantryMove(MultiStepper& gantry, AccelStepper& motor1, AccelStepper& motor2, long positions[NMOTOR], int speed);
// void gantryMove(MultiStepper& gantry, AccelStepper* motors[NMOTOR], long positions[NMOTOR], int speed);

void goHome(MultiStepper& gantry, AccelStepper& motor1, AccelStepper& motor2);

// void MoveToPos(AccelStepper& motor, int speed, int acceleration, int position);

#endif