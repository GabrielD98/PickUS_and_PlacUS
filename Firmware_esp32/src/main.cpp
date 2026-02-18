#include "Controller.h"

Controller controller;

int i = 1;

void setup()
{
  Serial.begin(115200);
}


void loop()
{
  if (i==1)
  {
    dataModel_t* dataModel = controller.dataModel.get();
    dataModel->command.id = CommandId::MOVE;
    dataModel->command.velocity = 300;
    dataModel->command.requestedPosition.x = 200;
    dataModel->command.requestedPosition.y = 400;
    dataModel->command.requestedPosition.z = 400;
    dataModel->command.requestedPosition.yaw = 400;
    controller.dataModel.release();
    i = 0;
  }
  controller.update();
}

