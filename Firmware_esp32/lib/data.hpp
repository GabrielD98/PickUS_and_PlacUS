#ifndef DATA_HPP
#define DATA_HPP

#include <stdint.h>

typedef struct __attribute__((packed)) position
{
	float x = 0;
	float y = 0;
	float z = 0;
	float yaw = 0;

}position_t;

typedef struct __attribute__((packed)) velocity
{
	float x = 0;
	float y = 0;
	float z = 0;
	float yaw = 0;

}velocity_t;

enum class CommandId : uint8_t
{
	STOP = 0,
	MOVE = 1,
	PICK = 2, 
	PLACE = 3, 
	HOME = 4, 
	EMPTY = 5
};

enum class MachineState : uint8_t
{
	ERROR = 0,
	READY = 1,
	MOVING = 2,
	PICKING = 3,
	PLACING = 4,
	HOMING = 5,
};

enum class HomingState : uint8_t
{
	INIT = 0,
	X = 1,
	Y = 2,
	Z = 3,
	YAW = 4,
	HOMING_DONE = 5,

};

enum class PickPlaceMode : uint8_t
{
	PICK = 0,
	PLACE = 1,
};

enum class PickPlaceState : uint8_t
{
	INIT = 0,
	GOING_DOWN = 1,
	CONTACT = 2,
	GOING_UP = 3,
	DONE = 4,
};


typedef struct __attribute__((packed)) command
{
	CommandId id;
	float velocity;
	position_t requestedPosition;

}command_t;

typedef struct __attribute__((packed)) statusFrame
{
	MachineState state;
	position_t position;
}statusFrame_t;

static_assert(sizeof(command_t) == 21, "command_t size must remain 21 bytes for protocol compatibility");
static_assert(sizeof(statusFrame_t) == 17, "statusFrame_t size must remain 17 bytes for protocol compatibility");
#endif