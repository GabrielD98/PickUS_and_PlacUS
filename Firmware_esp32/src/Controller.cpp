#include "Controller.h"

Controller::Controller()
{
    motorX = AccelStepper(AccelStepper::DRIVER, PIN_DX_STEP, PIN_DX_DIR);
    motorY = AccelStepper(AccelStepper::DRIVER, PIN_DY_STEP, PIN_DY_DIR);
    motorZ = AccelStepper(AccelStepper::DRIVER, PIN_DZ_STEP, PIN_DZ_DIR);
    motorYAW = AccelStepper(AccelStepper::DRIVER, PIN_DYAW_STEP, PIN_DYAW_DIR);

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
        state_ = MachineState::READY;
            break;
        
    }

    position_t newPos;
    newPos.x = motorX.currentPosition(); //New x position 
    newPos.y = motorY.currentPosition(); //New y position
    newPos.z = motorZ.currentPosition(); //New z position
    newPos.yaw = motorYAW.currentPosition(); //New yaw position 
    dataModel.get()->position = newPos;
    dataModel.release();
    dataModel.get()->state = state_;
    dataModel.release();
}

void Controller::setTargets()
{ 
    float speed = dataModel.get()->command.velocity; // Set the variable speed to the requested velocity in the command 
    dataModel.release();
    position_t position = dataModel.get()->command.requestedPosition; // Sets the variable to the position requested by command 
    dataModel.release();

    long target[4] =
    {
        static_cast<long>(position.x),
        static_cast<long>(position.y),
        static_cast<long>(position.z),
        static_cast<long>(position.yaw)
    };

    motorX.setMaxSpeed(speed);
    motorY.setMaxSpeed(speed);
    motorZ.setMaxSpeed(speed);
    motorYAW.setMaxSpeed(speed);
    
    motorSystem.moveTo(target);
}

