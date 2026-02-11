#ifndef CONTROLLER_H
#define CONTROLLER_H

#include <Arduino.h>
#include <AccelStepper.h>
#include <MultiStepper.h>

#define NMOTOR 4

#include "BoardConfig.h"

#include "../lib/data.hpp"
#include "DataModel.h"

class Controller
{
public :
    Controller();
    void update();
    DataModel dataModel;

private :
    AccelStepper* motors[NMOTOR];
    MultiStepper motorSystem;

    void setTargets();
    
};

#endif