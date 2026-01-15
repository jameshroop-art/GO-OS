#!/bin/bash
# ============================================
# HeckOS Installation Setup Launcher
# First step in the installation process
# Launches device type selection GUI
# ============================================
# LICENSE: MIT (see LICENSE file in repository root)
# 
# LEGAL NOTICE:
# This script is part of HeckOS, a derivative work based on Debian 12 (Bookworm).
# NOT an official Debian release. See LEGAL_COMPLIANCE.md.
# ============================================

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SETUP_SCRIPT="$SCRIPT_DIR/ghostos-installation-setup.py"

echo "========================================"
echo "  👻 HeckOS Installation Setup"
echo "  Device Type Selection"
echo "========================================"
echo ""

# Check if running as root (optional but recommended)
if [ "$EUID" -ne 0 ]; then 
    echo "ℹ️  Not running as root"
    echo "   Root privileges may be needed for some installation types"
    echo ""
fi

# Check dependencies
echo "[*] Checking dependencies..."

MISSING_DEPS=()

# Check Python
if ! command -v python3 &> /dev/null; then
    MISSING_DEPS+=("python3")
fi

# Check tkinter
if ! python3 -c "import tkinter" 2>/dev/null; then
    MISSING_DEPS+=("python3-tk")
fi

# Install missing dependencies
if [ ${#MISSING_DEPS[@]} -gt 0 ]; then
    echo ""
    echo "Missing dependencies: ${MISSING_DEPS[*]}"
    echo ""
    
    if [ "$EUID" -ne 0 ]; then
        echo "⚠️  Root privileges required to install dependencies"
        read -p "Run with sudo to install? (y/n): " response
        if [ "$response" = "y" ]; then
            exec sudo "$0" "$@"
        else
            echo "❌ Cannot continue without dependencies"
            exit 1
        fi
    fi
    
    if [ -f /etc/debian_version ]; then
        # Debian/Ubuntu
        echo "[*] Installing dependencies..."
        apt-get update
        apt-get install -y python3 python3-tk
    elif [ -f /etc/redhat-release ]; then
        # RedHat/Fedora/CentOS
        echo "[*] Installing dependencies..."
        dnf install -y python3 python3-tkinter
    elif [ -f /etc/arch-release ]; then
        # Arch Linux
        echo "[*] Installing dependencies..."
        pacman -Sy --noconfirm python python-tk
    else
        echo "❌ Unable to auto-install dependencies"
        echo "   Please install: python3 python3-tk"
        exit 1
    fi
fi

echo "[✓] All dependencies satisfied"
echo ""

# Launch GUI
echo "[*] Launching Installation Setup..."
echo ""

if [ ! -f "$SETUP_SCRIPT" ]; then
    echo "❌ Error: Setup script not found at $SETUP_SCRIPT"
    exit 1
fi

# Make executable
chmod +x "$SETUP_SCRIPT"

# Launch
if [ -n "$DISPLAY" ] || [ -n "$WAYLAND_DISPLAY" ]; then
    python3 "$SETUP_SCRIPT"
else
    echo "❌ Error: No graphical display detected"
    echo "   Please run from a desktop environment"
    exit 1
fi
