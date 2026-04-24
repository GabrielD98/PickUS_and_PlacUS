#include "testrunner.h"

TestRunner::TestRunner(Controller* ctrl) : ctrl(ctrl), testCom(ctrl)
{
}

bool TestRunner::runTests()
{
    bool pass = true;
	// Unwanted tests are to be put in commentary
	pass &= testLimits.run();
	pass &= testGeometry.run();
	pass &= testMove.run();
	pass &= testPick.run();
	pass &= testPlace.run();
	pass &= testHome.run();
    return pass;
}

bool TestRunner::runComTest()
{
	bool pass = true;
	pass &= testCom.run(15000);
	return pass;
}