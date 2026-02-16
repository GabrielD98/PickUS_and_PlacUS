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
    controller.dataModel.get()->command.id = CommandId::MOVE;
    controller.dataModel.release();
    controller.dataModel.get()->command.velocity = 800;
    controller.dataModel.release();
    controller.dataModel.get()->command.requestedPosition.x = 400;
    controller.dataModel.release();
    controller.dataModel.get()->command.requestedPosition.y = 400;
    controller.dataModel.release();
    controller.dataModel.get()->command.requestedPosition.z = 0;
    controller.dataModel.release();
    controller.dataModel.get()->command.requestedPosition.yaw = 0;
    controller.dataModel.release();
    i = 0;
  }
  controller.update();
}

