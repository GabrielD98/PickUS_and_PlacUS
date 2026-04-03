/**
 * @file testmove.h
 * @author PickusAndPlacus
 * @brief 
 * @version
 * @date
 */

#ifndef TESTMOVE_H
#define TESTMOVE_H

#include "../Controller.h"

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