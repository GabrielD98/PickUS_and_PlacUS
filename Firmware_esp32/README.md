# Firmware (ESP32-S3)

Firmware for motor control, sensor reading, and command execution on the PickUS and PlacUS machine.

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

### Pin Mapping (`boardconfig.h`)

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
| `Controller` | `controller.h/cpp` | Coordinates command handling, motion, homing, pick/place sequences, and machine state updates |
| `DataModel` | `datamodel.h/cpp` | Thread-safe shared command/position/state buffer between the controller and the communication task |
| `Communication` | `main.cpp` | UART protocol that receives `command_t` packets and sends back `statusFrame_t` replies |
| `Geometry` | `geometry.h/cpp` | Converts between cartesian coordinates and motor steps / velocities |
| `Mosfet` | `mosfet.h/cpp` | Controls the vacuum pump and valve outputs |
| `Pressure Sensor` | `pressuresensor.h/cpp` | Reads and converts the bit-banged pressure sensor signal into kPa |
| `Limit Switch` | `limitswitch.h/cpp` | Monitors X, Y, Z end-stops for homing and safety |

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
| `HOMING` | Executing the homing sequence |
| `ERROR` | Fault condition detected |

---

## Testing

### Run Unit Tests

The firmware includes test hooks controlled by `platformio.ini` build flags:

- `ENABLE_TEST=1` runs the internal test task instead of normal control/communication tasks.
- `ENABLE_COM_TEST=1` runs the communication test task alongside the test task.
- Both flags are set to `0` by default for normal firmware operation.

---

## Project Structure

```
Firmware_esp32/
├── src/                     # Firmware source files
│   ├── boardconfig.h
│   ├── controller.cpp/h
│   ├── datamodel.cpp/h
│   ├── geometry.cpp/h
│   ├── limitswitch.cpp/h
│   ├── main.cpp
│   ├── mosfet.cpp/h
│   ├── pressuresensor.cpp/h
│   └── tests/               # Internal test helpers and scenarios
├── lib/                     # Shared data types and external libraries
│   ├── data.hpp
│   └── AccelStepper/
├── include/                 # Header includes placeholder
├── output/                  # Generated build/output artifacts
├── test/                    # PlatformIO test entry point
│   └── README
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
- See [Mechanical README](../Mechanical/) for mechanical design
