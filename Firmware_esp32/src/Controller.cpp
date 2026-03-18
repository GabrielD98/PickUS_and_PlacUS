#include "Controller.h"
#include "Geometry.h"

#define STEP_PER_HOME_LOOP -1
#define PIECE_PRESSURE_THRESHOLD 80 //TODO: validate value;
#define NO_PIECE_PRESSURE_THRESHOLD 100 //TODO: validate value;

#define HOME_SPEED 1000
#define HOME_ACCEL 2000
#define POSITION_UPDATE_FREQ 10

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
    homingState = HomingState::HOMING_X;
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

            //request value is constrained and converted into step
            command.requestedPosition = mmToStep(command.requestedPosition);

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
            homingState = HomingState::HOMING_X;
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

        currentPosition = stepToMm(currentPosition);
        
        dataModel_t* dataModel = this->dataModel.get();
        dataModel->position = currentPosition;
        dataModel->state = machineState;
        this->dataModel.release();
        
        lastPositionUpdateMS = millis();
    }
}

void Controller::setTargets(position_t position, float speed)
{
    long target[4] =
    {
        (long)position.x,
        (long)position.y,
        (long)position.z,
        (long)position.yaw
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
            motorX.setMaxSpeed(HOME_SPEED);
            motorX.setAcceleration(HOME_ACCEL);
            motorX.move(STEP_PER_HOME_LOOP);
            motorX.run();
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
            motorY.setMaxSpeed(HOME_SPEED);
            motorY.setAcceleration(HOME_ACCEL);
            motorY.move(STEP_PER_HOME_LOOP);
            motorY.run();
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
            motorZ.setMaxSpeed(HOME_SPEED);
            motorZ.setAcceleration(HOME_ACCEL);
            motorZ.move(STEP_PER_HOME_LOOP);
            motorZ.run();
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