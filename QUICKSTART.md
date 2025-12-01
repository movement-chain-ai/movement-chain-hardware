# Quick Start Guide - Movement Chain Hardware

Get started with the Movement Chain hardware repository in 5 minutes.

## Prerequisites

- **Node.js 18+**: [Download](https://nodejs.org/)
- **KiCad 7+**: [Download](https://www.kicad.org/download/) (optional for full functionality)
- **Git**: Usually pre-installed on macOS/Linux

## 1. Setup (One-Time)

### Automated Setup

```bash
cd /Users/maxwsy/Desktop/workspace/movement-chain-hardware
./setup.sh
```

This will:
- Install npm dependencies
- Set up Git hooks
- Verify your environment

### Manual Setup

```bash
# Install dependencies
npm install

# Verify setup
./verify-setup.sh
```

## 2. Create Your First Hardware Design

### Open KiCad

```bash
# Start KiCad
kicad

# Or on macOS
open -a KiCad
```

### Create New Project

1. File → New Project
2. Save as: `movement-chain-hardware.kicad_pro`
3. Create schematic and PCB files

### Save Files

Your project should have:
- `*.kicad_pro` - Project file
- `*.kicad_sch` - Schematic file(s)
- `*.kicad_pcb` - PCB layout file

## 3. Make Your First Commit

### Stage Files

```bash
# Add all KiCad files
git add *.kicad_pro *.kicad_sch *.kicad_pcb
```

### Commit with Proper Format

```bash
# Use conventional commit format
git commit -m "feat: initial hardware design"
```

**Commit will be validated automatically!**

### Valid Commit Types

- `feat`: New circuit/feature
- `fix`: Bug fix/correction
- `sch`: Schematic changes
- `pcb`: PCB layout changes
- `bom`: BOM updates
- `docs`: Documentation

## 4. Push Your Changes

```bash
# Push to remote
git push origin main
```

**Pre-push hook will:**
- Run ERC (if KiCad installed)
- Run DRC (if KiCad installed)
- Check for BOM file

## 5. Create a Pull Request

### Create Branch

```bash
git checkout -b feature/my-hardware-change
```

### Make Changes

1. Edit schematic/PCB in KiCad
2. Save all files
3. Update BOM if needed

### Commit and Push

```bash
git add .
git commit -m "pcb: add decoupling capacitors"
git push origin feature/my-hardware-change
```

### Open PR on GitHub

1. Go to GitHub repository
2. Click "New Pull Request"
3. Select your branch
4. Fill out PR template
5. Submit

**CI will automatically:**
- Run ERC/DRC
- Export Gerbers
- Export BOM
- Upload artifacts

## Quick Reference

### Commit Message Format

```bash
<type>: <description>
```

**Examples:**
```bash
git commit -m "feat: add USB-C power delivery circuit"
git commit -m "pcb: route differential pairs for USB 3.0"
git commit -m "sch: add decoupling capacitors to MCU"
git commit -m "fix: correct R1 value from 10k to 1k"
git commit -m "bom: update capacitor values"
```

### Make Commands

```bash
make help       # Show all commands
make setup      # Initial setup
make check      # Run ERC + DRC
make erc        # Run ERC only
make drc        # Run DRC only
make gerbers    # Export Gerbers
make bom        # Export BOM
make clean      # Clean generated files
```

### Testing Locally

```bash
# Run ERC
make erc

# Run DRC
make drc

# Export everything
make exports
```

## Common Workflows

### Adding a New Circuit

```bash
# 1. Create branch
git checkout -b feature/power-supply

# 2. Edit in KiCad
# (Make your changes)

# 3. Check design
make check

# 4. Commit
git add *.kicad_sch *.kicad_pcb
git commit -m "sch: add 3.3V regulator circuit"

# 5. Push and create PR
git push origin feature/power-supply
```

### Fixing a Bug

```bash
# 1. Create branch
git checkout -b fix/incorrect-resistor

# 2. Fix in KiCad
# (Correct the value)

# 3. Commit
git commit -m "fix: correct R1 value from 10k to 1k (fixes #42)"

# 4. Push
git push origin fix/incorrect-resistor
```

### Updating PCB Layout

```bash
# 1. Create branch
git checkout -b pcb/high-speed-routing

# 2. Update layout in KiCad
# (Route traces)

# 3. Check DRC
make drc

# 4. Commit
git commit -m "pcb: route USB 3.0 differential pairs"

# 5. Push
git push origin pcb/high-speed-routing
```

## Troubleshooting

### Commit Rejected

**Error**: Invalid commit message

**Solution**:
```bash
# Fix your commit message
git commit --amend -m "feat: correct message format"
```

### Hook Not Running

**Error**: Git hook not executing

**Solution**:
```bash
# Make hooks executable
chmod +x .husky/*

# Or reinstall
npm run prepare
```

### KiCad CLI Not Found

**Warning**: kicad-cli not installed

**Solution**:
```bash
# Install KiCad 7+
brew install kicad  # macOS

# Or download from
# https://www.kicad.org/download/
```

## Next Steps

1. **Read Documentation**:
   - [CONTRIBUTING.md](CONTRIBUTING.md) - Full guidelines
   - [HOOKS_SETUP.md](HOOKS_SETUP.md) - Detailed hooks info
   - [SETUP_SUMMARY.md](SETUP_SUMMARY.md) - Complete reference

2. **Configure GitHub**:
   - Enable GitHub Actions
   - Set branch protection
   - Configure required reviewers

3. **Start Designing**:
   - Create your circuits
   - Follow design rules
   - Document your work

## Help & Support

- **Verify Setup**: Run `./verify-setup.sh`
- **Test Hooks**: Run `make test`
- **View Logs**: Check GitHub Actions for CI output
- **Ask Questions**: Create an issue on GitHub

## Resources

- [KiCad Documentation](https://docs.kicad.org/)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [Git Basics](https://git-scm.com/book/en/v2)

---

**Ready to build hardware! 🚀**

For detailed information, see:
- [README.md](README.md)
- [CONTRIBUTING.md](CONTRIBUTING.md)
- [HOOKS_SETUP.md](HOOKS_SETUP.md)
