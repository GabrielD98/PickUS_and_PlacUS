#include "PauseCommand.h"

PauseCommand::PauseCommand()
{
}

PauseCommand::~PauseCommand()
{
}

void PauseCommand::prepare()
{
	// No explicit action needed; pause is implicit when run() is not called
}

CommandState PauseCommand::run()
{
	// Pause is instantaneous, return Done immediately
	return CommandState::Done;
}

void PauseCommand::reset()
{
	// No state to reset for pause command
}

bool PauseCommand::setPayload(uint8_t* payload, uint16_t payloadSize)
{
	// Pause command does not use payload data
	(void)payload;
	(void)payloadSize;
	return true;
}
