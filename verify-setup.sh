#!/bin/bash

# Verification script for Movement Chain Hardware setup
# Checks that all required files are in place and properly configured

echo "🔍 Verifying Movement Chain Hardware Setup"
echo "=========================================="
echo ""

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

pass_count=0
fail_count=0
warn_count=0

# Function to check file exists
check_file() {
    if [ -f "$1" ]; then
        echo -e "${GREEN}✓${NC} $1"
        ((pass_count++))
        return 0
    else
        echo -e "${RED}✗${NC} $1 (missing)"
        ((fail_count++))
        return 1
    fi
}

# Function to check file is executable
check_executable() {
    if [ -x "$1" ]; then
        echo -e "${GREEN}✓${NC} $1 (executable)"
        ((pass_count++))
        return 0
    else
        echo -e "${YELLOW}⚠${NC} $1 (not executable)"
        ((warn_count++))
        return 1
    fi
}

# Function to check directory exists
check_dir() {
    if [ -d "$1" ]; then
        echo -e "${GREEN}✓${NC} $1/"
        ((pass_count++))
        return 0
    else
        echo -e "${RED}✗${NC} $1/ (missing)"
        ((fail_count++))
        return 1
    fi
}

# Check directories
echo "📁 Checking Directories:"
check_dir ".github/workflows"
check_dir ".github/ISSUE_TEMPLATE"
check_dir ".husky"
echo ""

# Check configuration files
echo "⚙️  Checking Configuration Files:"
check_file "package.json"
check_file "commitlint.config.js"
check_file ".gitignore"
check_file ".npmrc"
check_file "LICENSE"
echo ""

# Check Git hooks
echo "🪝 Checking Git Hooks:"
check_executable ".husky/commit-msg"
check_executable ".husky/pre-commit"
check_executable ".husky/pre-push"
echo ""

# Check GitHub workflow
echo "🤖 Checking GitHub Workflows:"
check_file ".github/workflows/pr-validation.yml"
echo ""

# Check GitHub templates
echo "📋 Checking GitHub Templates:"
check_file ".github/PULL_REQUEST_TEMPLATE.md"
check_file ".github/ISSUE_TEMPLATE/bug_report.md"
check_file ".github/ISSUE_TEMPLATE/feature_request.md"
check_file ".github/ISSUE_TEMPLATE/design_review.md"
echo ""

# Check documentation
echo "📚 Checking Documentation:"
check_file "README.md"
check_file "CONTRIBUTING.md"
check_file "HOOKS_SETUP.md"
check_file "SETUP_SUMMARY.md"
echo ""

# Check utility files
echo "🛠️  Checking Utility Files:"
check_executable "setup.sh"
check_file "Makefile"
echo ""

# Check Node.js installation
echo "🔧 Checking Prerequisites:"
if command -v node &> /dev/null; then
    echo -e "${GREEN}✓${NC} Node.js installed: $(node --version)"
    ((pass_count++))
else
    echo -e "${YELLOW}⚠${NC} Node.js not installed"
    ((warn_count++))
fi

if command -v npm &> /dev/null; then
    echo -e "${GREEN}✓${NC} npm installed: $(npm --version)"
    ((pass_count++))
else
    echo -e "${YELLOW}⚠${NC} npm not installed"
    ((warn_count++))
fi

if command -v git &> /dev/null; then
    echo -e "${GREEN}✓${NC} Git installed: $(git --version)"
    ((pass_count++))
else
    echo -e "${RED}✗${NC} Git not installed"
    ((fail_count++))
fi

if command -v kicad-cli &> /dev/null; then
    echo -e "${GREEN}✓${NC} KiCad CLI installed"
    ((pass_count++))
else
    echo -e "${YELLOW}⚠${NC} KiCad CLI not installed (optional)"
    ((warn_count++))
fi
echo ""

# Check npm dependencies
echo "📦 Checking npm Dependencies:"
if [ -d "node_modules" ]; then
    if [ -d "node_modules/husky" ]; then
        echo -e "${GREEN}✓${NC} husky installed"
        ((pass_count++))
    else
        echo -e "${RED}✗${NC} husky not installed"
        ((fail_count++))
    fi

    if [ -d "node_modules/@commitlint/cli" ]; then
        echo -e "${GREEN}✓${NC} @commitlint/cli installed"
        ((pass_count++))
    else
        echo -e "${RED}✗${NC} @commitlint/cli not installed"
        ((fail_count++))
    fi
else
    echo -e "${YELLOW}⚠${NC} node_modules not found - run 'npm install'"
    ((warn_count++))
fi
echo ""

# Test commitlint
echo "🧪 Testing Commit Validation:"
if command -v npx &> /dev/null; then
    if echo "feat: test commit message" | npx --no-install commitlint 2>/dev/null; then
        echo -e "${GREEN}✓${NC} commitlint working"
        ((pass_count++))
    else
        echo -e "${YELLOW}⚠${NC} commitlint test failed (may need 'npm install')"
        ((warn_count++))
    fi
else
    echo -e "${YELLOW}⚠${NC} npx not available"
    ((warn_count++))
fi
echo ""

# Check Git repository
echo "🔀 Checking Git Repository:"
if [ -d ".git" ]; then
    echo -e "${GREEN}✓${NC} Git repository initialized"
    ((pass_count++))

    if git config user.name &> /dev/null && git config user.email &> /dev/null; then
        echo -e "${GREEN}✓${NC} Git user configured"
        ((pass_count++))
    else
        echo -e "${YELLOW}⚠${NC} Git user not configured"
        ((warn_count++))
    fi
else
    echo -e "${RED}✗${NC} Not a Git repository"
    ((fail_count++))
fi
echo ""

# Summary
echo "=========================================="
echo "📊 Verification Summary:"
echo ""
echo -e "${GREEN}Passed:${NC}  $pass_count"
echo -e "${YELLOW}Warnings:${NC} $warn_count"
echo -e "${RED}Failed:${NC}  $fail_count"
echo ""

if [ $fail_count -eq 0 ] && [ $warn_count -eq 0 ]; then
    echo -e "${GREEN}🎉 Perfect! Setup is complete and verified!${NC}"
    exit 0
elif [ $fail_count -eq 0 ]; then
    echo -e "${YELLOW}⚠️  Setup is functional but has warnings.${NC}"
    echo "Consider installing optional components for full functionality."
    exit 0
else
    echo -e "${RED}❌ Setup has critical issues that need attention.${NC}"
    echo "Run './setup.sh' to fix issues."
    exit 1
fi
