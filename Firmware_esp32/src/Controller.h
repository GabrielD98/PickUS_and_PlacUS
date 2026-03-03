#ifndef CONTROLLER_H
#define CONTROLLER_H

#include <Arduino.h>
#include <AccelStepper.h>
#include <MultiStepper.h>

#include "BoardConfig.h"

#include "../lib/data.hpp"
#include "DataModel.h"
#include "LimitSwitch.h"

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

    LimitSwitch limSwitchX;
    LimitSwitch limSwitchY;
    LimitSwitch limSwitchZ;

    MachineState machineState;
    bool ValveState = false; 
    bool first = true; 

    void setTargets();
    void goHome();
};

#endif