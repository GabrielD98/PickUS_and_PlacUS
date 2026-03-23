#include "TestLimits.h"

TestLimits::TestLimits()
{
}

bool TestLimits::run()
{
    bool result = false;
	
	position_t testPosition; 
	testPosition.x = 100;
	testPosition.y = 330.0;
	testPosition.z = 20.0;
	testPosition.yaw = -180.0;

	position_t stepsPosition = dimensionLimits(testPosition);

	Serial.println(stepsPosition.x);
	Serial.println(stepsPosition.y);
	Serial.println(stepsPosition.z);
	Serial.println(stepsPosition.yaw);

	if (stepsPosition.x == 100.0 || stepsPosition.y == P_Y_MAX ||
		stepsPosition.z == P_Z_MAX || stepsPosition.yaw == P_Y_MIN)
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