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
    
    switch(dataModel.get()->command.id){
        case CommandId::STOP: // STOP
            
            break;

        case CommandId::MOVE: // MOVE
            setTargets();
            motorSystem.run();
            break;

        case CommandId::PICK: // PICK
            setTargets();
            motorSystem.run();
            break;

        case CommandId::PLACE: // PLACE
            setTargets();
            motorSystem.run();
            break;

        case CommandId::HOME: // HOME
            
            // setTargets();
            // Run till encounter limit-switches, then update absolute coordinates
            motorSystem.run();
            break;

        case CommandId::EMPTY: // EMPTY
            motorSystem.run();
            break;

        default:

    }
}

void Controller::setTargets()
{ 
    float speed = dataModel.get()->command.velocity; // Set the variable speed to the requested velocity in the command 
    position_t position = dataModel.get()->command.requestedPosition; // Sets the variable to the position requested by command 

    long target[4] =
    {
        position.x,
        position.y,
        position.z,
        position.yaw
    };

    for (int index = 0; index < sizeof(motors)/sizeof(motors[0]); index++){
    motors[index]->setMaxSpeed(speed);
    }
    
    motorSystem.moveTo(target);
}

