#!/bin/bash
# Heck-CheckOS ISO Builder - Self-Installation Script
# Installs the GUI builder into the target OS

set -e

echo "=========================================="
echo "  Heck-CheckOS ISO Builder - Installation"
echo "=========================================="
echo ""

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    echo "❌ Must run as root"
    echo "Run: sudo $0"
    exit 1
fi

# Installation directory
INSTALL_DIR="/opt/heckcheckos-builder"
BIN_DIR="/usr/local/bin"
DESKTOP_DIR="/usr/share/applications"
ICON_DIR="/usr/share/icons/hicolor/256x256/apps"

echo "[*] Installing Heck-CheckOS ISO Builder to $INSTALL_DIR..."

# Verify we're in the correct directory
# Accept both old and new directory names during transition
CURRENT_DIR=$(basename "$(dirname "$(pwd)")")/$(basename "$(pwd)")
if [ ! -f "main.py" ] || [ ! -f "iso_builder_backend.py" ] || [ ! -d "ui" ]; then
    echo "❌ Error: This script must be run from the gui/ghostos-iso-builder or gui/heckcheckos-iso-builder directory"
    echo "   Current directory: $(pwd)"
    echo "   Missing required files (main.py, iso_builder_backend.py, ui/)"
    exit 1
fi

# Create directories
mkdir -p "$INSTALL_DIR"
mkdir -p "$BIN_DIR"
mkdir -p "$DESKTOP_DIR"
mkdir -p "$ICON_DIR"

# Copy application files
echo "[*] Copying application files..."
cp -r . "$INSTALL_DIR/"

# Verify critical files were copied
if [ ! -f "$INSTALL_DIR/main.py" ]; then
    echo "❌ Error: Failed to copy main.py to $INSTALL_DIR"
    echo "   Installation incomplete. Please check permissions and disk space."
    exit 1
fi

chmod +x "$INSTALL_DIR/main.py"

# Install Python dependencies
echo "[*] Installing Python dependencies..."
pip3 install -r "$INSTALL_DIR/requirements.txt" || {
    echo "⚠️  Warning: Failed to install some dependencies"
    echo "    You may need to install them manually"
}

# Create launcher script
echo "[*] Creating launcher script..."
cat > "$BIN_DIR/heckcheckos-builder" << 'EOF'
#!/bin/bash
# Heck-CheckOS ISO Builder Launcher
# Runs as normal user - will prompt for privileges when building ISOs

# Simply launch the application as the current user
# The application will request elevation only when needed for ISO building
exec /opt/heckcheckos-builder/main.py "$@"
EOF

chmod +x "$BIN_DIR/heckcheckos-builder"

# Create desktop entry
echo "[*] Creating desktop entry..."
cat > "$DESKTOP_DIR/heckcheckos-builder.desktop" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=Heck-CheckOS ISO Builder
GenericName=ISO Builder and Customizer
Comment=Build custom Heck-CheckOS ISOs - GUI runs as user, prompts for privileges when building
Exec=heckcheckos-builder
Icon=heckcheckos-builder
Terminal=false
Categories=System;Development;Utility;
Keywords=iso;builder;heckcheckos;debian;linux;customization;
StartupNotify=true
EOF

# Create icon (placeholder - would use actual icon in production)
echo "[*] Creating application icon..."
cat > "$ICON_DIR/heckcheckos-builder.svg" << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<svg width="256" height="256" xmlns="http://www.w3.org/2000/svg">
  <rect width="256" height="256" fill="#1e1e1e"/>
  <circle cx="128" cy="128" r="80" fill="#0078d4"/>
  <text x="128" y="150" font-size="100" text-anchor="middle" fill="white">👻</text>
</svg>
EOF

# Update desktop database
echo "[*] Updating desktop database..."
update-desktop-database "$DESKTOP_DIR" 2>/dev/null || true

# Create standalone keyboard launcher
echo "[*] Creating standalone keyboard launcher..."
cat > "$BIN_DIR/heckcheckos-keyboard" << 'KEYBOARD_EOF'
#!/usr/bin/env python3
"""Standalone Touchscreen Keyboard Launcher"""
import sys
sys.path.insert(0, '/opt/heckcheckos-builder')

from PyQt6.QtWidgets import QApplication
from ui.touchscreen_keyboard import TouchscreenKeyboard

def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Heck-CheckOS Touchscreen Keyboard")
    
    keyboard = TouchscreenKeyboard()
    keyboard.show_keyboard()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
KEYBOARD_EOF

chmod +x "$BIN_DIR/heckcheckos-keyboard"

# Create keyboard desktop entry
echo "[*] Creating keyboard desktop entry..."
cat > "$DESKTOP_DIR/heckcheckos-keyboard.desktop" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=Heck-CheckOS Touchscreen Keyboard
GenericName=Virtual Keyboard
Comment=Touchscreen keyboard with calibration support
Exec=heckcheckos-keyboard
Icon=input-keyboard
Terminal=false
Categories=Utility;Accessibility;
Keywords=keyboard;touchscreen;virtual;osk;
StartupNotify=true
EOF

update-desktop-database "$DESKTOP_DIR" 2>/dev/null || true

# Create uninstaller
echo "[*] Creating uninstaller..."
cat > "$INSTALL_DIR/uninstall.sh" << 'UNINSTALL_EOF'
#!/bin/bash
# Heck-CheckOS ISO Builder - Uninstaller

if [ "$EUID" -ne 0 ]; then 
    echo "Must run as root: sudo $0"
    exit 1
fi

echo "Removing Heck-CheckOS ISO Builder..."

rm -rf /opt/heckcheckos-builder
rm -f /usr/local/bin/heckcheckos-builder
rm -f /usr/local/bin/heckcheckos-keyboard
rm -f /usr/share/applications/heckcheckos-builder.desktop
rm -f /usr/share/applications/heckcheckos-keyboard.desktop
rm -f /usr/share/icons/hicolor/256x256/apps/heckcheckos-builder.svg

update-desktop-database /usr/share/applications 2>/dev/null || true

echo "✓ Heck-CheckOS ISO Builder has been uninstalled"
UNINSTALL_EOF

chmod +x "$INSTALL_DIR/uninstall.sh"

echo ""
echo "=========================================="
echo "  ✓ Installation Complete!"
echo "=========================================="
echo ""
echo "Heck-CheckOS ISO Builder has been installed to:"
echo "  • Application: $INSTALL_DIR"
echo "  • Launcher: $BIN_DIR/heckcheckos-builder"
echo "  • Keyboard: $BIN_DIR/heckcheckos-keyboard"
echo "  • Desktop Entry: $DESKTOP_DIR/heckcheckos-builder.desktop"
echo "  • Keyboard Entry: $DESKTOP_DIR/heckcheckos-keyboard.desktop"
echo ""
echo "You can now:"
echo "  • Run GUI: heckcheckos-builder"
echo "  • Run keyboard standalone: heckcheckos-keyboard"
echo "  • Launch from application menu"
echo ""
echo "Features:"
echo "  ✓ Multi-ISO builder with all integrations"
echo "  ✓ Touchscreen keyboard with calibration"
echo "  ✓ Custom keyboard layout designer"
echo "  ✓ Theme customization (Gaming/Production)"
echo ""
echo "To uninstall: sudo $INSTALL_DIR/uninstall.sh"
echo ""
