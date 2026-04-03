#ifndef TESTRUNNER_H
#define TESTRUNNER_H

#include "../Controller.h"
#include "TestCom.h"
#include "TestMove.h"
#include "TestPick.h"
#include "TestPlace.h"
#include "TestHome.h"
#include "TestLimits.h"
#include "TestGeometry.h"

/**
 * @brief Manage tests of every software features on the ESP.
 */
class TestRunner {
public:
    /**
     * @brief Associates the controller in main() to the TestRunner object in order to allow communication testing.
     * 
     * @param ctrl Pointer to the controller instanciated in main().
     */
    explicit TestRunner(Controller* ctrl);

    /**
     * @brief Verify the execution of every contained tests as long as the previous test was a success.
     * 
     * @return true if all test succeeded.
     * @return false if one test failed.
     */
    bool runTests();

    /**
     * @brief Verify if the communication test execution was a success.
     * 
     * @return true if the test passed, else false.
     */
    bool runComTest();

private:
    /**
     * @brief Pointer to the controller instanciated in main() in order to allow communication with UI.
     */
    Controller* ctrl;

    /**
     * @brief Executes the communication testing.
     * 
     * @param durationMs Time limit to perform the test.
     * @return true if passed, else false.
     */
    bool TEST_communication(uint32_t durationMs);

    /**
     * @brief Executes the test for each controller features.
     * 
     * @return true if passed, else false.
     */
    bool TEST_MOVE(void);
    bool TEST_PICK(void);
    bool TEST_PLACE(void);
    bool TEST_HOME(void);
    bool TEST_LIMITS(void);
    bool TEST_GEOMETRY(void);
};

#endif