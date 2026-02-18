#include <stdint.h>

#include "Arduino.h"
#include "communication.hpp"
#include "../lib/data.hpp"

#define commandSize sizeof(command_t)

typedef struct __attribute__((packed)) infoToSend
{
	MachineState state;
	position_t position;
}infoToSend_t;

void communicationLoop(void *pvParameters) //to change for controller &
{
	(void)pvParameters;
	while(true)
	{
		if(Serial.available() >= commandSize)
		{
			command_t recieveCmd;
			uint8_t byteBuffer[commandSize];
	
			Serial.readBytes(byteBuffer, commandSize);
			memcpy(&recieveCmd, byteBuffer, commandSize);
			//setCommand
			
			delay(50);
			
			infoToSend_t infoToSend;
			memset(&infoToSend, 0, sizeof(infoToSend_t));
			//getState
			//getPos
			Serial.write((const uint8_t *)&infoToSend, sizeof(infoToSend_t));
		}
	}
}
