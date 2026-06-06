#include <cstring>
#include "ValveCommand.h"

ValveCommand::ValveCommand(ValveHardware* valveHardware)
	: valveHardware(valveHardware)
{
	valvePayload = {};
}

ValveCommand::~ValveCommand()
{
}

void ValveCommand::prepare()
{
	std::lock_guard<std::mutex> lock(commandMutex_);
	if (valveHardware == nullptr)
	{
		return;
	}
	if (valvePayload.toolheadNumber >= MAX_TOOLHEAD)
	{
		return;
	}
	Mosfet* valve = valveHardware->valve[valvePayload.toolheadNumber];
	if (valve == nullptr)
	{
		return;
	}
	if (valvePayload.enabled)
	{
		valve->on();
	}
	else
	{
		valve->off();
	}
}

CommandState ValveCommand::run()
{
	std::lock_guard<std::mutex> lock(commandMutex_);
	return CommandState::Done;
}

bool ValveCommand::setPayload(uint8_t* payload, uint16_t payloadSize)
{
	std::lock_guard<std::mutex> lock(commandMutex_);
	bool result = false;

	if (payload != nullptr && payloadSize == sizeof(ValvePayload))
	{
		ValvePayload nextPayload;
		memcpy(&nextPayload, payload, sizeof(ValvePayload));
		if (nextPayload.toolheadNumber < MAX_TOOLHEAD)
		{
			valvePayload = nextPayload;
			valvePayload.enabled = valvePayload.enabled ? 1 : 0;
			result = true;
		}
	}

	return result;
}
