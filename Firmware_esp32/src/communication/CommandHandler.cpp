#include "CommandHandler.h"

CommandHandler::CommandHandler()
	: currentCommandId(0), numberOfRegisteredCommands(0)
{
	for (uint8_t i = 0; i < MAX_COMMAND; i++)
	{
		registeredCommands[i] = nullptr;
	}
}

CommandHandler::~CommandHandler()
{
}

bool CommandHandler::registerCommand(Command* command)
{
	bool result = false;
	
	std::lock_guard<std::mutex> lock(mutex_);

	if (numberOfRegisteredCommands < MAX_COMMAND)
	{
		if (command != nullptr)
		{
			registeredCommands[numberOfRegisteredCommands] = command;
			numberOfRegisteredCommands++;
			result = true;
		}
	}

	return result;
}

Command* CommandHandler::getCurrentCommand()
{
	std::lock_guard<std::mutex> lock(mutex_);

	return registeredCommands[currentCommandId];
}

uint8_t CommandHandler::getCurrentCommandId()
{
	std::lock_guard<std::mutex> lock(mutex_);

	return currentCommandId;
}

bool CommandHandler::setCurrentCommand(uint8_t commandId, uint8_t* payload, uint16_t payloadSize)
{
	std::lock_guard<std::mutex> lock(mutex_);

	bool result = false;

	if (commandId < numberOfRegisteredCommands)
	{
		Command* selectedCommand = registeredCommands[commandId];
		if (selectedCommand != nullptr)
		{
			if (selectedCommand->setPayload(payload, payloadSize))
			{
				result = true;
				currentCommandId = commandId;
			}
		}
	}

	return result;
}

void CommandHandler::resetAllCommand()
{
	std::lock_guard<std::mutex> lock(mutex_);

	for (uint8_t i = 0; i < numberOfRegisteredCommands; i++)
	{
		if (registeredCommands[i] != nullptr)
		{
			registeredCommands[i]->reset();
		}
	}
}
