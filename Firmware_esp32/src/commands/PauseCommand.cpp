#include "PauseCommand.h"

PauseCommand::PauseCommand()
{
}

PauseCommand::~PauseCommand()
{
}

void PauseCommand::prepare()
{
	std::lock_guard<std::mutex> lock(commandMutex_);
	// No explicit action needed; pause is implicit when run() is not called
}

CommandState PauseCommand::run()
{
	std::lock_guard<std::mutex> lock(commandMutex_);
	// Pause is instantaneous, return Done immediately
	return CommandState::Done;
}


bool PauseCommand::setPayload(uint8_t* payload, uint16_t payloadSize)
{
	std::lock_guard<std::mutex> lock(commandMutex_);
	// Pause command does not use payload data
	(void)payload;
	(void)payloadSize;
	return true;
}
