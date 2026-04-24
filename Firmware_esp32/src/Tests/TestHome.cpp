#include "testhome.h"

TestHome::TestHome()
{
	Controller controller;
	testCtrl = &controller;
}

bool TestHome::run()
{
    positionCartesian_t testPosition;
	testPosition.x = 100;
	testPosition.y = 100;
	testPosition.z = 200;
	testPosition.yaw = 100;
	
	dataModel_t* dataModel = testCtrl->dataModel.get();
	dataModel->command.id = CommandId::HOME;
	dataModel->command.requestedPosition = testPosition;
	dataModel->command.velocityCartesian = 50;
	testCtrl->dataModel.release();
	
	testCtrl->update();

	dataModel = testCtrl->dataModel.get();
	dataModel->command.id = CommandId::EMPTY;
	dataModel->command.requestedPosition = testPosition;
	dataModel->command.velocityCartesian = 50;
	testCtrl->dataModel.release();

	uint8_t loopCount = 0;

	MachineState machineState = MachineState::HOMING;
	while(machineState != MachineState::READY)
	{
		loopCount++;
		if(loopCount == 200)
		{
			dataModel = testCtrl->dataModel.get();
			machineState = dataModel->state;
			testCtrl->dataModel.release();
			loopCount = 0;
		}
		testCtrl->update();
	}
	return true;
}