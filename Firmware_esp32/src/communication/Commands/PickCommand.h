/**
 * @file PickCommand.h
 * @author pickus plackus
 * @brief Pick command implementation
 * @version 0.1
 * @date 2026-04-26
 * 
 * @copyright Copyright (c) 2026
 * 
 */
#ifndef PICKCOMMAND_H
#define PICKCOMMAND_H

#include <stdint.h>
#include <mutex>
#include "Command.h"
#include "hardware/mosfet.h"
#include "hardware/pressureSensor.h"

#define MAX_TOOLHEAD 2 //TODO: Put this somewhere more global

/**
 * @brief Payload used by PickCommand.
 */
struct PickingPayload
{
	uint8_t toolheadNumber;
	uint16_t pressureThresholdKPa;
};

/**
 * @brief Hardware dependencies required by PickCommand.
 */
struct PickingHardware
{
	Mosfet* valve[MAX_TOOLHEAD];
	Mosfet* pump;
	PressureSensor* pressureSensor[MAX_TOOLHEAD];
};

class PickCommand : public Command
{
	public:
	/**
	 * @brief Construct a new Pick Command object.
	 *
	 * @param pickHardware All hardware addresses needed for picking.
	 */
	PickCommand(PickingHardware* pickHardware);

	/**
	 * @brief Destroy the Pick Command object.
	 */
	~PickCommand();

	/**
	 * @brief Prepare the pick command state machine.
	 */
	void prepare() override;

	/**
	 * @brief Execute one pick step and report progress.
	 *
	 * @return CommandState InProgress while running, Done when completed, Error on failure.
	 */
	CommandState run() override;

	/**
	 * @brief Reset the command state to allow a new pick cycle.
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
	PickingHardware* pickingHardware;
	PickingPayload pickingPayload;
};

#endif
