/**
 * @file controller.h
 * @author PickusAndPlacus
 * @brief Class to manage commands from the UI, update machine states and control hardware.
 * @version 1.0
 * @date 17/04/2026
 */

#ifndef CONTROLLER_H
#define CONTROLLER_H

#include <Arduino.h>
#include <AccelStepper.h>
#include <MultiStepper.h>
#include "BoardConfig.h"
#include "../lib/data.hpp"
#include "DataModel.h"
#include "Mosfet.h"
#include "LimitSwitch.h"
#include "pressureSensor.h"
#include "Geometry.h"

/**
 * @brief Control hardware components in response to commands received from the UI.
 * Exchange information with the UI via a shared chain of data.
 */
class Controller
{
public :
    /**
     * @brief Instantiates all hardware components, enable stepper drivers and initialize all system states.
     */
    Controller();

    /**
     * @brief Control hardware components in response to the command, regarding the current system states.
     * Updates machine state and current toolhead position to the dataModel at a time interval.
     */
    void update();
    
    /**
     * @brief Shared chain of data with UI.
     * Used to make current toolhead position and machine state accessible informations to the UI.
     */
    DataModel dataModel;

private :
    // Hardware components
    AccelStepper motorX;
    AccelStepper motorY;
    AccelStepper motorZ;
    AccelStepper motorYAW;
    MultiStepper motorSystem;

    Mosfet valve;
    Mosfet pump;
    PressureSensor pressureSensor;

    LimitSwitch limSwitchX;
    LimitSwitch limSwitchY;
    LimitSwitch limSwitchZ;

    // System states
    MachineState machineState;
    HomingState homingState;
    PickPlaceState pickPlaceState;

    // Stores the last time information was updated to the dataModel.
    uint64_t lastPositionUpdateMS;

    /**
     * @brief Set target positions and desired speed to all motors.
     * @param position targeted coordinates (mm and degree)
     * @param speed maximum speed (mm/s and degree/s)
     */
    void setTargets(positionCartesian_t position, float speed);

    /**
     * @brief Homing action to calibrate all motors, one axis at a time (Order : Z, X, Y)
     * Yaw current position is simply set to 0.
     * Updates the homing state.
     */
    void goHome();

    /**
     * @brief Controls pump and valve's activation during toolhead's ascencion and descent.
     * Updates the picking and placing state.
     * Reacts to pressure changes when contact is made at the nozzle.
     * @param mode 
     */
    void executePickPlace(PickPlaceMode mode);
};

#endif