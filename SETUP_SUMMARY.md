# Setup Summary - Movement Chain Hardware

This document provides a complete overview of the Git hooks and PR validation setup.

## Repository Structure

```
movement-chain-hardware/
├── .github/
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.md           # Bug report template
│   │   ├── feature_request.md      # Feature request template
│   │   └── design_review.md        # Design review template
│   ├── workflows/
│   │   └── pr-validation.yml       # Automated PR validation workflow
│   └── PULL_REQUEST_TEMPLATE.md    # Pull request template
│
├── .husky/
│   ├── commit-msg                  # Commit message validation (executable)
│   ├── pre-commit                  # Pre-commit checks (executable)
│   └── pre-push                    # Pre-push validation (executable)
│
├── .gitignore                      # Git ignore rules
├── .npmrc                          # npm configuration
├── commitlint.config.js            # Commit message rules
├── package.json                    # Node.js dependencies
├── Makefile                        # Convenience commands
├── setup.sh                        # Setup script (executable)
├── LICENSE                         # MIT License
├── README.md                       # Repository overview
├── CONTRIBUTING.md                 # Contribution guidelines
├── HOOKS_SETUP.md                  # Detailed hooks documentation
└── SETUP_SUMMARY.md                # This file
```

## Files Created

### Configuration Files

1. **package.json**
   - Purpose: Node.js project configuration
   - Dependencies: husky, @commitlint/cli, @commitlint/config-conventional
   - Script: `prepare` runs husky setup

2. **commitlint.config.js**
   - Purpose: Commit message validation rules
   - Types: Standard (feat, fix, docs, chore, etc.) + Hardware (hw, pcb, sch, bom, lib)
   - Format: Conventional Commits

3. **.gitignore**
   - Purpose: Ignore patterns for Git
   - Includes: node_modules, KiCad backup/temp files, OS files, IDE files
   - Excludes: Generated files (optional)

4. **.npmrc**
   - Purpose: npm configuration
   - Settings: No package-lock, exact versions, reduced logging

### Git Hooks

All hooks are in `.husky/` and are **executable** (`chmod +x`):

1. **commit-msg**
   - Validates commit message format
   - Runs: `commitlint --edit`
   - Blocks: Invalid commit messages

2. **pre-commit**
   - Checks for large files (>10MB)
   - Verifies KiCad project files exist
   - Warns about backup files
   - Behavior: Non-blocking warnings

3. **pre-push**
   - Runs ERC on schematic files
   - Runs DRC on PCB files
   - Checks for BOM file
   - Requires: kicad-cli (optional)
   - Behavior: Non-blocking warnings

### GitHub Workflows

1. **pr-validation.yml**
   - Trigger: PRs to main/develop branches
   - Container: setsoft/kicad_auto:latest
   - Steps:
     - Lists KiCad files
     - Runs ERC (continue-on-error)
     - Runs DRC (continue-on-error)
     - Exports Gerbers
     - Exports BOM
     - Uploads artifacts (7-day retention)
   - Artifacts:
     - gerbers-pr{number}
     - bom-pr{number}

### Templates

1. **PULL_REQUEST_TEMPLATE.md**
   - Sections: Description, Type, Changes, Testing, Screenshots, Checklist
   - Purpose: Standardize PR format

2. **Bug Report Template**
   - Location: .github/ISSUE_TEMPLATE/bug_report.md
   - Purpose: Report hardware design issues

3. **Feature Request Template**
   - Location: .github/ISSUE_TEMPLATE/feature_request.md
   - Purpose: Propose new circuits/features

4. **Design Review Template**
   - Location: .github/ISSUE_TEMPLATE/design_review.md
   - Purpose: Request design review

### Documentation

1. **README.md**
   - Purpose: Repository overview and quick start
   - Sections: Overview, Setup, Workflow, Prerequisites

2. **CONTRIBUTING.md**
   - Purpose: Contribution guidelines
   - Sections: Setup, Design guidelines, Commit format, PR process, Design rules

3. **HOOKS_SETUP.md**
   - Purpose: Detailed Git hooks documentation
   - Sections: Setup, Hook details, Workflow, Troubleshooting

4. **LICENSE**
   - Type: MIT License
   - Year: 2025
   - Holder: Movement Chain

### Utility Files

1. **setup.sh** (executable)
   - Purpose: Automated repository setup
   - Checks: Node.js, npm, Git, KiCad
   - Actions: Install dependencies, verify hooks

2. **Makefile**
   - Purpose: Convenience commands
   - Targets: setup, check, erc, drc, gerbers, bom, clean
   - Requirements: KiCad CLI for validation/export

## Setup Instructions

### Initial Setup

1. **Navigate to repository**:
   ```bash
   cd /Users/maxwsy/Desktop/workspace/movement-chain-hardware
   ```

2. **Run setup script**:
   ```bash
   ./setup.sh
   ```

   Or manually:
   ```bash
   npm install
   chmod +x .husky/commit-msg .husky/pre-commit .husky/pre-push
   ```

3. **Verify installation**:
   ```bash
   ls -la .husky/
   npx commitlint --version
   ```

### Optional: Install KiCad CLI

For automated ERC/DRC checks:

```bash
# macOS
brew install kicad

# Ubuntu/Debian
sudo apt-get install kicad

# Verify installation
kicad-cli version
```

## Usage Examples

### Using Make Commands

```bash
# View all available commands
make help

# Run setup
make setup

# Run all checks
make check

# Run ERC only
make erc

# Run DRC only
make drc

# Export Gerbers
make gerbers

# Export BOM
make bom

# Export both
make exports

# Clean generated files
make clean
```

### Manual Commands

```bash
# Install dependencies
npm install

# Run ERC
kicad-cli sch erc your-project.kicad_sch

# Run DRC
kicad-cli pcb drc your-project.kicad_pcb

# Export Gerbers
kicad-cli pcb export gerbers --output gerbers/ your-project.kicad_pcb

# Export BOM
kicad-cli sch export bom --output BOM.csv your-project.kicad_sch
```

### Commit Examples

```bash
# Valid commits
git commit -m "feat: add USB-C power delivery circuit"
git commit -m "pcb: route differential pairs for USB 3.0"
git commit -m "sch: add decoupling capacitors to MCU"
git commit -m "fix: correct R1 value from 10k to 1k"
git commit -m "bom: update capacitor values"

# Test commit message format
echo "feat: test message" | npx commitlint
```

### Creating a Pull Request

```bash
# Create feature branch
git checkout -b feature/usb-power-circuit

# Make changes in KiCad, save files

# Stage changes
git add *.kicad_sch *.kicad_pcb BOM.csv

# Commit with proper format
git commit -m "feat: add USB-C PD circuit with 60W support"

# Push branch
git push origin feature/usb-power-circuit

# Create PR on GitHub
# CI will automatically validate and export artifacts
```

## Validation Workflow

### Local (Developer)

1. Make changes in KiCad
2. Save all files
3. Run `make check` (optional)
4. Commit with proper format (validated by commit-msg hook)
5. Push (pre-push hook runs ERC/DRC if KiCad installed)

### Remote (GitHub Actions)

1. PR created/updated
2. CI checks out code
3. Lists KiCad files
4. Runs ERC on schematics
5. Runs DRC on PCB
6. Exports Gerbers
7. Exports BOM
8. Uploads artifacts
9. Creates summary

All steps use `continue-on-error: true` to avoid blocking PRs on warnings.

## Troubleshooting

### Hooks Not Running

```bash
# Reinstall hooks
npm run prepare

# Or
npx husky

# Verify executable
chmod +x .husky/*
```

### Commit Message Rejected

```bash
# View error details
# commitlint will show which rule failed

# Fix message
git commit --amend -m "feat: correct message format"
```

### KiCad CLI Not Found

```bash
# Check installation
which kicad-cli

# Install KiCad 7+
brew install kicad  # macOS

# Hooks will skip ERC/DRC with warning if not installed
```

### CI Workflow Fails

1. Check GitHub Actions logs
2. Verify KiCad files are valid
3. Check container compatibility
4. Review error messages in workflow output

## Next Steps

1. **Create KiCad Project**:
   - Open KiCad
   - Create new project
   - Add schematics and PCB
   - Save files

2. **Make First Commit**:
   ```bash
   git add *.kicad_pro *.kicad_sch *.kicad_pcb
   git commit -m "feat: initial hardware design"
   git push origin main
   ```

3. **Set Up Remote Repository**:
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/movement-chain-hardware.git
   git branch -M main
   git push -u origin main
   ```

4. **Configure GitHub**:
   - Enable GitHub Actions
   - Set branch protection for main
   - Configure required status checks

## Key Features

### Automated Validation
- Commit message format enforcement
- Pre-push ERC/DRC checks
- CI-based validation on PRs
- Automatic Gerber/BOM generation

### Non-Blocking Warnings
- All hardware checks are warnings
- Won't block commits/pushes
- Encourages good practices without friction

### Comprehensive Documentation
- README for overview
- CONTRIBUTING for guidelines
- HOOKS_SETUP for detailed info
- This summary for quick reference

### Hardware-Specific
- Custom commit types (pcb, sch, bom)
- KiCad file validation
- ERC/DRC automation
- Gerber/BOM export

## Additional Resources

- [KiCad Documentation](https://docs.kicad.org/)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [Husky Documentation](https://typicode.github.io/husky/)
- [commitlint](https://commitlint.js.org/)
- [GitHub Actions](https://docs.github.com/en/actions)

## Support

For issues or questions:
1. Review this documentation
2. Check HOOKS_SETUP.md
3. Review GitHub workflow logs
4. Create an issue on GitHub

---

**Repository**: movement-chain-hardware
**Location**: /Users/maxwsy/Desktop/workspace/movement-chain-hardware
**Created**: December 2025
**Maintainer**: Movement Chain Team
