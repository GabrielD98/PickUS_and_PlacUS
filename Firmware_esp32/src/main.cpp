#include "Controller.h"

Controller controller;

void setup()
{
  Serial.begin(115200);
}


void loop()
{
  controller.update();
  dataModel_t* dataModel = controller.dataModel.get();
  dataModel->command = 0;
  controller.dataModel.release();
  delay(50);
}

