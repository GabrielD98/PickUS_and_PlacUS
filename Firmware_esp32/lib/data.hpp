#include <stdint.h>

typedef struct Position
{
	float x = 0;
	float y = 0;
	float z = 0;
	float yaw = 0;

}position_t;

enum class CommandId
{
	STOP = 0,
	MOVE = 1,
	PICK = 2, 
	PLACE = 3, 
	HOME = 4, 
	EMPTY = 5,   
};

enum class MachineState
{
	ERROR = 0,
	READY = 1,
	MOVING = 2,
	PICKING = 3,
	PLACING = 4,
	DISCONNECTED = 5, 
};

typedef struct __attribute__((packed)) Command
{
	CommandId id;
	float velocity;
	position_t requestedPosition;

}command_t;