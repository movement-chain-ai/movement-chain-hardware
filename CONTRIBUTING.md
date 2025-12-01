# Contributing to Movement Chain Hardware

Thank you for your interest in contributing to the Movement Chain hardware project! This document provides guidelines for contributing hardware designs, schematics, and PCB layouts.

## Table of Contents

- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Hardware Design Guidelines](#hardware-design-guidelines)
- [Commit Guidelines](#commit-guidelines)
- [Pull Request Process](#pull-request-process)
- [Code Review](#code-review)
- [Design Rules](#design-rules)

## Getting Started

### Prerequisites

1. **KiCad 7+**: Download from [kicad.org](https://www.kicad.org/download/)
2. **Node.js 18+**: For commit hooks and validation
3. **Git**: Version 2.9 or higher

### Initial Setup

1. **Fork the repository** on GitHub

2. **Clone your fork**:
   ```bash
   git clone https://github.com/YOUR_USERNAME/movement-chain-hardware.git
   cd movement-chain-hardware
   ```

3. **Run setup script**:
   ```bash
   ./setup.sh
   ```

4. **Create a feature branch**:
   ```bash
   git checkout -b feature/my-hardware-change
   ```

## Development Setup

### Installing Dependencies

```bash
npm install
```

This installs:
- `husky`: Git hooks manager
- `commitlint`: Commit message validator
- Conventional commits configuration

### Verifying Setup

```bash
# Check hooks are installed
ls -la .husky/

# Test KiCad CLI
kicad-cli version

# Test commitlint
npx commitlint --version
```

## Hardware Design Guidelines

### File Organization

```
├── *.kicad_pro      # KiCad project file
├── *.kicad_sch      # Schematic files (hierarchical)
├── *.kicad_pcb      # PCB layout file
├── libraries/       # Custom symbol/footprint libraries
│   ├── symbols/     # Custom schematic symbols
│   └── footprints/  # Custom PCB footprints
├── 3d-models/       # Custom 3D models (STEP files)
└── docs/            # Design documentation
    ├── BOM.csv      # Bill of Materials
    └── design-notes.md
```

### Schematic Guidelines

1. **Organization**:
   - Use hierarchical sheets for complex designs
   - Group related circuits (power, MCU, peripherals)
   - One function per sheet

2. **Naming Conventions**:
   - Reference designators: U1, R1, C1, etc.
   - Net names: descriptive (e.g., `VCC_3V3`, `USB_DP`, `SDA_I2C1`)
   - Hierarchical labels: clear and consistent

3. **Documentation**:
   - Add title block with project info
   - Include revision history
   - Comment complex circuits
   - Add test points for debugging

4. **Component Selection**:
   - Use standard parts when possible
   - Document part numbers in fields
   - Specify tolerances and ratings
   - Include manufacturer and distributor info

### PCB Layout Guidelines

1. **Design Rules**:
   - Trace width: Minimum 0.15mm (6 mil) for signals
   - Trace width: 0.5mm+ for power (calculate based on current)
   - Clearance: Minimum 0.15mm (6 mil)
   - Via size: 0.6mm drill, 1.0mm pad (minimum)

2. **Layer Stack**:
   - 2-layer: Signal/GND, VCC/Signal
   - 4-layer: Signal, GND, VCC, Signal
   - Document stack-up in design notes

3. **Power Distribution**:
   - Wide traces for power rails
   - Proper decoupling capacitors
   - Star grounding where appropriate
   - Polygon pours for GND/VCC

4. **Signal Integrity**:
   - Keep high-speed traces short
   - Match lengths for differential pairs
   - Avoid sharp angles (45° or curved)
   - Proper termination for high-speed signals

5. **Manufacturing**:
   - Keep components on one side if possible
   - Minimum 0.5mm clearance from board edge
   - Add fiducials for automated assembly
   - Include mounting holes

### Component Libraries

1. **Using Standard Libraries**:
   - Prefer built-in KiCad libraries
   - Use official manufacturer symbols/footprints

2. **Creating Custom Components**:
   - Follow KiCad naming conventions
   - Verify footprint dimensions with datasheet
   - Add 3D models when available
   - Document custom components

### Running Design Checks

Before committing, run these checks:

```bash
# Electrical Rule Check (ERC)
kicad-cli sch erc your-project.kicad_sch

# Design Rule Check (DRC)
kicad-cli pcb drc your-project.kicad_pcb

# Export Gerbers (verify output)
kicad-cli pcb export gerbers --output gerbers/ your-project.kicad_pcb

# Export BOM
kicad-cli sch export bom --output BOM.csv your-project.kicad_sch
```

## Commit Guidelines

### Commit Message Format

We follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>: <description>

[optional body]

[optional footer]
```

### Types

**Standard**:
- `feat`: New circuit or feature
- `fix`: Bug fix or correction
- `docs`: Documentation changes
- `chore`: Maintenance tasks
- `refactor`: Design refactoring
- `test`: Test updates

**Hardware-Specific**:
- `hw`: General hardware changes
- `pcb`: PCB layout changes
- `sch`: Schematic changes
- `bom`: Bill of Materials updates
- `gerber`: Gerber generation
- `design`: Design rule changes
- `lib`: Component library updates

### Examples

```bash
# Good commit messages
git commit -m "sch: add USB-C PD controller circuit"
git commit -m "pcb: route high-speed USB differential pairs"
git commit -m "fix: correct R1 value from 10k to 1k"
git commit -m "bom: update capacitor values for power supply"
git commit -m "lib: add custom footprint for connector J1"

# Bad commit messages
git commit -m "Update files"  # Too vague
git commit -m "WIP"  # Not descriptive
git commit -m "Fixed stuff"  # No context
```

### Committing Changes

```bash
# Stage changes
git add *.kicad_sch *.kicad_pcb

# Commit with message
git commit -m "sch: add decoupling capacitors near IC"

# Or use interactive commit for detailed message
git commit
```

## Pull Request Process

### 1. Prepare Your Changes

```bash
# Ensure your branch is up to date
git checkout main
git pull upstream main
git checkout feature/my-change
git rebase main

# Run design checks locally
kicad-cli sch erc *.kicad_sch
kicad-cli pcb drc *.kicad_pcb
```

### 2. Create Pull Request

1. Push your branch:
   ```bash
   git push origin feature/my-change
   ```

2. Go to GitHub and create a Pull Request

3. Fill out the PR template:
   - **Title**: Clear, descriptive (e.g., "Add USB-C power delivery circuit")
   - **Description**:
     - What changed and why
     - Design decisions made
     - Testing performed
     - Screenshots/schematics if helpful

### 3. PR Checklist

- [ ] ERC passes (no errors)
- [ ] DRC passes (no errors)
- [ ] BOM is updated
- [ ] Schematic is annotated
- [ ] PCB layout is complete
- [ ] Commit messages follow conventions
- [ ] Documentation is updated
- [ ] Screenshots/renders included (if applicable)

### 4. CI Validation

GitHub Actions will automatically:
- Run ERC on schematics
- Run DRC on PCB
- Export Gerbers
- Export BOM
- Upload artifacts for review

Review the CI output and artifacts before requesting review.

### 5. Review Process

- Address reviewer feedback
- Make requested changes in new commits
- Don't force-push unless requested
- Respond to comments

## Code Review

### For Reviewers

Check:
1. **Electrical Design**:
   - Circuit correctness
   - Component values
   - Power ratings
   - Signal integrity

2. **PCB Layout**:
   - Trace routing
   - Clearances
   - Layer usage
   - Manufacturability

3. **Documentation**:
   - BOM accuracy
   - Reference designators
   - Net names
   - Comments

4. **Files**:
   - No backup files committed
   - Gerbers look correct
   - BOM is complete

### For Contributors

- Be responsive to feedback
- Explain design decisions
- Provide context for reviewers
- Test suggested changes

## Design Rules

### PCB Manufacturing Constraints

Based on standard PCB manufacturers (JLCPCB, PCBWay, OSH Park):

| Parameter | Minimum | Recommended |
|-----------|---------|-------------|
| Trace Width | 0.15mm (6 mil) | 0.2mm (8 mil) |
| Trace Spacing | 0.15mm (6 mil) | 0.2mm (8 mil) |
| Via Drill | 0.3mm (12 mil) | 0.6mm (24 mil) |
| Via Pad | 0.6mm (24 mil) | 1.0mm (40 mil) |
| Hole Size | 0.3mm | 0.6mm |
| Board Thickness | 1.6mm (standard) | 1.6mm |
| Copper Weight | 1 oz (35μm) | 1-2 oz |

### Power Trace Width

Calculate based on current:

| Current | 1 oz Copper | 2 oz Copper |
|---------|-------------|-------------|
| 0.5A | 0.25mm | 0.15mm |
| 1A | 0.5mm | 0.3mm |
| 2A | 1.0mm | 0.6mm |
| 3A | 1.5mm | 1.0mm |

Use online calculators for precise values.

### Spacing for High Voltage

| Voltage | Minimum Spacing |
|---------|----------------|
| < 50V | 0.2mm |
| 50-100V | 0.5mm |
| 100-300V | 1.5mm |
| > 300V | Consult standards |

## Questions?

- Check [HOOKS_SETUP.md](HOOKS_SETUP.md) for Git hooks info
- Review [KiCad Documentation](https://docs.kicad.org/)
- Create an issue for questions
- Join our community discussions

## License

By contributing, you agree that your contributions will be licensed under the same license as the project.

---

Thank you for contributing to Movement Chain Hardware!
