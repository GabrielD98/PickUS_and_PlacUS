#ifndef TESTRUNNER_H
#define TESTRUNNER_H

#include "Controller.h"
#include "TestMove.h"

class TestRunner {
public:
    explicit TestRunner(Controller* ctrl);
    bool runTests();
    bool runComTest();

private:
    Controller* ctrl;

    bool TEST_communication(uint32_t durationMs = 15000);
    bool TEST_MOVE(void);
    bool TEST_PICK(void);
    bool TEST_PLACE(void);
    bool TEST_HOME(void);
    bool TEST_LIMITS(void);
    bool TEST_GEOMETRY(void);
    // add more tests here
};

#endif