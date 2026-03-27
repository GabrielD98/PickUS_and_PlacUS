#include "Geometry.h"

position_t dimensionLimits(position_t targetPosition)
{
    if (targetPosition.x > P_X_MAX)
    {
        targetPosition.x = P_X_MAX;
    }
    if (targetPosition.x < P_X_MIN)
    {
        targetPosition.x = P_X_MIN;
    }
    if (targetPosition.y > P_Y_MAX)
    {
        targetPosition.y = P_Y_MAX;
    }
    if (targetPosition.y < P_Y_MIN)
    {
        targetPosition.y = P_Y_MIN;
    }
    if (targetPosition.z > P_Z_MAX)
    {
        targetPosition.z = P_Z_MAX;
    }
    if (targetPosition.z < P_Z_MIN)
    {
        targetPosition.z = P_Z_MIN;
    }
    if (targetPosition.yaw > P_YAW_MAX)
    {
        targetPosition.yaw = P_YAW_MAX;
    }
    if (targetPosition.yaw < P_YAW_MIN)
    {
        targetPosition.yaw = P_YAW_MIN;
    }

    return targetPosition;
}

position_t coordToStep(position_t distance)
{
    position_t constrainedPosition = dimensionLimits(distance);

    position_t steps;
    
    steps.x = round((constrainedPosition.x*STEPS_REVOLUTION*MICROSTEPPING_X)/MM_REVOLUTION);
    steps.y = round((constrainedPosition.y*STEPS_REVOLUTION*MICROSTEPPING_Y)/MM_REVOLUTION);
    steps.z = round((constrainedPosition.z*STEPS_REVOLUTION*MICROSTEPPING_Z)/MM_REVOLUTION);
    steps.yaw = round((constrainedPosition.yaw*STEPS_REVOLUTION*MICROSTEPPING_YAW)/360);


    return steps;
}

position_t stepToCoord(position_t steps)
{
    position_t distance;

    distance.x = (steps.x*MM_REVOLUTION)/float(STEPS_REVOLUTION*MICROSTEPPING_X);
    distance.y = (steps.y*MM_REVOLUTION)/float(STEPS_REVOLUTION*MICROSTEPPING_Y);
    distance.z = (steps.z*MM_REVOLUTION)/float(STEPS_REVOLUTION*MICROSTEPPING_Z);
    distance.yaw = (steps.yaw*360)/(STEPS_REVOLUTION*MICROSTEPPING_YAW);

    return distance;
}

velocity_t velocityToStep(float velocity)
{
    velocity_t stepsPerSec;
    const float speedAbs = fmin(fabs(velocity), SPEED_MAX);
    
    stepsPerSec.x = round((speedAbs*STEPS_REVOLUTION*MICROSTEPPING_X)/MM_REVOLUTION);
    stepsPerSec.y = round((speedAbs*STEPS_REVOLUTION*MICROSTEPPING_Y)/MM_REVOLUTION);
    stepsPerSec.z = round((speedAbs*STEPS_REVOLUTION*MICROSTEPPING_Z)/MM_REVOLUTION);
    stepsPerSec.yaw = round((speedAbs*STEPS_REVOLUTION*MICROSTEPPING_YAW)/360);


    return stepsPerSec;
}