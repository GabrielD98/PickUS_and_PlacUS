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


@dataclass(frozen=True)
class CartesianVelocity:
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0
    yaw: float = 0.0

    @classmethod
    def uniform(cls, speed: float) -> "CartesianVelocity":
        return cls(speed, speed, speed, speed)


def dimensionLimits(targetPosition: Position) -> Position:
    """Clamp a cartesian position to the machine workspace."""
    x = min(max(targetPosition.x, P_X_MIN), P_X_MAX)
    y = min(max(targetPosition.y, P_Y_MIN), P_Y_MAX)
    z = min(max(targetPosition.z, P_Z_MIN), P_Z_MAX)
    return Position(x, y, z, targetPosition.yaw)


def coordToStep(positionCartesian: Position) -> StepPosition:
    """Convert cartesian coordinates in mm/degrees to motor steps."""
    constrainedPosition = dimensionLimits(positionCartesian)
    return StepPosition(
        x=round((constrainedPosition.x * STEPS_REVOLUTION * MICROSTEPPING_X) / MM_REVOLUTION),
        y=round((constrainedPosition.y * STEPS_REVOLUTION * MICROSTEPPING_Y) / MM_REVOLUTION),
        z=round((constrainedPosition.z * STEPS_REVOLUTION * MICROSTEPPING_Z) / MM_REVOLUTION),
        yaw=round((constrainedPosition.yaw * STEPS_REVOLUTION * MICROSTEPPING_YAW) / 360.0),
    )


def stepToCoord(positionStep: StepPosition) -> Position:
    """Convert motor steps back to cartesian coordinates."""
    return Position(
        x=(positionStep.x * MM_REVOLUTION) / float(STEPS_REVOLUTION * MICROSTEPPING_X),
        y=(positionStep.y * MM_REVOLUTION) / float(STEPS_REVOLUTION * MICROSTEPPING_Y),
        z=(positionStep.z * MM_REVOLUTION) / float(STEPS_REVOLUTION * MICROSTEPPING_Z),
        yaw=(positionStep.yaw * 360.0) / float(STEPS_REVOLUTION * MICROSTEPPING_YAW),
    )


def velocityToStep(velocityCartesian: CartesianVelocity | float) -> StepVelocity:
    """Convert a cartesian velocity in mm/s to motor steps/s. Preserves sign for direction control."""
    if isinstance(velocityCartesian, (int, float)):
        velocityCartesian = CartesianVelocity.uniform(float(velocityCartesian))

    def signedStepVelocity(v: float, stepsRev: int, microstepping: int, mmRev: float) -> int:
        """Convert velocity to steps, preserving sign for direction."""
        sign = 1 if v >= 0 else -1
        absV = fabs(v)
        cappedV = min(absV, SPEED_MAX)
        return sign * round((cappedV * stepsRev * microstepping) / mmRev)

    return StepVelocity(
        x=signedStepVelocity(velocityCartesian.x, STEPS_REVOLUTION, MICROSTEPPING_X, MM_REVOLUTION),
        y=signedStepVelocity(velocityCartesian.y, STEPS_REVOLUTION, MICROSTEPPING_Y, MM_REVOLUTION),
        z=signedStepVelocity(velocityCartesian.z, STEPS_REVOLUTION, MICROSTEPPING_Z, MM_REVOLUTION),
        yaw=signedStepVelocity(velocityCartesian.yaw, STEPS_REVOLUTION, MICROSTEPPING_YAW, 360.0),
    )