#include <Arduino.h>
#include "MotorControl.h"
 
AccelStepper motor(1,4,5);  //1=using a driver, 11=step, 12=dir

void setup()
{
  Serial.begin(115200);

  //Ligne pour tester enable manuellement (A retravailler)
  //pinMode(46, OUTPUT);
  //digitalWrite(46, HIGH);

  //motor.move(400); //relative
  //motor.moveTo(400); //absolute
  
  MoveToPos(motor, 400, 800, 400);
}


void loop()
{

  //MoveToPosition(motor,1500,500);
}

