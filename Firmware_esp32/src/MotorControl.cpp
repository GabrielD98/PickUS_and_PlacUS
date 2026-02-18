#include "MotorControl.h"

void gantryMove(MultiStepper& gantry, AccelStepper& motor1, AccelStepper& motor2, long positions[2], int speed)
{
    motor1.setMaxSpeed(speed);
    motor2.setMaxSpeed(speed);
    gantry.moveTo(positions);
}

void goHome(MultiStepper& gantry, AccelStepper& motor1, AccelStepper& motor2)
{
    //Note : the arm will need to be up before moving
    long positions[2] = {0,0};
    gantryMove(gantry, motor1, motor2, positions, 400);
}

// void MoveToPos(AccelStepper& motor, int speed, int acceleration, int position)
// {

//     motor.setMaxSpeed(speed);
//     motor.setAcceleration(acceleration);
//     motor.moveTo(position);
//     while (motor.currentPosition() != position)
//     {
//         motor.run();
//     }

//     //motor.setCurrentPosition(position);
// }