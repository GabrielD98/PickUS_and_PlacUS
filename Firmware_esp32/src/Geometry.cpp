#include "Geometry.h"


Position dimensionLimits(Position targetPosition)
{
    if (targetPosition.x > P_LIM_X)
    {
        targetPosition.x = P_LIM_X;
    }
    if (targetPosition.y > P_LIM_Y)
    {
        targetPosition.y = P_LIM_Y;
    }
    if (targetPosition.z > P_LIM_Z)
    {
        targetPosition.z = P_LIM_Z;
    }
    if (targetPosition.yaw > P_LIM_YAW)
    {
        targetPosition.yaw = P_LIM_YAW;
    }
    return targetPosition;
}

Position mmToStep(Position distance)
{
    Position steps;
    dimensionLimits(distance);

    steps.x = round((distance.x*STEPS_REVOLUTION*MICROSTEPPING_X)/MM_REVOLUTION);
    steps.y = round((distance.y*STEPS_REVOLUTION*MICROSTEPPING_Y)/MM_REVOLUTION);

    //Beaucoup de questionnement sur cette formule je ne suis pas sure que ce soit bon
    steps.z = round((MICROSTEPPING_Z*STEPS_REVOLUTION*acos(1 - distance.z/CAME_DIAMETER))/2*PI);

    steps.yaw = round((distance.yaw*STEPS_REVOLUTION*MICROSTEPPING_YAW)/360);

    return steps;
}

Position stepToMm(Position steps)
{
    Position distance;

    distance.x = round((steps.x*MM_REVOLUTION)/(STEPS_REVOLUTION*MICROSTEPPING_X));
    distance.y = round((steps.y*MM_REVOLUTION)/(STEPS_REVOLUTION*MICROSTEPPING_Y));

    //Beaucoup de questionnement sur cette formule je ne suis pas sure que ce soit bon
    distance.z = round(CAME_DIAMETER*(1 - cos((steps.z*2*PI)/(STEPS_REVOLUTION*MICROSTEPPING_Z))));

    distance.yaw = round((steps.yaw*360)/(STEPS_REVOLUTION*MICROSTEPPING_YAW));

    return steps;
}


