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

void waitForConnection(void)
{
	Serial.println("Waiting for Python connection...");
	
	// Wait for handshake byte from Python
	while(true)
	{
		if(Serial.available() > 0)
		{
			return;
		}
	}
}

void communicationLoop(void) //to change for controller &
{
	while(true)
	{
		if(Serial.available() >= commandSize)
		{
			uint8_t byteBuffer[commandSize];
			command_t recieveCmd;
	
			Serial.readBytes(byteBuffer, commandSize);
			memcpy(&recieveCmd, byteBuffer, commandSize);
			//setCommand
			
			delay(50);
			
			infoToSend_t test;
			memset(&test, 0, sizeof(infoToSend_t));
			test.state = MachineState::READY;
			//getState
			//getPos
			Serial.write((const uint8_t *)&test, sizeof(infoToSend_t));
		}
	}
}
