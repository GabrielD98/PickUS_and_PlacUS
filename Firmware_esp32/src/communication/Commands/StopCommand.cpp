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
}

CommandState StopCommand::run()
{
	// Call the reset all callback to halt all motion and deactivate all outputs
	if (resetAllCb != nullptr)
	{
		resetAllCb();
	}
	return CommandState::Done;
}

void StopCommand::reset()
{
	// No state to reset for stop command
}

bool StopCommand::setPayload(uint8_t* payload, uint16_t payloadSize)
{
	// Stop command does not use payload data
	(void)payload;
	(void)payloadSize;
	return true;
}
