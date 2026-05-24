#include "CommandHandler.h"
#include <cstring>

CommandHandler::CommandHandler()
	: currentCommandId(0), currentCommandNumber(0), lastProcessedCommandNumber(UINT32_MAX), hasPendingCommand(false), numberOfRegisteredCommands(0)
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

bool CommandHandler::hasNewCommand()
{
	std::lock_guard<std::mutex> lock(mutex_);

	return hasPendingCommand;
}

bool CommandHandler::tryGetNextCommand(Command*& command)
{
	std::lock_guard<std::mutex> lock(mutex_);
	bool result = false;

	if (!hasPendingCommand)
	{
		command = nullptr;
	}
	else
	{
		command = registeredCommands[currentCommandId];
		if (command == nullptr)
		{
			hasPendingCommand = false;
		}
		else
		{
			lastProcessedCommandNumber = currentCommandNumber;
			hasPendingCommand = false;
			result = true;
		}
	}

	return result;
}

uint8_t CommandHandler::getCurrentCommandId()
{
	std::lock_guard<std::mutex> lock(mutex_);

	return currentCommandId;
}

uint32_t CommandHandler::getCurrentCommandNumber()
{
	std::lock_guard<std::mutex> lock(mutex_);

	return currentCommandNumber;
}

bool CommandHandler::setCurrentCommand(uint8_t* payload, uint16_t frameSize)
{
	std::lock_guard<std::mutex> lock(mutex_);

	bool result = false;

	if(payload != nullptr)
	{
		if (frameSize >= sizeof(CommmandFrameHeader))
		{
			CommmandFrameHeader commmandFrameHeader;
			memcpy(&commmandFrameHeader, payload, sizeof(CommmandFrameHeader));
		
			if (commmandFrameHeader.commandId < numberOfRegisteredCommands &&
				 frameSize == (sizeof(CommmandFrameHeader) + commmandFrameHeader.commandPayloadSize))
			{
				Command* selectedCommand = registeredCommands[commmandFrameHeader.commandId];
				if (selectedCommand != nullptr)
				{
					if (selectedCommand->setPayload(payload+sizeof(CommmandFrameHeader), commmandFrameHeader.commandPayloadSize))
					{
						result = true;
						currentCommandId = commmandFrameHeader.commandId;
						currentCommandNumber = commmandFrameHeader.commandNumber;
						hasPendingCommand = (currentCommandNumber != lastProcessedCommandNumber);
					}
				}
			}
		}
	}

	return result;
}


