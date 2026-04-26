#include <cstring>
#include "MoveCommand.h"

MoveCommand::MoveCommand(MovingHardware* movingHardware)
	: movingHardware(movingHardware)
{
	movingPayload = {};
}

MoveCommand::~MoveCommand()
{
}

void MoveCommand::prepare()
{
    long target[4] =
    {
        movingPayload.targetPosition.x,
        movingPayload.targetPosition.y,
        movingPayload.targetPosition.z,
        movingPayload.targetPosition.yaw

    };

    movingHardware->motorX->setMaxSpeed(movingPayload.velocity.x);
    movingHardware->motorY->setMaxSpeed(movingPayload.velocity.y);
    movingHardware->motorZ->setMaxSpeed(movingPayload.velocity.z);
    movingHardware->motorYaw->setMaxSpeed(movingPayload.velocity.yaw);
    
    // Assign targets to their axis corresponding AccelStepper object through MultiStepper
    movingHardware->motorSystem->moveTo(target);
}

CommandState MoveCommand::run()
{
    CommandState currentCommandState = CommandState::InProgress; 

    if(!movingHardware->motorSystem->run())
    {
        currentCommandState = CommandState::Done;
    }
	return currentCommandState;
}

void MoveCommand::reset()
{
}

bool MoveCommand::setPayload(uint8_t* payload, uint16_t payloadSize)
{
	bool result = false;

	if(payload != nullptr && payloadSize == sizeof(MovingPayload))
	{
		memcpy(&movingPayload, payload, sizeof(MovingPayload));
		result = true;
	}
	return result;
}
