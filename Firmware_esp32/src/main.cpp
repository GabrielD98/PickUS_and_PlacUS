#include "MotorControl.h"

//Driver : drv8825
AccelStepper motorX(AccelStepper::DRIVER, PIN_DX_STEP, PIN_DX_DIR);  //motor control type, step, dir
AccelStepper motorY(AccelStepper::DRIVER, PIN_DY_STEP, PIN_DY_DIR);
AccelStepper motors[NMOTOR] = {motorX, motorY};

MultiStepper gantry;

bool run_once = true;

// long positions[NMOTOR] = {400,400};
long positions[NMOTOR] = {100,1000};

bool doneX = false;
bool doneY = false;

void setup()
{
  Serial.begin(115200);

  gantry.addStepper(motorX);
  gantry.addStepper(motorY);
}


void loop()
{
  // gantryMove(gantry, motors, positions, 1000);
  gantryMove(gantry, motorX, motorY, positions, 1000);
  
  gantry.run();

  // Serial.print("moteur 1 : ");
  // Serial.println(motorX.currentPosition());
  // Serial.print("moteur 2 : ");
  // Serial.println(motorY.currentPosition());
  // delay(10);
  
  if ((motorX.currentPosition() == positions[0]) && (!doneX)){
    Serial.println("Moteur 1 à destination");
    doneX = true;
  }

  if ((motorY.currentPosition() == positions[1]) && (!doneY)){
    Serial.println("Moteur 2 à destination");
    doneY = true;
  }
}

