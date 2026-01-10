#!/bin/bash
# Launcher for Windows Driver Installer GUI
# Windows 10 22H2 minimal style driver management

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "Starting Windows Driver Installer GUI..."
echo "Minimal Windows 10 22H2 Style"
echo ""

# Check for PyQt6
if ! python3 -c "import PyQt6" 2>/dev/null; then
    echo "Error: PyQt6 not installed"
    echo "Install with: pip install PyQt6"
    exit 1
fi

# Run the GUI
cd "$SCRIPT_DIR"
python3 driver_installer_gui.py

exit $?
