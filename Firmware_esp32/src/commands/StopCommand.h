/**
 * @file StopCommand.h
 * @author pickus plackus
 * @brief Stop command implementation
 * @version 0.1
 * @date 2026-04-26
 * 
 * @copyright Copyright (c) 2026
 * 
 */
#ifndef STOPCOMMAND_H
#define STOPCOMMAND_H

#include <stdint.h>
#include <mutex>
#include "Command.h"

class StopCommand : public Command
{
	public:
	/**
	 * @brief Construct a new Stop Command object.
	 *
	 * @param resetAllCb Callback function pointer to reset all hardware
	 */
	StopCommand(void (*resetAllCb)());

	/**
	 * @brief Destroy the Stop Command object.
	 */
	~StopCommand();

	/**
	 * @brief Prepare the stop command by halting all motion and deactivating all outputs.
	 */
	void prepare() override;

	/**
	 * @brief Execute the stop command. Returns Done immediately as stop is instantaneous.
	 *
	 * @return CommandState Always returns Done.
	 */
	CommandState run() override;

	/**
	 * @brief Reset the command state.
	 */
	void reset() override;

	/**
	 * @brief Set command payload. Stop command does not use payload.
	 *
	 * @param payload Pointer to payload bytes (unused).
	 * @param payloadSize Size of payload in bytes (unused).
	 * @return true always, as stop accepts any payload.
	 */
	bool setPayload(uint8_t* payload, uint16_t payloadSize) override;

	private:
	std::mutex commandMutex_;
	void (*resetAllCb)();
};

#endif
