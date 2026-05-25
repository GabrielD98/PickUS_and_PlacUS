from PyQt5.QtWidgets import (
    QDoubleSpinBox,
    QFormLayout,
    QGroupBox,
    QLabel,
    QMessageBox,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from geometry import getWorkspaceLimits, setWorkspaceLimits
from gui.slice_info_widget import SliceInfoWidget
from settings import read_debug_settings, write_debug_settings


class SettingsWindow(QWidget):
    """Window for configuring machine geometry and pressure thresholds."""

    def __init__(self, slice_widget: SliceInfoWidget | None = None):
        super().__init__()
        self.setWindowTitle("Settings")
        self._sliceWidget = slice_widget

        self._buildUI()
        self._loadSettings()

    def _buildUI(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        pressureGroup = QGroupBox("Pressure Thresholds (kPa)")
        pressureLayout = QFormLayout()
        pressureGroup.setLayout(pressureLayout)

        self._pickThreshold = QSpinBox()
        self._pickThreshold.setRange(0, 500)
        self._placeThreshold = QSpinBox()
        self._placeThreshold.setRange(0, 500)

        applyPressure = QPushButton("Apply")
        applyPressure.clicked.connect(self._applyPressureThresholds)

        pressureLayout.addRow(QLabel("Pick"), self._pickThreshold)
        pressureLayout.addRow(QLabel("Place"), self._placeThreshold)
        pressureLayout.addRow(applyPressure)

        layout.addWidget(pressureGroup)

        geometryGroup = QGroupBox("Machine Geometry (mm)")
        geometryLayout = QFormLayout()
        geometryGroup.setLayout(geometryLayout)

        limits = getWorkspaceLimits()
        self._xMin = self._makeFloatSpin(limits.x_min)
        self._xMax = self._makeFloatSpin(limits.x_max)
        self._yMin = self._makeFloatSpin(limits.y_min)
        self._yMax = self._makeFloatSpin(limits.y_max)
        self._zMin = self._makeFloatSpin(limits.z_min)
        self._zMax = self._makeFloatSpin(limits.z_max)

        applyGeometry = QPushButton("Apply")
        applyGeometry.clicked.connect(self._applyGeometry)

        geometryLayout.addRow(QLabel("X min"), self._xMin)
        geometryLayout.addRow(QLabel("X max"), self._xMax)
        geometryLayout.addRow(QLabel("Y min"), self._yMin)
        geometryLayout.addRow(QLabel("Y max"), self._yMax)
        geometryLayout.addRow(QLabel("Z min"), self._zMin)
        geometryLayout.addRow(QLabel("Z max"), self._zMax)
        geometryLayout.addRow(applyGeometry)

        layout.addWidget(geometryGroup)

    def _makeFloatSpin(self, value: float) -> QDoubleSpinBox:
        spin = QDoubleSpinBox()
        spin.setDecimals(2)
        spin.setRange(-10000.0, 10000.0)
        spin.setValue(float(value))
        return spin

    def _applyPressureThresholds(self):
        if self._sliceWidget is not None:
            self._sliceWidget.setPressureThresholds(self._pickThreshold.value(), self._placeThreshold.value())
        self._saveSettings()

    def _applyGeometry(self):
        try:
            setWorkspaceLimits(
                self._xMin.value(),
                self._xMax.value(),
                self._yMin.value(),
                self._yMax.value(),
                self._zMin.value(),
                self._zMax.value(),
            )
        except ValueError as exc:
            QMessageBox.critical(self, "Invalid geometry", str(exc))
            return
        self._saveSettings()

    def _loadSettings(self):
        if self._sliceWidget is not None:
            pick, place = self._sliceWidget.getPressureThresholds()
            self._pickThreshold.setValue(int(pick))
            self._placeThreshold.setValue(int(place))

        settings = read_debug_settings()
        if not settings:
            return

        pressure = settings.get("pressure")
        if isinstance(pressure, dict):
            pick = self._coerce_int(pressure.get("pick"), self._pickThreshold.value())
            place = self._coerce_int(pressure.get("place"), self._placeThreshold.value())
            self._pickThreshold.setValue(pick)
            self._placeThreshold.setValue(place)
            if self._sliceWidget is not None:
                self._sliceWidget.setPressureThresholds(pick, place)

        geometry = settings.get("geometry")
        if isinstance(geometry, dict):
            limits = getWorkspaceLimits()
            x_min = self._coerce_float(geometry.get("x_min"), limits.x_min)
            x_max = self._coerce_float(geometry.get("x_max"), limits.x_max)
            y_min = self._coerce_float(geometry.get("y_min"), limits.y_min)
            y_max = self._coerce_float(geometry.get("y_max"), limits.y_max)
            z_min = self._coerce_float(geometry.get("z_min"), limits.z_min)
            z_max = self._coerce_float(geometry.get("z_max"), limits.z_max)
            try:
                setWorkspaceLimits(x_min, x_max, y_min, y_max, z_min, z_max)
                self._xMin.setValue(x_min)
                self._xMax.setValue(x_max)
                self._yMin.setValue(y_min)
                self._yMax.setValue(y_max)
                self._zMin.setValue(z_min)
                self._zMax.setValue(z_max)
            except ValueError:
                pass

    def _saveSettings(self):
        settings = read_debug_settings()
        settings["pressure"] = {
            "pick": int(self._pickThreshold.value()),
            "place": int(self._placeThreshold.value()),
        }
        settings["geometry"] = {
            "x_min": round(float(self._xMin.value()), 2),
            "x_max": round(float(self._xMax.value()), 2),
            "y_min": round(float(self._yMin.value()), 2),
            "y_max": round(float(self._yMax.value()), 2),
            "z_min": round(float(self._zMin.value()), 2),
            "z_max": round(float(self._zMax.value()), 2),
        }
        write_debug_settings(settings)

    @staticmethod
    def _coerce_float(value, fallback: float) -> float:
        try:
            return float(value)
        except (TypeError, ValueError):
            return float(fallback)

    @staticmethod
    def _coerce_int(value, fallback: int) -> int:
        try:
            return int(value)
        except (TypeError, ValueError):
            return int(fallback)
