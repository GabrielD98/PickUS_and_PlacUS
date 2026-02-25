#include "Arduino.h"
#include "../lib/data.hpp"
#include "BoardConfig.h"
#include "Controller.h"
#include "pressureSensor.hpp"

Controller ctrl;
PressureSensor pSensor(PIN_PSENSOR_CLK,PIN_PSENSOR_DATA);

void communicationLoop(void *pvParameters);
void controlLoop(void *pvParameters);
void testLoop(void*pvParameters);

void setup()
{
	Serial.begin(115200);
	delay(1000); // Wait for serial to initialize

	pinMode(PIN_LIMSWITCH_Z,INPUT);
	pSensor.init();

	xTaskCreatePinnedToCore(
		communicationLoop,
		"communicationTask",
		10000,
		&ctrl,
		1,
		NULL,
		0
	);
	if(!ENABLE_TEST)
	{
			xTaskCreatePinnedToCore(
			testLoop,
			"controlTask",
			10000,
			&ctrl,
			1,
			NULL,
			1
		);
	}
	else
	{
		xTaskCreatePinnedToCore(
			controlLoop,
			"controlTask",
			10000,
			&ctrl,
			1,
			NULL,
			1
		);
	}
	

}


void loop()
{}

void communicationLoop(void *pvParameters) //to change for controller &
{
	Controller* controller = (Controller*)pvParameters;
	uint16_t commandSize = sizeof(command_t);
	while(true)
	{
		if(Serial.available() >= commandSize)
		{
			command_t recieveCmd;
			uint8_t byteBuffer[commandSize];
	
			Serial.readBytes(byteBuffer, commandSize);
			memcpy(&recieveCmd, byteBuffer, commandSize);
			dataModel_t* dataModel = controller->dataModel.get();
			dataModel->command = recieveCmd;
			controller->dataModel.release();

			vTaskDelay(50); //TODO: Confirm this delay
			
			statusFrame_t statusFrame;
			dataModel = controller->dataModel.get();
			statusFrame.position = dataModel->position;
			statusFrame.state = dataModel->state;
			controller->dataModel.release();
			Serial.write((const uint8_t *)&statusFrame, sizeof(statusFrame_t));
		}
	}
}

void controlLoop(void *pvParameters)
{
	Controller* controller = (Controller*)pvParameters;
	while(1)
	{
		controller->update();
	}
}

void testLoop(void*pvParameters)
{
	Controller* controller = (Controller*)pvParameters;
	while(1)
	{
	}
}
