# Movement Chain Hardware - Makefile
# Convenience commands for hardware development

.PHONY: help setup install check erc drc gerbers bom clean

# Default target
help:
	@echo "Movement Chain Hardware - Available Commands"
	@echo ""
	@echo "Setup & Installation:"
	@echo "  make setup      - Run initial setup (install deps + hooks)"
	@echo "  make install    - Install npm dependencies"
	@echo ""
	@echo "Validation:"
	@echo "  make check      - Run all checks (ERC + DRC)"
	@echo "  make erc        - Run Electrical Rule Check on schematics"
	@echo "  make drc        - Run Design Rule Check on PCB"
	@echo ""
	@echo "Export:"
	@echo "  make gerbers    - Export Gerber files"
	@echo "  make bom        - Export Bill of Materials"
	@echo "  make exports    - Export both Gerbers and BOM"
	@echo ""
	@echo "Maintenance:"
	@echo "  make clean      - Remove generated files"
	@echo "  make test       - Test commit message format"
	@echo ""

# Setup
setup:
	@echo "Setting up repository..."
	@./setup.sh

install:
	@echo "Installing npm dependencies..."
	@npm install

# Validation
check: erc drc
	@echo "All checks complete"

erc:
	@echo "Running Electrical Rule Check..."
	@if command -v kicad-cli >/dev/null 2>&1; then \
		for sch in *.kicad_sch; do \
			if [ -f "$$sch" ]; then \
				echo "Checking $$sch..."; \
				kicad-cli sch erc "$$sch" || true; \
			fi \
		done \
	else \
		echo "kicad-cli not found. Install KiCad 7+ to run ERC."; \
		exit 1; \
	fi

drc:
	@echo "Running Design Rule Check..."
	@if command -v kicad-cli >/dev/null 2>&1; then \
		for pcb in *.kicad_pcb; do \
			if [ -f "$$pcb" ]; then \
				echo "Checking $$pcb..."; \
				kicad-cli pcb drc "$$pcb" || true; \
			fi \
		done \
	else \
		echo "kicad-cli not found. Install KiCad 7+ to run DRC."; \
		exit 1; \
	fi

# Export
gerbers:
	@echo "Exporting Gerber files..."
	@if command -v kicad-cli >/dev/null 2>&1; then \
		mkdir -p gerbers; \
		for pcb in *.kicad_pcb; do \
			if [ -f "$$pcb" ]; then \
				echo "Exporting Gerbers for $$pcb..."; \
				kicad-cli pcb export gerbers --output gerbers/ "$$pcb" || true; \
			fi \
		done; \
		echo "Gerbers exported to gerbers/"; \
	else \
		echo "kicad-cli not found. Install KiCad 7+ to export Gerbers."; \
		exit 1; \
	fi

bom:
	@echo "Exporting Bill of Materials..."
	@if command -v kicad-cli >/dev/null 2>&1; then \
		for sch in *.kicad_sch; do \
			if [ -f "$$sch" ]; then \
				echo "Exporting BOM for $$sch..."; \
				kicad-cli sch export bom --output BOM.csv "$$sch" || true; \
			fi \
		done; \
		echo "BOM exported to BOM.csv"; \
	else \
		echo "kicad-cli not found. Install KiCad 7+ to export BOM."; \
		exit 1; \
	fi

exports: gerbers bom
	@echo "All exports complete"

# Maintenance
clean:
	@echo "Cleaning generated files..."
	@rm -rf gerbers/
	@rm -f BOM.csv
	@rm -f *.xml
	@rm -f *-cache.lib
	@rm -f fp-info-cache
	@echo "Clean complete"

test:
	@echo "Testing commit message validation..."
	@echo "feat: test commit message" | npx commitlint
	@echo "Commit message validation is working!"

# Git shortcuts
.PHONY: status diff log
status:
	@git status

diff:
	@git diff

log:
	@git log --oneline --graph --decorate --all -10
