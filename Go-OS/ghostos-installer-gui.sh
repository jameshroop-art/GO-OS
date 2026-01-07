#!/bin/bash
# ============================================
# Heck-CheckOS GUI Installer Launcher
# Launches the Python GUI for USB creation and disk partitioning
# ============================================
# LICENSE: MIT (see LICENSE file in repository root)
# 
# LEGAL NOTICE:
# This script is part of Heck-CheckOS, a derivative work based on Debian 12 (Bookworm).
# NOT an official Debian release. See LEGAL_COMPLIANCE.md.
# ============================================

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
GUI_SCRIPT="$SCRIPT_DIR/heckcheckos-installer-gui.py"

echo "========================================"
echo "  👻 Heck-CheckOS Security Edition"
echo "  GUI Installer & USB Creator"
echo "========================================"
echo ""

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    echo "⚠️  Not running as root"
    echo "   Some features require root privileges"
    echo ""
    read -p "Run as root (sudo)? (y/n): " response
    if [ "$response" = "y" ]; then
        exec sudo "$0" "$@"
    fi
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

# Check required tools
for tool in lsblk parted dd sync wipefs partprobe rsync; do
    if ! command -v $tool &> /dev/null; then
        MISSING_DEPS+=("$tool")
    fi
done

# Install missing dependencies
if [ ${#MISSING_DEPS[@]} -gt 0 ]; then
    echo ""
    echo "Missing dependencies: ${MISSING_DEPS[*]}"
    echo ""
    
    if [ -f /etc/debian_version ]; then
        # Debian/Ubuntu
        echo "[*] Installing dependencies..."
        apt-get update
        apt-get install -y python3 python3-tk parted coreutils util-linux rsync dosfstools
    elif [ -f /etc/redhat-release ]; then
        # RedHat/Fedora/CentOS
        echo "[*] Installing dependencies..."
        dnf install -y python3 python3-tkinter parted coreutils util-linux rsync dosfstools
    elif [ -f /etc/arch-release ]; then
        # Arch Linux
        echo "[*] Installing dependencies..."
        pacman -Sy --noconfirm python python-tk parted coreutils util-linux rsync dosfstools
    else
        echo "❌ Unable to auto-install dependencies"
        echo "   Please install: python3 python3-tk parted rsync dosfstools"
        exit 1
    fi
fi

echo "[✓] All dependencies satisfied"
echo ""

# Check for filesystem tools
echo "[*] Checking filesystem tools..."

FS_TOOLS=(
    "mkfs.ext4:e2fsprogs"
    "mkfs.ext3:e2fsprogs"
    "mkfs.ntfs:ntfs-3g"
    "mkfs.vfat:dosfstools"
    "mkfs.exfat:exfat-utils"
    "mkfs.btrfs:btrfs-progs"
    "mkfs.xfs:xfsprogs"
    "mkfs.f2fs:f2fs-tools"
    "mkfs.jfs:jfsutils"
    "mkfs.reiserfs:reiserfsprogs"
    "mkswap:util-linux"
)

MISSING_FS=()

for entry in "${FS_TOOLS[@]}"; do
    tool="${entry%%:*}"
    package="${entry##*:}"
    
    if ! command -v "$tool" &> /dev/null; then
        MISSING_FS+=("$package")
    fi
done

if [ ${#MISSING_FS[@]} -gt 0 ]; then
    echo ""
    echo "⚠️  Some filesystem tools are missing:"
    for pkg in "${MISSING_FS[@]}"; do
        echo "   - $pkg"
    done
    echo ""
    read -p "Install filesystem tools? (y/n): " response
    if [ "$response" = "y" ]; then
        if [ -f /etc/debian_version ]; then
            apt-get install -y "${MISSING_FS[@]}"
        elif [ -f /etc/redhat-release ]; then
            dnf install -y "${MISSING_FS[@]}"
        elif [ -f /etc/arch-release ]; then
            pacman -Sy --noconfirm "${MISSING_FS[@]}"
        fi
    fi
fi

echo "[✓] Filesystem tools check complete"
echo ""

# Launch GUI
echo "[*] Launching Heck-CheckOS Installer GUI..."
echo ""

if [ ! -f "$GUI_SCRIPT" ]; then
    echo "❌ Error: GUI script not found at $GUI_SCRIPT"
    exit 1
fi

# Make executable
chmod +x "$GUI_SCRIPT"

# Launch
if [ -n "$DISPLAY" ] || [ -n "$WAYLAND_DISPLAY" ]; then
    python3 "$GUI_SCRIPT"
else
    echo "❌ Error: No graphical display detected"
    echo "   Please run from a desktop environment"
    exit 1
fi
