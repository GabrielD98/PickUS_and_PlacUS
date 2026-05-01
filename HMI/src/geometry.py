from dataclasses import dataclass
from math import fabs

from data import Position


# Physical travel limits of the machine.
P_X_MAX = 304.80
P_X_MIN = 0.0
P_Y_MAX = 306.39
P_Y_MIN = 0.0
P_Z_MAX = 0.0
P_Z_MIN = -24.0

SPEED_MAX = 1000.0

# Mechanical properties used for step conversion.
STEPS_REVOLUTION = 200
MM_REVOLUTION = 40.0

# Microstepping resolution.
MICROSTEPPING_X = 16
MICROSTEPPING_Y = 16
MICROSTEPPING_Z = 4
MICROSTEPPING_YAW = 4


@dataclass(frozen=True)
class StepPosition:
    x: int = 0
    y: int = 0
    z: int = 0
    yaw: int = 0


@dataclass(frozen=True)
class StepVelocity:
    x: int = 0
    y: int = 0
    z: int = 0
    yaw: int = 0


def dimension_limits(target_position: Position) -> Position:
    """Clamp a cartesian position to the machine workspace."""
    x = min(max(target_position.x, P_X_MIN), P_X_MAX)
    y = min(max(target_position.y, P_Y_MIN), P_Y_MAX)
    z = min(max(target_position.z, P_Z_MIN), P_Z_MAX)
    return Position(x, y, z, target_position.yaw)


def coord_to_step(position_cartesian: Position) -> StepPosition:
    """Convert cartesian coordinates in mm/degrees to motor steps."""
    constrained_position = dimension_limits(position_cartesian)
    return StepPosition(
        x=round((constrained_position.x * STEPS_REVOLUTION * MICROSTEPPING_X) / MM_REVOLUTION),
        y=round((constrained_position.y * STEPS_REVOLUTION * MICROSTEPPING_Y) / MM_REVOLUTION),
        z=round((constrained_position.z * STEPS_REVOLUTION * MICROSTEPPING_Z) / MM_REVOLUTION),
        yaw=round((constrained_position.yaw * STEPS_REVOLUTION * MICROSTEPPING_YAW) / 360.0),
    )


def step_to_coord(position_step: StepPosition) -> Position:
    """Convert motor steps back to cartesian coordinates."""
    return Position(
        x=(position_step.x * MM_REVOLUTION) / float(STEPS_REVOLUTION * MICROSTEPPING_X),
        y=(position_step.y * MM_REVOLUTION) / float(STEPS_REVOLUTION * MICROSTEPPING_Y),
        z=(position_step.z * MM_REVOLUTION) / float(STEPS_REVOLUTION * MICROSTEPPING_Z),
        yaw=(position_step.yaw * 360.0) / float(STEPS_REVOLUTION * MICROSTEPPING_YAW),
    )


def velocity_to_step(velocity_cartesian: float) -> StepVelocity:
    """Convert a cartesian velocity in mm/s to motor steps/s."""
    speed_abs = min(fabs(velocity_cartesian), SPEED_MAX)
    return StepVelocity(
        x=round((speed_abs * STEPS_REVOLUTION * MICROSTEPPING_X) / MM_REVOLUTION),
        y=round((speed_abs * STEPS_REVOLUTION * MICROSTEPPING_Y) / MM_REVOLUTION),
        z=round((speed_abs * STEPS_REVOLUTION * MICROSTEPPING_Z) / MM_REVOLUTION),
        yaw=round((speed_abs * STEPS_REVOLUTION * MICROSTEPPING_YAW) / 360.0),
    )