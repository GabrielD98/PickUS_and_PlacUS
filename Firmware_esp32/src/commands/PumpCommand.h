/**
 * @file PumpCommand.h
 * @author PickusAndPlacus
 * @brief Manual pump control command.
 * @version 0.1
 * @date 2026-05-25
 */
#ifndef PUMPCOMMAND_H
#define PUMPCOMMAND_H

#include <stdint.h>
#include <mutex>
#include "Command.h"
#include "hardware/mosfet.h"

struct PumpPayload
{
	uint8_t enabled;
};

struct PumpHardware
{
	Mosfet* pump;
};

class PumpCommand : public Command
{
	public:
	PumpCommand(PumpHardware* pumpHardware);
	~PumpCommand();

	void prepare() override;
	CommandState run() override;
	bool setPayload(uint8_t* payload, uint16_t payloadSize) override;

	private:
	std::mutex commandMutex_;
	PumpHardware* pumpHardware;
	PumpPayload pumpPayload;
};

#endif
