/**
 * @file dataHandler.h
 * @author PickusAndPlacus
 * @brief Handler for shared data exchange with hardware-aware status updates.
 * @version 1.0
 * @date 17/04/2026
 */

#ifndef DATAHANDLER_H
#define DATAHANDLER_H

#include "../lib/data.hpp"
#include <mutex>
#include <AccelStepper.h>

/**
 * @brief Chain of data used to exchange information.
 */
typedef struct dataModel
{
    positionStep_t position;
    MachineState state;

}dataModel_t;

/**
 * @brief Hardware configuration container for DataHandler.
 */
struct DataHandlerHardware
{
    AccelStepper* motorX;
    AccelStepper* motorY;
    AccelStepper* motorZ;
    AccelStepper* motorYaw;
};

/**
 * @brief Handles shared data exchange with hardware-aware status updates.
 */
class DataHandler
{   
    public :
        /**
         * @brief Construct a new Data Handler with hardware dependencies.
         *
         * @param hardware Struct containing pointers to all hardware needed
         * for reading position and state information.
         */
        DataHandler(DataHandlerHardware* hardware);

        /**
         * @brief Update the shared data model with current hardware state.
         *
         * Reads motor positions and updates the internal data model
         * with the current machine state.
         *
         * @param machineState Current machine state to store.
         */
        void updateInfo(MachineState machineState);



        /**
         * @brief Get a copy of the current data model state.
         * 
         * Thread-safe read that returns a copy of the dataModel under mutex lock.
         * No need to manually release - the lock is automatically released.
         * 
         * @return Copy of the dataModel_t structure.
         */
        dataModel_t getInfo();

    private :
        // Chain of data accessible to both Controller and Interface to exchange informations and commands.
        dataModel_t dataModel;
        // Mutex to lock the chain of data while used.
        std::mutex mutex_;
        // Hardware references for status updates
        DataHandlerHardware* hardware;
};

#endif