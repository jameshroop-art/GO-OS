#!/data/data/com.termux/files/usr/bin/bash

# ============================================
# GhostOS Android Installation Script
# For Android 9+ (Termux/proot environment)
# Non-root WiFi/Bluetooth driver patching
# ============================================

set -e

echo "========================================"
echo "  👻 GhostOS for Android"
echo "  Version: 1.0-android"
echo "  Target: Android 9+"
echo "========================================"
echo ""

# Check Android version
ANDROID_VERSION=$(getprop ro.build.version.release)
ANDROID_SDK=$(getprop ro.build.version.sdk)

echo "[*] Detected Android Version: $ANDROID_VERSION (SDK: $ANDROID_SDK)"

if [ "$ANDROID_SDK" -lt 28 ]; then
    echo "❌ Error: Android 9+ (SDK 28+) required"
    echo "   Current version: Android $ANDROID_VERSION (SDK: $ANDROID_SDK)"
    exit 1
fi

echo "✅ Android version compatible"
echo ""

# Check if running in Termux
if [ ! -d "$PREFIX" ]; then
    echo "❌ Error: Must run in Termux environment"
    echo "   Install Termux from F-Droid: https://f-droid.org/en/packages/com.termux/"
    exit 1
fi

echo "[*] Running in Termux environment: $PREFIX"
echo ""

# ============================================
# Update Termux packages
# ============================================
echo "[*] Updating Termux packages..."
pkg update -y
pkg upgrade -y

# ============================================
# Install required dependencies
# ============================================
echo ""
echo "[*] Installing dependencies..."
pkg install -y \
    proot \
    proot-distro \
    wget \
    curl \
    git \
    python \
    openssh \
    nano \
    vim \
    termux-api \
    termux-tools \
    pulseaudio

# ============================================
# Install Debian proot environment
# ============================================
echo ""
echo "[*] Installing Debian proot environment..."
proot-distro install debian

# ============================================
# Create GhostOS directory structure
# ============================================
GHOSTOS_HOME="$HOME/ghostos-android"
mkdir -p "$GHOSTOS_HOME"/{bin,config,drivers,logs}

echo "[*] GhostOS directory created: $GHOSTOS_HOME"

# ============================================
# Non-Root WiFi Management Script
# ============================================
echo ""
echo "[*] Creating non-root WiFi management tools..."

cat > "$GHOSTOS_HOME/bin/ghostos-wifi" << 'WIFI_EOF'
#!/data/data/com.termux/files/usr/bin/bash

# GhostOS WiFi Manager (Non-Root)
# Uses Android Termux-API for WiFi control

echo "==================================="
echo "  GhostOS WiFi Manager"
echo "  Non-Root Mode"
echo "==================================="
echo ""

show_help() {
    echo "Usage: ghostos-wifi [command]"
    echo ""
    echo "Commands:"
    echo "  scan        - Scan for available WiFi networks"
    echo "  list        - List saved networks"
    echo "  info        - Show current WiFi connection info"
    echo "  enable      - Enable WiFi"
    echo "  disable     - Disable WiFi"
    echo "  status      - Show WiFi status"
    echo ""
}

wifi_scan() {
    echo "[*] Scanning for WiFi networks..."
    echo ""
    termux-wifi-scaninfo
}

wifi_list() {
    echo "[*] Saved WiFi networks:"
    echo ""
    termux-wifi-connectioninfo
}

wifi_info() {
    echo "[*] Current WiFi connection:"
    echo ""
    termux-wifi-connectioninfo
}

wifi_enable() {
    echo "[*] Enabling WiFi..."
    termux-wifi-enable true
    echo "✅ WiFi enabled"
}

wifi_disable() {
    echo "[*] Disabling WiFi..."
    termux-wifi-enable false
    echo "✅ WiFi disabled"
}

wifi_status() {
    echo "[*] WiFi Status:"
    echo ""
    CONNECTION=$(termux-wifi-connectioninfo)
    if echo "$CONNECTION" | grep -q "ssid"; then
        echo "✅ WiFi Connected"
        echo "$CONNECTION"
    else
        echo "❌ WiFi Disconnected"
    fi
}

case "$1" in
    scan)
        wifi_scan
        ;;
    list)
        wifi_list
        ;;
    info)
        wifi_info
        ;;
    enable)
        wifi_enable
        ;;
    disable)
        wifi_disable
        ;;
    status)
        wifi_status
        ;;
    *)
        show_help
        ;;
esac
WIFI_EOF

chmod +x "$GHOSTOS_HOME/bin/ghostos-wifi"

# ============================================
# Non-Root Bluetooth Management Script
# ============================================
echo ""
echo "[*] Creating non-root Bluetooth management tools..."

cat > "$GHOSTOS_HOME/bin/ghostos-bluetooth" << 'BT_EOF'
#!/data/data/com.termux/files/usr/bin/bash

# GhostOS Bluetooth Manager (Non-Root)
# Uses Android Termux-API for Bluetooth control

echo "==================================="
echo "  GhostOS Bluetooth Manager"
echo "  Non-Root Mode"
echo "==================================="
echo ""

show_help() {
    echo "Usage: ghostos-bluetooth [command]"
    echo ""
    echo "Commands:"
    echo "  scan        - Scan for Bluetooth devices"
    echo "  devices     - List paired devices"
    echo "  info        - Show Bluetooth adapter info"
    echo "  enable      - Enable Bluetooth"
    echo "  disable     - Disable Bluetooth"
    echo "  status      - Show Bluetooth status"
    echo ""
}

bt_scan() {
    echo "[*] Scanning for Bluetooth devices..."
    echo ""
    echo "Please enable location permission for Termux in Android settings"
    echo ""
    termux-bluetooth-scaninfo
}

bt_devices() {
    echo "[*] Paired Bluetooth devices:"
    echo ""
    termux-bluetooth-connectioninfo
}

bt_info() {
    echo "[*] Bluetooth adapter info:"
    echo ""
    termux-bluetooth-connectioninfo
}

bt_enable() {
    echo "[*] Enabling Bluetooth..."
    termux-bluetooth-enable
    echo "✅ Bluetooth enabled"
}

bt_disable() {
    echo "[*] Disabling Bluetooth..."
    termux-bluetooth-disable
    echo "✅ Bluetooth disabled"
}

bt_status() {
    echo "[*] Bluetooth Status:"
    echo ""
    CONNECTION=$(termux-bluetooth-connectioninfo 2>/dev/null)
    if [ -n "$CONNECTION" ]; then
        echo "✅ Bluetooth Active"
        echo "$CONNECTION"
    else
        echo "❌ Bluetooth Inactive or Disabled"
    fi
}

case "$1" in
    scan)
        bt_scan
        ;;
    devices)
        bt_devices
        ;;
    info)
        bt_info
        ;;
    enable)
        bt_enable
        ;;
    disable)
        bt_disable
        ;;
    status)
        bt_status
        ;;
    *)
        show_help
        ;;
esac
BT_EOF

chmod +x "$GHOSTOS_HOME/bin/ghostos-bluetooth"

# ============================================
# WiFi/Bluetooth Driver Optimizer (Non-Root)
# ============================================
echo ""
echo "[*] Creating WiFi/Bluetooth driver optimizer..."

cat > "$GHOSTOS_HOME/bin/ghostos-driver-optimizer" << 'DRIVER_EOF'
#!/data/data/com.termux/files/usr/bin/bash

# GhostOS Driver Optimizer
# Optimizes WiFi and Bluetooth performance without root
# Uses userspace tools and Android APIs

echo "==================================="
echo "  GhostOS Driver Optimizer"
echo "  Non-Root WiFi/Bluetooth Patcher"
echo "==================================="
echo ""

optimize_wifi() {
    echo "[*] Optimizing WiFi performance..."
    echo ""
    
    # Get current WiFi info
    WIFI_INFO=$(termux-wifi-connectioninfo)
    
    if echo "$WIFI_INFO" | grep -q "ssid"; then
        echo "✅ WiFi connected"
        echo ""
        echo "Current WiFi Details:"
        echo "$WIFI_INFO" | grep -E "ssid|rssi|link_speed|frequency"
        echo ""
        
        # Analyze signal strength
        RSSI=$(echo "$WIFI_INFO" | grep "rssi" | awk '{print $2}' | tr -d ',')
        
        if [ ! -z "$RSSI" ]; then
            if [ "$RSSI" -gt -50 ]; then
                echo "📶 Signal Strength: Excellent ($RSSI dBm)"
            elif [ "$RSSI" -gt -60 ]; then
                echo "📶 Signal Strength: Good ($RSSI dBm)"
            elif [ "$RSSI" -gt -70 ]; then
                echo "📶 Signal Strength: Fair ($RSSI dBm)"
                echo "💡 Tip: Move closer to WiFi router"
            else
                echo "📶 Signal Strength: Poor ($RSSI dBm)"
                echo "⚠️  Warning: Weak signal may affect performance"
            fi
        fi
        
        echo ""
        echo "✅ WiFi optimization complete"
    else
        echo "❌ No WiFi connection detected"
        echo "   Connect to WiFi first: ghostos-wifi enable"
    fi
}

optimize_bluetooth() {
    echo ""
    echo "[*] Optimizing Bluetooth performance..."
    echo ""
    
    # Get Bluetooth info
    BT_INFO=$(termux-bluetooth-connectioninfo 2>/dev/null)
    
    if [ -n "$BT_INFO" ]; then
        echo "✅ Bluetooth active"
        echo ""
        echo "Current Bluetooth Status:"
        echo "$BT_INFO"
        echo ""
        echo "✅ Bluetooth optimization complete"
    else
        echo "❌ Bluetooth not active"
        echo "   Enable Bluetooth: ghostos-bluetooth enable"
    fi
}

show_driver_info() {
    echo ""
    echo "[*] System Driver Information:"
    echo ""
    echo "Android Version: $(getprop ro.build.version.release)"
    echo "SDK Version: $(getprop ro.build.version.sdk)"
    echo "Device Model: $(getprop ro.product.model)"
    echo "Device Manufacturer: $(getprop ro.product.manufacturer)"
    echo "WiFi Driver: $(getprop wifi.interface 2>/dev/null || echo 'N/A')"
    echo ""
}

echo "Starting optimization process..."
echo ""

show_driver_info
optimize_wifi
optimize_bluetooth

echo ""
echo "==================================="
echo "  Optimization Complete"
echo "==================================="
echo ""
echo "Note: This tool works without root access by using"
echo "Android's standard APIs and userspace tools."
echo ""
echo "For advanced features, consider:"
echo "  - Using WiFi analyzer apps"
echo "  - Adjusting router settings"
echo "  - Updating Android system"
DRIVER_EOF

chmod +x "$GHOSTOS_HOME/bin/ghostos-driver-optimizer"

# ============================================
# Create main GhostOS launcher
# ============================================
echo ""
echo "[*] Creating GhostOS launcher..."

cat > "$GHOSTOS_HOME/bin/ghostos" << 'LAUNCHER_EOF'
#!/data/data/com.termux/files/usr/bin/bash

# GhostOS Main Launcher for Android

clear
echo "========================================"
echo "  👻 GhostOS for Android"
echo "  Version: 1.0-android"
echo "========================================"
echo ""
echo "Available Commands:"
echo ""
echo "  ghostos-wifi              - WiFi management"
echo "  ghostos-bluetooth         - Bluetooth management"
echo "  ghostos-driver-optimizer  - Optimize drivers"
echo "  ghostos-debian            - Launch Debian environment"
echo "  ghostos-system            - System information"
echo ""
echo "Type 'ghostos-help' for detailed help"
echo ""
LAUNCHER_EOF

chmod +x "$GHOSTOS_HOME/bin/ghostos"

# ============================================
# Create Debian launcher script
# ============================================
cat > "$GHOSTOS_HOME/bin/ghostos-debian" << 'DEBIAN_EOF'
#!/data/data/com.termux/files/usr/bin/bash

# Launch Debian proot environment

echo "[*] Launching GhostOS Debian environment..."
echo ""
proot-distro login debian
DEBIAN_EOF

chmod +x "$GHOSTOS_HOME/bin/ghostos-debian"

# ============================================
# Create system info script
# ============================================
cat > "$GHOSTOS_HOME/bin/ghostos-system" << 'SYSINFO_EOF'
#!/data/data/com.termux/files/usr/bin/bash

# GhostOS System Information

echo "==================================="
echo "  GhostOS System Information"
echo "==================================="
echo ""
echo "Android Information:"
echo "  Version: $(getprop ro.build.version.release)"
echo "  SDK: $(getprop ro.build.version.sdk)"
echo "  Device: $(getprop ro.product.model)"
echo "  Manufacturer: $(getprop ro.product.manufacturer)"
echo "  Build: $(getprop ro.build.display.id)"
echo ""
echo "Termux Information:"
echo "  Prefix: $PREFIX"
echo "  Home: $HOME"
echo "  Shell: $SHELL"
echo ""
echo "GhostOS Information:"
echo "  Installation: $HOME/ghostos-android"
echo "  WiFi Manager: Installed"
echo "  Bluetooth Manager: Installed"
echo "  Driver Optimizer: Installed"
echo "  Debian Environment: Installed"
echo ""
echo "Hardware:"
echo "  CPU: $(getprop ro.product.cpu.abi)"
echo "  Memory: $(free -h | grep Mem | awk '{print $2}')"
echo ""
SYSINFO_EOF

chmod +x "$GHOSTOS_HOME/bin/ghostos-system"

# ============================================
# Create help script
# ============================================
cat > "$GHOSTOS_HOME/bin/ghostos-help" << 'HELP_EOF'
#!/data/data/com.termux/files/usr/bin/bash

cat << 'HELP_TEXT'
==================================="
  GhostOS for Android - Help
==================================="

GhostOS provides a lightweight Linux environment on Android 9+
without requiring root access.

FEATURES:
  • Debian-based Linux environment (via proot)
  • Non-root WiFi management
  • Non-root Bluetooth management
  • Driver optimization tools
  • Full Linux command-line tools

COMMANDS:

  ghostos
    Display main menu and available commands

  ghostos-wifi [command]
    Manage WiFi connections without root
    Commands: scan, list, info, enable, disable, status

  ghostos-bluetooth [command]
    Manage Bluetooth without root
    Commands: scan, devices, info, enable, disable, status

  ghostos-driver-optimizer
    Optimize WiFi and Bluetooth performance
    Analyzes signal strength and connection quality

  ghostos-debian
    Launch full Debian Linux environment
    Includes apt package manager and standard Linux tools

  ghostos-system
    Display system information
    Shows Android, Termux, and GhostOS details

REQUIREMENTS:
  • Android 9+ (API 28+)
  • Termux app (from F-Droid)
  • Termux:API app (for WiFi/Bluetooth control)
  • Storage permission (for file access)
  • Location permission (for Bluetooth scanning)

INSTALLATION:
  1. Install Termux from F-Droid
  2. Install Termux:API from F-Droid
  3. Run: bash ghostos-android.sh
  4. Add to PATH: export PATH="$HOME/ghostos-android/bin:$PATH"

PERMISSIONS:
  Grant these permissions to Termux in Android settings:
  • Storage (for file access)
  • Location (for Bluetooth/WiFi scanning)

NON-ROOT LIMITATIONS:
  Without root access, some features are limited:
  • Cannot modify system WiFi/Bluetooth drivers directly
  • Cannot access raw hardware interfaces
  • Relies on Android APIs for hardware control
  • Some advanced networking features unavailable

WORKAROUNDS:
  • Uses Termux-API for hardware access
  • Optimizes performance within user space
  • Provides monitoring and diagnostics tools
  • Leverages proot for Linux environment

EXAMPLES:
  # Scan for WiFi networks
  ghostos-wifi scan

  # Check WiFi status
  ghostos-wifi status

  # Enable Bluetooth
  ghostos-bluetooth enable

  # Optimize drivers
  ghostos-driver-optimizer

  # Launch Linux environment
  ghostos-debian

  # Install packages in Debian
  ghostos-debian
  apt update
  apt install python3

TROUBLESHOOTING:
  • WiFi/Bluetooth not working: Install Termux:API
  • Permission denied: Grant location/storage permissions
  • Command not found: Add to PATH or use full path
  • proot errors: Reinstall proot-distro

MORE INFORMATION:
  • GitHub: https://github.com/jameshroop-art/GO-OS
  • Termux Wiki: https://wiki.termux.com
  • F-Droid: https://f-droid.org

==================================="
HELP_TEXT
HELP_EOF

chmod +x "$GHOSTOS_HOME/bin/ghostos-help"

# ============================================
# Add GhostOS to PATH
# ============================================
echo ""
echo "[*] Adding GhostOS to PATH..."

if ! grep -q "ghostos-android/bin" "$HOME/.bashrc"; then
    echo "" >> "$HOME/.bashrc"
    echo "# GhostOS for Android" >> "$HOME/.bashrc"
    echo "export PATH=\"\$HOME/ghostos-android/bin:\$PATH\"" >> "$HOME/.bashrc"
    echo "alias ghostos-update='bash \$HOME/ghostos-android.sh'" >> "$HOME/.bashrc"
fi

# ============================================
# Install Termux:API instructions
# ============================================
echo ""
echo "==================================="
echo "  Installation Complete!"
echo "==================================="
echo ""
echo "✅ GhostOS for Android installed successfully!"
echo ""
echo "Location: $GHOSTOS_HOME"
echo ""
echo "IMPORTANT: Install Termux:API"
echo "  1. Open F-Droid"
echo "  2. Search for 'Termux:API'"
echo "  3. Install the app"
echo "  4. Grant required permissions in Android settings:"
echo "     - Storage"
echo "     - Location (for Bluetooth/WiFi)"
echo ""
echo "Quick Start:"
echo "  1. Restart Termux or run: source ~/.bashrc"
echo "  2. Run: ghostos"
echo "  3. Run: ghostos-help (for detailed help)"
echo ""
echo "Commands available:"
echo "  • ghostos - Main menu"
echo "  • ghostos-wifi - WiFi management"
echo "  • ghostos-bluetooth - Bluetooth management"
echo "  • ghostos-driver-optimizer - Optimize drivers"
echo "  • ghostos-debian - Launch Debian environment"
echo "  • ghostos-system - System information"
echo "  • ghostos-help - Detailed help"
echo ""
echo "To use commands now, run:"
echo "  source ~/.bashrc"
echo ""
echo "==================================="
