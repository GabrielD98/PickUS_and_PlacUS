/**
 * @file data.hpp
 * @author PickusAndPlacus
 * @brief Generally used struct and enum throughout the code.
 * @version 1.0
 * @date 17/04/2026
 */

#ifndef DATA_HPP
#define DATA_HPP

#include <stdint.h>

/**
 * @brief Contains coordinates of the X, Y and Z-axis, as well as an orientation in YAW.
 * All values are expressed in steps.
 * @return 
 */
typedef struct __attribute__((packed)) positionStep
{
	float x		=	0;
	float y		=	0;
	float z		=	0;
	float yaw	=	0;

}positionStep_t;


/**
 * @brief Contains coordinates of the X, Y and Z-axis, as well as an orientation in YAW.
 * X, Y and Z-axis are given in millimeters. Yaw is given in degree.
 * @return 
 */
typedef struct __attribute__((packed)) positionCartesian
{
	float x		=	0;
	float y		=	0;
	float z		=	0;
	float yaw	=	0;

}positionCartesian_t;


/**
 * @brief Contains motor speeds of the X, Y, Z and YAW-axis motors.
 * Values are given in step/s.
 * @return 
 */
typedef struct __attribute__((packed)) velocityStep
{
	float x		=	0;
	float y		=	0;
	float z		=	0;
	float yaw	=	0;

}velocityStep_t;


/**
 * @brief Contains toolhead translation speeds on the X, Y and Z-axis, as well as rotation speed in YAW.
 * Speeds in X, Y and Z are in millimeter/second, 
 * @return 
 */
typedef struct __attribute__((packed)) velocityCartesian
{
	float x		=	0;
	float y		=	0;
	float z		=	0;
	float yaw	=	0;

}velocityCartesian_t;


/**
 * @brief Lists all interface command id recognizable by the controller.
 */
enum class CommandId : uint8_t
{
	STOP	=	0,
	MOVE	=	1,
	PICK	=	2, 
	PLACE	=	3, 
	HOME	=	4, 
	EMPTY	=	5
};


/**
 * @brief Lists all machine states recognizable by the interface.
 */
enum class MachineState : uint8_t
{
	ERROR		=	0,
	READY		=	1,
	MOVING		=	2,
	PICKING		=	3,
	PLACING		=	4,
	HOMING		=	5
};


/**
 * @brief Lists all states required to home the machine.
 */
enum class HomingState : uint8_t
{
	INIT		=	0,
	X			=	1,
	Y			=	2,
	Z			=	3,
	YAW			=	4,
	HOMING_DONE	=	5
};


/**
 * @brief Specify if the machine is in the process of picking or placing.
 */
enum class PickPlaceMode : uint8_t
{
	PICK	=	0,
	PLACE	=	1
};


/**
 * @brief Lists all states required for the picking or the placing of a component.
 */
enum class PickPlaceState : uint8_t
{
	INIT		=	0,
	GOING_DOWN	=	1,
	CONTACT		=	2,
	DONE		=	3
};


/**
 * @brief Lists every parameters to define a command from the interface to the controller.
 * @return 
 */
typedef struct __attribute__((packed)) command
{
	CommandId id;
	float velocityCartesian;
	positionCartesian_t requestedPosition;

}command_t;


/**
 * @brief Lists every parameters to define a status from the controller to the interface.
 * @return  
 */
typedef struct __attribute__((packed)) statusFrame
{
	MachineState state;
	positionCartesian_t position;

}statusFrame_t;


static_assert(sizeof(command_t) == 21, "command_t size must remain 21 bytes for protocol compatibility");
static_assert(sizeof(statusFrame_t) == 17, "statusFrame_t size must remain 17 bytes for protocol compatibility");

#endif