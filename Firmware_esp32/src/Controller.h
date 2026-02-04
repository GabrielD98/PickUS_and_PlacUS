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
    ~Controller();
    void setCommand(command_t command);
    void update();
    position_t getPosition();
    MachineState getState();
private :
    MachineState state;
    position_t position;
    AccelStepper* motors[NMOTOR];
    MultiStepper motorSystem;

    Command command;

    void setTargets(position_t targets);
    void setState(MachineState newState);
    void setPosition(position_t newPosition);
    void setSpeed(float speed);
};

#endif