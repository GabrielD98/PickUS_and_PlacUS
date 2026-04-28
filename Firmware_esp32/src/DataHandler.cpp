#include "DataHandler.h"

DataHandler::DataHandler(DataHandlerHardware* hardware, CommandHandler* commandHandler)
    : hardware(hardware), commandHandler(commandHandler)
{
    dataModel = {};
}

/**
 * @brief Updates the shared data model with current hardware state.
 * 
 * Reads motor positions and stores them in the dataModel position fields.
 * Updates the machine state field.
 */
void DataHandler::updateInfo(MachineState machineState)
{
    std::lock_guard<std::mutex> lock(mutex_);
    
    // Update machine state
    dataModel.state = machineState;
    
    // Update hardware-backed fields (positions, pressures, valves, pump) if available
    if (hardware != nullptr)
    {
        // Read current step positions from motors
        if (hardware->motorX != nullptr)
            dataModel.position.x = hardware->motorX->currentPosition();
        if (hardware->motorY != nullptr)
            dataModel.position.y = hardware->motorY->currentPosition();
        if (hardware->motorZ != nullptr)
            dataModel.position.z = hardware->motorZ->currentPosition();
        if (hardware->motorYaw != nullptr)
            dataModel.position.yaw = hardware->motorYaw->currentPosition();

        // Pressure, valve states for each toolhead
        for (int i = 0; i < MAX_TOOLHEAD; ++i)
        {
            // Pressure
            if (hardware->pressureSensor[i] != nullptr)
            {
                dataModel.pressure[i] = hardware->pressureSensor[i]->getPressureKPa();
            }
            else
            {
                dataModel.pressure[i] = 0.0f;
            }

            // Valve state
            if (hardware->valve[i] != nullptr)
            {
                dataModel.valveState[i] = hardware->valve[i]->getState();
            }
            else
            {
                dataModel.valveState[i] = false;
            }
        }

        // Pump state
        if (hardware->pump != nullptr)
        {
            dataModel.pumpState = hardware->pump->getState();
        }
        else
        {
            dataModel.pumpState = false;
        }
    }

    // Update command id from command handler if available
    if (commandHandler != nullptr)
    {
        dataModel.currentCommandId = static_cast<CommandId>(commandHandler->getCurrentCommandId());
    }
}

// Get a thread-safe copy of current data
dataModel_t DataHandler::getInfo()
{
    std::lock_guard<std::mutex> lock(mutex_);
    return dataModel;
}
