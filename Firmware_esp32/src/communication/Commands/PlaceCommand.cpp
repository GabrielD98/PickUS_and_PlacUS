#include <cstring>
#include "PlaceCommand.h"

PlaceCommand::PlaceCommand(PlacingHardware* placingHardware)
	: placingHardware(placingHardware)
{
	placingPayload = {};
}

PlaceCommand::~PlaceCommand()
{
}

void PlaceCommand::prepare()
{
	placingHardware->valve[placingPayload.toolheadNumber]->on();
}

CommandState PlaceCommand::run()
{
	CommandState currentCommandState = CommandState::InProgress;

	if (placingHardware->pressureSensor[placingPayload.toolheadNumber]->getPressureKPa() > placingPayload.pressureThresholdKPa)
	{
		bool canClosePump = true;

		for(int i=0;i<MAX_TOOLHEAD;i++)
		{
			canClosePump = canClosePump && !placingHardware->valve[i]->getState();
		}
		if(canClosePump)
		{
			placingHardware->pump->off();
		}

		currentCommandState = CommandState::Done;
	}

	return currentCommandState;
}

void PlaceCommand::reset()
{
	placingHardware->pump->off();
	for(int i=0;i<MAX_TOOLHEAD;i++)
	{
		placingHardware->valve[i]->off();
	}
}

bool PlaceCommand::setPayload(uint8_t* payload, uint16_t payloadSize)
{
	bool result = false;

	if(payload != nullptr && payloadSize == sizeof(PlacingPayload))
	{
		PlacingPayload nextPayload;
		memcpy(&nextPayload, payload, sizeof(PlacingPayload));

		if(nextPayload.toolheadNumber < MAX_TOOLHEAD)
		{
			placingPayload = nextPayload;
			result = true;
		}
	}
	return result;
}
