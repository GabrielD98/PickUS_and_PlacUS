/**
 * @file MoveCommand.h
 * @author pickus plackus
 * @brief Move command implementation for the machine.
 * @version 0.1
 * @date 2026-04-24
 * 
 * @copyright Copyright (c) 2026
 * 
 */


#ifndef MOVECOMMAND_H
#define MOVECOMMAND_H

#include <stdint.h>
#include "Command.h"
#include <MultiStepper.h>
#include "../lib/data.hpp"

/**
 * @brief Data received to complete the command
 */
struct MovingPayload
{
	positionStep_t targetPosition;
	velocityStep_t velocity;
};

/**
 * @brief All hardware addresses needed for moving
 */
struct MovingHardware
{
	MultiStepper* motorSystem;
};


class MoveCommand : public Command
{
	public:
	
	/**
	 * @brief Construct a new Move Command object
	 * 
	 * @param movingHardware All hardware addresses needed for moving.
	 */
	MoveCommand(MovingHardware* movingHardware);
	
	/**
	 * @brief Destroy the Command object.
	 */
	~MoveCommand();

	/**
	 * @brief Prepare move execution by setting the target position.
	 *
	 */
	void prepare() override;

	/**
	 * @brief Execute one move step and report progress.
	 *
	 * @return CommandState InProgress while moving is ongoing, Done when completed, Error on failure.
	 */
	CommandState run() override;

	/**
	 * @brief No state to reset for this command
	 */
	void reset() override;

	/**
	 * @brief Accept payload for interface compatibility.
	 *
	 * @param payload Pointer to the payload buffer.
	 * @param payloadSize Size of the payload buffer in bytes.
	 * 
	 * @return true if payload was set, false if payload is not equal to intern struct size
	*/
	bool setPayload(uint8_t* payload, uint16_t payloadSize) override;

	private:

		MovingHardware* movingHardware;
		MovingPayload movingPayload;

};

#endif