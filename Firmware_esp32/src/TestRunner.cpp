#include "TestRunner.h"

TestRunner::TestRunner(Controller* ctrl) : ctrl(ctrl)
{
}

bool TestRunner::runTests()
{
    bool pass = true;
    pass &= TEST_MOVE();
    pass &= TEST_PICK();
    pass &= TEST_PLACE();
    pass &= TEST_HOME();
    // add more tests here
    return pass;
}

bool TestRunner::runComTest()
{
	bool pass = true;
    pass &= TEST_communication();
	return pass;
}

/**
 * @brief Integration test for the serial communication protocol between the HMI and the ESP32.
 *
 * This function runs indefinitely on core 1 (via testLoop), in parallel with communicationLoop
 * on core 0. It simulates the behaviour of the real Controller::update() without driving any
 * hardware, allowing the full HMI ↔ ESP32 communication path to be validated without motors or
 * sensors being connected.
 *
 * Behaviour per iteration (every 10 ms):
 *   - Acquires the shared DataModel mutex.
 *   - Forces MachineState to READY so the HMI state machine always sees the machine as available.
 *   - Reads the latest command written by communicationLoop and echoes the requested position
 *     back into the DataModel position field, mimicking instant command completion:
 *       - MOVE / PICK / PLACE : copy requestedPosition → position (simulate reaching setpoint).
 *       - HOME                : reset position to (0, 0, 0, 0) (simulate homing sequence).
 *       - STOP / EMPTY        : no position change, state stays READY.
 *   - Releases the mutex so communicationLoop can read state + position and send the statusFrame
 *     reply back to the HMI.
 *
 * The actual pass/fail verdict of this test is evaluated on the HMI side
 * (test_controller_communication.py), which verifies that the controller reaches DONE state
 * after sending the expected command sequence (MOVE, PICK, PLACE, HOME).
 *
 * @note Serial must NOT be used for debug output inside this function — the same UART port
 *       is used for binary communication with the HMI.
 *
 * @param durationMs How long to run the test loop in milliseconds (default: 15000 ms).
 *                   Should be longer than the HMI-side test timeout (ESP32_TEST_TIMEOUT).
 *                   After this duration the function returns and testLoop goes idle.
 * @return Always returns true. Result is assessed by the HMI.
 */
bool TestRunner::TEST_communication(uint32_t durationMs)
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
				dataModel->position.x = 0.0f;
				dataModel->position.y = 0.0f;
				dataModel->position.z = 0.0f;
				dataModel->position.yaw = 0.0f;
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

bool TestRunner::TEST_MOVE(void)
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

bool TestRunner::TEST_PICK(void)
{
	position_t testPosition;
	testPosition.x = 100;
	testPosition.y = 100;
	testPosition.z = 200;
	testPosition.yaw = 100;
	
	dataModel_t* dataModel = ctrl->dataModel.get();
	dataModel->command.id = CommandId::PICK;
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

	MachineState machineState = MachineState::PICKING;
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

bool TestRunner::TEST_PLACE(void)
{
	position_t testPosition;
	testPosition.x = 100;
	testPosition.y = 100;
	testPosition.z = 200;
	testPosition.yaw = 100;
	
	dataModel_t* dataModel = ctrl->dataModel.get();
	dataModel->command.id = CommandId::PLACE;
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

	MachineState machineState = MachineState::PLACING;
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

bool TestRunner::TEST_HOME(void)
{
	position_t testPosition;
	testPosition.x = 100;
	testPosition.y = 100;
	testPosition.z = 200;
	testPosition.yaw = 100;
	
	dataModel_t* dataModel = ctrl->dataModel.get();
	dataModel->command.id = CommandId::HOME;
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

	MachineState machineState = MachineState::HOMING;
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