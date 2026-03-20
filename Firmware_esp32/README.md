# Firmware (ESP32-S3)

Real-time firmware for motor control, sensor reading, and command execution on the PickUS and PlacUS machine.

## Prerequisites

- [PlatformIO](https://platformio.org/) (VS Code extension recommended)
- ESP32-S3 DevKitC-1 board
- USB-to-Serial cable for flashing

## Installation

1. **Install PlatformIO**
   - Open VS Code and install the PlatformIO extension

2. **Open the project**
   ```bash
   cd Firmware_esp32
   ```

3. **Build and upload**
   ```bash
   pio run --target upload
   ```

4. **Monitor serial output** (115200 baud)
   ```bash
   pio device monitor
   ```

---

## Configuration

### Pin Mapping (`BoardConfig.h`)

| Signal | Pin | Direction |
|--------|-----|-----------|
| Motor X DIR/STEP/EN | 6 / 7 / 15 | Output |
| Motor Y DIR/STEP/EN | 16 / 17 / 18 | Output |
| Motor Z DIR/STEP/EN | 3 / 46 / 11 | Output |
| Motor YAW DIR/STEP/EN | 12 / 13 / 14 | Output |
| Vacuum pump | 5 | Output |
| Valve | 4 | Output |
| Limit switch X | 35 | Input |
| Limit switch Y | 36 | Input |
| Limit switch Z | 37 | Input |
| Pressure sensor CLK/DATA | 2 / 1 | I/O |
| CAN TX/RX | 47 / 48 | I/O |

### Serial Communication

- **Baud Rate**: 115200
- **Protocol**: Command-based (see Command IDs below)
- **Flow Control**: None

---

## Usage

### Firmware Overview

The firmware consists of these key modules:

| Module | File | Responsibility |
|--------|------|---|
| `Controller` | `Controller.h/cpp` | Drives stepper motors using AccelStepper/MultiStepper; manages motion profiles |
| `DataModel` | `DataModel.h/cpp` | Thread-safe shared state for control and communication tasks |
| `Communication` | `main.cpp` | UART serial protocol receiving commands from HMI |
| `Pressure Sensor` | `pressureSensor.h/cpp` | Reads pressure using a bit-banged clock+data interface (1 bit per clock pulse) to detect component pickup success |
| `Limit Switch` | `LimitSwitch.h/cpp` | Monitors X, Y, Z end-stops for homing and safety |

### Command IDs

| Command | Value | Description | Parameters |
|---------|-------|-------------|------------|
| `STOP` | 0 | Stop all motors | None |
| `MOVE` | 1 | Move to position at velocity | x, y, z, yaw, velocity |
| `PICK` | 2 | Pick sequence (lower Z, activate pump) | None |
| `PLACE` | 3 | Place sequence (activate valve) | None |
| `HOME` | 4 | Run homing sequence | None |
| `EMPTY` | 5 | No-op / idle | None |

### Machine States

| State | Description |
|-------|-------------|
| `READY` | Idle, waiting for a command |
| `MOVING` | Executing a MOVE command |
| `PICKING` | Executing a PICK sequence |
| `PLACING` | Executing a PLACE sequence |
| `ERROR` | Fault condition detected |
| `DISCONNECTED` | No active HMI connection |

---

## Testing

### Run Unit Tests

---

## Project Structure

```
Firmware_esp32/
├── src/                     # C++ source files
│   ├── main.cpp
│   ├── Controller.cpp/h
│   ├── DataModel.cpp/h
│   ├── BoardConfig.h
│   ├── pressureSensor.cpp/h
│   ├── LimitSwitch.cpp/h
│   └── ...
├── lib/                     # External libraries
│   └── AccelStepper/
├── test/                    # Unit tests
├── include/                 # Header files
├── platformio.ini           # PlatformIO configuration
└── README.md
```

---

## Dependencies

- [AccelStepper](https://github.com/waspinator/AccelStepper) (`waspinator/AccelStepper@^1.64`) — stepper motor control

---

## Troubleshooting

### Serial Monitor Not Connecting
- Verify USB cable is connected
- Check Device Manager (Windows) or `/dev/ttyUSB*` (Linux) for the correct COM port
- Ensure baud rate is set to 115200

### Build Fails
- Clean the build: `pio run --target clean`
- Check that all libraries are installed and up to date

---

## Next Steps

- See [main README](../README.md) for project overview
- See [HMI README](../HMI/) for host interface setup
- See [Electrical README](../Electrical/) for hardware design
