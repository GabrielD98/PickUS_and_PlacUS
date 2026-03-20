#include "TestMove.h"

TestMove::TestMove()
{
}

bool TestMove::runTest()
{
    position_t testPosition;
	testPosition.x = 100;
	testPosition.y = 100;
	testPosition.z = 100;
	testPosition.yaw = 100;

	dataModel_t* dataModel = ctrl->dataModel.get();
	dataModel->command.id = CommandId::MOVE;
	dataModel->command.requestedPosition = testPosition;
	dataModel->command.velocity = 200;
	ctrl->dataModel.release();

	ctrl->update();

	dataModel = ctrl->dataModel.get();
	dataModel->command.id = CommandId::EMPTY;
	dataModel->command.requestedPosition = testPosition;
	dataModel->command.velocity = 200;
	ctrl->dataModel.release();

	uint8_t loopCount = 0;

	MachineState machineState = MachineState::MOVING;
	while(machineState != MachineState::READY)
	{
		loopCount++;
		if(loopCount == 200)
		{
			dataModel = ctrl->dataModel.get();
			machineState = dataModel->state;
			ctrl->dataModel.release();
			loopCount = 0;
		}
		ctrl->update();
	}
	return true;
}