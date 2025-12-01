#!/bin/bash

# Movement Chain Hardware - Setup Script
# This script sets up the development environment for the hardware repository

set -e  # Exit on error

echo "🚀 Setting up Movement Chain Hardware repository..."
echo ""

# Check Node.js installation
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed"
    echo "Please install Node.js 18+ from https://nodejs.org/"
    exit 1
fi

echo "✅ Node.js found: $(node --version)"
echo "✅ npm found: $(npm --version)"
echo ""

# Install npm dependencies
echo "📦 Installing npm dependencies..."
npm install
echo ""

# Verify Git hooks
echo "🔍 Verifying Git hooks..."
if [ -f ".husky/commit-msg" ] && [ -x ".husky/commit-msg" ]; then
    echo "✅ commit-msg hook installed"
else
    echo "⚠️  commit-msg hook missing or not executable"
fi

if [ -f ".husky/pre-commit" ] && [ -x ".husky/pre-commit" ]; then
    echo "✅ pre-commit hook installed"
else
    echo "⚠️  pre-commit hook missing or not executable"
fi

if [ -f ".husky/pre-push" ] && [ -x ".husky/pre-push" ]; then
    echo "✅ pre-push hook installed"
else
    echo "⚠️  pre-push hook missing or not executable"
fi
echo ""

# Check KiCad installation
echo "🔍 Checking KiCad installation..."
if command -v kicad-cli &> /dev/null; then
    echo "✅ KiCad CLI found: $(kicad-cli version 2>&1 | head -n 1 || echo 'version unknown')"
    echo "   Hardware validation hooks will run ERC/DRC checks"
else
    echo "⚠️  KiCad CLI not found"
    echo "   Install KiCad 7+ to enable automated ERC/DRC checks"
    echo "   - macOS: brew install kicad"
    echo "   - Ubuntu/Debian: sudo apt-get install kicad"
    echo "   - Windows: https://www.kicad.org/download/"
fi
echo ""

# Check Git configuration
echo "🔍 Checking Git configuration..."
if git config user.name &> /dev/null && git config user.email &> /dev/null; then
    echo "✅ Git user configured: $(git config user.name) <$(git config user.email)>"
else
    echo "⚠️  Git user not fully configured"
    echo "   Run: git config user.name \"Your Name\""
    echo "   Run: git config user.email \"your.email@example.com\""
fi
echo ""

# Test commit message validation
echo "🧪 Testing commit message validation..."
if npx commitlint --version &> /dev/null; then
    echo "✅ commitlint is working"
else
    echo "⚠️  commitlint may not be working properly"
fi
echo ""

echo "✅ Setup complete!"
echo ""
echo "📚 Next steps:"
echo "   1. Open KiCad and create/edit your project files"
echo "   2. Make commits using conventional format:"
echo "      git commit -m \"sch: add power supply circuit\""
echo "   3. Create a pull request - CI will validate and export Gerbers/BOM"
echo ""
echo "📖 For detailed documentation, see HOOKS_SETUP.md"
echo ""
