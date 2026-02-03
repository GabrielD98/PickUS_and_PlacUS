#include <AccelStepper.h>
#include <Arduino.h>



void MoveToPos(AccelStepper& motor, int speed, int acceleration, int position)
{

    motor.setMaxSpeed(speed);
    motor.setAcceleration(acceleration);
    motor.moveTo(position);
    while (motor.currentPosition() != position)
    {
        motor.run();
    }

    //motor.setCurrentPosition(position);
}