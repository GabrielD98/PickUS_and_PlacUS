#include "TestGeometry.h"

TestGeometry::TestGeometry()
{
}

bool TestGeometry::run()
{
    bool result = true;

	position_t testPosition; 
	testPosition.x = 100;
	testPosition.y = 200;
	testPosition.z = -20;
	testPosition.yaw = 180;

	position_t stepsPosition = coordToStep(testPosition);

	position_t mmPosition = stepToCoord(stepsPosition);

	// Thresholds are given from a single motor step, converted in their output unit (Millimeters for x, y, z ; Degrees for yaw)
	float Threshold_x = MM_REVOLUTION/(STEPS_REVOLUTION*MICROSTEPPING_X);
	float Threshold_y = MM_REVOLUTION/(STEPS_REVOLUTION*MICROSTEPPING_Y);
	float Threshold_z = abs(CAM_RADIUS*(cos((STEPS_REVOLUTION*MICROSTEPPING_Z/4.0 - 1)*2.0*PI/float(STEPS_REVOLUTION*MICROSTEPPING_Z)))); // Greatest jump in the z axis for a single step
	float Threshold_yaw = 360/(STEPS_REVOLUTION*MICROSTEPPING_YAW);
	
	if ((mmPosition.x < testPosition.x - Threshold_x || mmPosition.x > testPosition.x + Threshold_x))
	{
		result = false;
		Serial.println("Error on x position.");
	}
	if ((mmPosition.y < testPosition.y - Threshold_y || mmPosition.y > testPosition.y + Threshold_y))
	{
		result = false;
		Serial.println("Error on y position.");
	}
	if ((mmPosition.z < testPosition.z - Threshold_z || mmPosition.z > testPosition.z + Threshold_z))
	{
		result = false;
		Serial.println("Error on z position.");
	}
	if ((mmPosition.yaw < testPosition.yaw - Threshold_yaw || mmPosition.yaw > testPosition.yaw + Threshold_yaw))
	{
		result = false;
		Serial.println("Error on yaw position.");
	}

	if(result)
	{
		Serial.println("GEOMETRY PASSED");
	}
	else
	{
		Serial.println("GEOMETRY FAILED");
	}

	return result;
}