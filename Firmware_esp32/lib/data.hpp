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
	DISCONNECTED = 5
};

typedef struct Command
{
	CommandId id;
	float velocity;
	position_t requestedPosition;

}command_t;

#endif