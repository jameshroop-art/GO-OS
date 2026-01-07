#!/bin/bash
# GhostOS ISO Builder - Self-Installation Script
# Installs the GUI builder into the target OS

set -e

echo "=========================================="
echo "  GhostOS ISO Builder - Installation"
echo "=========================================="
echo ""

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    echo "❌ Must run as root"
    echo "Run: sudo $0"
    exit 1
fi

# Installation directory
INSTALL_DIR="/opt/ghostos-builder"
BIN_DIR="/usr/local/bin"
DESKTOP_DIR="/usr/share/applications"
ICON_DIR="/usr/share/icons/hicolor/256x256/apps"

echo "[*] Installing GhostOS ISO Builder to $INSTALL_DIR..."

# Create directories
mkdir -p "$INSTALL_DIR"
mkdir -p "$BIN_DIR"
mkdir -p "$DESKTOP_DIR"
mkdir -p "$ICON_DIR"

# Copy application files
echo "[*] Copying application files..."
cp -r . "$INSTALL_DIR/"
chmod +x "$INSTALL_DIR/main.py"

# Install Python dependencies
echo "[*] Installing Python dependencies..."
pip3 install -r "$INSTALL_DIR/requirements.txt" || {
    echo "⚠️  Warning: Failed to install some dependencies"
    echo "    You may need to install them manually"
}

# Create launcher script
echo "[*] Creating launcher script..."
cat > "$BIN_DIR/ghostos-builder" << 'EOF'
#!/bin/bash
# GhostOS ISO Builder Launcher

# Check if running with required privileges
if [ "$EUID" -ne 0 ]; then
    # Try to elevate with pkexec (GUI) or sudo (terminal)
    if command -v pkexec &> /dev/null; then
        pkexec env DISPLAY=$DISPLAY XAUTHORITY=$XAUTHORITY /opt/ghostos-builder/main.py "$@"
    else
        sudo /opt/ghostos-builder/main.py "$@"
    fi
else
    /opt/ghostos-builder/main.py "$@"
fi
EOF

chmod +x "$BIN_DIR/ghostos-builder"

# Create desktop entry
echo "[*] Creating desktop entry..."
cat > "$DESKTOP_DIR/ghostos-builder.desktop" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=GhostOS ISO Builder
GenericName=ISO Builder and Customizer
Comment=Build custom GhostOS ISOs with multi-source support and theme customization
Exec=ghostos-builder
Icon=ghostos-builder
Terminal=false
Categories=System;Development;Utility;
Keywords=iso;builder;ghostos;debian;linux;customization;
StartupNotify=true
EOF

# Create icon (placeholder - would use actual icon in production)
echo "[*] Creating application icon..."
cat > "$ICON_DIR/ghostos-builder.svg" << 'EOF'
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
cat > "$BIN_DIR/ghostos-keyboard" << 'KEYBOARD_EOF'
#!/usr/bin/env python3
"""Standalone Touchscreen Keyboard Launcher"""
import sys
sys.path.insert(0, '/opt/ghostos-builder')

from PyQt6.QtWidgets import QApplication
from ui.touchscreen_keyboard import TouchscreenKeyboard

def main():
    app = QApplication(sys.argv)
    app.setApplicationName("GhostOS Touchscreen Keyboard")
    
    keyboard = TouchscreenKeyboard()
    keyboard.show_keyboard()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
KEYBOARD_EOF

chmod +x "$BIN_DIR/ghostos-keyboard"

# Create keyboard desktop entry
echo "[*] Creating keyboard desktop entry..."
cat > "$DESKTOP_DIR/ghostos-keyboard.desktop" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=GhostOS Touchscreen Keyboard
GenericName=Virtual Keyboard
Comment=Touchscreen keyboard with calibration support
Exec=ghostos-keyboard
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
# GhostOS ISO Builder - Uninstaller

if [ "$EUID" -ne 0 ]; then 
    echo "Must run as root: sudo $0"
    exit 1
fi

echo "Removing GhostOS ISO Builder..."

rm -rf /opt/ghostos-builder
rm -f /usr/local/bin/ghostos-builder
rm -f /usr/local/bin/ghostos-keyboard
rm -f /usr/share/applications/ghostos-builder.desktop
rm -f /usr/share/applications/ghostos-keyboard.desktop
rm -f /usr/share/icons/hicolor/256x256/apps/ghostos-builder.svg

update-desktop-database /usr/share/applications 2>/dev/null || true

echo "✓ GhostOS ISO Builder has been uninstalled"
UNINSTALL_EOF

chmod +x "$INSTALL_DIR/uninstall.sh"

echo ""
echo "=========================================="
echo "  ✓ Installation Complete!"
echo "=========================================="
echo ""
echo "GhostOS ISO Builder has been installed to:"
echo "  • Application: $INSTALL_DIR"
echo "  • Launcher: $BIN_DIR/ghostos-builder"
echo "  • Keyboard: $BIN_DIR/ghostos-keyboard"
echo "  • Desktop Entry: $DESKTOP_DIR/ghostos-builder.desktop"
echo "  • Keyboard Entry: $DESKTOP_DIR/ghostos-keyboard.desktop"
echo ""
echo "You can now:"
echo "  • Run GUI: ghostos-builder"
echo "  • Run keyboard standalone: ghostos-keyboard"
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
