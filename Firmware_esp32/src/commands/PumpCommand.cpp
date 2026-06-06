#include <cstring>
#include "PumpCommand.h"

PumpCommand::PumpCommand(PumpHardware* pumpHardware)
	: pumpHardware(pumpHardware)
{
	pumpPayload = {};
}

PumpCommand::~PumpCommand()
{
}

void PumpCommand::prepare()
{
	std::lock_guard<std::mutex> lock(commandMutex_);
	if (pumpHardware == nullptr || pumpHardware->pump == nullptr)
	{
		return;
	}
	if (pumpPayload.enabled)
	{
		pumpHardware->pump->on();
	}
	else
	{
		pumpHardware->pump->off();
	}
}

CommandState PumpCommand::run()
{
	std::lock_guard<std::mutex> lock(commandMutex_);
	return CommandState::Done;
}

bool PumpCommand::setPayload(uint8_t* payload, uint16_t payloadSize)
{
	std::lock_guard<std::mutex> lock(commandMutex_);
	bool result = false;

	if (payload != nullptr && payloadSize == sizeof(PumpPayload))
	{
		PumpPayload nextPayload;
		memcpy(&nextPayload, payload, sizeof(PumpPayload));
		pumpPayload = nextPayload;
		pumpPayload.enabled = pumpPayload.enabled ? 1 : 0;
		result = true;
	}

	return result;
}
