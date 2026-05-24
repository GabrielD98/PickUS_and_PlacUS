#include "StopCommand.h"

StopCommand::StopCommand(void (*resetAllCb)())
	: resetAllCb(resetAllCb)
{
}

StopCommand::~StopCommand()
{
}

void StopCommand::prepare()
{
	std::lock_guard<std::mutex> lock(commandMutex_);
}

CommandState StopCommand::run()
{
	std::lock_guard<std::mutex> lock(commandMutex_);
	if (resetAllCb != nullptr)
	{
		resetAllCb();
	}
	return CommandState::Done;
}


bool StopCommand::setPayload(uint8_t* payload, uint16_t payloadSize)
{
	std::lock_guard<std::mutex> lock(commandMutex_);
	// Stop command does not use payload data
	(void)payload;
	(void)payloadSize;
	return true;
}
