#ifndef CONTROLLER_H
#define CONTROLLER_H

#include <Arduino.h>
#include <AccelStepper.h>
#include <MultiStepper.h>

#include "BoardConfig.h"

#include "../lib/data.hpp"
#include "DataModel.h"

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

    bool ValveState = false; 
    bool first = true; 

    void setTargets();
};

#endif