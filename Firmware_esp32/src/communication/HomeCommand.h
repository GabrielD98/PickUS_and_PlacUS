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


class HomeCommand : public Command
{
	public:
	
	/**
	 * @brief Destroy the Home Command object
	 * 
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
	 * Home command currently does not require payload data.
	 * @param payload Pointer to the payload buffer (unused for HOME).
	 * @param payloadSize Size of the payload buffer in bytes (unused for HOME).
	 * 
	 * @return true if payload was set, false if payload is not equal to intern struct size
	*/
	bool setPayload(uint8_t* payload, uint16_t payloadSize) override;

	private:

		HomingHardware* homingHardware;
		HomingPayload homingPayload;
		HomingState homingState;

};

/**
 * @brief Data received to complete the command
 * 
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
 * @brief All hardware address needed for homing
 * 
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

#endif