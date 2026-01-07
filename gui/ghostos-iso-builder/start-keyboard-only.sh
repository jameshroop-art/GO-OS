#!/usr/bin/env bash
# Heck-CheckOS Touchscreen Keyboard - Standalone Launcher
# Run keyboard independently without full GUI

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}=========================================="
echo "  Heck-CheckOS Touchscreen Keyboard (Standalone)"
echo -e "==========================================${NC}"
echo ""

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Check Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 not found${NC}"
    echo "Install with: apt install python3 (or pkg install python for Termux)"
    exit 1
fi

echo -e "${GREEN}✓${NC} Python found: $(python3 --version)"

# Check PyQt6
if ! python3 -c "import PyQt6" 2>/dev/null; then
    echo -e "${YELLOW}⚠  PyQt6 not found${NC}"
    echo "Installing PyQt6..."
    pip3 install PyQt6 || {
        echo -e "${RED}❌ Failed to install PyQt6${NC}"
        exit 1
    }
fi

echo -e "${GREEN}✓${NC} PyQt6 available"

# Check display
if [ -z "$DISPLAY" ] && [ -z "$WAYLAND_DISPLAY" ]; then
    echo -e "${YELLOW}⚠  No display detected${NC}"
    echo "Set DISPLAY variable or start a display server first"
    echo "For VNC: export DISPLAY=:1"
    echo "For X11: export DISPLAY=:0"
    exit 1
fi

echo -e "${GREEN}✓${NC} Display: ${DISPLAY:-$WAYLAND_DISPLAY}"

# Launch keyboard
cd "$SCRIPT_DIR"
echo ""
echo -e "${BLUE}Starting keyboard...${NC}"

python3 << 'EOF'
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

try:
    from PyQt6.QtWidgets import QApplication
    from ui.touchscreen_keyboard import TouchscreenKeyboard
    
    app = QApplication(sys.argv)
    app.setApplicationName("Heck-CheckOS Touchscreen Keyboard")
    
    keyboard = TouchscreenKeyboard()
    keyboard.show_keyboard()
    
    print("✓ Keyboard running")
    print("  Press Ctrl+C to exit")
    
    sys.exit(app.exec())
    
except ImportError as e:
    print(f"Error: {e}")
    print("Install dependencies: pip3 install -r requirements.txt")
    sys.exit(1)
except KeyboardInterrupt:
    print("\nKeyboard closed")
    sys.exit(0)
EOF

echo ""
echo -e "${GREEN}✓ Keyboard closed${NC}"
