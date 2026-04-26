/**
 * @file HomeCommand.h
 * @author pickus plackus
 * @brief Home command implementation for the machine homing sequence.
 * @version 0.1
 * @date 2026-04-24
 * 
 * @copyright Copyright (c) 2026
 * 
 */


#ifndef HOMECOMMAND_H
#define HOMECOMMAND_H

#include <stdint.h>
#include "Command.h"
#include <AccelStepper.h>
#include "hardware/limitswitch.h"
#include "../lib/data.hpp"

/**
 * @brief Data received to complete the command
 */
struct HomingPayload
{
	velocityStep_t homingVelocity;
};

/**
 * @brief Lists all states required to home the machine.
 */
enum class HomingState : uint8_t
{
	Init,
	X,
	Y,
	Z,
	Yaw,
	HomingDone
};

/**
 * @brief All hardware addresses needed for homing
 */
struct HomingHardware
{
	AccelStepper* motorX;
	AccelStepper* motorY;
	AccelStepper* motorZ;
	AccelStepper* motorYaw;
	LimitSwitch* limSwitchX;
	LimitSwitch* limSwitchY;
	LimitSwitch* limSwitchZ;
};


class HomeCommand : public Command
{
	public:
	
	/**
	 * @brief Construct a new Home Command object
	 * 
	 * @param homingHardware all hardware address needed for homing
	 */
	HomeCommand(HomingHardware* homingHardware);
	
	/**
	 * @brief Destroy the Command object.
	 */
	~HomeCommand();

	/**
	 * @brief Prepare homing execution by initializing the homing state machine.
	 *
	 */
	void prepare() override;

	/**
	 * @brief Execute one homing step and report progress.
	 *
	 * Expected sequence follows the controller homing flow:
	 * INIT -> Z -> X -> Y -> YAW -> done.
	 *
	 * @return CommandState InProgress while homing is ongoing, Done when completed, Error on failure.
	 */
	CommandState run() override;

	/**
	 * @brief Reset the command state to allow a new homing cycle.
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

		HomingHardware* homingHardware;
		HomingPayload homingPayload;
		HomingState homingState;

};

#endif