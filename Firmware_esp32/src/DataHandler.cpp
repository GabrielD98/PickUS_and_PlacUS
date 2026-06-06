#include "DataHandler.h"

DataHandler::DataHandler(DataHandlerHardware* hardware, CommandHandler* commandHandler)
    : hardware(hardware), commandHandler(commandHandler)
{
    lastSystemInfo = {};
}

/**
 * @brief Updates the shared data model with current hardware state.
 * 
 * Reads motor positions and stores them in the lastSystemInfo position fields.
 * Updates the machine state field.
 */
void DataHandler::updateInfo(MachineState machineState)
{
    std::lock_guard<std::mutex> lock(mutex_);
    
    // Update machine state
    lastSystemInfo.state = machineState;
    
    // Update hardware-backed fields (positions, pressures, valves, pump) if available
    if (hardware != nullptr)
    {
        // Read current step positions from motors
        if (hardware->motorX != nullptr)
            lastSystemInfo.position.x = hardware->motorX->currentPosition();
        if (hardware->motorY != nullptr)
            lastSystemInfo.position.y = hardware->motorY->currentPosition();
        if (hardware->motorZ != nullptr)
            lastSystemInfo.position.z = hardware->motorZ->currentPosition();
        if (hardware->motorYaw != nullptr)
            lastSystemInfo.position.yaw = hardware->motorYaw->currentPosition();

        // Pressure, valve states for each toolhead
        for (int i = 0; i < MAX_TOOLHEAD; ++i)
        {
            // Pressure
            if (hardware->pressureSensor[i] != nullptr)
            {
                lastSystemInfo.pressure[i] = hardware->pressureSensor[i]->getPressureKPa();
            }
            else
            {
                lastSystemInfo.pressure[i] = 0.0f;
            }

            // Valve state
            if (hardware->valve[i] != nullptr)
            {
                lastSystemInfo.valveState[i] = hardware->valve[i]->getState();
            }
            else
            {
                lastSystemInfo.valveState[i] = false;
            }
        }

        // Pump state
        if (hardware->pump != nullptr)
        {
            lastSystemInfo.pumpState = hardware->pump->getState();
        }
        else
        {
            lastSystemInfo.pumpState = false;
        }
    }

    // Update command id from command handler if available
    if (commandHandler != nullptr)
    {
        lastSystemInfo.currentCommandId = static_cast<CommandId>(commandHandler->getCurrentCommandId());
    }
}

// Get a thread-safe copy of current data
dataModel_t DataHandler::getInfo()
{
    std::lock_guard<std::mutex> lock(mutex_);
    return lastSystemInfo;
}
