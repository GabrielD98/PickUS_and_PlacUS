#include "TestCom.h"

TestCom::TestCom(Controller* ctrl) : ctrl(ctrl)
{
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