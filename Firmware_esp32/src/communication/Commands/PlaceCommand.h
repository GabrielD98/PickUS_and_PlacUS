/**
 * @file PlaceCommand.h
 * @author pickus plackus
 * @brief Place command implementation
 * @version 0.1
 * @date 2026-04-26
 * 
 * @copyright Copyright (c) 2026
 * 
 */
#ifndef PLACECOMMAND_H
#define PLACECOMMAND_H

#include <stdint.h>
#include <mutex>
#include "Command.h"
#include "hardware/mosfet.h"
#include "hardware/pressureSensor.h"

#define MAX_TOOLHEAD 2 //TODO: Put this somewhere more global

/**
 * @brief Payload used by PlaceCommand.
 */
struct PlacingPayload
{
	uint8_t toolheadNumber;
	uint16_t pressureThresholdKPa;
};

/**
 * @brief Hardware dependencies required by PlaceCommand.
 */
struct PlacingHardware
{
	Mosfet* valve[MAX_TOOLHEAD];
	Mosfet* pump;
	PressureSensor* pressureSensor[MAX_TOOLHEAD];
};

class PlaceCommand : public Command
{
	public:
	/**
	 * @brief Construct a new Place Command object.
	 *
	 * @param placingHardware All hardware addresses needed for placing.
	 */
	PlaceCommand(PlacingHardware* placingHardware);

	/**
	 * @brief Destroy the Place Command object.
	 */
	~PlaceCommand();

	/**
	 * @brief Prepare the place command state machine.
	 */
	void prepare() override;

	/**
	 * @brief Execute one place step and report progress.
	 *
	 * @return CommandState InProgress while running, Done when completed, Error on failure.
	 */
	CommandState run() override;

	/**
	 * @brief Reset the command state to allow a new place cycle.
	 */
	void reset() override;

	/**
	 * @brief Set command payload.
	 *
	 * @param payload Pointer to payload bytes.
	 * @param payloadSize Size of payload in bytes.
	 * @return true if payload was accepted, false otherwise.
	 */
	bool setPayload(uint8_t* payload, uint16_t payloadSize) override;

	private:
	std::mutex commandMutex_;
	PlacingHardware* placingHardware;
	PlacingPayload placingPayload;
};

#endif
