# PickUS and PlacUS

A 4-axis (X, Y, Z, Yaw) PCB pick-and-place machine for automated SMD component assembly. Built for the S4 robotics project at Université de Sherbrooke.

## Table of Contents

1. [About](#about)
2. [Features](#features)
3. [Tech Stack](#tech-stack)
4. [Project Structure](#project-structure)
5. [Quick Start](#quick-start)
6. [Roadmap](#roadmap)
7. [Contributing](#contributing)
8. [License](#license)
9. [Contact](#contact)

---

## About

### Problem
Manual SMD component placement onto PCBs is time-consuming and error-prone. Small labs and educational institutions need an affordable pick-and-place machine for fast prototyping.

### Solution
PickUS and PlacUS is an open-source, 4-axis automated pick-and-place machine that:
- Picks SMD components using a vacuum pump system
- Places them onto PCBs with positional accuracy
- Uses stepper motors for precise X, Y, Z, and rotational (Yaw) control
- Integrates with KiCad placement files for automated workflows

### Audience
Ideal for robotics project teams, PCB assembly labs, and makers who need to automate component placement without high capital investment.

---

## Features

- **4-Axis Control**: X, Y, Z positioning + Yaw rotation for flexible placement
- **Vacuum Pick System**: Pneumatic pump and valve for reliable component pickup
- **Pressure Sensing**: Real-time feedback to detect successful component pickup
- **End-Stop Protection**: Z-axis limit switch to prevent collision damage
- **ESP32-S3 Controller**: Over-the-air updateable firmware with multiple I/O options
- **Python HMI**: Cross-platform graphical interface for machine control
- **KiCad Integration**: Direct import of `.pos` placement files for batch production
- **Modular Design**: Separate electrical, firmware, and HMI components

---

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Microcontroller | ESP32-S3 (32-bit, dual-core, 240 MHz) |
| Motor Control | Stepper drivers (NEMA-17 steppers on X,Y,Z and NEMA_8 on YAW) |
| Firmware | C++ with PlatformIO / Arduino framework |
| Motor Library | [AccelStepper](https://github.com/waspinator/AccelStepper) |
| Communication | UART (serial) at 115200 baud |
| HMI | Python 3 + PyQt5/PySimpleGUI |
| Serial Library | `pyserial` |
| PCB Design | KiCad 8+ |
| Schematic | `circuitPNP/` main board + `PCB_test/` test board |

---

## Project Structure

```
PickUS_and_PlacUS/
├── Electrical/              # KiCad schematics and PCB layouts
│   ├── circuitPNP/          # Main control board
│   ├── PCB_test/            # Test board for validation
│   └── README.md            # Electrical recreation guide
├── Firmware_esp32/          # ESP32-S3 firmware (PlatformIO)
│   ├── src/                 # C++ source files
│   ├── lib/                 # Libraries (AccelStepper, etc.)
│   ├── test/                # Unit tests
│   ├── include/             # Header files
│   └── platformio.ini       # PlatformIO config
└── HMI/                     # Python host interface
    ├── src/                 # Main HMI modules
    │   ├── gui/             # GUI components
    │   ├── communication.py # Serial protocol
    │   ├── controller.py    # Command orchestration
    │   ├── main.py          # Entry point
    │   └── ...
    └── tests/               # Unit and integration tests
```

---

## Quick Start

Each subsystem has its own detailed README:

- **[Firmware_esp32/](Firmware_esp32/)** — ESP32-S3 firmware setup and configuration
- **[HMI/](HMI/)** — Python host interface installation and usage
- **[Electrical/](Electrical/)** — PCB design and electrical recreation guide

---

## Getting Started

### For Developers

1. Clone this repository
2. Navigate to the subsystem folder of interest (Firmware, HMI, or Electrical)
3. Follow the README in that folder for detailed setup instructions

### Project Overview

| Subsystem | Technology | Purpose |
|-----------|-----------|---------|
| **Firmware_esp32** | C++ with PlatformIO | Real-time motor control, sensor reading, and command execution |
| **HMI** | Python 3 + PyQt5 | Cross-platform UI for machine operation and KiCad file import |
| **Electrical** | KiCad 8+ | Circuit design and PCB layouts |

---

## Roadmap

- [ ] Multi-head support for parallel placement
- [ ] Vision-based component alignment
- [ ] Auto feeder implementation
- [ ] Machine learning for optimal pick order optimization

---

## Contributing

Contributions are welcome!

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Commit your changes: `git commit -m "Add your feature"`
4. Push to the branch: `git push origin feature/your-feature-name`
5. Open a pull request

Please ensure all tests pass before submitting a PR.

---

## License

This project is licensed under the **MIT License**. See [LICENSE](LICENSE) for details.

---

## Contact

**Project Maintainers**: S4 Robotics Team  
**Institution**: Université de Sherbrooke  
**Email**: [your-email@example.com]  
**Repository**: [https://github.com/GabrielD98/PickUS_and_PlacUS](https://github.com/GabrielD98/PickUS_and_PlacUS)

---

## Acknowledgments

- [PlatformIO](https://platformio.org/) for embedded development tools
- [KiCad](https://www.kicad.org/) for PCB design
- [AccelStepper Library](https://www.airspayce.com/mikem/arduino/AccelStepper/) for motor control
- Université de Sherbrooke robotics program
- All contributors and testers
