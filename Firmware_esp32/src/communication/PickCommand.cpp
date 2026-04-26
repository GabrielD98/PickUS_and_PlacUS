#include <cstring>
#include "PickCommand.h"

PickCommand::PickCommand(PickHardware* pickHardware)
	: pickHardware(pickHardware)
{
	pickingPayload = {};
}

PickCommand::~PickCommand()
{
}

void PickCommand::prepare()
{
	pickHardware->pump->on();
	pickHardware->valve[pickingPayload.toolheadNumber]->on();
}

CommandState PickCommand::run()
{
	CommandState currentCommandState = CommandState::InProgress;

	pickHardware->valve[pickingPayload.toolheadNumber]->off();
	if (pickHardware->pressureSensor[pickingPayload.toolheadNumber]->getPressureKPa() < pickingPayload.pressureThresholdKPa)
	{
		currentCommandState = CommandState::Done;
	}

	return currentCommandState;
}

void PickCommand::reset()
{
}

bool PickCommand::setPayload(uint8_t* payload, uint16_t payloadSize)
{
	bool result = false;

	if(payload != nullptr && payloadSize == sizeof(PickingPayload))
	{
		PickingPayload nextPayload;
		memcpy(&nextPayload, payload, sizeof(PickingPayload));

		if(nextPayload.toolheadNumber < MAX_TOOLHEAD)
		{
			pickingPayload = nextPayload;
			result = true;
		}
	}
	return result;
}
