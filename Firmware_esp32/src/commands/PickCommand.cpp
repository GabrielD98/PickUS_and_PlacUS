#include <cstring>
#include "PickCommand.h"

PickCommand::PickCommand(PickingHardware* pickingHardware)
	: pickingHardware(pickingHardware)
{
	pickingPayload = {};
}

PickCommand::~PickCommand()
{
}

void PickCommand::prepare()
{
	std::lock_guard<std::mutex> lock(commandMutex_);
	pickingHardware->pump->on();
	pickingHardware->valve[pickingPayload.toolheadNumber]->off();
}

CommandState PickCommand::run()
{
	std::lock_guard<std::mutex> lock(commandMutex_);
	CommandState currentCommandState = CommandState::InProgress;

	if (pickingHardware->pressureSensor[pickingPayload.toolheadNumber]->getPressureKPa() < pickingPayload.pressureThresholdKPa)
	{
		currentCommandState = CommandState::Done;
	}

	return currentCommandState;
}

void PickCommand::reset()
{
	std::lock_guard<std::mutex> lock(commandMutex_);
	pickingHardware->pump->off();
	for(int i=0;i<MAX_TOOLHEAD;i++)
	{
		pickingHardware->valve[i]->off();
	}
}

bool PickCommand::setPayload(uint8_t* payload, uint16_t payloadSize)
{
	std::lock_guard<std::mutex> lock(commandMutex_);
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
