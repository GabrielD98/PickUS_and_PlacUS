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
	// Call the reset all callback to halt all motion and deactivate all outputs
	if (resetAllCb != nullptr)
	{
		resetAllCb();
	}
	return CommandState::Done;
}

void StopCommand::reset()
{
	std::lock_guard<std::mutex> lock(commandMutex_);
	// No state to reset for stop command
}

bool StopCommand::setPayload(uint8_t* payload, uint16_t payloadSize)
{
	std::lock_guard<std::mutex> lock(commandMutex_);
	// Stop command does not use payload data
	(void)payload;
	(void)payloadSize;
	return true;
}
