/**
 * @file testplace.h
 * @author PickusAndPlacus
 * @brief Class to execute a component placing test.
 * @version 1.0
 * @date 17/04/2026
 */

#ifndef TESTPLACE_H
#define TESTPLACE_H

#include "../controller.h"

/**
 * @brief Confirms the machine can activate the valve once the nozzle reaches the board,
 * then go back up and deactivate the pump and the valve.
 */
class TestPlace
{
public:
    /**
     * @brief Instantiate a local controller, independant from the UI.
     */
    TestPlace();

    /**
     * @brief Targets a test position to go to, then commands to place.
     * Updates the machine state at a certain loop count.
     * @return true if passed, else false.
     */
    bool run();
private:
    /**
     * @brief Pointer to local controller.
     */
    Controller* testCtrl;
};

#endif