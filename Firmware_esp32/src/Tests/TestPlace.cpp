#include "TestPlace.h"

TestPlace::TestPlace()
{
	Controller controller;
	testCtrl = &controller;
}

bool TestPlace::run()
{
    position_t testPosition;
	testPosition.x = 100;
	testPosition.y = 100;
	testPosition.z = 200;
	testPosition.yaw = 100;
	
	dataModel_t* dataModel = testCtrl->dataModel.get();
	dataModel->command.id = CommandId::PLACE;
	dataModel->command.requestedPosition = testPosition;
	dataModel->command.velocity = 200;
	testCtrl->dataModel.release();
	
	testCtrl->update();

	dataModel = testCtrl->dataModel.get();
	dataModel->command.id = CommandId::EMPTY;
	dataModel->command.requestedPosition = testPosition;
	dataModel->command.velocity = 200;
	testCtrl->dataModel.release();

	uint8_t loopCount = 0;

	MachineState machineState = MachineState::PLACING;
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