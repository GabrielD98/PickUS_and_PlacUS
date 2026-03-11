#include "Controller.h"
#include "Geometry.h"

Controller controller;

int i = 1;

void setup()
{
  Serial.begin(115200);

  printf("TEST GEOMETRIE \n");
  position_t testPosition; 
  testPosition.x = 200;
  testPosition.y = 300;
  testPosition.z = 20;
  testPosition.yaw = 180;
  
  position_t stepsPosition;
  position_t mmPosition;
  printf("POSITIONS : x = %f y = %f z = %f yaw = %f", testPosition.x,testPosition.y,testPosition.z,testPosition.yaw);
  stepsPosition = coordToStep(testPosition);
  printf("POSITIONS : x = %f y = %f z = %f yaw = %f", stepsPosition.x,stepsPosition.y,stepsPosition.z,stepsPosition.yaw);
  stepToCoord(stepsPosition);
  printf("POSITIONS : x = %f y = %f z = %f yaw = %f", mmPosition.x,mmPosition.y,mmPosition.z,mmPosition.yaw);
}


void loop()
{
  // if (i==1)
  // {
  //   dataModel_t* dataModel = controller.dataModel.get();
  //   dataModel->command.id = CommandId::MOVE;
  //   dataModel->command.velocity = 300;
  //   dataModel->command.requestedPosition.x = 200;
  //   dataModel->command.requestedPosition.y = 400;
  //   dataModel->command.requestedPosition.z = 400;
  //   dataModel->command.requestedPosition.yaw = 400;
  //   controller.dataModel.release();
  //   i = 0;
  // }
  // controller.update();
}

