#ifndef TESTRUNNER_H
#define TESTRUNNER_H

#include "Controller.h"

class TestRunner {
public:
    explicit TestRunner(Controller* ctrl);
    bool runTests();

private:
    Controller* ctrl;

    bool TEST_communication(uint32_t durationMs = 15000);
    // add more tests here
};

#endif