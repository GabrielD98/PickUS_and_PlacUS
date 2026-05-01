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
#include "commands/Command.h"

/**
 * @brief Maximum number of command instances that can be registered.
 */
#define MAX_COMMAND 6

/**
 * @brief Lists all interface command id recognizable by the controller.
 */
enum class CommandId : uint8_t
{
	Stop,
	Pause,
	Move,
	Pick,
	Place,
	Home
};
struct __attribute__((packed)) CommmandFrameHeader
{
	uint8_t commandId;
	uint32_t commandNumber;
	uint16_t commandPayloadSize;

};

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
		 * @brief Check whether a new command has been received.
		 *
		 * @return true when the current command differs from the last consumed one.
		 */
		bool hasNewCommand();

		/**
		 * @brief Atomically consume the next pending command.
		 *
		 * If a new command is pending, this method returns its pointer in one
		 * locked operation and clears the pending flag.
		 *
		 * @param command Output pointer to the command to execute.
		 * @return true if a pending command was consumed, false otherwise.
		 */
		bool tryGetNextCommand(Command*& command);

		/**
		 * @brief Get the identifier of the currently selected command.
		 *
		 * @return uint8_t Current command identifier.
		 */
		uint8_t getCurrentCommandId();

		/**
		 * @brief Get the command request number of the current command.
		 *
		 * @return uint32_t Current command request number.
		 */
		uint32_t getCurrentCommandNumber();

		/**
		 * @brief Select the active command and forward a full command frame.
		 *
		 * @param payload Pointer to the frame bytes, starting with CommmandFrameHeader.
		 * @param frameSize Total frame size in bytes, including the header and command payload.
		 * @return true if the command exists and accepts the payload, false otherwise.
		 */
		bool setCurrentCommand(uint8_t* payload, uint16_t frameSize);

		/**
		 * @brief Reset all registered commands to their initial state.
		 */
		void resetAllCommand();


	private:
		std::mutex mutex_;
		uint8_t currentCommandId;
		uint32_t currentCommandNumber;
		uint32_t lastProcessedCommandNumber;
		bool hasPendingCommand;
		Command* registeredCommands[MAX_COMMAND];
		uint8_t numberOfRegisteredCommands;

};

#endif