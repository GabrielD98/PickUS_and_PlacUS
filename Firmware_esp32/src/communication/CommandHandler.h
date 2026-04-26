/**
 * @file CommandHandler.h
 * @author pickus plackus
 * @brief Interface for command registration, selection, and lifecycle reset.
 * @version 0.1
 * @date 2026-04-26
 *
 * @copyright Copyright (c) 2026
 */

#ifndef COMMANDHANDLER_H
#define COMMANDHANDLER_H

#include <stdint.h>
#include <mutex>
#include "Commands/Command.h"

/**
 * @brief Maximum number of command instances that can be registered.
 */
#define MAX_COMMAND 6

/**
 * @brief Stores and manages available commands for the communication layer.
 *
 * The handler keeps an indexed table of command objects and tracks which
 * command is currently active.
 */
class CommandHandler
{
	public:
		/**
		 * @brief Construct a new Command Handler object.
		 */
		CommandHandler();

		/**
		 * @brief Destroy the Command Handler object.
		 */
		~CommandHandler();

		/**
		 * @brief Register a command instance in the internal command table.
		 *
		 * @param command Pointer to a command object implementing the Command interface.
		 * @return bool true if the command is valid and there is place, false otherwise.
		 */
		bool registerCommand(Command* command);

		/**
		 * @brief Access the currently selected command entry.
		 * 
		 * @return Command* pointer to the function to run
		 */
		Command* getCurrentCommand();

		/**
		 * @brief Select the active command and forward its payload.
		 *
		 * @param commandId Identifier of the command to activate.
		 * @param payload Pointer to payload bytes associated with this command.
		 * @param payloadSize Size of payload in bytes.
		 * @return true if the command exists and accepts the payload, false otherwise.
		 */
		bool setCurrentCommand(uint8_t commandId, uint8_t* payload, uint16_t payloadSize);

		/**
		 * @brief Reset all registered commands to their initial state.
		 */
		void resetAllCommand();


	private:
		std::mutex mutex_;
		uint8_t currentCommandId;
		Command* registeredCommands[MAX_COMMAND];
		uint8_t numberOfRegisteredCommands;

};

#endif