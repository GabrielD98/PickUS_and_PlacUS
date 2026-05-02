/**
 * @file testrunner.h
 * @author PickusAndPlacus
 * @brief Class to manage integration tests on the ESP.
 * @version 1.0
 * @date 17/04/2026
 */

#ifndef TESTRUNNER_H
#define TESTRUNNER_H

#include "../controller.h"

/**
 * @brief Manage tests of every software features on the ESP.
 */
class TestRunner {
public:
    /**
     * @brief Associates the controller in main() to the TestRunner object in order to allow communication testing.
     * @param ctrl Pointer to the controller instanciated in main().
     */
    explicit TestRunner(Controller* ctrl);

    /**
     * @brief Verify the execution of every contained tests as long as the previous test was a success.
     * @return true if all test succeeded.
     * @return false if one test failed.
     */
    bool runTests();

    /**
     * @brief Verify if the communication test execution was a success.
     * @return true if the test passed, else false.
     */
    bool runComTest();

private:
    /**
     * @brief Pointer to the controller instanciated in main() in order to allow communication with UI.
     */
    Controller* ctrl;
};

#endif