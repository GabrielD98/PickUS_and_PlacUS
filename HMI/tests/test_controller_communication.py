import sys
import os
import time

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

import unittest
from controller import Controller
from data import Position, ControllerState, MachineState
from command_interface import MoveCommand, PickCommand, PlaceCommand, HomeCommand, CartesianVelocity


ESP32_PORT = os.getenv("ESP32_PORT")
ESP32_BAUD = int(os.getenv("ESP32_BAUD", "115200"))
ESP32_TEST_TIMEOUT = float(os.getenv("ESP32_TEST_TIMEOUT", "10"))


class TestControllerCommunication(unittest.TestCase):
	def test_sequence_with_esp32(self):

		if not ESP32_PORT:
			self.skipTest("ESP32_PORT environment variable not set – skipping hardware test")

		print("\nTEST COMMUNICATION")

		controller = Controller()

		try:
			controller.connectionToMachine(ESP32_PORT, ESP32_BAUD)
		except Exception as e:
			self.skipTest(f"Could not open {ESP32_PORT}: {e}")
		try:
			self._wait_for_machine_ready(controller, ESP32_TEST_TIMEOUT)

			with controller.mutex:
				controller._controllerState = ControllerState.RUNNING

			# --- MOVE ---
			move_pos = Position(1.0, 2.0, 3.0, 4.0)
			controller.queueCommand(MoveCommand(move_pos, CartesianVelocity.uniform(50.0)))
			self._wait_for_position(controller, move_pos, ESP32_TEST_TIMEOUT)
			_, _, pos = controller.getState()
			self._assertPositionEqual(pos, move_pos, "MOVE")

			# --- PICK ---
			controller.queueCommand(PickCommand())
			self._wait_for_position(controller, move_pos, ESP32_TEST_TIMEOUT)
			_, _, pos = controller.getState()
			self._assertPositionEqual(pos, move_pos, "PICK")

			# --- PLACE ---
			controller.queueCommand(PlaceCommand())
			self._wait_for_position(controller, move_pos, ESP32_TEST_TIMEOUT)
			_, _, pos = controller.getState()
			self._assertPositionEqual(pos, move_pos, "PLACE")

			# --- HOME ---
			home_pos = Position(0.0, 0.0, 0.0, 0.0)
			controller.queueCommand(HomeCommand())
			self._wait_for_position(controller, home_pos, ESP32_TEST_TIMEOUT)
			_, _, pos = controller.getState()
			self._assertPositionEqual(pos, home_pos, "HOME")

			# --- Final state check ---
			self._wait_for_controller_state(controller, ControllerState.DONE, ESP32_TEST_TIMEOUT)
			controller_state, machine_state, _ = controller.getState()
			self.assertEqual(controller_state, ControllerState.DONE)
			self.assertNotEqual(machine_state, MachineState.ERROR)

		finally:
			controller.disconnectionFromMachine()

	def _assertPositionEqual(self, actual: Position, expected: Position, label: str):
		"""Assert that two positions are exactly equal."""
		self.assertEqual(actual.x,   expected.x)
		self.assertEqual(actual.y,   expected.y)
		self.assertEqual(actual.z,   expected.z)
		self.assertEqual(actual.yaw, expected.yaw)

	def _wait_for_position(self, controller: Controller, expected: Position, timeout_seconds: float):
		"""Wait until the reported position exactly matches expected."""
		end_time = time.monotonic() + timeout_seconds
		while time.monotonic() < end_time:
			_, _, pos = controller.getState()
			if (pos.x == expected.x and
				pos.y == expected.y and
				pos.z == expected.z and
				pos.yaw == expected.yaw):
				print(pos)
				return
			time.sleep(0.05)
		_, _, pos = controller.getState()
		self.fail(
			f"Position did not reach {expected} within {timeout_seconds}s "
			f"(last reported: {pos})"
		)

	def _wait_for_controller_state(self, controller: Controller, target_state: ControllerState, timeout_seconds: float):
		end_time = time.monotonic() + timeout_seconds
		while time.monotonic() < end_time:
			if controller.getState()[0] == target_state:
				return
			time.sleep(0.05)
		self.fail(f"Controller state did not reach {target_state} within {timeout_seconds}s")

	def _wait_for_machine_ready(self, controller: Controller, timeout_seconds: float):
		end_time = time.monotonic() + timeout_seconds
		while time.monotonic() < end_time:
			_, machine_state, _ = controller.getState()
			if machine_state != MachineState.HOMING:
				return
			time.sleep(0.05)
		self.fail(f"Machine did not respond within {timeout_seconds}s")

