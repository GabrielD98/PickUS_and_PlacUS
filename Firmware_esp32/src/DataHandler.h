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
#include "hardware/mosfet.h"
#include "hardware/pressureSensor.h"
#include "CommandHandler.h"
#include "boardconfig.h"



/**
 * @brief Chain of data used to exchange information.
 */
typedef struct dataModel
{
    MachineState state;
    CommandId currentCommandId;
    positionStep_t position;
    float pressure[MAX_TOOLHEAD];
    bool valveState[MAX_TOOLHEAD];
    bool pumpState;

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
    Mosfet* valve[MAX_TOOLHEAD];
	Mosfet* pump;
	PressureSensor* pressureSensor[MAX_TOOLHEAD];

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
         * @param commandHandler Pointer to the command manager used to
         * query or update the currently executing command Id.
         */
        DataHandler(DataHandlerHardware* hardware, CommandHandler* commandHandler);

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
        dataModel_t lastSystemInfo;
        // Mutex to lock the chain of data while used.
        std::mutex mutex_;
        // Hardware references for status updates
        DataHandlerHardware* hardware;

        CommandHandler* commandHandler;
};

#endif