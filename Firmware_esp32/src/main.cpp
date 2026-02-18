#include "Arduino.h"
#include "communication.hpp"

#define ENABLE_TEST true


void setup()
{
	Serial.begin(115200);
	delay(1000); // Wait for serial to initialize

	xTaskCreatePinnedToCore(
		communicationLoop,
		"communicationTask",
		512,
		NULL, // add controller address here
		1,
		NULL,
		0
	);

	if(ENABLE_TEST)
	{

	}


}


void loop()
{
}

