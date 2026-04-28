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
 */
typedef struct __attribute__((packed)) positionStep
{
	long x		=	0;
	long y		=	0;
	long z		=	0;
	long yaw	=	0;

}positionStep_t;


/**
 * @brief Contains motor speeds of the X, Y, Z and YAW-axis motors.
 * Values are given in step/s.
 */
typedef struct __attribute__((packed)) velocityStep
{
	int16_t x		=	0;
	int16_t y		=	0;
	int16_t z		=	0;
	int16_t yaw	=	0;

}velocityStep_t;

/**
 * @brief Lists all interface command id recognizable by the controller.
 */
enum class CommandId : uint8_t
{
	Stop,
	Pause,
	Move,
	Pick,
	Place,
	Home
};


/**
 * @brief Lists all machine states recognizable by the interface.
 */
enum class MachineState : uint8_t
{
	Error,
	Ready,
	Running

};

#endif