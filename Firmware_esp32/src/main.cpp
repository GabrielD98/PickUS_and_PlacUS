#include "Arduino.h"
#include "communication.hpp"

void setup()
{
  Serial.begin(115200);
  delay(1000); // Wait for serial to initialize
  
  waitForConnection(); // Wait for Python to connect
}


void loop()
{
  communicationLoop();
}

