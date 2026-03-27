#ifndef TESTPICK_H
#define TESTPICK_H

#include "../Controller.h"

/**
 * @brief Confirms the machine can activate the pump before descending to the board, releases the valve once the nozzle reaches the board,
 * then go back up once a sufficient vaccum is attained.
 */
class TestPick
{
public:
    /**
     * @brief Instantiate a local controller, independant from the UI.
     */
    TestPick();

    /**
     * @brief Targets a test position to go to, then command to pick.
     * Updates the machine state at a certain loop count.
     * 
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