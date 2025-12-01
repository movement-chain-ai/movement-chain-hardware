# Git Hooks Setup for Movement Chain Hardware

This document explains the Git hooks and workflow automation for the Movement Chain hardware repository.

## Overview

This repository uses Git hooks to maintain code quality and automate hardware validation for KiCad PCB projects.

## Prerequisites

- **Node.js** (v18+): Required for commitlint and husky
- **KiCad 7+**: Required for automated ERC/DRC checks (optional but recommended)
- **Git**: Version 2.9+

## Initial Setup

### 1. Install Dependencies

```bash
npm install
```

This will:
- Install `husky`, `@commitlint/cli`, and `@commitlint/config-conventional`
- Automatically run `husky` to set up Git hooks

### 2. Verify Hooks Installation

Check that hooks are executable:

```bash
ls -la .husky/
```

You should see:
- `commit-msg` (executable)
- `pre-commit` (executable)
- `pre-push` (executable)

If they're not executable:

```bash
chmod +x .husky/commit-msg .husky/pre-commit .husky/pre-push
```

## Git Hooks

### commit-msg Hook

**Purpose**: Validates commit message format

**Rules**: Enforces [Conventional Commits](https://www.conventionalcommits.org/) format

**Standard Types**:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `chore`: Maintenance tasks
- `refactor`: Code refactoring
- `test`: Testing changes
- `style`: Code style changes
- `ci`: CI/CD changes
- `build`: Build system changes

**Hardware-Specific Types**:
- `hw`: General hardware changes
- `pcb`: PCB layout changes
- `sch`: Schematic changes
- `bom`: Bill of Materials updates
- `gerber`: Gerber file generation
- `design`: Design rule or constraint changes
- `lib`: Component library updates

**Examples**:

```bash
# Valid commits
git commit -m "feat: add USB-C power delivery circuit"
git commit -m "pcb: update trace widths for high-current paths"
git commit -m "sch: add decoupling capacitors to MCU"
git commit -m "fix: correct footprint for U1"
git commit -m "bom: update resistor values for LED current limiting"

# Invalid commits (will be rejected)
git commit -m "Update schematic"  # Missing type
git commit -m "FEAT: add circuit"  # Type must be lowercase
git commit -m "feat: Add circuit." # Subject must not end with period
```

### pre-commit Hook

**Purpose**: Validates repository state before commit

**Checks**:
1. **Large Files**: Warns about files larger than 10MB
2. **KiCad Project**: Verifies `.kicad_pro` file exists
3. **Backup Files**: Warns about backup files (`*-bak`, `*.bak`, `*~`)

**Behavior**: All checks are non-blocking (warnings only)

### pre-push Hook

**Purpose**: Validates hardware design before pushing to remote

**Checks** (if `kicad-cli` is installed):
1. **ERC (Electrical Rule Check)**: Validates schematic files
2. **DRC (Design Rule Check)**: Validates PCB layout
3. **BOM**: Checks if Bill of Materials file exists

**Behavior**: All checks are non-blocking (warnings only)

**Installing KiCad CLI**:

```bash
# macOS (via Homebrew)
brew install kicad

# Ubuntu/Debian
sudo apt-get install kicad

# Windows
# Download from https://www.kicad.org/download/
```

## GitHub Actions Workflow

### PR Validation (`pr-validation.yml`)

**Triggers**: Pull requests to `main` or `develop` branches

**Steps**:
1. **Checkout**: Pulls PR code
2. **List Files**: Documents KiCad files in PR
3. **Run ERC**: Electrical rule check on schematics
4. **Run DRC**: Design rule check on PCBs
5. **Export Gerbers**: Generates manufacturing files
6. **Export BOM**: Generates Bill of Materials
7. **Upload Artifacts**: Stores Gerbers and BOM for review

**Container**: Uses `setsoft/kicad_auto:latest` with KiCad pre-installed

**Artifacts**:
- `gerbers-pr<number>`: Manufacturing files (7-day retention)
- `bom-pr<number>`: Bill of Materials CSV (7-day retention)

### Viewing Artifacts

1. Go to the PR's "Checks" tab
2. Click on "Hardware PR Validation"
3. Scroll to "Artifacts" section
4. Download Gerbers and BOM files

## KiCad Workflow

### Creating a New Design

```bash
# Create KiCad project
# (Use KiCad GUI to create .kicad_pro, .kicad_sch, .kicad_pcb files)

# Stage files
git add *.kicad_pro *.kicad_sch *.kicad_pcb

# Commit with proper format
git commit -m "sch: initial schematic for power circuit"

# Push (will trigger ERC/DRC checks)
git push origin feature/power-circuit
```

### Making PCB Changes

```bash
# Make changes in KiCad
# Save files

# Check what changed
git status
git diff

# Commit with descriptive message
git commit -m "pcb: increase trace width for power rails to 1mm"

# Push changes
git push
```

### Creating a Pull Request

```bash
# Push your branch
git push origin feature/my-hardware-change

# Create PR via GitHub
# CI will automatically run:
# - ERC checks
# - DRC checks
# - Generate Gerbers
# - Generate BOM
```

## Troubleshooting

### Hook Not Running

```bash
# Reinstall hooks
npm run prepare

# Or manually
npx husky
```

### Commit Message Rejected

```bash
# View the error message
# It will show which rule failed

# Fix your commit message format
git commit --amend -m "feat: correct commit message format"
```

### KiCad CLI Not Found

```bash
# Check if kicad-cli is installed
which kicad-cli

# If not installed, pre-push checks will be skipped (with warning)
# Install KiCad 7+ to enable automated checks
```

### Large File Warning

```bash
# Check file sizes
find . -type f -size +10M

# If necessary files, commit with caution
# Consider using Git LFS for large binaries
git lfs install
git lfs track "*.step"
git add .gitattributes
```

## Best Practices

### Commit Messages

- Use **imperative mood**: "add circuit" not "added circuit"
- Be **specific**: "sch: add USB-C PD controller" not "sch: update"
- Reference **issues**: "fix: correct R1 value (closes #42)"

### Version Control

- **Commit early, commit often**: Small, focused commits
- **Don't commit generated files**: Gerbers, PDFs (unless needed)
- **Use branches**: Feature branches for new circuits
- **Review before push**: Check ERC/DRC locally first

### KiCad Files

- **Save all files**: Project, schematic, PCB together
- **Update BOM**: Keep Bill of Materials current
- **Run checks**: ERC/DRC before committing
- **Annotate**: Use consistent reference designators

### Pull Requests

- **Clear titles**: "Add power supply circuit for 3.3V rail"
- **Descriptions**: Document design decisions
- **Review artifacts**: Download and verify Gerbers/BOM
- **Address feedback**: Update based on code review

## Additional Resources

- [KiCad Documentation](https://docs.kicad.org/)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [Husky Documentation](https://typicode.github.io/husky/)
- [GitHub Actions](https://docs.github.com/en/actions)

## Support

For issues or questions:
1. Check this documentation first
2. Review commit hook error messages
3. Check GitHub Actions logs
4. Create an issue in the repository

---

**Last Updated**: December 2025
**Repository**: movement-chain-hardware
**Maintainer**: Movement Chain Team
