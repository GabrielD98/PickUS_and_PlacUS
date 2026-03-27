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

class TestRunner {
public:
    explicit TestRunner(Controller* ctrl);
    bool runTests();
    bool runComTest();

private:
    Controller* ctrl;

    bool TEST_communication(uint32_t durationMs);
    bool TEST_MOVE(void);
    bool TEST_PICK(void);
    bool TEST_PLACE(void);
    bool TEST_HOME(void);
    bool TEST_LIMITS(void);
    bool TEST_GEOMETRY(void);
};

#endif