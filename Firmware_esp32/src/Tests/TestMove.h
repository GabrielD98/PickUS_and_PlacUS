/**
 * @file testmove.h
 * @author PickusAndPlacus
 * @brief Class to execute a gantry movement test in 3 axes.
 * @version 1.0
 * @date 17/04/2026
 */

#ifndef TESTMOVE_H
#define TESTMOVE_H

#include "../controller.h"

/**
 * @brief Confirms the machine can move the toolhead to a specified location in X, Y, Z and YAW.
 */
class TestMove
{
public:
    /**
     * @brief Instantiate a local controller, independant from the UI.
     */
    TestMove();
    
    /**
     * @brief Targets a test position to go to, then command to move.
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