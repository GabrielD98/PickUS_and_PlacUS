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


void Controller::update()
{
    switch(command.id){
        case CommandId::STOP: // STOP
            
            break;

        case CommandId::MOVE: // MOVE
            setTargets(command.requestedPosition);
            motorSystem.run();
            break;

        case CommandId::PICK: // PICK
            setTargets(command.requestedPosition);
            motorSystem.run();
            break;

        case CommandId::PLACE: // PLACE
            setTargets(command.requestedPosition);
            motorSystem.run();
            break;

        case CommandId::HOME: // HOME
            
            // setTargets(command.requestedPosition);
            // Run till encounter limit-switches, then update absolute coordinates
            motorSystem.run();
            break;

        case CommandId::EMPTY: // EMPTY
            motorSystem.run();
            break;

        default:

    }
}

void Controller::setTargets(position_t targets)
{ 
    motorSystem.moveTo(targets);
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