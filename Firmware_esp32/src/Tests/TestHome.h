#ifndef TESTHOME_H
#define TESTHOME_H

#include "../Controller.h"

/**
 * @brief Confirms the machine moves towards the origin corner until it reaches a limit switch,
 * one degree of freedom at a time.
 */
class TestHome
{
public:
    /**
     * @brief Instantiate a local controller, independant from the UI.
     */
    TestHome();

    /**
     * @brief Targets a test position to go to, then commands to home.
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