#include "TestRunner.h"

TestRunner::TestRunner(Controller* ctrl) : ctrl(ctrl)
{
}

bool TestRunner::runTests()
{
    bool pass = true;
	pass &= TEST_LIMITS();
	pass &= TEST_GEOMETRY();
    pass &= TEST_MOVE();
    pass &= TEST_PICK();
    pass &= TEST_PLACE();
    pass &= TEST_HOME();
    return pass;
}

bool TestRunner::runComTest()
{
	bool pass = true;
    pass &= TEST_communication(15000);
	return pass;
}

bool TestRunner::TEST_communication(uint32_t durationMs)
{
	TestCom testCom(ctrl);
	return testCom.run(durationMs);
}

bool TestRunner::TEST_MOVE(void)
{
	TestMove testMove;
	return testMove.run();
}

bool TestRunner::TEST_PICK(void)
{
	TestPick testPick;
	return testPick.run();
}

bool TestRunner::TEST_PLACE(void)
{
	TestPlace testPlace;
	return testPlace.run();
}

bool TestRunner::TEST_HOME(void)
{
	TestHome testHome;
	return testHome.run();
}

bool TestRunner::TEST_LIMITS(void)
{
	TestLimits testLimits;
	return testLimits.run();
}

bool TestRunner::TEST_GEOMETRY(void)
{
	TestGeometry testGeometry;
	return testGeometry.run();
}