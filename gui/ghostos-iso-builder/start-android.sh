#!/data/data/com.termux/files/usr/bin/bash
# GhostOS Touchscreen Keyboard - Android Launcher
# Optimized for Termux on Android

set -e

echo "========================================"
echo "  GhostOS Keyboard - Android Launcher"
echo "========================================"
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Check if running in Termux
if [ ! -d "/data/data/com.termux" ]; then
    echo -e "${YELLOW}⚠  Not running in Termux${NC}"
    echo "This script is optimized for Termux on Android"
    echo "Trying to continue anyway..."
fi

# Check Android version
if command -v getprop &> /dev/null; then
    ANDROID_VERSION=$(getprop ro.build.version.release)
    echo -e "${BLUE}[*]${NC} Android version: $ANDROID_VERSION"
    
    # Check if Android 9+
    MAJOR_VERSION=$(echo $ANDROID_VERSION | cut -d. -f1)
    if [ "$MAJOR_VERSION" -lt 9 ]; then
        echo -e "${YELLOW}⚠  Android 9.0+ recommended${NC}"
        echo "Current version: $ANDROID_VERSION"
        echo "Keyboard may not work optimally"
    fi
fi

# Check Python
echo -e "${BLUE}[*]${NC} Checking Python..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
    echo -e "${GREEN}✓${NC} Python $PYTHON_VERSION found"
else
    echo -e "${RED}❌ Python not found${NC}"
    echo "Install with: pkg install python"
    exit 1
fi

# Check PyQt6
echo -e "${BLUE}[*]${NC} Checking PyQt6..."
if python3 -c "import PyQt6" 2>/dev/null; then
    echo -e "${GREEN}✓${NC} PyQt6 found"
else
    echo -e "${YELLOW}⚠  PyQt6 not found${NC}"
    echo "Installing PyQt6..."
    pip install PyQt6 || {
        echo -e "${RED}❌ Failed to install PyQt6${NC}"
        echo "Try manually: pip install PyQt6"
        exit 1
    }
fi

# Check display
echo -e "${BLUE}[*]${NC} Checking display..."
if [ -z "$DISPLAY" ]; then
    echo -e "${YELLOW}⚠  DISPLAY not set${NC}"
    echo ""
    echo "You need to run a display server first:"
    echo ""
    echo "Option 1 - VNC Server:"
    echo "  pkg install tigervnc"
    echo "  vncserver :1"
    echo "  export DISPLAY=:1"
    echo ""
    echo "Option 2 - Termux:X11:"
    echo "  1. Install Termux:X11 from F-Droid"
    echo "  2. Start Termux:X11 app"
    echo "  3. export DISPLAY=:0"
    echo ""
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
else
    echo -e "${GREEN}✓${NC} Display: $DISPLAY"
fi

# Check device info
if command -v getprop &> /dev/null; then
    DEVICE_MODEL=$(getprop ro.product.model 2>/dev/null || echo "Unknown")
    DEVICE_ARCH=$(getprop ro.product.cpu.abi 2>/dev/null || echo "Unknown")
    echo -e "${BLUE}[*]${NC} Device: $DEVICE_MODEL ($DEVICE_ARCH)"
fi

# Create config directory
CONFIG_DIR="$HOME/.config/ghostos-builder"
mkdir -p "$CONFIG_DIR"
echo -e "${GREEN}✓${NC} Config directory: $CONFIG_DIR"

# Detect screen size and adjust
if command -v xrandr &> /dev/null 2>&1; then
    SCREEN_SIZE=$(xrandr 2>/dev/null | grep " connected" | awk '{print $3}' | cut -d+ -f1)
    if [ -n "$SCREEN_SIZE" ]; then
        echo -e "${BLUE}[*]${NC} Screen size: $SCREEN_SIZE"
    fi
fi

echo ""
echo "========================================"
echo "  Starting Keyboard"
echo "========================================"
echo ""

# Set environment for Android
export QT_QPA_PLATFORM=${QT_QPA_PLATFORM:-xcb}
export QT_AUTO_SCREEN_SCALE_FACTOR=${QT_AUTO_SCREEN_SCALE_FACTOR:-1}

# Launch keyboard
cd "$SCRIPT_DIR"

# Check if running with GUI or standalone keyboard
if [ "$1" == "--gui" ]; then
    echo "Starting full GUI..."
    python3 main.py
elif [ "$1" == "--keyboard-only" ] || [ -z "$1" ]; then
    echo "Starting keyboard only..."
    python3 << 'EOF'
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

try:
    from PyQt6.QtWidgets import QApplication
    from ui.touchscreen_keyboard import TouchscreenKeyboard
    
    print("Creating application...")
    app = QApplication(sys.argv)
    app.setApplicationName("GhostOS Touchscreen Keyboard")
    
    print("Creating keyboard...")
    keyboard = TouchscreenKeyboard()
    
    # Optimize for Android
    keyboard.resize(700, 250)  # Smaller for Android screens
    
    print("Showing keyboard...")
    keyboard.show_keyboard()
    
    print("Keyboard ready!")
    print("Tip: Tap 🎯 to calibrate touch input")
    
    sys.exit(app.exec())
    
except ImportError as e:
    print(f"Error: {e}")
    print("\nMissing dependencies. Install with:")
    print("  pip install PyQt6")
    sys.exit(1)
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
EOF
else
    echo "Unknown option: $1"
    echo ""
    echo "Usage:"
    echo "  $0              - Start keyboard only (default)"
    echo "  $0 --gui        - Start full GUI"
    echo "  $0 --keyboard-only - Start keyboard only"
    exit 1
fi

EXIT_CODE=$?

if [ $EXIT_CODE -ne 0 ]; then
    echo ""
    echo -e "${RED}❌ Keyboard exited with error: $EXIT_CODE${NC}"
    echo ""
    echo "Troubleshooting:"
    echo "  • Ensure VNC or X11 server is running"
    echo "  • Check DISPLAY is set: echo \$DISPLAY"
    echo "  • Verify PyQt6: pip list | grep PyQt6"
    echo "  • Check logs in: $CONFIG_DIR/"
    exit $EXIT_CODE
fi

echo ""
echo -e "${GREEN}✓ Keyboard closed${NC}"
