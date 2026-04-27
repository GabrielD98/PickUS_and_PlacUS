#include "DataHandler.h"

DataHandler::DataHandler(DataHandlerHardware* hardware)
    : hardware(hardware)
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
    
    // Update position from motors if hardware is available
    if (hardware != nullptr)
    {
        // Read current step positions from motors and convert to cartesian coordinates
        if (hardware->motorX != nullptr)
            dataModel.position.x = hardware->motorX->currentPosition();
        if (hardware->motorY != nullptr)
            dataModel.position.y = hardware->motorY->currentPosition();
        if (hardware->motorZ != nullptr)
            dataModel.position.z = hardware->motorZ->currentPosition();
        if (hardware->motorYaw != nullptr)
            dataModel.position.yaw = hardware->motorYaw->currentPosition();
    }
}

// Get a thread-safe copy of current data
dataModel_t DataHandler::getInfo()
{
    std::lock_guard<std::mutex> lock(mutex_);
    return dataModel;
}
