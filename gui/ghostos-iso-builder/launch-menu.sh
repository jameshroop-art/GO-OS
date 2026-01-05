#!/usr/bin/env bash
# GhostOS Component Launcher Menu
# Run individual components on an as-needed basis

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

clear
echo -e "${CYAN}╔════════════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║        GhostOS - Component Launcher Menu             ║${NC}"
echo -e "${CYAN}║        Run components independently as needed         ║${NC}"
echo -e "${CYAN}╚════════════════════════════════════════════════════════╝${NC}"
echo ""

# Function to check if component is running
is_running() {
    local component=$1
    pgrep -f "$component" > /dev/null 2>&1
}

# Display menu
show_menu() {
    echo -e "${BLUE}Available Components:${NC}"
    echo ""
    echo "  1) Full GUI (ISO Builder + Keyboard)"
    echo "  2) Touchscreen Keyboard Only"
    echo "  3) ISO Builder GUI Only (No Keyboard)"
    echo "  4) Port Manager (Check/Allocate Ports)"
    echo "  5) Windows VM Port Configuration"
    echo ""
    echo "  9) Run All Components"
    echo "  0) Exit"
    echo ""
    
    # Show running status
    echo -e "${YELLOW}Status:${NC}"
    if is_running "main.py"; then
        echo -e "  • ISO Builder: ${GREEN}RUNNING ✓${NC}"
    else
        echo -e "  • ISO Builder: ${RED}STOPPED${NC}"
    fi
    
    if is_running "touchscreen_keyboard"; then
        echo -e "  • Keyboard: ${GREEN}RUNNING ✓${NC}"
    else
        echo -e "  • Keyboard: ${RED}STOPPED${NC}"
    fi
    echo ""
}

# Launch full GUI
launch_full_gui() {
    echo -e "${BLUE}[*]${NC} Launching Full GUI..."
    cd "$SCRIPT_DIR"
    ./start-gui.sh
}

# Launch keyboard only
launch_keyboard() {
    echo -e "${BLUE}[*]${NC} Launching Touchscreen Keyboard..."
    cd "$SCRIPT_DIR"
    
    if [ -f "./start-keyboard-only.sh" ]; then
        ./start-keyboard-only.sh
    else
        # Fallback to direct Python
        python3 << 'EOF'
import sys
sys.path.insert(0, '.')
from PyQt6.QtWidgets import QApplication
from ui.touchscreen_keyboard import TouchscreenKeyboard

app = QApplication(sys.argv)
keyboard = TouchscreenKeyboard()
keyboard.show_keyboard()
sys.exit(app.exec())
EOF
    fi
}

# Launch GUI without keyboard
launch_gui_no_keyboard() {
    echo -e "${BLUE}[*]${NC} Launching ISO Builder (No Keyboard)..."
    cd "$SCRIPT_DIR"
    
    export GHOSTOS_NO_KEYBOARD=1
    python3 main.py
}

# Run port manager
launch_port_manager() {
    echo -e "${BLUE}[*]${NC} Running Port Manager..."
    echo ""
    cd "$SCRIPT_DIR"
    
    if [ -f "./port_manager.py" ]; then
        python3 port_manager.py
    else
        echo -e "${RED}❌ Port manager not found${NC}"
        return 1
    fi
    
    echo ""
    echo -e "${GREEN}✓ Port analysis complete${NC}"
    echo "Press Enter to continue..."
    read
}

# Configure Windows VM ports
configure_windows_ports() {
    echo -e "${BLUE}[*]${NC} Configuring Windows VM Ports..."
    echo ""
    cd "$SCRIPT_DIR"
    
    if [ ! -f "./port_manager.py" ]; then
        echo -e "${RED}❌ Port manager not found${NC}"
        return 1
    fi
    
    python3 port_manager.py
    
    echo ""
    echo -e "${YELLOW}Windows VM Port Configuration:${NC}"
    
    CONFIG_FILE="$HOME/.config/ghostos-builder/windows_vm_ports.conf"
    if [ -f "$CONFIG_FILE" ]; then
        echo ""
        cat "$CONFIG_FILE"
        echo ""
        echo -e "${GREEN}✓ Configuration saved to: $CONFIG_FILE${NC}"
    else
        echo -e "${RED}❌ Configuration file not generated${NC}"
    fi
    
    echo ""
    echo "Press Enter to continue..."
    read
}

# Run all components
launch_all() {
    echo -e "${BLUE}[*]${NC} Launching all components..."
    
    # First run port manager
    launch_port_manager
    
    # Launch keyboard in background
    echo -e "${BLUE}[*]${NC} Starting keyboard in background..."
    ./start-keyboard-only.sh &
    KEYBOARD_PID=$!
    
    sleep 2
    
    # Launch main GUI
    echo -e "${BLUE}[*]${NC} Starting main GUI..."
    ./start-gui.sh
    
    # Cleanup
    if [ -n "$KEYBOARD_PID" ]; then
        kill $KEYBOARD_PID 2>/dev/null || true
    fi
}

# Main loop
while true; do
    show_menu
    echo -n "Select option: "
    read -r choice
    
    case $choice in
        1)
            launch_full_gui
            ;;
        2)
            launch_keyboard
            ;;
        3)
            launch_gui_no_keyboard
            ;;
        4)
            launch_port_manager
            ;;
        5)
            configure_windows_ports
            ;;
        9)
            launch_all
            ;;
        0)
            echo -e "${GREEN}Goodbye!${NC}"
            exit 0
            ;;
        *)
            echo -e "${RED}Invalid option${NC}"
            sleep 1
            ;;
    esac
    
    clear
done
