/**
 * @file command.h
 * @author PickusAndPlacus
 * @brief Abstract base class defining the command interface for all PnP operations.
 * @version 0.1
 * @date 2026-04-24
 * 
 * @copyright Copyright (c) 2026
 * 
 */

#ifndef COMMAND_H
#define COMMAND_H

#include <stdint.h>

enum class CommandState : uint8_t
{
	Done,
	InProgress,
	Error
};

class Command
{
	public:

		/**
		 * @brief Destroy the Command object.
		 */
		virtual ~Command() = default;

		/**
		 * @brief Prepare the command for the next execution cycle.
		 */
		virtual void prepare() = 0;

		/**
		 * @brief Execute the command logic and report its current execution state.
		 *
		 * @return CommandState Indicates whether the command is done, still in progress, or failed.
		 */
		virtual CommandState run() = 0;

		/**
		 * @brief Reset the command to its initial state.
		 */
		virtual void reset() = 0;

		/**
		 * @brief Provide the raw payload associated with the command.
		 *
		 * @param payload Pointer to the payload buffer.
		 * @param payloadSize Size of the payload buffer in bytes.
		 * 
		 * @return true if payload was set
		 * 		   false if payload is not equal to intern struct size or is equal to nullptr
		 */
		virtual bool setPayload(uint8_t* payload, uint16_t payloadSize) = 0;

};

#endif