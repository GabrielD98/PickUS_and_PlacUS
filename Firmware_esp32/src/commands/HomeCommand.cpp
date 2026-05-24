#include <cstring>
#include "HomeCommand.h"


HomeCommand::HomeCommand(HomingHardware* homingHardware)
	: homingHardware(homingHardware)
{
	homingState = HomingState::Init;
	homingPayload = {};
}

HomeCommand::~HomeCommand()
{
}

void HomeCommand::prepare()
{
    std::lock_guard<std::mutex> lock(commandMutex_);
	homingState = HomingState::Init;
}


//TODO: ADD ERROR if timeout
CommandState HomeCommand::run()
{
    std::lock_guard<std::mutex> lock(commandMutex_);
	CommandState currentCommandState = CommandState::InProgress;

	switch (homingState)
    {
        case HomingState::Init:
            homingState = HomingState::Z;
            homingHardware->motorZ->setMaxSpeed(homingPayload.homingVelocity.z);
            homingHardware->motorZ->setSpeed(homingPayload.homingVelocity.z);
            break;

            
		// Homing Z-axis first in order to avoid collisions with the nozzle
		case HomingState::Z:
			if(homingHardware->limSwitchZ->isTriggered())
			{
				homingHardware->motorZ->setCurrentPosition(0);
				homingState = HomingState::X;
				homingHardware->motorX->setMaxSpeed(homingPayload.homingVelocity.x);
				homingHardware->motorX->setSpeed(homingPayload.homingVelocity.x);
			}
			else
			{
				homingHardware->motorZ->runSpeed();
			}
			break;

        case HomingState::X:
            if(homingHardware->limSwitchX->isTriggered())
            {
                homingHardware->motorX->setCurrentPosition(0);
                homingState = HomingState::Y;
                homingHardware->motorY->setMaxSpeed(homingPayload.homingVelocity.y);
                homingHardware->motorY->setSpeed(homingPayload.homingVelocity.y);
            }
            else
            {
                homingHardware->motorX->runSpeed();
            }
            break;


        case HomingState::Y:
            if(homingHardware->limSwitchY->isTriggered())
            {
                homingHardware->motorY->setCurrentPosition(0);
                homingState = HomingState::Yaw;
            }
            else
            {
                homingHardware->motorY->runSpeed();
            }
            break;


        case HomingState::Yaw:
            homingHardware->motorYaw->setCurrentPosition(0);
            homingState = HomingState::HomingDone;
            break;


        case HomingState::HomingDone:
			currentCommandState = CommandState::Done;
            break;
    }

	return currentCommandState;
}



bool HomeCommand::setPayload(uint8_t* payload, uint16_t payloadSize)
{
    std::lock_guard<std::mutex> lock(commandMutex_);
	bool result = false;

	if(payload != nullptr && payloadSize == sizeof(HomingPayload))
	{
		memcpy(&homingPayload, payload, sizeof(HomingPayload));
		result = true;
	}
	return result;
}

