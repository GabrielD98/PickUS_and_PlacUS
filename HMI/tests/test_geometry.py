import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

import unittest

from data import Position
from geometry import (
    P_X_MAX,
    P_X_MIN,
    P_Y_MAX,
    P_Y_MIN,
    P_Z_MAX,
    P_Z_MIN,
    StepPosition,
    coord_to_step,
    dimension_limits,
    step_to_coord,
    velocity_to_step,
)


class TestGeometry(unittest.TestCase):
    def test_dimension_limits(self):
        position = Position(-10.0, 400.0, 4.0, 45.0)

        constrained = dimension_limits(position)

        self.assertEqual(constrained.x, P_X_MIN)
        self.assertEqual(constrained.y, P_Y_MAX)
        self.assertEqual(constrained.z, P_Z_MAX)
        self.assertEqual(constrained.yaw, position.yaw)

    def test_coord_step_round_trip(self):
        position = Position(100.0, 200.0, -20.0, 180.0)

        step_position = coord_to_step(position)
        restored_position = step_to_coord(step_position)

        self.assertIsInstance(step_position, StepPosition)
        self.assertAlmostEqual(restored_position.x, position.x, delta=40.0 / (200 * 16))
        self.assertAlmostEqual(restored_position.y, position.y, delta=40.0 / (200 * 16))
        self.assertAlmostEqual(restored_position.z, position.z, delta=40.0 / (200 * 4))
        self.assertAlmostEqual(restored_position.yaw, position.yaw, delta=360.0 / (200 * 4))

    def test_velocity_clamp(self):
        step_velocity = velocity_to_step(5000.0)

        self.assertGreater(step_velocity.x, 0)
        self.assertEqual(step_velocity.x, step_velocity.y)
        self.assertGreater(step_velocity.z, 0)
        self.assertGreater(step_velocity.yaw, 0)


if __name__ == '__main__':
    unittest.main()