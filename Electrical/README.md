# Electrical Guide

PCB design and schematics for the PickUS and PlacUS machine. Includes main control board and test board for validation.

## Scope

The electrical work is split into two KiCad projects:

- `PNP_MOBO_V1/` — Main control board for the machine
- `PNP_TEST_CIRCUIT_V1/` — Test board for validating pick and place operation

## Prerequisites

- KiCad 8 (recommended)
- Basic soldering tools and bench power supply for bring-up
- Optional for production:
  - PCB manufacturer account (JLCPCB, PCBWay, etc.)
  - Assembly service for SMT components

---

## Installation & Setup

1. **Install KiCad**
   - Download from [https://www.kicad.org/](https://www.kicad.org/)
   - Install version 8 or later

2. **Open a project**
   ```bash
   cd Electrical/circuitPNP
   ```
   Or for the test board:
   ```bash
   cd Electrical/PCB_test
   ```

3. **Open in KiCad**
   - Double-click the `.kicad_pro` file, or
   - Launch KiCad and open the project file

---

## Project Structure

```
Electrical/
├── circuitPNP/
│   ├── circuitPNP.kicad_sch      # Main board schematic
│   ├── circuitPNP.kicad_pcb      # Main board PCB layout
│   ├── circuitPNP.kicad_pro      # Project file
│   ├── fabricationFile.zip       # Gerber, drill, and BOM exports
│   └── bom/                      # Bill of materials
├── PCB_test/
|   ├── STENCIL.3mf
│   ├── PCB_test.kicad_sch        # Test board schematic
│   ├── PCB_test.kicad_pcb        # Test board PCB layout
│   └── PCB_test.kicad_pro        # Project file
└── README.md
```

---

## Main Board (`circuitPNP`)

### Key Subsystems

- **ESP32 Control & Communication**: Control and USB serial lines
- **Stepper Driver Interfaces**: DIR/STEP/EN signals for X, Y, Z, YAW motors
- **Vacuum Pump & Valve Switching**: Power control for pickup system
- **Pressure Sensor Interface**: Two-wire clock+data interface (bit-banged): toggle clock, sensor outputs one data bit per pulse (used for grip detection)
- **End-Stop Connectors**: Limit switch inputs for X, Y, Z axes
- **Can/I2C Connectors**: Additional expansion headers

---

## Test Board (`PCB_test`)

### Purpose

Validate the pick-and-place workflow with a dedicated test board featuring standard footprints.

---

## Bring-Up & Validation

Complete this checklist as you recreate each board:

- [ ] KiCad project opens without missing symbol/footprint errors
- [ ] ERC passes with no critical errors
- [ ] All connectors have clear pin naming in schematic and silkscreen
- [ ] DRC passes with no critical errors
- [ ] Gerber and drill files exported
- [ ] BOM exported and validated with available stock
- [ ] Board assembled and visually inspected
- [ ] Continuity test completed on power rails and critical nets
- [ ] First power-on done with current-limited supply (no shorts)
- [ ] ESP32 and peripherals communication validated via firmware
- [ ] Motors, pump/valve, and sensors verified functionally

---

## Versioning & Release

- Use a version tag in the board title block and filenames (e.g., `v1`, `v2`)
- Commit schematic and PCB changes together

---

## BOM Organization

Recommended workflow:

- **PCB parts:** use the KiCad interactive BOM export (`PNP_MOBO_V1/bom/ibom.html`)
- **All non-PCB parts (electrical + mechanical):** TODO

## Fabrication Tools

- **For stencil generation:** we use [gerber_to_scad](https://github.com/kirberich/gerber_to_scad)
- **Purpose:** generate stencil or fabrication geometry from the PCB source files

---

## Troubleshooting

### Missing Symbols or Footprints
- Verify all library paths are configured in KiCad
- Check that custom symbols/footprints are in the project library directory

### ERC or DRC Errors
- Review each error and determine if it's a genuine violation or a false positive
- Suppress false positives only after verification

### Design Rule Violations
- Consult your PCB manufacturer's design rules for clearance, trace width, and via sizes
- Update KiCad design rules to match your manufacturer specifications

---

## Next Steps

- See [main README](../README.md) for project overview
- See [Firmware README](../Firmware_esp32/) for ESP32 setup and firmware details
- See [HMI README](../HMI/) for host interface setup
