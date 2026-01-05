#!/bin/bash
# GhostOS ISO Builder GUI Launcher
# Easy startup script with all integrations

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}=========================================="
echo "  GhostOS ISO Builder - GUI Launcher"
echo -e "==========================================${NC}"
echo ""

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
GUI_DIR="$SCRIPT_DIR"

# Check if we're in the right directory
if [ ! -f "$GUI_DIR/main.py" ]; then
    echo -e "${RED}❌ Error: main.py not found${NC}"
    echo "Expected location: $GUI_DIR/main.py"
    echo "Please run this script from the gui/ghostos-iso-builder directory"
    exit 1
fi

# Check Python version
echo -e "${BLUE}[*]${NC} Checking Python version..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
    echo -e "${GREEN}✓${NC} Python $PYTHON_VERSION found"
else
    echo -e "${RED}❌ Python 3 not found${NC}"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

# Check for required dependencies
echo -e "${BLUE}[*]${NC} Checking dependencies..."
MISSING_DEPS=0

python3 -c "import PyQt6" 2>/dev/null || {
    echo -e "${YELLOW}⚠${NC}  PyQt6 not found"
    MISSING_DEPS=1
}

python3 -c "import requests" 2>/dev/null || {
    echo -e "${YELLOW}⚠${NC}  requests not found"
    MISSING_DEPS=1
}

if [ $MISSING_DEPS -eq 1 ]; then
    echo ""
    echo -e "${YELLOW}Some dependencies are missing.${NC}"
    echo "Would you like to install them now? (y/n)"
    read -r response
    if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
        echo -e "${BLUE}[*]${NC} Installing dependencies..."
        if [ -f "$GUI_DIR/requirements.txt" ]; then
            pip3 install -r "$GUI_DIR/requirements.txt" || {
                echo -e "${RED}❌ Failed to install dependencies${NC}"
                echo "Try manually: pip3 install -r requirements.txt"
                exit 1
            }
            echo -e "${GREEN}✓${NC} Dependencies installed"
        else
            echo -e "${RED}❌ requirements.txt not found${NC}"
            exit 1
        fi
    else
        echo -e "${RED}Cannot start GUI without required dependencies${NC}"
        exit 1
    fi
else
    echo -e "${GREEN}✓${NC} All dependencies found"
fi

# Check for integrations
echo -e "${BLUE}[*]${NC} Checking integrations..."
INTEGRATIONS_DIR="$(dirname "$SCRIPT_DIR")/integrations"
if [ -d "$INTEGRATIONS_DIR" ]; then
    echo -e "${GREEN}✓${NC} Integrations directory found: $INTEGRATIONS_DIR"
    
    # Count available integrations
    if [ -f "$INTEGRATIONS_DIR/repos.json" ]; then
        REPO_COUNT=$(grep -o '"name":' "$INTEGRATIONS_DIR/repos.json" 2>/dev/null | wc -l) || REPO_COUNT=0
        if [ "$REPO_COUNT" -gt 0 ]; then
            echo -e "${GREEN}✓${NC} $REPO_COUNT integrations available"
        fi
    fi
else
    echo -e "${YELLOW}⚠${NC}  Integrations directory not found (optional)"
fi

# Check if running with GUI support
echo -e "${BLUE}[*]${NC} Checking display..."
if [ -z "$DISPLAY" ] && [ -z "$WAYLAND_DISPLAY" ]; then
    echo -e "${RED}❌ No display detected${NC}"
    echo "This GUI requires X11 or Wayland"
    echo "If running remotely, try: ssh -X user@host"
    exit 1
fi
echo -e "${GREEN}✓${NC} Display available"

# Create config directory if it doesn't exist
CONFIG_DIR="$HOME/.config/ghostos-builder"
mkdir -p "$CONFIG_DIR"
echo -e "${GREEN}✓${NC} Config directory: $CONFIG_DIR"

# Check for touchscreen support
echo -e "${BLUE}[*]${NC} Detecting input devices..."
if command -v xinput &> /dev/null; then
    TOUCHSCREEN=$(xinput list | grep -i touch | head -1)
    if [ -n "$TOUCHSCREEN" ]; then
        echo -e "${GREEN}✓${NC} Touchscreen detected: $TOUCHSCREEN"
        echo -e "${BLUE}   Touchscreen keyboard will be available${NC}"
    else
        echo -e "${YELLOW}⚠${NC}  No touchscreen detected (keyboard still available)"
    fi
fi

echo ""
echo -e "${BLUE}=========================================="
echo "  Starting GhostOS ISO Builder GUI"
echo -e "==========================================${NC}"
echo ""
echo -e "${GREEN}Features available:${NC}"
echo "  • Multi-ISO source loading"
echo "  • Touchscreen keyboard with calibration"
echo "  • Theme customization (Gaming/Production)"
echo "  • Repository integrations"
echo "  • Live preview"
echo "  • Custom file integration"
echo ""

# Launch the GUI
cd "$GUI_DIR"

# Check if running as root (needed for some ISO operations)
if [ "$EUID" -eq 0 ]; then
    echo -e "${YELLOW}⚠${NC}  Running as root"
    echo "   ISO building operations will have full permissions"
    echo ""
fi

# Run with error handling
python3 main.py "$@" || {
    EXIT_CODE=$?
    echo ""
    echo -e "${RED}❌ GUI exited with error code: $EXIT_CODE${NC}"
    echo ""
    echo "Troubleshooting:"
    echo "  • Check that all dependencies are installed"
    echo "  • Verify Python version is 3.8+"
    echo "  • Check $CONFIG_DIR/ghostos-builder.log for details"
    echo "  • Try: pip3 install --upgrade -r requirements.txt"
    exit $EXIT_CODE
}

echo ""
echo -e "${GREEN}✓ GhostOS ISO Builder closed${NC}"
