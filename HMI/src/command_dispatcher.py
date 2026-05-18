"""Queue and dispatch commands for the controller.

This service owns the command buffer used by the controller control loop and
translates commands into packets before sending them through the serial link.
"""

from command_interface import CommandPacket, CommandInterface, PauseCommand


class CommandDispatcher:
    """Manage queued commands and packet sending for the controller."""

    def __init__(self, controller):
        self._controller = controller

    def queueCommand(self, command: CommandPacket):
        """Append a single command to the controller queue."""
        with self._controller.mutex:
            self._controller._commands.append(command)

    def queueCommands(self, commands: list[CommandPacket]):
        """Append multiple commands to the controller queue."""
        with self._controller.mutex:
            self._controller._commands.extend(commands)

    def clearCommands(self):
        """Clear all queued commands."""
        with self._controller.mutex:
            self._controller._commands = []

    def nextCommand(self) -> CommandPacket | None:
        """Pop the next queued command and remember it as the last command."""
        nextCommand = None
        with self._controller.mutex:
            if self._controller._commands:
                nextCommand = self._controller._commands.pop(0)
                self._controller._lastCommand = nextCommand
        return nextCommand

    def requeueLastCommand(self):
        """Reinsert the last sent command at the front of the queue."""
        with self._controller.mutex:
            if self._controller._lastCommand is not None:
                self._controller._commands.insert(0, self._controller._lastCommand)

    def sendCommand(self, command: CommandPacket | None):
        """Serialize and send a command, or send a heartbeat when idle."""
        if self._controller._com is None:
            return

        if command is None:
            heartbeat = PauseCommand()
            packet = self._controller._commandInterface.buildPacket(heartbeat, True)
            if packet is not None:
                self._controller._com.sendData(packet)
                self._controller._lastSentCommand = heartbeat
            return

        is_new_command = command is not self._controller._lastSentCommand
        packet = self._controller._commandInterface.buildPacket(command, is_new_command)

        if packet is not None:
            self._controller._com.sendData(packet)
            self._controller._lastSentCommand = command