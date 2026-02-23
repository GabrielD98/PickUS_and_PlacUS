#include <stdint.h>

#include "Arduino.h"
#include "communication.hpp"
#include "Controller.h"
#include "DataModel.h"
#include "../lib/data.hpp"

#define commandSize sizeof(command_t)

typedef struct __attribute__((packed)) infoToSend
{
	MachineState state;
	position_t position;
}infoToSend_t;

void communicationLoop(void *pvParameters) //to change for controller &
{
	Controller* controller = (Controller*)pvParameters;

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

			delay(50);
			
			infoToSend_t infoToSend;
			dataModel = controller->dataModel.get();
			infoToSend.position = dataModel->position;
			infoToSend.state = dataModel->state;
			controller->dataModel.release();
			Serial.write((const uint8_t *)&infoToSend, sizeof(infoToSend_t));
		}
	}
}
