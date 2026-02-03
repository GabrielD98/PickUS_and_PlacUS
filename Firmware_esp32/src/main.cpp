#include "Controller.h"

Controller controller;

void setup()
{
  Serial.begin(115200);
}


void loop()
{
  controller.update();
  delay(50);
}

