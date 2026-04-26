/**
 * @file PauseCommand.h
 * @author pickus plackus
 * @brief Pause command implementation
 * @version 0.1
 * @date 2026-04-26
 * 
 * @copyright Copyright (c) 2026
 * 
 */
#ifndef PAUSECOMMAND_H
#define PAUSECOMMAND_H

#include <stdint.h>
#include "Command.h"
#include <MultiStepper.h>


class PauseCommand : public Command
{
	public:
	/**
	 * @brief Construct a new Pause Command object.
	 *
	 */
	PauseCommand();

	/**
	 * @brief Destroy the Pause Command object.
	 */
	~PauseCommand();

	/**
	 * @brief Prepare the pause command. Pauses all motor motion.
	 */
	void prepare() override;

	/**
	 * @brief Execute the pause command. Returns Done immediately as pause is instantaneous.
	 *
	 * @return CommandState Always returns Done.
	 */
	CommandState run() override;

	/**
	 * @brief Reset the command state.
	 */
	void reset() override;

	/**
	 * @brief Set command payload. Pause command does not use payload.
	 *
	 * @param payload Pointer to payload bytes (unused).
	 * @param payloadSize Size of payload in bytes (unused).
	 * @return true always, as pause accepts any payload.
	 */
	bool setPayload(uint8_t* payload, uint16_t payloadSize) override;

};

#endif
