#include <Arduino.h>

//Positions definitions 
#define P0_Z
#define P_END_Z
#define P0_Y
#define P_END_Y
#define P0_X
#define P_END_X
#define P0_YAW
#define P_END_YAW

//Size definitions (mm)
#define BASE_WIDTH 290
#define BASE_LENGTH 290

//Motor steps definitions 
#define STEPS_REVOLUTION_YAW 200
#define MOTOR_REVOLUTION_STEPS 200

float mmToStep(float distance);
