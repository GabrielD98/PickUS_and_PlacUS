/**
 * @file testcom.h
 * @author PickusAndPlacus
 * @brief Class to execute a communication test between the UI and the controller.
 * @version 1.0
 * @date 17/04/2026
 */

#ifndef TESTCOM_H
#define TESTCOM_H

#include "../Controller.h"

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
class TestCom
{
public:
    TestCom(Controller* ctrl);
    bool run(uint32_t durationMs);

private:
    Controller* ctrl;
};

#endif