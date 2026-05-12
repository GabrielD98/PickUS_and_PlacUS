import os
import struct
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

import unittest

from command_interface import (
	CommandInterface,
	CartesianVelocity,
	DEFAULT_HOME_VELOCITY,
	DEFAULT_PICK_PRESSURE_KPA,
	DEFAULT_PLACE_PRESSURE_KPA,
	DEFAULT_PRESSURE_THRESHOLD_KPA,
	FirmwareCommandId,
	HomeCommand,
	MoveCommand,
	PauseCommand,
	PickCommand,
	PlaceCommand,
	StopCommand,
)
from data import Position
from geometry import coordToStep, velocityToStep


class TestCommandInterface(unittest.TestCase):
	def setUp(self):
		self.builder = CommandInterface()

	def test_build_move_packet(self):
		command = MoveCommand(Position(100.0, 200.0, -20.0, 180.0), CartesianVelocity(50.0, 60.0, 70.0, 80.0))

		packet = self.builder.buildPacket(command)
		header = struct.unpack('<BIH', packet[:7])
		payload = struct.unpack('<llllhhhh', packet[7:])

		position_step = coordToStep(command.position)
		velocity_step = velocityToStep(command.velocity)

		self.assertEqual(header[0], FirmwareCommandId.MOVE)
		self.assertEqual(header[1], 1)
		self.assertEqual(header[2], 24)
		self.assertEqual(payload, (
			position_step.x,
			position_step.y,
			position_step.z,
			position_step.yaw,
			velocity_step.x,
			velocity_step.y,
			velocity_step.z,
			velocity_step.yaw,
		))

	def test_build_pick_and_place_packets(self):
		pick_packet = self.builder.buildPacket(PickCommand())
		place_packet = self.builder.buildPacket(PlaceCommand())

		pick_header = struct.unpack('<BIH', pick_packet[:7])
		place_header = struct.unpack('<BIH', place_packet[:7])
		pick_payload = struct.unpack('<BxH', pick_packet[7:])
		place_payload = struct.unpack('<BxH', place_packet[7:])

		self.assertEqual(pick_header[0], FirmwareCommandId.PICK)
		self.assertEqual(place_header[0], FirmwareCommandId.PLACE)
		self.assertEqual(pick_payload, (0, DEFAULT_PICK_PRESSURE_KPA))
		self.assertEqual(place_payload, (0, DEFAULT_PLACE_PRESSURE_KPA))

	def test_build_pick_and_place_packets_with_interface_defaults(self):
		custom_builder = CommandInterface(toolheadIndex=0, pressureThresholdKpa=DEFAULT_PRESSURE_THRESHOLD_KPA)
		pick_packet = custom_builder.buildPacket(PickCommand(toolheadIndex=None, pressureThresholdKpa=None))
		place_packet = custom_builder.buildPacket(PlaceCommand(toolheadIndex=None, pressureThresholdKpa=None))

		pick_payload = struct.unpack('<BxH', pick_packet[7:])
		place_payload = struct.unpack('<BxH', place_packet[7:])

		self.assertEqual(pick_payload, (0, DEFAULT_PRESSURE_THRESHOLD_KPA))
		self.assertEqual(place_payload, (0, DEFAULT_PRESSURE_THRESHOLD_KPA))

	def test_build_home_stop_and_pause_packets(self):
		home_packet = self.builder.buildPacket(HomeCommand())
		stop_packet = self.builder.buildPacket(StopCommand())
		pause_packet = self.builder.buildPacket(PauseCommand())

		home_header = struct.unpack('<BIH', home_packet[:7])
		home_payload = struct.unpack('<hhhh', home_packet[7:])
		stop_header = struct.unpack('<BIH', stop_packet[:7])
		pause_header = struct.unpack('<BIH', pause_packet[:7])

		default_home_velocity = velocityToStep(DEFAULT_HOME_VELOCITY)
		self.assertEqual(home_header[0], FirmwareCommandId.HOME)
		self.assertEqual(home_payload, (
			default_home_velocity.x,
			default_home_velocity.y,
			default_home_velocity.z,
			default_home_velocity.yaw,
		))
		self.assertEqual(stop_header[0], FirmwareCommandId.STOP)
		self.assertEqual(pause_header[0], FirmwareCommandId.PAUSE)


if __name__ == '__main__':
	unittest.main()