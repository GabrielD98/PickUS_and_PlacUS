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

void Controller::update()
{
    CommandId command_id = dataModel.get()->command.id;    
    dataModel.release();
    MachineState state_;

    switch(command_id){
        case CommandId::STOP: // STOP
            state_ = MachineState::READY;
            break;

        case CommandId::MOVE: // MOVE
            setTargets();
            if (motorSystem.run())
            {
                state_ = MachineState::MOVING;
            }
            else
            {
                state_ = MachineState::READY;
            }
            break;

        case CommandId::PICK: // PICK
            setTargets();
            if (motorSystem.run())
            {
                state_ = MachineState::PICKING;
            }
            else
            {
                state_ = MachineState::READY;
            }
            break;

        case CommandId::PLACE: // PLACE
            setTargets();
            if (motorSystem.run())
            {
                state_ = MachineState::PLACING;
            }
            else
            {
                state_ = MachineState::READY;
            }
            break;

        case CommandId::HOME: // HOME
            
            setTargets();
            // Run till encounter limit-switches, then update absolute coordinates
            if (motorSystem.run())
            {
                state_ = MachineState::MOVING;
            }
            else
            {
                state_ = MachineState::READY;
            }
            break;

        case CommandId::EMPTY: // EMPTY
            if (motorSystem.run())
            {
            }
            else 
            {
                state_ = MachineState::READY;
            }
            break;

        default:

        position_t newPos;
        newPos.x = motors[0]->currentPosition(); //New x position 
        newPos.y = motors[1]->currentPosition(); //New y position
        newPos.z = motors[2]->currentPosition(); //New z position
        newPos.yaw = motors[3]->currentPosition(); //New yaw position 

        dataModel.get()->position = newPos;
        dataModel.release();
        
        dataModel.get()->state = state_;
        dataModel.release();

    }
}

void Controller::setTargets()
{ 
    float speed = dataModel.get()->command.velocity; // Set the variable speed to the requested velocity in the command 
    dataModel.release();
    position_t position = dataModel.get()->command.requestedPosition; // Sets the variable to the position requested by command 
    dataModel.release();

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

