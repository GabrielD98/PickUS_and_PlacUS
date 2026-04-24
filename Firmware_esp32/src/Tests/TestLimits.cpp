#include "testlimits.h"

TestLimits::TestLimits()
{
}

bool TestLimits::run()
{
    bool result = false;
	
	positionCartesian_t testPosition; 
	testPosition.x = -100;
	testPosition.y = 330.0;
	testPosition.z = 20.0;
	testPosition.yaw = -180.0;

	testPosition = dimensionLimits(testPosition);

	Serial.println(testPosition.x);
	Serial.println(testPosition.y);
	Serial.println(testPosition.z);
	Serial.println(testPosition.yaw);

	if (testPosition.x == P_X_MIN || testPosition.y == P_Y_MAX ||
		testPosition.z == P_Z_MAX || testPosition.yaw == P_Y_MIN)
	{
		result = true;
	}

	if(result)
	{
		Serial.println("PHYSICAL LIMIT PASSED");
	}
	else
	{
		Serial.println("PHYSICAL LIMIT FAILED");
	}

	return result;
}