#include "Controller.h"

#define STEP_PER_HOME_LOOP -1

#define contactHeight -200
#define zAxisSpeed 200

Controller::Controller()
    : motorX(AccelStepper::DRIVER, PIN_DX_STEP, PIN_DX_DIR),
      motorY(AccelStepper::DRIVER, PIN_DY_STEP, PIN_DY_DIR),
      motorZ(AccelStepper::DRIVER, PIN_DZ_STEP, PIN_DZ_DIR),
      motorYAW(AccelStepper::DRIVER, PIN_DYAW_STEP, PIN_DYAW_DIR),
      limSwitchX(PIN_LIMSWITCH_X),
      limSwitchY(PIN_LIMSWITCH_Y),
      limSwitchZ(PIN_LIMSWITCH_Z)
{
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
    homingState = HomingState::HOMING_X;
    pickingState = PickingState::PICKING_INIT;
    placingState = PlacingState::PLACING_INIT;
}

Controller::~Controller()
{
}

void Controller::update()
{
    command_t command =  dataModel.get()->command;
    dataModel.release();

    switch (machineState)
    {
    case MachineState::ERROR:
        //TODO
        break;
    
    case MachineState::READY:
        switch (command.id)
        {
        case CommandId::STOP:
            break;
            
        case CommandId::MOVE:
            machineState = MachineState::MOVING;
            setTargets(command.requestedPosition,command.velocity);
            break;

        case CommandId::PICK:
            machineState = MachineState::PICKING;
            break;

        case CommandId::PLACE:
            machineState = MachineState::PLACING;
            break;

        case CommandId::HOME:
            machineState = MachineState::HOMING;
            break;

        case CommandId::EMPTY:
            break;

        }
    
    case MachineState::MOVING:
        if(!motorSystem.run())
        {
            machineState = MachineState::READY;
        }
        break;
    
    case MachineState::PLACING:
        picking();
        if(pickingState == PickingState::PICKING_DONE)
        {
            machineState = MachineState::READY;
            pickingState = PickingState::PICKING_INIT;
        }
        break;
    
    case MachineState::PICKING:
        //TODO
        break;
    
    case MachineState::HOMING:
        goHome();
        if(homingState == HomingState::HOMING_DONE)
        {
            machineState = MachineState::READY;
            homingState = HomingState::HOMING_X;
        }
        break;
    
    }

    position_t currentPosition;
    currentPosition.x = motorX.currentPosition();
    currentPosition.y = motorY.currentPosition();
    currentPosition.z = motorZ.currentPosition();
    currentPosition.yaw = motorYAW.currentPosition();

    dataModel_t* dataModel = dataModel.get();
    data->position = currentPosition;
    data->state = machineState;
    dataModel.release();
}

void Controller::setTargets(position_t position, float speed)
{
    long target[4] =
    {
        position.x,
        position.y,
        position.z,
        position.yaw
    };

    motorX.setMaxSpeed(speed);
    motorY.setMaxSpeed(speed);
    motorZ.setMaxSpeed(speed);
    motorYAW.setMaxSpeed(speed);
    
    motorSystem.moveTo(target);
}


void Controller::goHome()
{
    switch (homingState)
    {
    case HomingState::HOMING_X:

        if(limSwitchX.isTriggered())
        {
            motorX.setCurrentPosition(0);
            homingState = HomingState::HOMING_Y;
        }
        else
        {
            motorX.move(STEP_PER_HOME_LOOP);
        }
        break;

    case HomingState::HOMING_Y:

        if(limSwitchY.isTriggered())
        {
            motorY.setCurrentPosition(0);
            homingState = HomingState::HOMING_Z;
        }
        else
        {
            motorY.move(STEP_PER_HOME_LOOP);
        }
        break;

    case HomingState::HOMING_Z:

        if(limSwitchZ.isTriggered())
        {
            motorZ.setCurrentPosition(0);
            homingState = HomingState::HOMING_YAW;
        }
        else
        {
            motorZ.move(STEP_PER_HOME_LOOP);
        }
        break;
        
    case HomingState::HOMING_YAW:

        motorYAW.setCurrentPosition(0);
        homingState = HomingState::HOMING_DONE;
        break;

    case HomingState::HOMING_DONE:
        break;
    }
}

void Controller::picking()
{
    switch (pickingState)
    {
    case PickingState::PICKING_INIT:
        pump.on();
        delay(100);
        valve.on();
        pickingState = PickingState::PICKING_GOING_DOWN;
        break;

    case PickingState::PICKING_GOING_DOWN:
        motorZ.setMaxSpeed(zAxisSpeed);    
        motorZ.moveTo(contactHeight);
        if(motorZ.distanceToGo() == 0)
        {
            pickingState = PickingState::PICKING_CONTACT;
        }
        break;

    case PickingState::PICKING_CONTACT:
        valve.off();
        delay(100);
        pickingState = PickingState::PICKING_GOING_UP;
        break;

    case PickingState::PICKING_GOING_UP:
        motorZ.setMaxSpeed(zAxisSpeed); 
        motorZ.moveTo(0);
        if(motorZ.distanceToGo() == 0)
        {
            pickingState = PickingState::PICKING_DONE;
        }
        break;

    case PickingState::PICKING_DONE:
        break;
    }
}


void Controller::placing()
{
    switch (placingState)
    {
    case PlacingState::PLACING_INIT:
        valve.off();
        placingState = PlacingState::PLACING_GOING_DOWN;
        break;

    case PlacingState::PLACING_GOING_DOWN:
        motorZ.setMaxSpeed(zAxisSpeed);    
        motorZ.moveTo(contactHeight);
        if(motorZ.distanceToGo() == 0)
        {
            placingState = PlacingState::PLACING_CONTACT;
        }
        break;

    case PlacingState::PLACING_CONTACT:
        valve.on();
        delay(100);
        placingState = PlacingState::PLACING_GOING_UP;
        break;

    case PlacingState::PLACING_GOING_UP:
        motorZ.setMaxSpeed(zAxisSpeed); 
        motorZ.moveTo(0);
        if(motorZ.distanceToGo() == 0)
        {
            placingState = PlacingState::PLACING_DONE;
        }
        break;

    case PlacingState::PLACING_DONE:
        valve.off();
        pump.off();
        break;
    }
}
