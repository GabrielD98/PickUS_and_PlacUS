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

class Controller
{
public :
    Controller();
    ~Controller();
    void update();
    DataModel dataModel;

private :
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

    MachineState machineState;
    HomingState homingState;
    PickPlaceState pickPlaceState;

    uint64_t lastPositionUpdateMS;

    void setTargets(position_t position, float speed);
    void goHome();
    void picking();
    void placing();
    void executePickPlace(PickPlaceMode mode);
};

#endif