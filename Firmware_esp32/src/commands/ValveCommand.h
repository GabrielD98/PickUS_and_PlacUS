/**
 * @file ValveCommand.h
 * @author PickusAndPlacus
 * @brief Manual valve control command.
 * @version 0.1
 * @date 2026-05-25
 */
#ifndef VALVECOMMAND_H
#define VALVECOMMAND_H

#include <stdint.h>
#include <mutex>
#include "Command.h"
#include "hardware/mosfet.h"
#include "boardconfig.h"

struct ValvePayload
{
	uint8_t toolheadNumber;
	uint8_t enabled;
};

struct ValveHardware
{
	Mosfet* valve[MAX_TOOLHEAD];
};

class ValveCommand : public Command
{
	public:
	ValveCommand(ValveHardware* valveHardware);
	~ValveCommand();

	void prepare() override;
	CommandState run() override;
	bool setPayload(uint8_t* payload, uint16_t payloadSize) override;

	private:
	std::mutex commandMutex_;
	ValveHardware* valveHardware;
	ValvePayload valvePayload;
};

#endif
