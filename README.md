# PickUS and PlacUS

A 4-axis (X, Y, Z, Yaw) PCB pick-and-place machine built for the S4 robotics project at Université de Sherbrooke. The machine uses stepper motors, a vacuum pump/valve system, and a pressure sensor to pick and place SMD components onto a PCB.

---

## Project Structure

```
PickUS_and_PlacUS/
├── Electrical/         # KiCad schematics and PCB layouts
├── Firmware_esp32/     # ESP32-S3 firmware (PlatformIO / Arduino framework)
└── HMI/                # Python host interface (PC-side controller)
```

---

## Firmware (ESP32-S3)

### Prerequisites

- [PlatformIO](https://platformio.org/) (VS Code extension recommended)
- ESP32-S3 DevKitC-1 board

### Setup & Flash

1. Open `Firmware_esp32/` as a PlatformIO project.
2. Build and upload:
   ```
   pio run --target upload
   ```
3. Open the serial monitor at **115200 baud**:
   ```
   pio device monitor
   ```

### Pin Mapping (`BoardConfig.h`)

| Signal         | Pin |
|----------------|-----|
| Motor X DIR/STEP/EN | 6 / 7 / 15 |
| Motor Y DIR/STEP/EN | 16 / 17 / 18 |
| Motor Z DIR/STEP/EN | 3 / 46 / 11 |
| Motor YAW DIR/STEP/EN | 12 / 13 / 14 |
| Vacuum pump    | 5   |
| Valve          | 4   |
| Limit switch Z | 37  |
| Pressure sensor CLK/DATA | 2 / 1 |
| CAN TX/RX      | 47 / 48 |

### Key Modules

| Module | Description |
|--------|-------------|
| `Controller` | Drives the four stepper motors using AccelStepper/MultiStepper; calls `update()` every loop iteration. |
| `DataModel` | Thread-safe shared state between the control task and the communication task. |
| `communication` | UART serial protocol for receiving commands from the HMI. |
| `pressureSensor` | Reads the pressure sensor over bit-bang SPI to detect when a component is picked. |

### Command IDs

| Command | Value | Description |
|---------|-------|-------------|
| `STOP`  | 0 | Stop all motors |
| `MOVE`  | 1 | Move to a target position (x, y, z, yaw) at a given velocity |
| `PICK`  | 2 | Pick a component (lower Z, activate pump) |
| `PLACE` | 3 | Place a component (lower Z, open valve) |
| `HOME`  | 4 | Run homing sequence |
| `EMPTY` | 5 | No-op / idle command |

### Machine States

| State | Description |
|-------|-------------|
| `READY` | Idle, waiting for a command |
| `MOVING` | Executing a MOVE command |
| `PICKING` | Executing a PICK sequence |
| `PLACING` | Executing a PLACE sequence |
| `ERROR` | Fault condition |
| `DISCONNECTED` | No active connection from the HMI |

---

## HMI (Python)

The HMI runs on a PC and communicates with the ESP32 over USB serial.

### Prerequisites

```
pip install pyserial
```

### Running the HMI

```
cd HMI/src
python main.py
```

By default `main.py` connects to **COM19** at **115200 baud**. Edit the port in `main.py` before running:

```python
test.connectionToMachine("COM19", 115200)  # change COM19 to your port
```

### Key Modules

| Module | Description |
|--------|-------------|
| `Controller` | Orchestrates communication, state tracking, and command queuing. Runs the control loop in a background thread. |
| `Communication` | Low-level UART wrapper around `pyserial` (`open`, `close`, `sendData`, `receiveData`). |
| `FileInterpreter` | Parses a KiCad `.pos` placement file and returns a list of `Piece` objects. |
| `Slicer` | Takes the list of pieces and generates an ordered list of `Command` objects (pick → move → place) for each component. |
| `Storage` | Tracks which components are available in the feeder trays. |

### Typical Workflow
TODO
### Running the Tests

```
cd HMI/tests
python run_test.py
```

---

## Electrical

KiCad schematics and PCB layouts are located in `Electrical/`:

- `circuitPNP/` — main control board schematic and PCB
- `PCB_test/` — test board for validating the pick and place

---

## Dependencies

| Component | Dependency |
|-----------|------------|
| Firmware | [AccelStepper](https://github.com/waspinator/AccelStepper) (`waspinator/AccelStepper@^1.64`) |
| HMI | `pyserial` |
