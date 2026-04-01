#include "Geometry.h"

positionCartesian_t dimensionLimits(positionCartesian_t targetPosition)
{
    if (targetPosition.x > P_X_MAX){
        targetPosition.x = P_X_MAX;}
    if (targetPosition.x < P_X_MIN){
        targetPosition.x = P_X_MIN;}

    if (targetPosition.y > P_Y_MAX){
        targetPosition.y = P_Y_MAX;}
    if (targetPosition.y < P_Y_MIN){
        targetPosition.y = P_Y_MIN;}

    if (targetPosition.z > P_Z_MAX){
        targetPosition.z = P_Z_MAX;}
    if (targetPosition.z < P_Z_MIN){
        targetPosition.z = P_Z_MIN;}

    if (targetPosition.yaw > P_YAW_MAX){
        targetPosition.yaw = P_YAW_MAX;}
    if (targetPosition.yaw < P_YAW_MIN){
        targetPosition.yaw = P_YAW_MIN;}

    return targetPosition;
}


positionStep_t coordToStep(positionCartesian_t positionCartesian)
{
    positionCartesian_t constrainedPosition = dimensionLimits(positionCartesian);

    positionStep_t positionStep;
    
    positionStep.x = round((constrainedPosition.x*STEPS_REVOLUTION*MICROSTEPPING_X)/MM_REVOLUTION);
    positionStep.y = round((constrainedPosition.y*STEPS_REVOLUTION*MICROSTEPPING_Y)/MM_REVOLUTION);
    positionStep.z = round((MICROSTEPPING_Z*STEPS_REVOLUTION*acos(1 + constrainedPosition.z/CAM_RADIUS))/(2*PI));
    positionStep.yaw = round((constrainedPosition.yaw*STEPS_REVOLUTION*MICROSTEPPING_YAW)/360);

    return positionStep;
}


positionCartesian_t stepToCoord(positionStep_t positionStep)
{
    positionCartesian_t positionCartesian;

    positionCartesian.x = (positionStep.x*MM_REVOLUTION)/float(STEPS_REVOLUTION*MICROSTEPPING_X); // mm
    positionCartesian.y = (positionStep.y*MM_REVOLUTION)/float(STEPS_REVOLUTION*MICROSTEPPING_Y); // mm
    positionCartesian.z = CAM_RADIUS*(cos((positionStep.z*2.0*PI)/float(STEPS_REVOLUTION*MICROSTEPPING_Z)) - 1.0); // mm
    positionCartesian.yaw = (positionStep.yaw*360)/(STEPS_REVOLUTION*MICROSTEPPING_YAW); // degrees

    return positionCartesian;
}


velocityStep_t velocityToStep(float velocityCartesian)
{
    velocityStep_t stepsPerSec;
    const float speedAbs = fmin(fabs(velocityCartesian), SPEED_MAX);
    
    stepsPerSec.x = round((speedAbs*STEPS_REVOLUTION*MICROSTEPPING_X)/MM_REVOLUTION);
    stepsPerSec.y = round((speedAbs*STEPS_REVOLUTION*MICROSTEPPING_Y)/MM_REVOLUTION);
    // Z has a nonlinear cam profile; using an average mm->steps velocity mapping instead.
    stepsPerSec.z = round((speedAbs*STEPS_REVOLUTION*MICROSTEPPING_Z)/(4.0*CAM_RADIUS));
    stepsPerSec.yaw = round((speedAbs*STEPS_REVOLUTION*MICROSTEPPING_YAW)/360);

    return stepsPerSec;
}