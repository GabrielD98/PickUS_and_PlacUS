#include "Arduino.h"
#include "../lib/data.hpp"
#include "BoardConfig.h"
#include "Controller.h"
#include "communication.hpp"
#include "pressureSensor.hpp"

#define ENABLE_TEST true

Controller ctrl;
PressureSensor pSensor(PIN_PSENSOR_CLK,PIN_PSENSOR_DATA);

void controlLoop(void *pvParameters);

void setup()
{
	Serial.begin(115200);
	delay(1000); // Wait for serial to initialize

	pinMode(PIN_LIMSWITCH_Z,INPUT);
	pSensor.init();

	/*
	xTaskCreatePinnedToCore(
		communicationLoop,
		"communicationTask",
		10000,
		&ctrl,
		1,
		NULL,
		0
	);
	*/

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


void loop()
{
	
}

void controlLoop(void *pvParameters)
{
	Controller* controller = (Controller*)pvParameters;
	digitalWrite(PIN_PUMP,HIGH);
	int timeForPressure = millis();

	while(1)
	{
		dataModel_t* dataModel = controller->dataModel.get();
		dataModel->command.id = CommandId::MOVE;
		dataModel->command.velocity = 200;

		if(!digitalRead(PIN_LIMSWITCH_Z))
		{
			if(dataModel->state == MachineState::READY)
			{
				dataModel->command.requestedPosition.x = 400;
				dataModel->command.requestedPosition.y = 400;
				dataModel->command.requestedPosition.yaw = 400;
				dataModel->command.requestedPosition.z = 400;
			}
			
			digitalWrite(PIN_VALVE,HIGH);
			
		}
		else
		{
			if(dataModel->state == MachineState::READY)
			{
				dataModel->command.requestedPosition.x = 0;
				dataModel->command.requestedPosition.y = 0;
				dataModel->command.requestedPosition.yaw = 0;
				dataModel->command.requestedPosition.z = 0;
			}

			digitalWrite(PIN_VALVE,LOW);
			
		}
		//Serial.println(pSensor.getPressureKPa());

		controller->dataModel.release();
		controller->update();
		
	}
	

}
