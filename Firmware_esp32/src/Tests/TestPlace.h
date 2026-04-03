#ifndef TESTPLACE_H
#define TESTPLACE_H

#include "../Controller.h"

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
     * @brief Targets a test position to go to, then command to place.
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