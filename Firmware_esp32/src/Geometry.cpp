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

position_t mmToStep(position_t distance)
{
    position_t constrainedPosition = dimensionLimits(distance);

    position_t steps;
    
    steps.x = round((constrainedPosition.x*STEPS_REVOLUTION*MICROSTEPPING_X)/MM_REVOLUTION);
    steps.y = round((constrainedPosition.y*STEPS_REVOLUTION*MICROSTEPPING_Y)/MM_REVOLUTION);
    steps.z = round((MICROSTEPPING_Z*STEPS_REVOLUTION*acos(1 + constrainedPosition.z/CAM_DIAMETER))/(2*PI));
    steps.yaw = round((constrainedPosition.yaw*STEPS_REVOLUTION*MICROSTEPPING_YAW)/360);


    return steps;
}

position_t stepToMm(position_t steps)
{
    position_t distance;

    distance.x = (steps.x*MM_REVOLUTION)/float(STEPS_REVOLUTION*MICROSTEPPING_X);
    distance.y = (steps.y*MM_REVOLUTION)/float(STEPS_REVOLUTION*MICROSTEPPING_Y);
    distance.z = CAM_DIAMETER*(cos((steps.z*2.0*PI)/float(STEPS_REVOLUTION*MICROSTEPPING_Z)) - 1.0);
    distance.yaw = (steps.yaw*360)/(STEPS_REVOLUTION*MICROSTEPPING_YAW);

    return distance;
}


