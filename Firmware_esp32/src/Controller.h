/**
 * @file controller.h
 * @author PickusAndPlacus
 * @brief Controller interface coordinating command execution and machine state updates.
 * @version 1.0
 * @date 17/04/2026
 */

#ifndef CONTROLLER_H
#define CONTROLLER_H

#include <Arduino.h>
#include "../lib/data.hpp"
#include "datamodel.h"
#include "communication/CommandHandler.h"


/**
 * @brief Central coordinator for command-driven machine control.
 *
 * The controller consumes commands from the shared data model, executes the
 * corresponding hardware actions, and periodically publishes machine status
 * back to the shared data model for the UI.
 */
class Controller
{
public :
    /**
     * @brief Construct a controller instance.
     *
     * @param commanddHandler Command registry/dispatcher used to access and
     * execute concrete command implementations.
     */
    Controller(CommandHandler* commandHandler);

    /**
     * @brief Execute one control-cycle iteration.
     *
     * This method reads the latest command from the shared data model,
     * advances the controller state machine, drives hardware accordingly, and
     * periodically publishes machine state and position feedback.
     */
    void update();


private :


    CommandHandler* commandHandler;

    /**
     * @brief Current high-level machine operating state.
     */
    MachineState machineState;

    /**
     * @brief Timestamp of the last status publication to the shared data model.
     */
    uint64_t lastDataUpdateMS;

};

#endif