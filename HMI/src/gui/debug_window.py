from collections import deque
import threading
import time

from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import (
    QCheckBox,
    QComboBox,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QPlainTextEdit,
    QVBoxLayout,
    QWidget,
)

from command_interface import FirmwareCommandId, SetPumpCommand, SetValveCommand
from controller import Controller
from gui.jog_widget import JogWidget
from settings import read_debug_settings, write_debug_settings
from data import MAX_TOOLHEAD, MachineState


class DebugWindow(QWidget):
    """Debug window for comm logs, manual control, and telemetry."""

    def __init__(self, controller: Controller):
        super().__init__()
        self.setWindowTitle("Debug")
        self._controller = controller

        self._logLock = threading.Lock()
        self._logQueue = deque()
        self._logHistory = deque(maxlen=1000)
        self._logListener = self._onLogEntry
        self._commandFilterName: str | None = None

        self._controller.addCommLogListener(self._logListener)

        self._buildUI()
        self._loadSettings()
        self._startLogTimer()
        self._startTelemetryTimer()

    def _buildUI(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        logGroup = QGroupBox("Comm Logs")
        logLayout = QVBoxLayout()
        logGroup.setLayout(logLayout)

        controlsLayout = QHBoxLayout()
        self._parseCheck = QCheckBox("Enable parsing")
        self._parseCheck.setChecked(self._controller.isCommandParsingEnabled())
        self._parseCheck.toggled.connect(self._toggleParsing)
        clearButton = QPushButton("Clear")
        clearButton.clicked.connect(self._clearLogs)
        controlsLayout.addWidget(self._parseCheck)
        controlsLayout.addStretch()
        controlsLayout.addWidget(clearButton)

        self._logView = QPlainTextEdit()
        self._logView.setReadOnly(True)

        filterLayout = QHBoxLayout()
        self._inCheck = QCheckBox("IN")
        self._inCheck.setChecked(True)
        self._inCheck.toggled.connect(self._refreshLogView)
        self._outCheck = QCheckBox("OUT")
        self._outCheck.setChecked(True)
        self._outCheck.toggled.connect(self._refreshLogView)
        self._cmdFilterEntry = QLineEdit()
        self._cmdFilterEntry.setPlaceholderText("Cmd id/name")
        self._cmdFilterEntry.textChanged.connect(self._updateCommandFilter)

        filterLayout.addWidget(QLabel("Filter"))
        filterLayout.addWidget(self._inCheck)
        filterLayout.addWidget(self._outCheck)
        filterLayout.addWidget(self._cmdFilterEntry)

        logLayout.addLayout(controlsLayout)
        logLayout.addLayout(filterLayout)
        logLayout.addWidget(self._logView)
        layout.addWidget(logGroup)

        telemetryGroup = QGroupBox("Telemetry")
        telemetryLayout = QVBoxLayout()
        telemetryGroup.setLayout(telemetryLayout)

        self._machineStateLabel = QLabel("Machine State : -")
        self._positionLabel = QLabel("Position (mm) : -")
        self._pressureLabel = QLabel("Pressure : -")
        self._valveLabel = QLabel("Valves : -")
        self._pumpLabel = QLabel("Pump : -")

        telemetryLayout.addWidget(self._machineStateLabel)
        telemetryLayout.addWidget(self._positionLabel)
        telemetryLayout.addWidget(self._pressureLabel)
        telemetryLayout.addWidget(self._valveLabel)
        telemetryLayout.addWidget(self._pumpLabel)

        layout.addWidget(telemetryGroup)

        outputsGroup = QGroupBox("Outputs")
        outputsLayout = QVBoxLayout()
        outputsGroup.setLayout(outputsLayout)

        valveLayout = QHBoxLayout()
        self._valveSelect = QComboBox()
        self._valveSelect.addItems([str(index) for index in range(MAX_TOOLHEAD)])
        self._valveToggleButton = QPushButton("Valve ON")
        self._valveToggleButton.clicked.connect(self._toggleValve)
        valveLayout.addWidget(QLabel("Valve"))
        valveLayout.addWidget(self._valveSelect)
        valveLayout.addWidget(self._valveToggleButton)

        pumpLayout = QHBoxLayout()
        self._pumpToggleButton = QPushButton("Pump ON")
        self._pumpToggleButton.clicked.connect(self._togglePump)
        pumpLayout.addWidget(QLabel("Pump"))
        pumpLayout.addWidget(self._pumpToggleButton)

        outputsLayout.addLayout(valveLayout)
        outputsLayout.addLayout(pumpLayout)
        layout.addWidget(outputsGroup)

        manualGroup = QGroupBox("Manual Control")
        manualLayout = QVBoxLayout()
        manualGroup.setLayout(manualLayout)
        manualLayout.addWidget(JogWidget(isMain=False))
        layout.addWidget(manualGroup)

    def _startLogTimer(self):
        self._logTimer = QTimer(self)
        self._logTimer.setInterval(100)
        self._logTimer.timeout.connect(self._flushLogs)
        self._logTimer.start()

    def _startTelemetryTimer(self):
        self._telemetryTimer = QTimer(self)
        self._telemetryTimer.setInterval(200)
        self._telemetryTimer.timeout.connect(self._updateTelemetry)
        self._telemetryTimer.start()

    def _toggleParsing(self, enabled: bool):
        self._controller.setCommandParsingEnabled(enabled)
        self._saveSettings()

    def _clearLogs(self):
        self._logView.clear()
        with self._logLock:
            self._logQueue.clear()
            self._logHistory.clear()

    def _loadSettings(self):
        settings = read_debug_settings()
        if not settings:
            return

        if "parsing_enabled" in settings:
            self._controller.setCommandParsingEnabled(bool(settings.get("parsing_enabled")))
            self._parseCheck.blockSignals(True)
            self._parseCheck.setChecked(self._controller.isCommandParsingEnabled())
            self._parseCheck.blockSignals(False)

    def _toggleValve(self):
        if self._controller.getMachineState() != MachineState.READY:
            return
        toolhead = self._valveSelect.currentIndex()
        current_state = False
        if hasattr(self, "_latestValveStates") and toolhead < len(self._latestValveStates):
            current_state = bool(self._latestValveStates[toolhead])
        self._controller.queueCommand(SetValveCommand(toolheadIndex=toolhead, enabled=not current_state))

    def _togglePump(self):
        if self._controller.getMachineState() != MachineState.READY:
            return
        current_state = bool(getattr(self, "_latestPumpState", False))
        self._controller.queueCommand(SetPumpCommand(enabled=not current_state))

    def _onLogEntry(self, direction: str, message: str):
        stamp = time.strftime("%H:%M:%S")
        with self._logLock:
            entry = (stamp, direction, message)
            self._logQueue.append(entry)
            self._logHistory.append(entry)

    def _flushLogs(self):
        lines = []
        with self._logLock:
            while self._logQueue:
                lines.append(self._logQueue.popleft())
        if not lines:
            return
        for stamp, direction, message in lines:
            if self._passesLogFilter(direction, message):
                self._logView.appendPlainText(f"{stamp} {direction} {message}")

    def _refreshLogView(self):
        self._logView.clear()
        with self._logLock:
            history = list(self._logHistory)
        for stamp, direction, message in history:
            if self._passesLogFilter(direction, message):
                self._logView.appendPlainText(f"{stamp} {direction} {message}")

    def _updateCommandFilter(self):
        text = self._cmdFilterEntry.text().strip()
        if not text:
            self._commandFilterName = None
            self._refreshLogView()
            return

        if text.isdigit():
            try:
                self._commandFilterName = FirmwareCommandId(int(text)).name
            except ValueError:
                self._commandFilterName = None
        else:
            try:
                self._commandFilterName = FirmwareCommandId[text.upper()].name
            except KeyError:
                self._commandFilterName = text.upper()

        self._refreshLogView()

    def _passesLogFilter(self, direction: str, message: str) -> bool:
        if direction == "IN" and not self._inCheck.isChecked():
            return False
        if direction == "OUT" and not self._outCheck.isChecked():
            return False

        if self._commandFilterName is None:
            return True

        cmd_name = self._extractCommandName(message)
        if cmd_name is None:
            return False

        return cmd_name.upper() == self._commandFilterName.upper()

    @staticmethod
    def _extractCommandName(message: str) -> str | None:
        marker = "cmd="
        start = message.find(marker)
        if start == -1:
            return None
        start += len(marker)
        end = message.find(" ", start)
        if end == -1:
            end = len(message)
        return message[start:end]

    def _updateTelemetry(self):
        machine_state = self._controller.getMachineState()
        position = self._controller.getGripperPosition()
        pressures = self._controller.getMachinePressures()
        valves = self._controller.getMachineValveStates()
        pump_state = self._controller.getMachinePumpState()

        self._latestValveStates = valves
        self._latestPumpState = pump_state

        pressure_text = ", ".join([f"{pressure:.2f}" for pressure in pressures]) if pressures else "-"
        valve_text = ", ".join(["ON" if state else "OFF" for state in valves]) if valves else "-"

        self._machineStateLabel.setText(f"Machine State : {machine_state}")
        self._positionLabel.setText(
            f"Position (mm) : {position.x:.2f}, {position.y:.2f}, {position.z:.2f}, {position.yaw:.2f}"
        )
        self._pressureLabel.setText(f"Pressure : {pressure_text}")
        self._valveLabel.setText(f"Valves : {valve_text}")
        self._pumpLabel.setText(f"Pump : {'ON' if pump_state else 'OFF'}")

        toolhead = self._valveSelect.currentIndex()
        valve_state = valves[toolhead] if toolhead < len(valves) else False
        self._valveToggleButton.setText("Valve OFF" if valve_state else "Valve ON")
        self._pumpToggleButton.setText("Pump OFF" if pump_state else "Pump ON")

    def closeEvent(self, event):
        self._controller.removeCommLogListener(self._logListener)
        if hasattr(self, "_logTimer"):
            self._logTimer.stop()
        if hasattr(self, "_telemetryTimer"):
            self._telemetryTimer.stop()
        super().closeEvent(event)
