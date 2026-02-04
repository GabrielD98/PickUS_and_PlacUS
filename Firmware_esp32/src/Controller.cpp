#include "Controller.h"

Controller::Controller()
{
    AccelStepper motorX(AccelStepper::DRIVER, PIN_DX_STEP, PIN_DX_DIR);
    AccelStepper motorY(AccelStepper::DRIVER, PIN_DY_STEP, PIN_DY_DIR);
    AccelStepper motorZ(AccelStepper::DRIVER, PIN_DZ_STEP, PIN_DZ_DIR);
    AccelStepper motorYAW(AccelStepper::DRIVER, PIN_DYAW_STEP, PIN_DYAW_DIR);
    motors[0] = &motorX;
    motors[1] = &motorY;
    motors[2] = &motorZ;
    motors[3] = &motorYAW;

    motorSystem.addStepper(motorX);
    motorSystem.addStepper(motorY);
    motorSystem.addStepper(motorZ);
    motorSystem.addStepper(motorYAW);
}

Controller::~Controller()
{

}

void Controller::setCommand(command_t newCommand)
{
    command = newCommand;
}

void Controller::update()
{
    switch(command.id){
        case 0: // STOP
            
            break;

        case 1: // MOVE
            setSpeed(command.velocity);
            setTargets(command.requestedPosition);
            motorSystem.run();
            break;

        case 2: // PICK
            setSpeed(command.velocity);
            setTargets(command.requestedPosition);
            motorSystem.run();
            break;

        case 3: // PLACE
            setSpeed(command.velocity);
            setTargets(command.requestedPosition);
            motorSystem.run();
            break;

        case 4: // HOME
            setSpeed(command.velocity);
            
            // setTargets(command.requestedPosition);
            // Run till encounter limit-switches, then update absolute coordinates
            motorSystem.run();
            break;

        case 5: // EMPTY
            motorSystem.run();
            break;

        default:

    }
}

position_t Controller::getPosition()
{
    return position;
}

MachineState Controller::getState()
{
    return state;
}

void Controller::setTargets(position_t targets)
{
    motorSystem.moveTo(targets);
}

void Controller::setState(MachineState newState)
{
    state = newState;
}

void Controller::setPosition(position_t newPosition)
{
    position = newPosition;
}

void Controller::setSpeed(float speed)
{
    motors[0]->setMaxSpeed(speed);
    motors[1]->setMaxSpeed(speed);
    motors[2]->setMaxSpeed(speed);
    motors[3]->setMaxSpeed(speed);
}

// void setTargets(MultiStepper& gantry, AccelStepper* motors[NMOTOR], long positions[NMOTOR])
// {
//     gantry.moveTo(positions);
// }

// void setSpeed(float speed){
//     for (int index = 0; index < sizeof(motors)/sizeof(motors[0]); index++){
//     motors[index]->setMaxSpeed(speed);
//     }
// }