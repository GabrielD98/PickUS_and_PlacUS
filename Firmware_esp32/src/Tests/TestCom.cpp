#include "TestCom.h"

TestCom::TestCom(Controller* ctrl) : ctrl(ctrl)
{
}

bool TestCom::run(uint32_t durationMs = 15000)
{
    uint32_t startTime = millis();
	while(millis() - startTime < durationMs) {
		dataModel_t* dataModel = ctrl->dataModel.get();
		CommandId currentCommand = dataModel->command.id;
		
		// Always ensure machine is in READY state for the test
		dataModel->state = MachineState::READY;
		
		switch (currentCommand) {
			case CommandId::MOVE:
				dataModel->position.x = dataModel->command.requestedPosition.x;
				dataModel->position.y = dataModel->command.requestedPosition.y;
				dataModel->position.z = dataModel->command.requestedPosition.z;
				dataModel->position.yaw = dataModel->command.requestedPosition.yaw;
				break;
				
			case CommandId::PICK:
				dataModel->position.x = dataModel->command.requestedPosition.x;
				dataModel->position.y = dataModel->command.requestedPosition.y;
				dataModel->position.z = dataModel->command.requestedPosition.z;
				dataModel->position.yaw = dataModel->command.requestedPosition.yaw;
				break;
				
			case CommandId::PLACE:
				dataModel->position.x = dataModel->command.requestedPosition.x;
				dataModel->position.y = dataModel->command.requestedPosition.y;
				dataModel->position.z = dataModel->command.requestedPosition.z;
				dataModel->position.yaw = dataModel->command.requestedPosition.yaw;
				break;
				
			case CommandId::HOME:
				dataModel->position.x = 0.0;
				dataModel->position.y = 0.0;
				dataModel->position.z = 0.0;
				dataModel->position.yaw = 0.0;
				break;
				
			case CommandId::STOP:
				break;
				
			case CommandId::EMPTY:
				break;
				
			default:
				break;
		}
		
		ctrl->dataModel.release();
		vTaskDelay(10);
	}
	
	return true;
}