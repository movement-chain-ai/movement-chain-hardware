# Movement Chain Hardware

KiCad PCB design repository for Movement Chain hardware components.

## Overview

This repository contains the hardware design files for Movement Chain's PCB using KiCad 7+.

## Repository Structure

```
movement-chain-hardware/
├── .github/
│   └── workflows/
│       └── pr-validation.yml    # Automated PR validation
├── .husky/
│   ├── commit-msg               # Commit message validation
│   ├── pre-commit               # Pre-commit checks
│   └── pre-push                 # Pre-push hardware validation
├── *.kicad_pro                  # KiCad project file
├── *.kicad_sch                  # Schematic files
├── *.kicad_pcb                  # PCB layout files
├── BOM.*                        # Bill of Materials
├── commitlint.config.js         # Commit message rules
├── package.json                 # Node.js dependencies
├── HOOKS_SETUP.md              # Detailed setup guide
└── README.md                    # This file
```

## Quick Start

### 1. Clone Repository

```bash
git clone <repository-url>
cd movement-chain-hardware
```

### 2. Install Dependencies

```bash
npm install
```

This will automatically set up Git hooks for commit validation and hardware checks.

### 3. Install KiCad (Optional but Recommended)

- **macOS**: `brew install kicad`
- **Ubuntu/Debian**: `sudo apt-get install kicad`
- **Windows**: Download from [kicad.org](https://www.kicad.org/download/)

### 4. Open Project in KiCad

```bash
# Open the .kicad_pro file in KiCad
open *.kicad_pro  # macOS
```

## Development Workflow

### Making Changes

1. Create a feature branch:
   ```bash
   git checkout -b feature/my-hardware-change
   ```

2. Make changes in KiCad (schematic or PCB)

3. Commit with conventional format:
   ```bash
   git commit -m "pcb: add decoupling capacitors near IC"
   ```

4. Push changes:
   ```bash
   git push origin feature/my-hardware-change
   ```

5. Create a Pull Request on GitHub

### Commit Message Format

Use [Conventional Commits](https://www.conventionalcommits.org/) with hardware-specific types:

**Standard Types**:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `chore`: Maintenance

**Hardware Types**:
- `hw`: General hardware changes
- `pcb`: PCB layout changes
- `sch`: Schematic changes
- `bom`: Bill of Materials updates
- `lib`: Component library updates

**Examples**:
```bash
git commit -m "sch: add USB-C power delivery circuit"
git commit -m "pcb: update trace widths for high-current paths"
git commit -m "bom: update capacitor values"
git commit -m "fix: correct footprint assignment for U1"
```

## Git Hooks

This repository uses automated Git hooks:

- **commit-msg**: Validates commit message format
- **pre-commit**: Checks for large files and backup files
- **pre-push**: Runs KiCad ERC/DRC checks (if KiCad CLI is installed)

All checks are non-blocking to avoid interrupting your workflow.

## GitHub Actions

Pull requests trigger automated validation:

1. **ERC (Electrical Rule Check)**: Validates schematics
2. **DRC (Design Rule Check)**: Validates PCB layout
3. **Gerber Export**: Generates manufacturing files
4. **BOM Export**: Generates Bill of Materials

Artifacts (Gerbers and BOM) are available for download from the PR page for 7 days.

## Prerequisites

- **Node.js**: v18+ (for commit hooks)
- **KiCad**: 7+ (for design and validation)
- **Git**: 2.9+

## Documentation

- [HOOKS_SETUP.md](HOOKS_SETUP.md) - Detailed Git hooks and workflow guide
- [KiCad Documentation](https://docs.kicad.org/)

## Support

For questions or issues:
1. Check [HOOKS_SETUP.md](HOOKS_SETUP.md)
2. Review GitHub Actions logs
3. Create an issue in this repository

## License

[Specify your license here]

---

**Project**: Movement Chain Hardware
**Last Updated**: December 2025
