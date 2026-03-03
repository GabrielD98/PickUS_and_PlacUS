#include "Controller.h"

Controller::Controller()
{
    motorX = AccelStepper(AccelStepper::DRIVER, PIN_DX_STEP, PIN_DX_DIR);
    motorY = AccelStepper(AccelStepper::DRIVER, PIN_DY_STEP, PIN_DY_DIR);
    motorZ = AccelStepper(AccelStepper::DRIVER, PIN_DZ_STEP, PIN_DZ_DIR);
    motorYAW = AccelStepper(AccelStepper::DRIVER, PIN_DYAW_STEP, PIN_DYAW_DIR);

    // Enable stepper drivers (active LOW)
    pinMode(PIN_DX_EN, OUTPUT);   digitalWrite(PIN_DX_EN, LOW);
    pinMode(PIN_DY_EN, OUTPUT);   digitalWrite(PIN_DY_EN, LOW);
    pinMode(PIN_DZ_EN, OUTPUT);   digitalWrite(PIN_DZ_EN, LOW);
    pinMode(PIN_DYAW_EN, OUTPUT); digitalWrite(PIN_DYAW_EN, LOW);

    motorSystem.addStepper(motorX);
    motorSystem.addStepper(motorY);
    motorSystem.addStepper(motorZ);
    motorSystem.addStepper(motorYAW);

    machineState = MachineState::READY;
}

Controller::~Controller()
{

}

void Controller::update()
{
    command_t command =  dataModel.get()->command;
    dataModel.release();

    switch (this->machineState)
    {
    case MachineState::ERROR:
        //TODO
        break;
    
    case MachineState::READY:
        /* code */
        break;
    
    case MachineState::MOVING:
        /* code */
        break;
    
    case MachineState::PLACING:
        /* code */
        break;
    
    case MachineState::PICKING:
        /* code */
        break;
    
    case MachineState::HOMING:
        /* code */
        break;
    
    }

    position_t currentPosition;
    currentPosition.x = motorX.currentPosition();
    currentPosition.y = motorY.currentPosition();
    currentPosition.z = motorZ.currentPosition();
    currentPosition.yaw = motorYAW.currentPosition();

    dataModel_t* dataModel = this->dataModel.get();
    dataModel->position = currentPosition;
    dataModel->state = this->machineState;
    this->dataModel.release();
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
