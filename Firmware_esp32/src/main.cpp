#include "Arduino.h"
#include "communication.hpp"

#define ENABLE_TEST true


void controlLoop(void *pvParameters);

void setup()
{
	Serial.begin(115200);
	delay(1000); // Wait for serial to initialize

	xTaskCreatePinnedToCore(
		communicationLoop,
		"communicationTask",
		10000,
		NULL, // add controller address here
		1,
		NULL,
		0
	);

	xTaskCreatePinnedToCore(
		controlLoop,
		"controlTask",
		10000,
		NULL, // add controller address here
		1,
		NULL,
		1
	);

	if(ENABLE_TEST)
	{

	}


}


void loop()
{
}

void controlLoop(void *pvParameters)
{
	while(1)
	{
		delay(1000)
	}
}