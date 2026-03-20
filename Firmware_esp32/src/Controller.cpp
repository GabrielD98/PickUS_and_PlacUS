#include "Controller.h"
#include "Geometry.h"

#define HOME_DIRECTION -1.0f
#define PIECE_PRESSURE_THRESHOLD 80 //TODO: validate value;
#define NO_PIECE_PRESSURE_THRESHOLD 100 //TODO: validate value;

#define HOME_SPEED 50.0
#define POSITION_UPDATE_FREQ 100

const velocity_t homeVelocity = velocityToStep(HOME_SPEED);

Controller::Controller()
    : motorX(AccelStepper::DRIVER, PIN_DX_STEP, PIN_DX_DIR),
      motorY(AccelStepper::DRIVER, PIN_DY_STEP, PIN_DY_DIR),
      motorZ(AccelStepper::DRIVER, PIN_DZ_STEP, PIN_DZ_DIR),
      motorYAW(AccelStepper::DRIVER, PIN_DYAW_STEP, PIN_DYAW_DIR),
      limSwitchX(PIN_LIMSWITCH_X,true),
      limSwitchY(PIN_LIMSWITCH_Y,true),
      limSwitchZ(PIN_LIMSWITCH_Z,true),
      valve(PIN_VALVE),
      pump(PIN_PUMP),
      pressureSensor(PIN_PSENSOR_CLK,PIN_PSENSOR_DATA)
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

    pressureSensor.init(); //TODO create a controller init

    machineState = MachineState::READY;
    homingState = HomingState::INIT;
    pickPlaceState = PickPlaceState::INIT;

    lastPositionUpdateMS = millis();
}

Controller::~Controller()
{
}

void Controller::update()
{
    command_t command =  dataModel.get()->command;
    dataModel.release();

    if(command.id == CommandId::STOP)
    {
        machineState = MachineState::READY;
    }

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
                    setTargets(command.requestedPosition,command.velocity);
                    machineState = MachineState::PICKING;
                    break;

                case CommandId::PLACE:
                    setTargets(command.requestedPosition,command.velocity);
                    machineState = MachineState::PLACING;
                    break;

                case CommandId::HOME:
                    homingState = HomingState::INIT;
                    machineState = MachineState::HOMING;
                    break;

                case CommandId::EMPTY:
                    break;

            }
    break;
    
    case MachineState::MOVING:

        if(!motorSystem.run())
        {
            machineState = MachineState::READY;
        }
        break;
    
    case MachineState::PLACING:

        executePickPlace(PickPlaceMode::PLACE);

        if(pickPlaceState == PickPlaceState::DONE)
        {
            machineState = MachineState::READY;
            pickPlaceState = PickPlaceState::INIT;
        }
        break;
    
    case MachineState::PICKING:

        executePickPlace(PickPlaceMode::PICK);

        if(pickPlaceState == PickPlaceState::DONE)
        {
            machineState = MachineState::READY;
            pickPlaceState = PickPlaceState::INIT;
        }
        break;
    
    case MachineState::HOMING:

        goHome();
        if(homingState == HomingState::HOMING_DONE)
        {
            machineState = MachineState::READY;
            homingState = HomingState::INIT;
        }
        break;
    
    }

    if((millis() - lastPositionUpdateMS) >= 1000/POSITION_UPDATE_FREQ)
    {
        position_t currentPosition;
        currentPosition.x = motorX.currentPosition();
        currentPosition.y = motorY.currentPosition();
        currentPosition.z = motorZ.currentPosition();
        currentPosition.yaw = motorYAW.currentPosition();

        currentPosition = stepToCoord(currentPosition);
        
        dataModel_t* dataModel = this->dataModel.get();
        dataModel->position = currentPosition;
        dataModel->state = machineState;
        this->dataModel.release();
        
        lastPositionUpdateMS = millis();
    }
}

void Controller::setTargets(position_t position, float speed)
{
    position = coordToStep(position);

    long target[4] =
    {
        (long)position.x,
        (long)position.y,
        (long)position.z,
        (long)position.yaw
    };

    velocity_t convertedSpeed = velocityToStep(speed);

    motorX.setMaxSpeed(convertedSpeed.x);
    motorY.setMaxSpeed(convertedSpeed.y);
    motorZ.setMaxSpeed(convertedSpeed.z);
    motorYAW.setMaxSpeed(convertedSpeed.yaw);
    
    motorSystem.moveTo(target);
}


void Controller::goHome()
{
    switch (homingState)
    {
        case HomingState::INIT:
            homingState = HomingState::Z;
            motorZ.setMaxSpeed(homeVelocity.z / 10.0f);
            motorZ.setSpeed(HOME_DIRECTION * (homeVelocity.z / 2.0f));
            break;

        case HomingState::Z:
            if(limSwitchZ.isTriggered())
            {
                motorZ.setCurrentPosition(0);
                homingState = HomingState::X;
                motorX.setMaxSpeed(homeVelocity.x);
                motorX.setSpeed(HOME_DIRECTION * homeVelocity.x);
            }
            else
            {
                motorZ.runSpeed();
            }
            break;

        case HomingState::X:
            if(limSwitchX.isTriggered())
            {
                motorX.setCurrentPosition(0);
                homingState = HomingState::Y;
                motorY.setMaxSpeed(homeVelocity.y);
                motorY.setSpeed(HOME_DIRECTION * homeVelocity.y);
            }
            else
            {
                motorX.runSpeed();
            }
            break;

        case HomingState::Y:
            if(limSwitchY.isTriggered())
            {
                motorY.setCurrentPosition(0);
                homingState = HomingState::YAW;
            }
            else
            {
                motorY.runSpeed();
            }
            break;

        case HomingState::YAW:

            motorYAW.setCurrentPosition(0);
            homingState = HomingState::HOMING_DONE;
            break;

        case HomingState::HOMING_DONE:
            break;
        }
}


void Controller::executePickPlace(PickPlaceMode mode)
{
    switch (pickPlaceState)
    {
    case PickPlaceState::INIT:

        if (mode == PickPlaceMode::PICK)
        {
            pump.on();
            valve.on();
        }
        else
        {
            valve.off();
        }

        pickPlaceState = PickPlaceState::GOING_DOWN;
        break;

    case PickPlaceState::GOING_DOWN:

        if (!motorSystem.run())
            pickPlaceState = PickPlaceState::CONTACT;
        break;

    case PickPlaceState::CONTACT:

        if (mode == PickPlaceMode::PICK)
        {
            valve.off();
            if(pressureSensor.getPressureKPa() < PIECE_PRESSURE_THRESHOLD) //TODO: Add timeout
            {
                pickPlaceState = PickPlaceState::GOING_UP;
            }
        }
        else
        {
            valve.on();
            if(pressureSensor.getPressureKPa() > NO_PIECE_PRESSURE_THRESHOLD) //TODO: Add timeout
            {
                pickPlaceState = PickPlaceState::GOING_UP;
            }
        }

        if(pickPlaceState == PickPlaceState::GOING_UP)
        {
            position_t currentStepPosition;
            currentStepPosition.x = motorX.currentPosition();
            currentStepPosition.y = motorY.currentPosition();
            currentStepPosition.z = 0;
            currentStepPosition.yaw = motorYAW.currentPosition();

            setTargets(currentStepPosition,motorZ.maxSpeed());

        }

        break;

    case PickPlaceState::GOING_UP:

        if (!motorSystem.run())
        {
            pickPlaceState = PickPlaceState::DONE;
        }
        if (mode == PickPlaceMode::PLACE)
        {
            valve.off(); pump.off();
        }
        break;

    case PickPlaceState::DONE:
        break;
    }
}