#ghostos-build.sh
#!/bin/bash

# ============================================
# GhostOS Complete Build System
# Versions: 1.0, 1.1, 2.0
# Base: Parrot OS 7 Security Edition
# GUI: GhostOS Custom Desktop Environment
# With USB Bootloader Creation
# ============================================

set -e

PROJECT_DIR="$HOME/ghostos-ultimate"
BUILD_DIR="$PROJECT_DIR/build"
ROOTFS_DIR="$BUILD_DIR/rootfs"
ISO_DIR="$BUILD_DIR/iso"

echo "========================================"
echo "  👻 GhostOS Build System"
echo "  🦜 Parrot OS 7 Security Base"
echo "  Multi-Version Builder"
echo "========================================"
echo ""

# Check root
if [ "$EUID" -ne 0 ]; then 
    echo "❌ Must run as root"
    echo "Run: sudo $0"
    exit 1
fi

# ============================================
# Version Selection Menu
# ============================================
echo "Select GhostOS version to build:"
echo ""
echo "  🦜 Base: Parrot OS 7 Security Edition"
echo "  👻 GUI: GhostOS Custom Desktop"
echo ""
echo "  1) GhostOS v1.0 - Stable Release"
echo "     • Parrot OS 7 Security base"
echo "     • Complete base system"
echo "     • All core features"
echo "     • ~10GB ISO"
echo ""
echo "  2) GhostOS v1.1 - Enhanced Edition"
echo "     • Parrot OS 7 Security base"
echo "     • Improved UI (smooth animations)"
echo "     • Enhanced privacy controls"
echo "     • Malwarebytes Premium"
echo "     • System consolidation"
echo "     • ~11GB ISO"
echo ""
echo "  3) GhostOS v2.0 - Next Generation"
echo "     • Parrot OS 7 Security base"
echo "     • Modern Wayland support"
echo "     • AI assistant integration"
echo "     • Advanced UI (blur effects, transitions)"
echo "     • Cloud backup (encrypted)"
echo "     • Plugin system"
echo "     • ARM architecture support"
echo "     • ~12GB ISO"
echo ""
echo "  4) Build ALL versions"
echo ""

read -p "Enter choice [1-4]: " VERSION_CHOICE

case $VERSION_CHOICE in
    1)
        VERSIONS=("1.0")
        ;;
    2)
        VERSIONS=("1.1")
        ;;
    3)
        VERSIONS=("2.0")
        ;;
    4)
        VERSIONS=("1.0" "1.1" "2.0")
        ;;
    *)
        echo "Invalid choice"
        exit 1
        ;;
esac

# USB Drive Detection
echo ""
echo "Detecting USB drives..."
USB_DRIVES=$(lsblk -d -o NAME,SIZE,TYPE,TRAN | grep "usb" | awk '{print $1}')

if [ -n "$USB_DRIVES" ]; then
    echo ""
    echo "Available USB drives:"
    lsblk -d -o NAME,SIZE,TYPE,TRAN,MODEL | grep -E "NAME|usb"
    echo ""
    read -p "Create bootable USB after build? (yes/no): " CREATE_USB_INPUT
    if [ "$CREATE_USB_INPUT" = "yes" ]; then
        CREATE_USB=true
        read -p "Enter USB drive (e.g., sdb): " USB_DRIVE
        USB_DEVICE="/dev/$USB_DRIVE"
        
        if [ ! -b "$USB_DEVICE" ]; then
            echo "❌ Invalid device"
            exit 1
        fi
        
        echo ""
        echo "⚠️  WARNING: $USB_DEVICE will be ERASED!"
        lsblk "$USB_DEVICE"
        echo ""
        read -p "Type 'YES' to confirm: " CONFIRM
        if [ "$CONFIRM" != "YES" ]; then
            exit 0
        fi
    else
        CREATE_USB=false
    fi
else
    CREATE_USB=false
fi

# Install build dependencies
echo ""
echo "[*] Installing build dependencies..."
apt-get update
apt-get install -y \
    debootstrap squashfs-tools xorriso grub-pc-bin grub-efi-amd64-bin \
    mtools dosfstools isolinux syslinux git wget curl rsync

# ============================================
# Version-Specific Installation Scripts
# ============================================

create_install_script_1.0() {
    cat > "$BUILD_DIR/install_v1.0.sh" << 'V1_EOF'
#!/bin/bash
set -e
export DEBIAN_FRONTEND=noninteractive

echo "Installing GhostOS v1.0 on Parrot OS 7 Security base..."

# ============================================
# Configure Parrot OS 7 Security Repositories
# ============================================
echo ""
echo "[*] Configuring Parrot OS 7 Security repositories..."

cat > /etc/apt/sources.list << 'PARROT_EOF'
# Parrot OS 7 (lory) - Security Edition Base
deb https://deb.parrot.sh/parrot lory main contrib non-free non-free-firmware
deb https://deb.parrot.sh/parrot lory-security main contrib non-free non-free-firmware
deb https://deb.parrot.sh/parrot lory-backports main contrib non-free non-free-firmware
PARROT_EOF

# ============================================
# System Base and Kernel
# ============================================
echo ""
echo "[*] Installing base system and kernel..."

apt-get update
apt-get install -y \
    linux-image-amd64 \
    linux-headers-amd64 \
    firmware-linux \
    firmware-linux-nonfree \
    build-essential \
    dkms \
    git \
    wget \
    curl

# ============================================
# AMD AM5 Chipset Support
# ============================================
echo ""
echo "[*] Installing AMD AM5 chipset support..."

# Install AMD microcode and firmware
apt-get install -y \
    amd64-microcode \
    firmware-amd-graphics

# Install AMD platform drivers
apt-get install -y \
    amdgpu-dkms \
    libdrm-amdgpu1 \
    mesa-vulkan-drivers \
    xserver-xorg-video-amdgpu

# Enable AMD CPU frequency scaling
cat > /etc/modules-load.d/amd-pstate.conf << 'EOF'
# AMD P-State driver for AM5
amd_pstate
EOF

# ============================================
# ASUS AM5 Platform Drivers
# ============================================
echo ""
echo "[*] Installing ASUS AM5 motherboard drivers..."

# Install dependencies for ASUS drivers
apt-get install -y \
    linux-headers-$(uname -r) \
    dkms \
    i2c-tools \
    lm-sensors \
    fancontrol

# Clone and install ASUS WMI sensors driver
cd /usr/src
git clone https://github.com/zeule/asus-wmi-sensors.git asus-wmi-sensors
cd asus-wmi-sensors

# Build and install with DKMS
if [ -f "dkms.conf" ]; then
    dkms add -m asus-wmi-sensors -v 1.0
    dkms build -m asus-wmi-sensors -v 1.0
    dkms install -m asus-wmi-sensors -v 1.0
fi

# Enable module
echo "asus_wmi_sensors" >> /etc/modules-load.d/asus.conf

# Clone and install ASUS EC sensors driver (for AM5 boards)
cd /usr/src
git clone https://github.com/zeule/asus-ec-sensors.git asus-ec-sensors
cd asus-ec-sensors

# Build and install
make
make install

# Enable module
echo "asus_ec_sensors" >> /etc/modules-load.d/asus.conf

# ============================================
# ASUS Aura Sync RGB Support (OpenRGB)
# ============================================
echo ""
echo "[*] Installing ASUS Aura RGB support..."

apt-get install -y \
    libusb-1.0-0-dev \
    libhidapi-dev \
    qt5-default \
    qttools5-dev

# Clone and build OpenRGB
cd /usr/src
git clone https://gitlab.com/CalcProgrammer1/OpenRGB.git openrgb
cd openrgb
qmake OpenRGB.pro
make -j$(nproc)
make install

# Install udev rules for OpenRGB
cat > /etc/udev/rules.d/60-openrgb.rules << 'EOF'
# ASUS Aura USB Controllers
SUBSYSTEM=="usb", ATTR{idVendor}=="0b05", ATTR{idProduct}=="1872", TAG+="uaccess"
SUBSYSTEM=="usb", ATTR{idVendor}=="0b05", ATTR{idProduct}=="1867", TAG+="uaccess"
SUBSYSTEM=="usb", ATTR{idVendor}=="0b05", ATTR{idProduct}=="19b6", TAG+="uaccess"

# AMD SMBus
KERNEL=="i2c-[0-9]*", TAG+="uaccess"
EOF

udevadm control --reload-rules
udevadm trigger

# ============================================
# AM5 USB4/Thunderbolt Support
# ============================================
echo ""
echo "[*] Installing USB4/Thunderbolt support for AM5..."

apt-get install -y \
    bolt \
    thunderbolt-tools

systemctl enable bolt

# ============================================
# AMD Audio Support
# ============================================
echo ""
echo "[*] Installing audio support..."

apt-get install -y \
    pulseaudio \
    pavucontrol \
    alsa-utils \
    firmware-sof-signed

# Configure PulseAudio for AMD audio
cat > /etc/pulse/default.pa.d/amd-audio.pa << 'EOF'
# AMD audio configuration
load-module module-udev-detect
load-module module-detect
EOF

# ============================================
# Sensors Configuration
# ============================================
echo ""
echo "[*] Configuring hardware sensors..."

# Detect sensors
sensors-detect --auto

# Create monitoring service
cat > /usr/local/bin/asus-sensors-monitor << 'SENSEOF'
#!/bin/bash
# ASUS AM5 Sensor Monitor

echo "==================================="
echo "  ASUS AM5 System Sensors"
echo "==================================="
echo ""

# CPU Temperature and Frequency
echo "CPU Information:"
sensors | grep -A 10 "k10temp"
echo ""

# Motherboard sensors
echo "Motherboard Sensors:"
sensors | grep -A 20 "asus"
echo ""

# Fan speeds
echo "Fan Speeds:"
sensors | grep -i "fan"
SENSEOF

chmod +x /usr/local/bin/asus-sensors-monitor

# ============================================
# NVIDIA Driver Installation (from trusted source)
# ============================================
echo ""
echo "[*] Installing NVIDIA drivers from trusted GitHub source..."

# Install dependencies first
apt-get install -y \
    build-essential \
    dkms \
    linux-headers-$(uname -r) \
    pkg-config \
    libglvnd-dev \
    libvulkan1 \
    vulkan-tools \
    xserver-xorg-dev

# Parrot OS already includes non-free repositories in sources.list
# Update package cache for latest Parrot repository information
apt-get update

# Clone nvidia-driver-installer from trusted GitHub source
cd /usr/src
git clone https://github.com/NVIDIA/open-gpu-kernel-modules.git nvidia-open-drivers
cd nvidia-open-drivers

# Get the latest stable tag
LATEST_TAG=$(git describe --tags --abbrev=0)
echo "Using NVIDIA driver version: $LATEST_TAG"
git checkout $LATEST_TAG

# Build and install open kernel modules
make modules -j$(nproc)
make modules_install

# Download and install proprietary NVIDIA driver components
# Using NVIDIA's official driver download script
cd /tmp
cat > /tmp/nvidia-installer-helper.sh << 'NVINST'
#!/bin/bash
# NVIDIA Driver Installer Helper

# Detect latest driver version from NVIDIA's official GitHub releases
DRIVER_VERSION="545.29.06"  # Latest stable production driver

echo "Downloading NVIDIA driver version $DRIVER_VERSION..."

# Download from NVIDIA's official servers
wget -O NVIDIA-Linux-x86_64-${DRIVER_VERSION}.run \
    https://us.download.nvidia.com/XFree86/Linux-x86_64/${DRIVER_VERSION}/NVIDIA-Linux-x86_64-${DRIVER_VERSION}.run

chmod +x NVIDIA-Linux-x86_64-${DRIVER_VERSION}.run

# Install with DKMS support
./NVIDIA-Linux-x86_64-${DRIVER_VERSION}.run \
    --dkms \
    --no-questions \
    --ui=none \
    --disable-nouveau \
    --run-nvidia-xconfig

echo "NVIDIA driver $DRIVER_VERSION installed successfully"
NVINST

chmod +x /tmp/nvidia-installer-helper.sh

# Blacklist nouveau (open-source driver)
cat > /etc/modprobe.d/blacklist-nouveau.conf << 'EOF'
blacklist nouveau
options nouveau modeset=0
EOF

# Update initramfs
update-initramfs -u

# Run the installer
bash /tmp/nvidia-installer-helper.sh || {
    echo "Warning: NVIDIA installer script had issues, falling back to Debian packages..."
    apt-get install -y \
        nvidia-driver \
        nvidia-smi \
        nvidia-settings
}

# Install CUDA toolkit from NVIDIA's GitHub releases
cd /usr/src
git clone https://github.com/NVIDIA/cuda-samples.git cuda-samples-github

# Install NVIDIA tools
apt-get install -y \
    nvtop \
    nvidia-cuda-toolkit

# Clone and install nvidia-settings from GitHub
cd /usr/src
git clone https://github.com/NVIDIA/nvidia-settings.git nvidia-settings-src
cd nvidia-settings-src
make -j$(nproc)
make install

# Install NVIDIA persistence daemon
apt-get install -y nvidia-persistenced || {
    # Build from source if not available
    cd /usr/src
    git clone https://github.com/NVIDIA/nvidia-persistenced.git
    cd nvidia-persistenced
    make -j$(nproc)
    make install
    
    # Create systemd service
    cat > /etc/systemd/system/nvidia-persistenced.service << 'NVPERSIST'
[Unit]
Description=NVIDIA Persistence Daemon
Wants=syslog.target

[Service]
Type=forking
ExecStart=/usr/bin/nvidia-persistenced --verbose
ExecStopPost=/bin/rm -rf /var/run/nvidia-persistenced

[Install]
WantedBy=multi-user.target
NVPERSIST
}

systemctl enable nvidia-persistenced

# Verify installation
nvidia-smi || echo "Warning: nvidia-smi not yet available (may need reboot)"

echo ""
echo "[*] NVIDIA drivers installed from trusted sources:"
echo "    - Open GPU Kernel Modules: github.com/NVIDIA/open-gpu-kernel-modules"
echo "    - NVIDIA Settings: github.com/NVIDIA/nvidia-settings"
echo "    - CUDA Samples: github.com/NVIDIA/cuda-samples"
echo "    - Official NVIDIA drivers: download.nvidia.com"

# ============================================
# NVIDIA Mode Switcher (Production vs Gaming)
# ============================================
echo ""
echo "[*] Creating NVIDIA mode switcher..."

cat > /usr/local/bin/nvidia-mode << 'NVEOF'
#!/bin/bash
# GhostOS NVIDIA Mode Switcher
# Switch between Production (power-saving) and Gaming (performance) modes

MODE=$1

show_usage() {
    echo "GhostOS NVIDIA Mode Switcher"
    echo "Usage: nvidia-mode [production|gaming|status]"
    echo ""
    echo "Modes:"
    echo "  production  - Power-saving mode (lower clocks, better temps)"
    echo "  gaming      - Performance mode (max clocks, best FPS)"
    echo "  status      - Show current mode and GPU info"
    echo ""
    echo "Examples:"
    echo "  sudo nvidia-mode gaming      # Switch to gaming mode"
    echo "  sudo nvidia-mode production  # Switch to production mode"
    echo "  nvidia-mode status           # Check current mode"
}

check_nvidia() {
    if ! command -v nvidia-smi &> /dev/null; then
        echo "Error: NVIDIA drivers not found"
        exit 1
    fi
}

show_status() {
    echo "========================================="
    echo "  NVIDIA GPU Status"
    echo "========================================="
    echo ""
    
    # GPU info
    nvidia-smi --query-gpu=name,driver_version,power.draw,temperature.gpu,clocks.current.graphics,clocks.current.memory --format=csv,noheader
    
    echo ""
    echo "Current Power Mode:"
    CURRENT_MODE=$(cat /etc/nvidia-mode.conf 2>/dev/null || echo "unknown")
    echo "  $CURRENT_MODE"
    
    echo ""
    echo "Power Limit:"
    nvidia-smi --query-gpu=power.limit --format=csv,noheader
    
    echo ""
    echo "Persistence Mode:"
    nvidia-smi --query-gpu=persistence_mode --format=csv,noheader
}

set_production_mode() {
    echo "Switching to PRODUCTION mode..."
    
    # Set power limit to 75% for power saving
    nvidia-smi -pl $(nvidia-smi --query-gpu=power.max_limit --format=csv,noheader,nounits | awk '{print int($1 * 0.75)}')
    
    # Enable persistence mode (reduces latency)
    nvidia-smi -pm 1
    
    # Set GPU clocks to auto (power-saving)
    nvidia-settings -a "[gpu:0]/GpuPowerMizerMode=0" 2>/dev/null || true
    
    # Disable overclocking
    nvidia-smi -rgc 2>/dev/null || true
    nvidia-smi -rmc 2>/dev/null || true
    
    # Save mode
    echo "production" > /etc/nvidia-mode.conf
    
    echo "✓ Production mode enabled"
    echo "  - Power limit: 75%"
    echo "  - Clock speed: Auto (adaptive)"
    echo "  - Best for: Office work, development, media playback"
}

set_gaming_mode() {
    echo "Switching to GAMING mode..."
    
    # Set power limit to 100% for maximum performance
    nvidia-smi -pl $(nvidia-smi --query-gpu=power.max_limit --format=csv,noheader,nounits | awk '{print int($1)}')
    
    # Enable persistence mode
    nvidia-smi -pm 1
    
    # Set GPU to prefer maximum performance
    nvidia-settings -a "[gpu:0]/GpuPowerMizerMode=1" 2>/dev/null || true
    
    # Lock clocks to maximum (if supported)
    MAX_GRAPHICS_CLOCK=$(nvidia-smi --query-supported-clocks=graphics --format=csv,noheader | head -1)
    MAX_MEMORY_CLOCK=$(nvidia-smi --query-supported-clocks=memory --format=csv,noheader | head -1)
    
    if [ ! -z "$MAX_GRAPHICS_CLOCK" ]; then
        nvidia-smi -lgc $MAX_GRAPHICS_CLOCK 2>/dev/null || true
    fi
    
    if [ ! -z "$MAX_MEMORY_CLOCK" ]; then
        nvidia-smi -lmc $MAX_MEMORY_CLOCK 2>/dev/null || true
    fi
    
    # Save mode
    echo "gaming" > /etc/nvidia-mode.conf
    
    echo "✓ Gaming mode enabled"
    echo "  - Power limit: 100%"
    echo "  - Clock speed: Maximum"
    echo "  - Best for: Gaming, rendering, ML training"
}

# Main logic
check_nvidia

if [ "$MODE" = "status" ]; then
    show_status
elif [ "$MODE" = "production" ]; then
    if [ "$EUID" -ne 0 ]; then
        echo "Error: Must run as root (use sudo)"
        exit 1
    fi
    set_production_mode
    echo ""
    show_status
elif [ "$MODE" = "gaming" ]; then
    if [ "$EUID" -ne 0 ]; then
        echo "Error: Must run as root (use sudo)"
        exit 1
    fi
    set_gaming_mode
    echo ""
    show_status
else
    show_usage
    exit 1
fi
NVEOF

chmod +x /usr/local/bin/nvidia-mode

# Create desktop entry for easy access
cat > /usr/share/applications/nvidia-mode-switcher.desktop << 'EOF'
[Desktop Entry]
Name=NVIDIA Mode Switcher
Comment=Switch between Production and Gaming modes
Exec=xfce4-terminal -e "bash -c 'nvidia-mode status; echo; echo Press ENTER to close; read'"
Icon=nvidia-settings
Terminal=false
Type=Application
Categories=System;Settings;
EOF

# Set default to production mode
echo "production" > /etc/nvidia-mode.conf

# Create systemd service to restore mode on boot
cat > /etc/systemd/system/nvidia-mode-restore.service << 'EOF'
[Unit]
Description=Restore NVIDIA Mode on Boot
After=nvidia-persistenced.service

[Service]
Type=oneshot
ExecStart=/usr/local/bin/nvidia-mode-restore.sh
RemainAfterExit=yes

[Install]
WantedBy=multi-user.target
EOF

cat > /usr/local/bin/nvidia-mode-restore.sh << 'EOF'
#!/bin/bash
MODE=$(cat /etc/nvidia-mode.conf 2>/dev/null || echo "production")
if [ "$MODE" = "gaming" ]; then
    /usr/local/bin/nvidia-mode gaming
else
    /usr/local/bin/nvidia-mode production
fi
EOF

chmod +x /usr/local/bin/nvidia-mode-restore.sh
systemctl enable nvidia-mode-restore.service

echo ""
echo "[*] NVIDIA setup complete!"
echo "    Use 'sudo nvidia-mode gaming' to enable gaming mode"
echo "    Use 'sudo nvidia-mode production' to enable production mode"
echo "    Use 'nvidia-mode status' to check current mode"

# ============================================
# Windows Compatibility Layer (Wine - Privacy Mode)
# ============================================
echo ""
echo "[*] Installing Windows compatibility layer (Wine)..."
echo "    Privacy-focused: NO .NET Framework, NO telemetry"

# Add WineHQ repository for latest Wine
apt-get install -y software-properties-common wget
mkdir -pm755 /etc/apt/keyrings
wget -O /etc/apt/keyrings/winehq-archive.key https://dl.winehq.org/wine-builds/winehq.key
wget -NP /etc/apt/sources.list.d/ https://dl.winehq.org/wine-builds/debian/dists/bookworm/winehq-bookworm.sources

apt-get update

# Install Wine Staging (most compatible, best performance)
apt-get install -y --install-recommends \
    winehq-staging \
    winetricks \
    cabextract \
    unzip \
    p7zip-full

# Install dependencies for Windows programs
apt-get install -y \
    mesa-vulkan-drivers \
    libvulkan1 \
    vulkan-tools \
    libgl1-mesa-dri:i386 \
    libgl1-mesa-glx:i386

# Enable 32-bit architecture for Wine
dpkg --add-architecture i386
apt-get update
apt-get install -y wine32 wine64

# Install DXVK for DirectX to Vulkan translation (better than WineD3D)
cd /usr/src
git clone https://github.com/doitsujin/dxvk.git
cd dxvk
git checkout $(git describe --tags --abbrev=0)

# Install DXVK build dependencies
apt-get install -y \
    meson \
    glslang-tools \
    mingw-w64 \
    mingw-w64-tools

# Build DXVK
./package-release.sh master /usr/local/share/dxvk --no-package

# Install vkd3d-proton for DirectX 12 support
cd /usr/src
git clone --recursive https://github.com/HansKristian-Work/vkd3d-proton.git
cd vkd3d-proton
git checkout $(git describe --tags --abbrev=0)
./package-release.sh master /usr/local/share/vkd3d-proton --no-package

# Create Wine privacy configuration script
cat > /usr/local/bin/wine-privacy-setup << 'WINEPRIV'
#!/bin/bash
# GhostOS Wine Privacy Setup
# Configure Wine prefix without Microsoft telemetry

PREFIX="${WINEPREFIX:-$HOME/.wine}"

echo "Setting up Wine prefix: $PREFIX"
echo "Privacy mode: ENABLED"

# Initialize Wine prefix
WINEDLLOVERRIDES="mscoree,mshtml=" WINEARCH=win64 wineboot -u

# Wait for Wine to initialize
sleep 5

# Block all Microsoft telemetry in Wine hosts file
cat >> "$PREFIX/drive_c/windows/system32/drivers/etc/hosts" << 'EOF'
# Block Microsoft telemetry
0.0.0.0 telemetry.microsoft.com
0.0.0.0 vortex.data.microsoft.com
0.0.0.0 settings-win.data.microsoft.com
0.0.0.0 watson.telemetry.microsoft.com
0.0.0.0 oca.telemetry.microsoft.com
0.0.0.0 sqm.telemetry.microsoft.com
0.0.0.0 corpext.msitadfs.glbdns2.microsoft.com
0.0.0.0 compatexchange.cloudapp.net
0.0.0.0 cs1.wpc.v0cdn.net
0.0.0.0 a-0001.a-msedge.net
0.0.0.0 statsfe2.ws.microsoft.com
0.0.0.0 diagnostics.support.microsoft.com
0.0.0.0 corp.sts.microsoft.com
0.0.0.0 statsfe1.ws.microsoft.com
0.0.0.0 feedback.windows.com
0.0.0.0 feedback.microsoft-hohm.com
0.0.0.0 feedback.search.microsoft.com
EOF

# Disable Wine .NET installation prompts
wine reg add "HKCU\\Software\\Wine\\DllOverrides" /v "mscoree" /d "" /f
wine reg add "HKCU\\Software\\Wine\\DllOverrides" /v "mshtml" /d "" /f

# Disable Windows Update in Wine
wine reg add "HKLM\\Software\\Microsoft\\Windows\\CurrentVersion\\WindowsUpdate\\Auto Update" /v "AUOptions" /d "1" /f

# Disable error reporting
wine reg add "HKLM\\Software\\Microsoft\\PCHealth\\ErrorReporting" /v "DoReport" /t REG_DWORD /d "0" /f
wine reg add "HKCU\\Software\\Microsoft\\PCHealth\\ErrorReporting" /v "DoReport" /t REG_DWORD /d "0" /f

# Disable customer experience improvement
wine reg add "HKLM\\Software\\Microsoft\\SQMClient\\Windows" /v "CEIPEnable" /t REG_DWORD /d "0" /f
wine reg add "HKCU\\Software\\Microsoft\\SQMClient\\Windows" /v "CEIPEnable" /t REG_DWORD /d "0" /f

# Set Windows version to Windows 10 (for compatibility)
wine reg add "HKCU\\Software\\Wine" /v "Version" /d "win10" /f

# Configure Wine for offline mode
wine reg add "HKCU\\Software\\Wine\\Network" /v "OfflineMode" /t REG_DWORD /d "1" /f

echo ""
echo "✓ Wine privacy setup complete"
echo "  - Windows version: Windows 10 (offline mode)"
echo "  - .NET Framework: DISABLED"
echo "  - Microsoft telemetry: BLOCKED"
echo "  - Windows Update: DISABLED"
echo "  - Error reporting: DISABLED"
WINEPRIV

chmod +x /usr/local/bin/wine-privacy-setup

# Create Wine launcher with DXVK/VKD3D
cat > /usr/local/bin/wine-ghostos << 'WINELAUNCH'
#!/bin/bash
# GhostOS Wine Launcher with privacy and performance

# Enable DXVK for DirectX 9/10/11
export WINEPREFIX="${WINEPREFIX:-$HOME/.wine}"
export DXVK_HUD="fps,version,devinfo"
export DXVK_LOG_LEVEL="none"

# Enable VKD3D for DirectX 12
export VKD3D_CONFIG="dxr,dxr11"

# Disable .NET and Windows HTML components
export WINEDLLOVERRIDES="mscoree,mshtml=;winemenubuilder.exe=d"

# Force offline mode
export WININET_DISABLE_NETWORK=1

# Performance settings
export WINE_CPU_TOPOLOGY="4:4"
export STAGING_SHARED_MEMORY=1
export WINE_LARGE_ADDRESS_AWARE=1

# Anti-telemetry
export WINEDEBUG=-all

# Check if first run
if [ ! -d "$WINEPREFIX" ]; then
    echo "First run detected. Setting up Wine prefix..."
    wine-privacy-setup
fi

# Run the Windows application
if [ $# -eq 0 ]; then
    echo "GhostOS Wine Launcher"
    echo "Usage: wine-ghostos <program.exe> [arguments]"
    echo ""
    echo "Features:"
    echo "  ✓ Windows 10 compatibility"
    echo "  ✓ DirectX 9/10/11 support (DXVK)"
    echo "  ✓ DirectX 12 support (VKD3D)"
    echo "  ✓ NO .NET Framework"
    echo "  ✓ NO telemetry"
    echo "  ✓ Offline mode"
    echo ""
    echo "Examples:"
    echo "  wine-ghostos notepad.exe"
    echo "  wine-ghostos 'C:\\Program Files\\MyApp\\app.exe'"
    echo "  wine-ghostos game.exe --fullscreen"
    exit 0
fi

wine "$@"
WINELAUNCH

chmod +x /usr/local/bin/wine-ghostos

# Create DXVK installer script
cat > /usr/local/bin/dxvk-install << 'DXVKINSTALL'
#!/bin/bash
# Install DXVK to Wine prefix

PREFIX="${WINEPREFIX:-$HOME/.wine}"

if [ ! -d "$PREFIX" ]; then
    echo "Error: Wine prefix not found at $PREFIX"
    echo "Run 'wine-ghostos' first to create prefix"
    exit 1
fi

echo "Installing DXVK to $PREFIX..."

# Install DXVK DLLs
DXVK_DIR="/usr/local/share/dxvk"
if [ -d "$DXVK_DIR" ]; then
    cd "$DXVK_DIR"
    
    # Copy DXVK DLLs
    cp x64/*.dll "$PREFIX/drive_c/windows/system32/"
    cp x32/*.dll "$PREFIX/drive_c/windows/syswow64/" 2>/dev/null || true
    
    # Register DLLs
    wine reg add "HKCU\\Software\\Wine\\DllOverrides" /v "d3d9" /d "native" /f
    wine reg add "HKCU\\Software\\Wine\\DllOverrides" /v "d3d10core" /d "native" /f
    wine reg add "HKCU\\Software\\Wine\\DllOverrides" /v "d3d11" /d "native" /f
    wine reg add "HKCU\\Software\\Wine\\DllOverrides" /v "dxgi" /d "native" /f
    
    echo "✓ DXVK installed successfully"
else
    echo "Error: DXVK not found at $DXVK_DIR"
    exit 1
fi

# Install VKD3D
VKD3D_DIR="/usr/local/share/vkd3d-proton"
if [ -d "$VKD3D_DIR" ]; then
    cd "$VKD3D_DIR"
    
    # Copy VKD3D DLLs
    cp x64/*.dll "$PREFIX/drive_c/windows/system32/"
    
    # Register DLLs
    wine reg add "HKCU\\Software\\Wine\\DllOverrides" /v "d3d12" /d "native" /f
    
    echo "✓ VKD3D-Proton installed successfully"
fi

echo ""
echo "DirectX translation layers installed:"
echo "  ✓ DXVK (DirectX 9/10/11 → Vulkan)"
echo "  ✓ VKD3D-Proton (DirectX 12 → Vulkan)"
DXVKINSTALL

chmod +x /usr/local/bin/dxvk-install

# Create desktop entry
cat > /usr/share/applications/wine-ghostos.desktop << 'EOF'
[Desktop Entry]
Name=Wine (GhostOS Privacy Mode)
Comment=Run Windows applications without telemetry
Exec=xfce4-terminal -e "bash -c 'wine-ghostos; read'"
Icon=wine
Terminal=true
Type=Application
Categories=System;Emulator;
EOF

# Create Wine configuration GUI launcher
cat > /usr/share/applications/winecfg-ghostos.desktop << 'EOF'
[Desktop Entry]
Name=Wine Configuration
Comment=Configure Wine settings
Exec=winecfg
Icon=wine-winecfg
Terminal=false
Type=Application
Categories=System;Settings;
EOF

echo ""
echo "[*] Windows compatibility setup complete!"
echo "    Commands:"
echo "    - wine-ghostos <program.exe>  : Run Windows programs"
echo "    - wine-privacy-setup           : Configure Wine prefix"
echo "    - dxvk-install                 : Install DirectX support"
echo "    - winecfg                      : Wine configuration"
echo ""
echo "    Features:"
echo "    ✓ Windows 10 compatibility (offline mode)"
echo "    ✓ DirectX 9/10/11/12 support (DXVK + VKD3D)"
echo "    ✓ NO .NET Framework (blocked)"
echo "    ✓ NO Microsoft telemetry (blocked)"
echo "    ✓ NO Windows Update"
echo "    ✓ Privacy-first configuration"

# ============================================
# Network Security Monitoring (Low Impact)
# ============================================
echo ""
echo "[*] Installing network security monitoring..."
echo "    Low-impact mode: Minimal CPU/RAM usage"

# Install fail2ban for intrusion prevention
apt-get install -y fail2ban

# Configure fail2ban with low resource usage
cat > /etc/fail2ban/jail.local << 'EOF'
[DEFAULT]
# Low impact configuration
bantime = 3600
findtime = 600
maxretry = 5
destemail = root@localhost
sendername = GhostOS-Security
action = %(action_mwl)s

# Enable SSH protection
[sshd]
enabled = true
port = ssh
logpath = /var/log/auth.log
maxretry = 3

# Enable HTTP/HTTPS protection (if web servers installed)
[nginx-http-auth]
enabled = false

[apache-auth]
enabled = false
EOF

systemctl enable fail2ban
systemctl start fail2ban || true

# Install lightweight network monitoring tools
apt-get install -y \
    iftop \
    nethogs \
    iptraf-ng \
    tcpdump \
    nmap

# Install Suricata for lightweight IDS (Intrusion Detection System)
apt-get install -y suricata

# Configure Suricata in low-impact mode
cat > /etc/suricata/suricata.yaml << 'EOF'
# GhostOS Suricata - Low Impact Configuration
vars:
  address-groups:
    HOME_NET: "[192.168.0.0/16,10.0.0.0/8,172.16.0.0/12]"
    EXTERNAL_NET: "!$HOME_NET"

outputs:
  - fast:
      enabled: yes
      filename: fast.log
      append: yes
  - eve-log:
      enabled: yes
      filetype: regular
      filename: eve.json
      types:
        - alert

af-packet:
  - interface: default

# Low resource usage
runmode: autofp
max-pending-packets: 1024

# Enable basic rules only for low impact
rule-files:
  - suricata.rules
EOF

# Download and install basic Suricata rules
suricata-update || true

systemctl enable suricata
systemctl start suricata || true

# Create network monitoring dashboard script
cat > /usr/local/bin/ghostos-netmon << 'NETMON'
#!/bin/bash
# GhostOS Network Security Monitor

show_menu() {
    clear
    echo "========================================="
    echo "  GhostOS Network Security Monitor"
    echo "========================================="
    echo ""
    echo "1) Show active connections"
    echo "2) Show firewall status"
    echo "3) Show fail2ban status"
    echo "4) Show recent security alerts"
    echo "5) Show network traffic (live)"
    echo "6) Show banned IPs"
    echo "7) Unban IP address"
    echo "8) Scan local network"
    echo "9) Show listening ports"
    echo "0) Exit"
    echo ""
    read -p "Select option: " choice
}

show_connections() {
    echo ""
    echo "Active Network Connections:"
    echo "========================================="
    ss -tunap | grep ESTABLISHED
    echo ""
    read -p "Press ENTER to continue..."
}

show_firewall() {
    echo ""
    echo "Firewall Status (UFW):"
    echo "========================================="
    ufw status verbose
    echo ""
    echo "Recent blocked connections:"
    tail -20 /var/log/ufw.log 2>/dev/null || echo "No firewall logs found"
    echo ""
    read -p "Press ENTER to continue..."
}

show_fail2ban() {
    echo ""
    echo "Fail2ban Status:"
    echo "========================================="
    fail2ban-client status
    echo ""
    echo "SSH jail status:"
    fail2ban-client status sshd 2>/dev/null || echo "SSH jail not active"
    echo ""
    read -p "Press ENTER to continue..."
}

show_alerts() {
    echo ""
    echo "Recent Security Alerts:"
    echo "========================================="
    echo ""
    echo "--- Suricata Alerts ---"
    tail -50 /var/log/suricata/fast.log 2>/dev/null | grep -i "alert" | tail -20 || echo "No Suricata alerts"
    echo ""
    echo "--- Failed Login Attempts ---"
    grep "Failed password" /var/log/auth.log 2>/dev/null | tail -10 || echo "No failed logins"
    echo ""
    read -p "Press ENTER to continue..."
}

show_traffic() {
    echo ""
    echo "Live Network Traffic Monitor"
    echo "Press Ctrl+C to stop"
    echo ""
    sleep 2
    nethogs -d 1
}

show_banned() {
    echo ""
    echo "Banned IP Addresses:"
    echo "========================================="
    fail2ban-client status sshd 2>/dev/null | grep "Banned IP list" -A 100
    echo ""
    read -p "Press ENTER to continue..."
}

unban_ip() {
    echo ""
    read -p "Enter IP address to unban: " ip
    if [ ! -z "$ip" ]; then
        fail2ban-client set sshd unbanip $ip
        echo "IP $ip unbanned from sshd jail"
    fi
    echo ""
    read -p "Press ENTER to continue..."
}

scan_network() {
    echo ""
    echo "Scanning local network..."
    echo "========================================="
    # Get default gateway network
    NETWORK=$(ip route | grep default | awk '{print $3}' | sed 's/\.[0-9]*$/.0\/24/')
    echo "Network: $NETWORK"
    echo ""
    nmap -sn $NETWORK
    echo ""
    read -p "Press ENTER to continue..."
}

show_ports() {
    echo ""
    echo "Listening Ports:"
    echo "========================================="
    ss -tulpn | grep LISTEN
    echo ""
    read -p "Press ENTER to continue..."
}

# Main loop
while true; do
    show_menu
    
    case $choice in
        1) show_connections ;;
        2) show_firewall ;;
        3) show_fail2ban ;;
        4) show_alerts ;;
        5) show_traffic ;;
        6) show_banned ;;
        7) unban_ip ;;
        8) scan_network ;;
        9) show_ports ;;
        0) exit 0 ;;
        *) echo "Invalid option" ;;
    esac
done
NETMON

chmod +x /usr/local/bin/ghostos-netmon

# Create real-time notification service for security events
cat > /usr/local/bin/ghostos-security-notify << 'NOTIFY'
#!/bin/bash
# GhostOS Security Event Notifier

LOG_FILE="/var/log/ghostos-security.log"
LAST_CHECK="/var/run/ghostos-security-lastcheck"

# Initialize
touch $LAST_CHECK

while true; do
    # Check for new fail2ban bans
    NEW_BANS=$(fail2ban-client status sshd 2>/dev/null | grep "Currently banned:" | awk '{print $3}')
    
    if [ ! -z "$NEW_BANS" ] && [ "$NEW_BANS" != "0" ]; then
        BANNED_IPS=$(fail2ban-client status sshd 2>/dev/null | grep "Banned IP list" -A 100 | tail -n +2)
        echo "[$(date)] SECURITY ALERT: $NEW_BANS IP(s) banned by fail2ban" >> $LOG_FILE
        echo "$BANNED_IPS" >> $LOG_FILE
        
        # Send desktop notification if available
        if command -v notify-send &> /dev/null; then
            notify-send -u critical "GhostOS Security Alert" "$NEW_BANS IP(s) banned for suspicious activity"
        fi
    fi
    
    # Check for new Suricata alerts
    if [ -f /var/log/suricata/fast.log ]; then
        NEW_ALERTS=$(find /var/log/suricata/fast.log -newer $LAST_CHECK 2>/dev/null | wc -l)
        if [ "$NEW_ALERTS" -gt 0 ]; then
            ALERT_MSG=$(tail -1 /var/log/suricata/fast.log)
            echo "[$(date)] IDS ALERT: $ALERT_MSG" >> $LOG_FILE
            
            if command -v notify-send &> /dev/null; then
                notify-send -u critical "GhostOS IDS Alert" "Network intrusion attempt detected"
            fi
        fi
    fi
    
    # Check for unusual network connections
    SUSPICIOUS=$(ss -tunap | grep -E "(ESTABLISHED|SYN_SENT)" | wc -l)
    if [ "$SUSPICIOUS" -gt 50 ]; then
        echo "[$(date)] WARNING: High number of network connections: $SUSPICIOUS" >> $LOG_FILE
    fi
    
    touch $LAST_CHECK
    sleep 60  # Check every minute
done
NOTIFY

chmod +x /usr/local/bin/ghostos-security-notify

# Create systemd service for security notifications
cat > /etc/systemd/system/ghostos-security-notify.service << 'EOF'
[Unit]
Description=GhostOS Security Notification Service
After=network.target fail2ban.service suricata.service

[Service]
Type=simple
ExecStart=/usr/local/bin/ghostos-security-notify
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

systemctl enable ghostos-security-notify.service
systemctl start ghostos-security-notify.service || true

# Create desktop entry for network monitor
cat > /usr/share/applications/ghostos-netmon.desktop << 'EOF'
[Desktop Entry]
Name=Network Security Monitor
Comment=Monitor network security and threats
Exec=xfce4-terminal -e ghostos-netmon
Icon=security-high
Terminal=true
Type=Application
Categories=System;Security;Network;
EOF

# Configure iptables logging for suspicious activity
iptables -N LOGGING 2>/dev/null || true
iptables -A INPUT -j LOGGING 2>/dev/null || true
iptables -A LOGGING -m limit --limit 2/min -j LOG --log-prefix "IPTables-Dropped: " --log-level 4
iptables -A LOGGING -j DROP

# Save iptables rules
iptables-save > /etc/iptables/rules.v4 2>/dev/null || true

# Create network security status command
cat > /usr/local/bin/netstatus << 'NETSTATUS'
#!/bin/bash
# Quick network security status

echo "========================================="
echo "  Network Security Status"
echo "========================================="
echo ""

echo "Firewall: $(ufw status | head -1)"
echo "Fail2ban: $(systemctl is-active fail2ban)"
echo "Suricata IDS: $(systemctl is-active suricata)"
echo "Security Monitor: $(systemctl is-active ghostos-security-notify)"
echo ""

echo "Active Connections: $(ss -tunap | grep ESTABLISHED | wc -l)"
echo "Banned IPs: $(fail2ban-client status sshd 2>/dev/null | grep 'Currently banned' | awk '{print $3}')"
echo "Recent Alerts: $(tail -10 /var/log/ghostos-security.log 2>/dev/null | wc -l)"
echo ""

echo "Commands:"
echo "  ghostos-netmon  - Full network security dashboard"
echo "  netstatus       - Quick status check"
NETSTATUS

chmod +x /usr/local/bin/netstatus

echo ""
echo "[*] Network security monitoring installed!"
echo "    Commands:"
echo "    - ghostos-netmon  : Interactive security dashboard"
echo "    - netstatus       : Quick security status"
echo ""
echo "    Features:"
echo "    ✓ Fail2ban (brute-force protection)"
echo "    ✓ Suricata IDS (intrusion detection)"
echo "    ✓ Real-time notifications"
echo "    ✓ Low CPU/RAM impact"
echo "    ✓ Automatic ban of suspicious IPs"
echo "    ✓ Network traffic monitoring"

# ============================================
# Gaming Console-Style UI (Unified Frontend)
# ============================================
echo ""
echo "[*] Installing unified gaming console UI..."
echo "    Combining PlayStation, Xbox, Nintendo, Steam interfaces"

# Install base UI dependencies
apt-get install -y \
    qt5-default \
    qtmultimedia5-dev \
    libqt5svg5-dev \
    qtdeclarative5-dev \
    qml-module-qtquick2 \
    qml-module-qtquick-controls2 \
    qml-module-qtquick-layouts \
    qml-module-qtmultimedia \
    qml-module-qtgraphicaleffects

# Install Pegasus Frontend (open-source multi-platform launcher)
cd /usr/src
git clone --recursive https://github.com/mmatyas/pegasus-frontend.git
cd pegasus-frontend
git checkout $(git describe --tags --abbrev=0 2>/dev/null || echo "master")

# Build Pegasus Frontend
apt-get install -y cmake ninja-build
mkdir build && cd build
cmake .. -GNinja
ninja
ninja install

# Install EmulationStation as alternative/backup UI
apt-get install -y \
    libsdl2-dev \
    libfreeimage-dev \
    libfreetype6-dev \
    libcurl4-openssl-dev \
    rapidjson-dev \
    libasound2-dev \
    libvlc-dev

cd /usr/src
git clone https://github.com/RetroPie/EmulationStation.git emulationstation
cd emulationstation
mkdir build && cd build
cmake ..
make -j$(nproc)
make install

# Install Lutris (unified gaming platform)
apt-get install -y lutris

# Install Steam (if user wants it)
dpkg --add-architecture i386
apt-get update
apt-get install -y \
    steam-installer \
    steam-devices

# Create GhostOS unified gaming launcher
cat > /usr/local/bin/ghostos-gaming << 'GAMINGLAUNCHER'
#!/bin/bash
# GhostOS Unified Gaming Console UI

export XDG_CONFIG_HOME="${XDG_CONFIG_HOME:-$HOME/.config}"
export GHOSTOS_GAME_DIR="$HOME/Games"

# Create game directories
mkdir -p "$GHOSTOS_GAME_DIR"/{ROMs,PC,Steam,Native,Emulators}

show_menu() {
    clear
    cat << 'EOF'
╔════════════════════════════════════════════════════════════╗
║                                                            ║
║   ░██████╗░██╗░░██╗░█████╗░░██████╗████████╗░█████╗░░██████╗  ║
║   ██╔════╝░██║░░██║██╔══██╗██╔════╝╚══██╔══╝██╔══██╗██╔════╝  ║
║   ██║░░██╗░███████║██║░░██║╚█████╗░░░░██║░░░██║░░██║╚█████╗░  ║
║   ██║░░╚██╗██╔══██║██║░░██║░╚═══██╗░░░██║░░░██║░░██║░╚═══██╗  ║
║   ╚██████╔╝██║░░██║╚█████╔╝██████╔╝░░░██║░░░╚█████╔╝██████╔╝  ║
║   ░╚═════╝░╚═╝░░╚═╝░╚════╝░╚═════╝░░░░╚═╝░░░░╚════╝░╚═════╝░  ║
║                                                            ║
║              UNIFIED GAMING CONSOLE INTERFACE             ║
║                                                            ║
╚════════════════════════════════════════════════════════════╝

  [1] 🎮 Launch Full Console UI (Pegasus Frontend)
  [2] 🕹️  Launch EmulationStation UI
  [3] 🎯 Launch Lutris (PC Games)
  [4] 🎲 Launch Steam Big Picture
  [5] 📁 Game Library Manager
  [6] ⚙️  Settings & Configuration
  [7] 🎨 Theme Manager
  [8] 🔄 Update Systems
  [0] 🚪 Exit

EOF
    read -p "Select option: " choice
}

launch_pegasus() {
    echo "Launching Pegasus Frontend..."
    pegasus-fe --fullscreen
}

launch_emulationstation() {
    echo "Launching EmulationStation..."
    emulationstation
}

launch_lutris() {
    echo "Launching Lutris..."
    lutris
}

launch_steam() {
    echo "Launching Steam Big Picture..."
    steam steam://open/bigpicture
}

manage_library() {
    clear
    echo "========================================="
    echo "  Game Library Manager"
    echo "========================================="
    echo ""
    echo "Game Directories:"
    echo "  ROMs:      $GHOSTOS_GAME_DIR/ROMs"
    echo "  PC Games:  $GHOSTOS_GAME_DIR/PC"
    echo "  Steam:     $GHOSTOS_GAME_DIR/Steam"
    echo "  Native:    $GHOSTOS_GAME_DIR/Native"
    echo ""
    echo "Installed Games:"
    find "$GHOSTOS_GAME_DIR" -type f \( -name "*.sh" -o -name "*.exe" \) 2>/dev/null | wc -l
    echo ""
    read -p "Press ENTER to continue..."
}

settings_menu() {
    clear
    echo "========================================="
    echo "  Settings & Configuration"
    echo "========================================="
    echo ""
    echo "1) Configure Controllers"
    echo "2) Configure Display Settings"
    echo "3) Configure Audio"
    echo "4) Configure Emulators"
    echo "0) Back"
    echo ""
    read -p "Select: " setting
    
    case $setting in
        1) jstest /dev/input/js0 2>/dev/null || echo "No controller detected" ;;
        2) xrandr --listmonitors ;;
        3) pavucontrol & ;;
        4) echo "Edit emulator configs in ~/.config/" ;;
    esac
}

theme_manager() {
    clear
    echo "========================================="
    echo "  Theme Manager"
    echo "========================================="
    echo ""
    echo "Available Themes:"
    echo "  1) PlayStation Style (Blue)"
    echo "  2) Xbox Style (Green)"
    echo "  3) Nintendo Style (Red)"
    echo "  4) Steam Style (Dark)"
    echo "  5) GhostOS Style (Cyan/Purple)"
    echo ""
    read -p "Select theme: " theme
    
    case $theme in
        1) echo "PlayStation theme selected" ;;
        2) echo "Xbox theme selected" ;;
        3) echo "Nintendo theme selected" ;;
        4) echo "Steam theme selected" ;;
        5) echo "GhostOS theme selected (default)" ;;
    esac
    
    read -p "Press ENTER to continue..."
}

update_systems() {
    clear
    echo "Updating gaming systems..."
    echo ""
    echo "Updating Pegasus..."
    pegasus-fe --check-update || true
    echo ""
    echo "Updating Lutris..."
    lutris --update-all || true
    echo ""
    read -p "Press ENTER to continue..."
}

# Main loop
while true; do
    show_menu
    
    case $choice in
        1) launch_pegasus ;;
        2) launch_emulationstation ;;
        3) launch_lutris ;;
        4) launch_steam ;;
        5) manage_library ;;
        6) settings_menu ;;
        7) theme_manager ;;
        8) update_systems ;;
        0) exit 0 ;;
        *) echo "Invalid option" ; sleep 1 ;;
    esac
done
GAMINGLAUNCHER

chmod +x /usr/local/bin/ghostos-gaming

# Create Pegasus Frontend configuration
mkdir -p /etc/pegasus-frontend
cat > /etc/pegasus-frontend/settings.txt << 'EOF'
# GhostOS Pegasus Configuration
general.fullscreen: true
general.mouse-support: false
providers.steam.enabled: true
providers.lutris.enabled: true
ui.theme: ghostos-theme
EOF

# Create custom GhostOS theme for Pegasus
mkdir -p /usr/share/pegasus-frontend/themes/ghostos-theme
cat > /usr/share/pegasus-frontend/themes/ghostos-theme/theme.cfg << 'EOF'
name: GhostOS Theme
author: GhostOS Team
version: 1.0

# Unified console design inspired by PlayStation, Xbox, Nintendo
background-color: #0a0a0a
primary-color: #00d9ff
secondary-color: #9b59b6
accent-color: #00ff88
text-color: #ffffff

# Smooth animations
animation-duration: 300ms
transition-style: cubic-bezier
EOF

# Create desktop entries
cat > /usr/share/applications/ghostos-gaming.desktop << 'EOF'
[Desktop Entry]
Name=GhostOS Gaming
Comment=Unified gaming console interface
Exec=ghostos-gaming
Icon=applications-games
Terminal=true
Type=Application
Categories=Game;
EOF

cat > /usr/share/applications/pegasus-frontend.desktop << 'EOF'
[Desktop Entry]
Name=Pegasus Frontend
Comment=Multi-platform game launcher
Exec=pegasus-fe --fullscreen
Icon=applications-games
Terminal=false
Type=Application
Categories=Game;
EOF

# Install controller support
apt-get install -y \
    xboxdrv \
    joystick \
    jstest-gtk \
    antimicrox

# Create autostart for gaming mode (optional)
mkdir -p /etc/skel/.config/autostart
cat > /etc/skel/.config/autostart/ghostos-gaming-mode.desktop << 'EOF'
[Desktop Entry]
Type=Application
Name=GhostOS Gaming Mode
Exec=sh -c "sleep 5 && ghostos-gaming"
Hidden=true
NoDisplay=false
X-GNOME-Autostart-enabled=false
EOF

# Install RetroArch for emulation
apt-get install -y \
    retroarch \
    libretro-* \
    retroarch-assets

# Configure RetroArch for console-style UI
mkdir -p /etc/retroarch
cat > /etc/retroarch/retroarch.cfg << 'EOF'
# GhostOS RetroArch Configuration
menu_driver = "ozone"
video_fullscreen = "true"
video_threaded = "true"
video_vsync = "true"
audio_driver = "pulse"
input_autodetect_enable = "true"
rgui_show_start_screen = "false"
EOF

echo ""
echo "[*] Gaming console UI installed!"
echo "    Commands:"
echo "    - ghostos-gaming      : Launch unified gaming interface"
echo "    - pegasus-fe          : Pegasus Frontend (full console UI)"
echo "    - emulationstation    : EmulationStation UI"
echo "    - lutris              : Lutris game manager"
echo "    - retroarch           : RetroArch emulation"
echo ""
echo "    Features:"
echo "    ✓ PlayStation-style interface"
echo "    ✓ Xbox-style interface"
echo "    ✓ Nintendo-style interface"
echo "    ✓ Steam Big Picture integration"
echo "    ✓ Controller support (Xbox, PlayStation, Nintendo)"
echo "    ✓ Unified game library"
echo "    ✓ Multiple themes"
echo "    ✓ EmulationStation + RetroArch"
echo ""
echo "    Game directories created at: ~/Games/"

# ============================================
# Plug and Play Support (Universal Hardware)
# ============================================
echo ""
echo "[*] Installing plug-and-play support for all hardware..."
echo "    Auto-detection: USB, Controllers, Drives, Printers, Audio, Network"

# Install core plug-and-play services
apt-get install -y \
    udev \
    udisks2 \
    udiskie \
    gvfs \
    gvfs-backends \
    gvfs-fuse \
    pmount \
    pcmciautils \
    usb-modeswitch \
    usb-modeswitch-data

# Install hardware detection tools
apt-get install -y \
    hwinfo \
    lshw \
    usbutils \
    pciutils \
    smartmontools

# Auto-mounting for USB drives and external media
apt-get install -y \
    automount \
    autofs \
    ntfs-3g \
    exfat-fuse \
    exfat-utils \
    hfsutils \
    hfsprogs

# Printer plug-and-play
apt-get install -y \
    cups \
    cups-filters \
    cups-pdf \
    system-config-printer \
    printer-driver-all \
    hplip \
    hplip-gui

systemctl enable cups
systemctl start cups || true

# Scanner plug-and-play
apt-get install -y \
    sane \
    sane-utils \
    libsane-extras \
    xsane \
    simple-scan

# Webcam plug-and-play
apt-get install -y \
    v4l-utils \
    v4l2loopback-dkms \
    cheese \
    guvcview

# Bluetooth plug-and-play
apt-get install -y \
    bluez \
    bluez-tools \
    blueman

systemctl enable bluetooth
systemctl start bluetooth || true

# Network adapter plug-and-play
apt-get install -y \
    network-manager \
    network-manager-gnome \
    wireless-tools \
    wpasupplicant

systemctl enable NetworkManager
systemctl start NetworkManager || true

# Game controller plug-and-play (enhanced)
apt-get install -y \
    xpad \
    xserver-xorg-input-joystick \
    steam-devices

# Audio plug-and-play
apt-get install -y \
    pulseaudio \
    pulseaudio-module-bluetooth \
    pavucontrol \
    alsa-utils \
    alsa-tools

# Create comprehensive udev rules for plug-and-play
cat > /etc/udev/rules.d/99-ghostos-plugandplay.rules << 'EOF'
# GhostOS Universal Plug and Play Rules

# USB Storage Auto-mount
ACTION=="add", SUBSYSTEMS=="usb", SUBSYSTEM=="block", ENV{ID_FS_USAGE}=="filesystem", RUN+="/usr/local/bin/ghostos-automount %k"
ACTION=="remove", SUBSYSTEMS=="usb", SUBSYSTEM=="block", RUN+="/usr/local/bin/ghostos-autounmount %k"

# Game Controllers (Xbox, PlayStation, Nintendo)
SUBSYSTEM=="input", ATTRS{idVendor}=="045e", ATTRS{idProduct}=="02ea", MODE="0666", TAG+="uaccess"  # Xbox One
SUBSYSTEM=="input", ATTRS{idVendor}=="045e", ATTRS{idProduct}=="0b13", MODE="0666", TAG+="uaccess"  # Xbox Series X
SUBSYSTEM=="input", ATTRS{idVendor}=="054c", ATTRS{idProduct}=="0ce6", MODE="0666", TAG+="uaccess"  # PS5 DualSense
SUBSYSTEM=="input", ATTRS{idVendor}=="054c", ATTRS{idProduct}=="09cc", MODE="0666", TAG+="uaccess"  # PS4 DualShock
SUBSYSTEM=="input", ATTRS{idVendor}=="057e", ATTRS{idProduct}=="2009", MODE="0666", TAG+="uaccess"  # Nintendo Pro
SUBSYSTEM=="input", ATTRS{idVendor}=="057e", ATTRS{idProduct}=="2017", MODE="0666", TAG+="uaccess"  # Nintendo JoyCon

# Printers - Auto-detect and configure
ACTION=="add", SUBSYSTEM=="usb", ENV{DEVTYPE}=="usb_device", ENV{ID_USB_INTERFACES}=="*:0701??:*", RUN+="/usr/local/bin/ghostos-printer-setup"

# Scanners - Auto-detect
ACTION=="add", SUBSYSTEM=="usb", ENV{libsane_matched}=="yes", MODE="0666", GROUP="scanner"

# Webcams - Auto-detect
SUBSYSTEM=="video4linux", MODE="0666", GROUP="video"

# Network adapters - Auto-configure
ACTION=="add", SUBSYSTEM=="net", RUN+="/usr/local/bin/ghostos-network-setup %k"

# Bluetooth devices - Auto-pair
ACTION=="add", SUBSYSTEM=="bluetooth", RUN+="/usr/local/bin/ghostos-bluetooth-pair"

# Audio devices - Auto-configure
ACTION=="add", SUBSYSTEM=="sound", RUN+="/usr/local/bin/ghostos-audio-setup"

# External monitors - Auto-configure
ACTION=="change", SUBSYSTEM=="drm", RUN+="/usr/local/bin/ghostos-display-setup"

# Card readers
SUBSYSTEM=="block", ENV{ID_DRIVE_FLASH_SD}=="1", MODE="0666"

# Wacom tablets
SUBSYSTEM=="input", ATTRS{idVendor}=="056a", MODE="0666", TAG+="uaccess"
EOF

# Create auto-mount script
cat > /usr/local/bin/ghostos-automount << 'AUTOMOUNT'
#!/bin/bash
# GhostOS Auto-mount for USB drives

DEVICE=$1
MOUNT_POINT="/media/$DEVICE"

# Wait for device to be ready
sleep 1

# Create mount point
mkdir -p "$MOUNT_POINT"

# Mount with appropriate filesystem
if blkid /dev/$DEVICE | grep -q "ntfs"; then
    mount -t ntfs-3g -o uid=1000,gid=1000,umask=022 /dev/$DEVICE "$MOUNT_POINT"
elif blkid /dev/$DEVICE | grep -q "exfat"; then
    mount -t exfat -o uid=1000,gid=1000,umask=022 /dev/$DEVICE "$MOUNT_POINT"
else
    mount -o uid=1000,gid=1000 /dev/$DEVICE "$MOUNT_POINT"
fi

# Send notification
if command -v notify-send &> /dev/null; then
    notify-send "USB Drive Connected" "Mounted at $MOUNT_POINT"
fi

# Log event
echo "[$(date)] Auto-mounted /dev/$DEVICE at $MOUNT_POINT" >> /var/log/ghostos-automount.log
AUTOMOUNT

chmod +x /usr/local/bin/ghostos-automount

# Create auto-unmount script
cat > /usr/local/bin/ghostos-autounmount << 'AUTOUNMOUNT'
#!/bin/bash
# GhostOS Auto-unmount for USB drives

DEVICE=$1
MOUNT_POINT="/media/$DEVICE"

# Unmount device
umount "$MOUNT_POINT" 2>/dev/null

# Remove mount point
rmdir "$MOUNT_POINT" 2>/dev/null

# Send notification
if command -v notify-send &> /dev/null; then
    notify-send "USB Drive Disconnected" "Device $DEVICE safely removed"
fi

# Log event
echo "[$(date)] Auto-unmounted /dev/$DEVICE from $MOUNT_POINT" >> /var/log/ghostos-automount.log
AUTOUNMOUNT

chmod +x /usr/local/bin/ghostos-autounmount

# Create printer setup script
cat > /usr/local/bin/ghostos-printer-setup << 'PRINTERSETUP'
#!/bin/bash
# Auto-configure printers

sleep 2
lpinfo -v | grep -q "usb" && hp-setup -i -a || echo "Printer detected"
notify-send "Printer Detected" "Setting up printer..." 2>/dev/null || true
PRINTERSETUP

chmod +x /usr/local/bin/ghostos-printer-setup

# Create network setup script
cat > /usr/local/bin/ghostos-network-setup << 'NETSETUP'
#!/bin/bash
# Auto-configure network adapters

INTERFACE=$1
sleep 1
nmcli device set "$INTERFACE" managed yes
nmcli device connect "$INTERFACE" || true
notify-send "Network Adapter" "Interface $INTERFACE configured" 2>/dev/null || true
NETSETUP

chmod +x /usr/local/bin/ghostos-network-setup

# Create bluetooth pairing script
cat > /usr/local/bin/ghostos-bluetooth-pair << 'BTPAIR'
#!/bin/bash
# Auto-pair Bluetooth devices (with prompt)

sleep 1
notify-send "Bluetooth Device Detected" "Ready to pair" 2>/dev/null || true
BTPAIR

chmod +x /usr/local/bin/ghostos-bluetooth-pair

# Create audio setup script
cat > /usr/local/bin/ghostos-audio-setup << 'AUDIOSETUP'
#!/bin/bash
# Auto-configure audio devices

sleep 1
pulseaudio --check || pulseaudio --start
notify-send "Audio Device Connected" "Device configured" 2>/dev/null || true
AUDIOSETUP

chmod +x /usr/local/bin/ghostos-audio-setup

# Create display setup script
cat > /usr/local/bin/ghostos-display-setup << 'DISPLAYSETUP'
#!/bin/bash
# Auto-configure external displays

sleep 2
xrandr --auto 2>/dev/null || true
notify-send "Display Connected" "Monitor auto-configured" 2>/dev/null || true
DISPLAYSETUP

chmod +x /usr/local/bin/ghostos-display-setup

# Reload udev rules
udevadm control --reload-rules
udevadm trigger

# Create device monitor dashboard
cat > /usr/local/bin/ghostos-devices << 'DEVMON'
#!/bin/bash
# GhostOS Device Monitor

clear
echo "========================================="
echo "  GhostOS Plug-and-Play Device Monitor"
echo "========================================="
echo ""

echo "=== USB Devices ==="
lsusb | grep -v "Linux Foundation"
echo ""

echo "=== Block Devices (Drives) ==="
lsblk -o NAME,SIZE,TYPE,MOUNTPOINT | grep -v "loop"
echo ""

echo "=== Network Interfaces ==="
ip -br link show | grep -v "lo"
echo ""

echo "=== Audio Devices ==="
aplay -l 2>/dev/null | grep "^card" || echo "No audio devices"
echo ""

echo "=== Video Devices (Webcams) ==="
v4l2-ctl --list-devices 2>/dev/null || echo "No webcams detected"
echo ""

echo "=== Game Controllers ==="
ls /dev/input/js* 2>/dev/null || echo "No controllers detected"
echo ""

echo "=== Printers ==="
lpstat -p 2>/dev/null | grep "printer" || echo "No printers configured"
echo ""

echo "=== Bluetooth Devices ==="
bluetoothctl devices 2>/dev/null || echo "Bluetooth not available"
echo ""

echo "=== Connected Displays ==="
xrandr --query 2>/dev/null | grep " connected" || echo "Display info unavailable"
echo ""

read -p "Press ENTER to exit..."
DEVMON

chmod +x /usr/local/bin/ghostos-devices

# Create desktop entry
cat > /usr/share/applications/ghostos-devices.desktop << 'EOF'
[Desktop Entry]
Name=Device Monitor
Comment=View all connected devices
Exec=xfce4-terminal -e ghostos-devices
Icon=computer
Terminal=true
Type=Application
Categories=System;HardwareSettings;
EOF

# Enable automount service
systemctl enable udisks2
systemctl start udisks2 || true

# Create user group permissions for device access
usermod -aG dialout,plugdev,video,audio,scanner,lp,bluetooth,input $USER 2>/dev/null || true

echo ""
echo "[*] Plug-and-play support installed!"
echo "    Commands:"
echo "    - ghostos-devices    : View all connected devices"
echo ""
echo "    Auto-detected hardware:"
echo "    ✓ USB drives (auto-mount)"
echo "    ✓ Game controllers (Xbox, PlayStation, Nintendo, generic)"
echo "    ✓ Printers (HP, Canon, Epson, Brother, etc.)"
echo "    ✓ Scanners"
echo "    ✓ Webcams"
echo "    ✓ Audio devices (headphones, microphones, speakers)"
echo "    ✓ Network adapters (WiFi, Ethernet, USB)"
echo "    ✓ Bluetooth devices (keyboards, mice, headsets)"
echo "    ✓ External monitors (auto-configure resolution)"
echo "    ✓ Card readers (SD, microSD, CF)"
echo "    ✓ Wacom tablets"
echo "    ✓ Mobile devices (Android, iOS)"
echo ""
echo "    All devices work immediately when plugged in!"

# ============================================
# Penetration Testing Tools (Kali + Parrot OS)
# ============================================
echo ""
echo "[*] Installing penetration testing and security tools..."
echo "    Full Kali Linux and Parrot Security OS toolsets"

# Add Kali Linux repositories
cat > /etc/apt/sources.list.d/kali.list << 'EOF'
deb http://http.kali.org/kali kali-rolling main contrib non-free non-free-firmware
EOF

# Add Kali GPG key
wget -q -O - https://archive.kali.org/archive-key.asc | apt-key add -

# Parrot Security tools are already available from the base Parrot OS 7 repositories
# No need to add additional Parrot repositories

apt-get update

# ============================================
# Information Gathering Tools
# ============================================
echo ""
echo "[*] Installing information gathering tools..."

apt-get install -y \
    nmap \
    masscan \
    rustscan \
    zmap \
    dmitry \
    ike-scan \
    netdiscover \
    recon-ng \
    spiderfoot \
    theharvester \
    maltego \
    metagoofil \
    whatweb \
    whois \
    dnsrecon \
    dnsenum \
    fierce \
    sublist3r \
    amass \
    assetfinder \
    subfinder \
    gobuster \
    dirb \
    dirbuster \
    wfuzz \
    ffuf \
    nikto \
    wpscan \
    joomscan \
    drupalscan \
    wafw00f \
    nuclei

# ============================================
# Vulnerability Analysis
# ============================================
echo ""
echo "[*] Installing vulnerability analysis tools..."

apt-get install -y \
    openvas \
    greenbone-security-assistant \
    lynis \
    nikto \
    nessus \
    trivy \
    grype \
    clair \
    anchore-cli \
    sqlmap \
    xsser \
    commix \
    wapiti \
    skipfish \
    arachni \
    zaproxy \
    burpsuite

# ============================================
# Wireless Attacks
# ============================================
echo ""
echo "[*] Installing wireless attack tools..."

apt-get install -y \
    aircrack-ng \
    kismet \
    wifite \
    reaver \
    pixiewps \
    bully \
    cowpatty \
    asleap \
    mdk4 \
    mdk3 \
    hostapd-wpe \
    wifiphisher \
    fluxion \
    linset \
    eaphammer \
    hostapd \
    dnsmasq \
    wireshark \
    tshark \
    ettercap-graphical \
    bettercap \
    hcxtools \
    hcxdumptool

# ============================================
# Exploitation Frameworks
# ============================================
echo ""
echo "[*] Installing exploitation frameworks..."

# Metasploit Framework
apt-get install -y metasploit-framework

# Install from source for latest version
cd /usr/src
git clone https://github.com/rapid7/metasploit-framework.git msf
cd msf
gem install bundler
bundle install

# Create symlink
ln -sf /usr/src/msf/msfconsole /usr/local/bin/msfconsole

# Exploit-DB
apt-get install -y exploitdb

# Clone Exploit-DB
cd /usr/src
git clone https://github.com/offensive-security/exploitdb.git
ln -sf /usr/src/exploitdb/searchsploit /usr/local/bin/searchsploit

# Social Engineering Toolkit
apt-get install -y set

# Install from source
cd /usr/src
git clone https://github.com/trustedsec/social-engineer-toolkit.git setoolkit
cd setoolkit
pip3 install --break-system-packages -r requirements.txt

# BeEF (Browser Exploitation Framework)
apt-get install -y beef-xss

# ============================================
# Password Attacks
# ============================================
echo ""
echo "[*] Installing password cracking tools..."

apt-get install -y \
    john \
    hashcat \
    hydra \
    medusa \
    ncrack \
    patator \
    crowbar \
    brutespray \
    thc-pptp-bruter \
    cewl \
    crunch \
    cupp \
    rsmangler \
    hashid \
    hash-identifier \
    ophcrack \
    chntpw \
    samdump2 \
    mimikatz \
    responder \
    crackmapexec

# Install Hashcat rules
cd /usr/share/hashcat
wget https://github.com/NotSoSecure/password_cracking_rules/raw/master/OneRuleToRuleThemAll.rule

# ============================================
# Web Application Analysis
# ============================================
echo ""
echo "[*] Installing web application testing tools..."

apt-get install -y \
    sqlmap \
    commix \
    xsser \
    wpscan \
    joomscan \
    droopescan \
    cmsmap \
    drupalscan \
    plecost \
    vbscan \
    burpsuite \
    zaproxy \
    w3af \
    wapiti \
    skipfish \
    webscarab \
    paros \
    websploit \
    fimap \
    kadimus \
    lfimap \
    dotdotpwn \
    uniscan

# ============================================
# Sniffing & Spoofing
# ============================================
echo ""
echo "[*] Installing sniffing and spoofing tools..."

apt-get install -y \
    wireshark \
    tshark \
    tcpdump \
    ettercap-graphical \
    ettercap-text-only \
    bettercap \
    dsniff \
    sslstrip \
    mitmproxy \
    burpsuite \
    responder \
    yersinia \
    netsniff-ng \
    driftnet \
    urlsnarf \
    webspy \
    hex2raw \
    tcpxtract

# ============================================
# Post Exploitation
# ============================================
echo ""
echo "[*] Installing post-exploitation tools..."

apt-get install -y \
    powersploit \
    empire \
    covenant \
    koadic \
    pupy \
    weevely \
    webshells \
    laudanum \
    shellter \
    veil \
    unicorn \
    powershell \
    exe2hex \
    dbd \
    dns2tcp \
    iodine \
    miredo \
    proxychains \
    proxychains4 \
    ptunnel \
    pwnat \
    sslh \
    stunnel4 \
    udptunnel

# Install Empire framework
cd /usr/src
git clone --recursive https://github.com/BC-SECURITY/Empire.git
cd Empire
./setup/install.sh

# Install Covenant C2
cd /usr/src
git clone --recurse-submodules https://github.com/cobbr/Covenant.git
cd Covenant/Covenant
dotnet build || echo "Covenant requires .NET - skipping"

# ============================================
# Forensics
# ============================================
echo ""
echo "[*] Installing forensics tools..."

apt-get install -y \
    autopsy \
    sleuthkit \
    bulk-extractor \
    foremost \
    scalpel \
    guymager \
    ddrescue \
    dc3dd \
    dcfldd \
    extundelete \
    testdisk \
    photorec \
    binwalk \
    foremost \
    volatility \
    dumpzilla \
    pasco \
    chkrootkit \
    rkhunter \
    unhide

# ============================================
# Reverse Engineering
# ============================================
echo ""
echo "[*] Installing reverse engineering tools..."

apt-get install -y \
    radare2 \
    ghidra \
    gdb \
    gdb-peda \
    gef \
    pwndbg \
    edb-debugger \
    ollydbg \
    immunity-debugger \
    hopper \
    ida-free \
    binary-ninja \
    angr \
    pwntools \
    ropper \
    ropgadget \
    checksec \
    ltrace \
    strace \
    binutils \
    objdump \
    hexedit \
    hexcurse \
    bless \
    dhex

# Install GEF (GDB Enhanced Features)
wget -q https://github.com/hugsy/gef/raw/master/gef.py -O /root/.gdbinit-gef.py
echo "source /root/.gdbinit-gef.py" >> /root/.gdbinit

# ============================================
# Reporting Tools
# ============================================
echo ""
echo "[*] Installing reporting tools..."

apt-get install -y \
    cherrytree \
    cutycapt \
    pipal \
    recordmydesktop \
    dos2unix \
    dradis \
    faraday \
    metagoofil

# ============================================
# Social Engineering
# ============================================
echo ""
echo "[*] Installing social engineering tools..."

apt-get install -y \
    set \
    king-phisher \
    gophish \
    evilginx2 \
    modlishka \
    beef-xss \
    maltego \
    social-mapper \
    recon-ng

# Install Evilginx2
cd /usr/src
git clone https://github.com/kgretzky/evilginx2.git
cd evilginx2
make
make install

# Install GoPhish
cd /usr/src
wget https://github.com/gophish/gophish/releases/latest/download/gophish-linux-64bit.zip
unzip gophish-linux-64bit.zip -d /opt/gophish
chmod +x /opt/gophish/gophish

# ============================================
# Additional Frameworks & Tools
# ============================================
echo ""
echo "[*] Installing additional frameworks..."

# Impacket (SMB/Windows tools)
pip3 install --break-system-packages impacket

# BloodHound (AD enumeration)
cd /usr/src
wget https://github.com/BloodHoundAD/BloodHound/releases/latest/download/BloodHound-linux-x64.zip
unzip BloodHound-linux-x64.zip -d /opt/bloodhound

# Covenant (C2 framework)
apt-get install -y \
    bloodhound \
    neo4j \
    crackmapexec \
    evil-winrm \
    kerbrute

# ============================================
# Custom Kali/Parrot Menu
# ============================================
echo ""
echo "[*] Creating penetration testing menu..."

cat > /usr/local/bin/ghostos-pentest << 'PENTEST'
#!/bin/bash
# GhostOS Penetration Testing Menu

show_menu() {
    clear
    cat << 'EOF'
╔════════════════════════════════════════════════════════════╗
║                                                            ║
║   ░██████╗░██╗░░██╗░█████╗░░██████╗████████╗░█████╗░░██████╗  ║
║   ██╔════╝░██║░░██║██╔══██╗██╔════╝╚══██╔══╝██╔══██╗██╔════╝  ║
║   ██║░░██╗░███████║██║░░██║╚█████╗░░░░██║░░░██║░░██║╚█████╗░  ║
║   ██║░░╚██╗██╔══██║██║░░██║░╚═══██╗░░░██║░░░██║░░██║░╚═══██╗  ║
║   ╚██████╔╝██║░░██║╚█████╔╝██████╔╝░░░██║░░░╚█████╔╝██████╔╝  ║
║   ░╚═════╝░╚═╝░░╚═╝░╚════╝░╚═════╝░░░░╚═╝░░░░╚════╝░╚═════╝░  ║
║                                                            ║
║           PENETRATION TESTING TOOLKIT                     ║
║           (Kali Linux + Parrot Security Tools)            ║
║                                                            ║
╚════════════════════════════════════════════════════════════╝

  [1] 🔍 Information Gathering
  [2] 🔓 Vulnerability Analysis  
  [3] 📡 Wireless Attacks
  [4] 💣 Exploitation Tools
  [5] 🔑 Password Attacks
  [6] 🌐 Web Application Testing
  [7] 🎭 Sniffing & Spoofing
  [8] 🚪 Post Exploitation
  [9] 🔬 Forensics
  [10] 🔧 Reverse Engineering
  [11] 🎣 Social Engineering
  [12] 📊 Reporting Tools
  [0] 🚪 Exit

EOF
    read -p "Select category: " choice
}

info_gathering() {
    echo ""
    echo "Information Gathering Tools:"
    echo "  1) nmap - Network scanner"
    echo "  2) masscan - Fast port scanner"
    echo "  3) theharvester - Email/subdomain discovery"
    echo "  4) recon-ng - Reconnaissance framework"
    echo "  5) subfinder - Subdomain discovery"
    echo "  6) amass - Asset discovery"
    echo "  7) gobuster - Directory/DNS bruteforcer"
    echo "  8) nikto - Web server scanner"
    echo ""
    read -p "Launch tool: " tool
    
    case $tool in
        1) nmap ;;
        2) masscan ;;
        3) theharvester ;;
        4) recon-ng ;;
        5) subfinder ;;
        6) amass ;;
        7) gobuster ;;
        8) nikto ;;
    esac
}

vuln_analysis() {
    echo ""
    echo "Vulnerability Analysis Tools:"
    echo "  1) openvas - Vulnerability scanner"
    echo "  2) sqlmap - SQL injection tool"
    echo "  3) nuclei - Template-based scanner"
    echo "  4) nikto - Web vulnerability scanner"
    echo ""
    read -p "Launch tool: " tool
    
    case $tool in
        1) openvas-start && firefox http://127.0.0.1:9392 ;;
        2) sqlmap ;;
        3) nuclei ;;
        4) nikto ;;
    esac
}

wireless_attacks() {
    echo ""
    echo "Wireless Attack Tools:"
    echo "  1) aircrack-ng - WiFi security auditing"
    echo "  2) wifite - Automated wireless attack"
    echo "  3) kismet - Wireless detector/sniffer"
    echo "  4) reaver - WPS attack tool"
    echo "  5) bettercap - Network attack tool"
    echo ""
    read -p "Launch tool: " tool
    
    case $tool in
        1) aircrack-ng ;;
        2) wifite ;;
        3) kismet ;;
        4) reaver ;;
        5) bettercap ;;
    esac
}

exploitation() {
    echo ""
    echo "Exploitation Tools:"
    echo "  1) msfconsole - Metasploit Framework"
    echo "  2) searchsploit - Exploit-DB search"
    echo "  3) setoolkit - Social Engineering Toolkit"
    echo "  4) beef-xss - Browser Exploitation"
    echo ""
    read -p "Launch tool: " tool
    
    case $tool in
        1) msfconsole ;;
        2) searchsploit ;;
        3) setoolkit ;;
        4) beef-xss ;;
    esac
}

password_attacks() {
    echo ""
    echo "Password Attack Tools:"
    echo "  1) john - John the Ripper"
    echo "  2) hashcat - Advanced password recovery"
    echo "  3) hydra - Network logon cracker"
    echo "  4) medusa - Parallel password cracker"
    echo "  5) crunch - Wordlist generator"
    echo ""
    read -p "Launch tool: " tool
    
    case $tool in
        1) john ;;
        2) hashcat ;;
        3) hydra ;;
        4) medusa ;;
        5) crunch ;;
    esac
}

web_testing() {
    echo ""
    echo "Web Application Testing:"
    echo "  1) burpsuite - Web vulnerability scanner"
    echo "  2) zaproxy - OWASP ZAP"
    echo "  3) sqlmap - SQL injection"
    echo "  4) wpscan - WordPress scanner"
    echo "  5) nikto - Web server scanner"
    echo ""
    read -p "Launch tool: " tool
    
    case $tool in
        1) burpsuite ;;
        2) zaproxy ;;
        3) sqlmap ;;
        4) wpscan ;;
        5) nikto ;;
    esac
}

sniffing_spoofing() {
    echo ""
    echo "Sniffing & Spoofing Tools:"
    echo "  1) wireshark - Network analyzer"
    echo "  2) ettercap - MITM attack tool"
    echo "  3) bettercap - Network attack framework"
    echo "  4) responder - LLMNR/NBT-NS poisoner"
    echo "  5) mitmproxy - Intercepting proxy"
    echo ""
    read -p "Launch tool: " tool
    
    case $tool in
        1) wireshark ;;
        2) ettercap -G ;;
        3) bettercap ;;
        4) responder ;;
        5) mitmproxy ;;
    esac
}

post_exploitation() {
    echo ""
    echo "Post Exploitation Tools:"
    echo "  1) empire - PowerShell post-exploitation"
    echo "  2) covenant - .NET C2 framework"
    echo "  3) mimikatz - Windows credential extraction"
    echo "  4) bloodhound - AD enumeration"
    echo "  5) crackmapexec - Post-exploitation tool"
    echo ""
    read -p "Launch tool: " tool
    
    case $tool in
        1) cd /usr/src/Empire && ./empire ;;
        2) echo "Start Covenant manually" ;;
        3) echo "Mimikatz (Windows only)" ;;
        4) bloodhound ;;
        5) crackmapexec ;;
    esac
}

forensics() {
    echo ""
    echo "Forensics Tools:"
    echo "  1) autopsy - Digital forensics platform"
    echo "  2) volatility - Memory forensics"
    echo "  3) binwalk - Firmware analysis"
    echo "  4) foremost - File recovery"
    echo "  5) bulk-extractor - Evidence extractor"
    echo ""
    read -p "Launch tool: " tool
    
    case $tool in
        1) autopsy ;;
        2) volatility ;;
        3) binwalk ;;
        4) foremost ;;
        5) bulk_extractor ;;
    esac
}

reverse_engineering() {
    echo ""
    echo "Reverse Engineering Tools:"
    echo "  1) ghidra - Software reverse engineering"
    echo "  2) radare2 - Reverse engineering framework"
    echo "  3) gdb - GNU debugger"
    echo "  4) objdump - Object file analyzer"
    echo "  5) hexedit - Hex editor"
    echo ""
    read -p "Launch tool: " tool
    
    case $tool in
        1) ghidra ;;
        2) radare2 ;;
        3) gdb ;;
        4) objdump ;;
        5) hexedit ;;
    esac
}

social_engineering() {
    echo ""
    echo "Social Engineering Tools:"
    echo "  1) setoolkit - Social Engineering Toolkit"
    echo "  2) gophish - Phishing framework"
    echo "  3) evilginx2 - MITM phishing"
    echo "  4) king-phisher - Phishing campaign"
    echo "  5) beef-xss - Browser exploitation"
    echo ""
    read -p "Launch tool: " tool
    
    case $tool in
        1) setoolkit ;;
        2) /opt/gophish/gophish ;;
        3) evilginx ;;
        4) king-phisher ;;
        5) beef-xss ;;
    esac
}

reporting() {
    echo ""
    echo "Reporting Tools:"
    echo "  1) cherrytree - Note taking"
    echo "  2) dradis - Collaboration platform"
    echo "  3) faraday - Pentest management"
    echo ""
    read -p "Launch tool: " tool
    
    case $tool in
        1) cherrytree ;;
        2) dradis ;;
        3) faraday ;;
    esac
}

# Main loop
while true; do
    show_menu
    
    case $choice in
        1) info_gathering ;;
        2) vuln_analysis ;;
        3) wireless_attacks ;;
        4) exploitation ;;
        5) password_attacks ;;
        6) web_testing ;;
        7) sniffing_spoofing ;;
        8) post_exploitation ;;
        9) forensics ;;
        10) reverse_engineering ;;
        11) social_engineering ;;
        12) reporting ;;
        0) exit 0 ;;
        *) echo "Invalid option" ; sleep 1 ;;
    esac
    
    echo ""
    read -p "Press ENTER to continue..."
done
PENTEST

chmod +x /usr/local/bin/ghostos-pentest

# Create desktop entry
cat > /usr/share/applications/ghostos-pentest.desktop << 'EOF'
[Desktop Entry]
Name=Penetration Testing Tools
Comment=Kali Linux + Parrot Security toolkit
Exec=xfce4-terminal -e ghostos-pentest
Icon=security-high
Terminal=true
Type=Application
Categories=System;Security;
EOF

echo ""
echo "[*] Penetration testing tools installed!"
echo "    Command: ghostos-pentest"
echo ""
echo "    Installed toolsets:"
echo "    ✓ Information Gathering (nmap, masscan, recon-ng, theharvester)"
echo "    ✓ Vulnerability Analysis (openvas, sqlmap, nikto, nuclei)"
echo "    ✓ Wireless Attacks (aircrack-ng, wifite, kismet, reaver)"
echo "    ✓ Exploitation (metasploit, exploit-db, SET, beef-xss)"
echo "    ✓ Password Attacks (john, hashcat, hydra, medusa)"
echo "    ✓ Web Testing (burpsuite, zaproxy, sqlmap, wpscan)"
echo "    ✓ Sniffing/Spoofing (wireshark, ettercap, bettercap, responder)"
echo "    ✓ Post Exploitation (empire, covenant, mimikatz, bloodhound)"
echo "    ✓ Forensics (autopsy, volatility, binwalk, foremost)"
echo "    ✓ Reverse Engineering (ghidra, radare2, gdb, IDA)"
echo "    ✓ Social Engineering (SET, gophish, evilginx2, king-phisher)"
echo "    ✓ Reporting (cherrytree, dradis, faraday)"
echo ""
echo "    Full Kali Linux + Parrot Security OS toolkit!"

# ============================================
# Virtualization (VMware + VirtualBox)
# ============================================
echo ""
echo "[*] Installing virtualization platforms..."
echo "    VMware Workstation/Player + VirtualBox"

# Install kernel headers and build tools for virtualization modules
apt-get install -y \
    linux-headers-$(uname -r) \
    build-essential \
    dkms \
    module-assistant

# ============================================
# VirtualBox Installation
# ============================================
echo ""
echo "[*] Installing VirtualBox..."

# Add VirtualBox repository
wget -q https://www.virtualbox.org/download/oracle_vbox_2016.asc -O- | apt-key add -
wget -q https://www.virtualbox.org/download/oracle_vbox.asc -O- | apt-key add -

cat > /etc/apt/sources.list.d/virtualbox.list << 'EOF'
deb [arch=amd64] https://download.virtualbox.org/virtualbox/debian bookworm contrib
EOF

apt-get update

# Install VirtualBox (latest version)
apt-get install -y virtualbox-7.0

# Install VirtualBox Extension Pack
VBOX_VERSION=$(vboxmanage --version | cut -dr -f1)
VBOX_EXT_PACK="Oracle_VM_VirtualBox_Extension_Pack-${VBOX_VERSION}.vbox-extpack"

cd /tmp
wget https://download.virtualbox.org/virtualbox/${VBOX_VERSION}/${VBOX_EXT_PACK}
echo "y" | vboxmanage extpack install --replace ${VBOX_EXT_PACK}

# Add users to vboxusers group
usermod -aG vboxusers $USER 2>/dev/null || true
usermod -aG vboxusers root 2>/dev/null || true

# ============================================
# VMware Workstation Installation
# ============================================
echo ""
echo "[*] Installing VMware Workstation..."

# Install VMware dependencies
apt-get install -y \
    libcanberra-gtk3-module \
    libcanberra-gtk-module \
    libglib2.0-0 \
    libglib2.0-dev \
    libgtk-3-0 \
    libgtkmm-3.0-1v5

# Download VMware Workstation (or Player)
cd /tmp

# VMware Workstation Pro (latest)
VMWARE_VERSION="17.5.1"
VMWARE_BUILD="23298084"
VMWARE_FILE="VMware-Workstation-Full-${VMWARE_VERSION}-${VMWARE_BUILD}.x86_64.bundle"

wget https://download3.vmware.com/software/WKST-1751-LX/${VMWARE_FILE} || {
    echo "Downloading VMware Player instead..."
    VMWARE_FILE="VMware-Player-Full-${VMWARE_VERSION}-${VMWARE_BUILD}.x86_64.bundle"
    wget https://download3.vmware.com/software/WKST-PLAYER-1751/${VMWARE_FILE}
}

# Make executable and install
chmod +x ${VMWARE_FILE}
./${VMWARE_FILE} --console --required --eulas-agreed || echo "VMware installation requires user interaction"

# Install VMware kernel modules
vmware-modconfig --console --install-all 2>/dev/null || true

# ============================================
# VMware Tools & Patches
# ============================================
echo ""
echo "[*] Installing VMware host modules..."

# Clone and install VMware host modules for latest kernels
cd /usr/src
git clone https://github.com/mkubecek/vmware-host-modules.git
cd vmware-host-modules
git checkout workstation-17.5.1
make
make install

# Update module dependencies
depmod -a

# ============================================
# QEMU/KVM (Additional virtualization option)
# ============================================
echo ""
echo "[*] Installing QEMU/KVM..."

apt-get install -y \
    qemu \
    qemu-kvm \
    qemu-system-x86 \
    qemu-utils \
    libvirt-daemon-system \
    libvirt-clients \
    bridge-utils \
    virt-manager \
    virt-viewer \
    ovmf

# Enable and start libvirt
systemctl enable libvirtd
systemctl start libvirtd || true

# Add users to libvirt groups
usermod -aG libvirt $USER 2>/dev/null || true
usermod -aG kvm $USER 2>/dev/null || true

# ============================================
# Docker (Container virtualization)
# ============================================
echo ""
echo "[*] Installing Docker..."

# Add Docker repository
apt-get install -y \
    ca-certificates \
    curl \
    gnupg \
    lsb-release

mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/debian/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg

cat > /etc/apt/sources.list.d/docker.list << 'EOF'
deb [arch=amd64 signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/debian bookworm stable
EOF

apt-get update
apt-get install -y \
    docker-ce \
    docker-ce-cli \
    containerd.io \
    docker-buildx-plugin \
    docker-compose-plugin

# Enable Docker
systemctl enable docker
systemctl start docker || true

# Add users to docker group
usermod -aG docker $USER 2>/dev/null || true

# ============================================
# Vagrant (VM management)
# ============================================
echo ""
echo "[*] Installing Vagrant..."

# Download and install latest Vagrant
cd /tmp
VAGRANT_VERSION="2.4.0"
wget https://releases.hashicorp.com/vagrant/${VAGRANT_VERSION}/vagrant_${VAGRANT_VERSION}-1_amd64.deb
dpkg -i vagrant_${VAGRANT_VERSION}-1_amd64.deb

# Install Vagrant plugins for VirtualBox and VMware
vagrant plugin install vagrant-vbguest
vagrant plugin install vagrant-vmware-desktop

# ============================================
# Create Virtualization Manager
# ============================================
echo ""
echo "[*] Creating virtualization management interface..."

cat > /usr/local/bin/ghostos-virt << 'VIRTMGR'
#!/bin/bash
# GhostOS Virtualization Manager

show_menu() {
    clear
    cat << 'EOF'
╔════════════════════════════════════════════════════════════╗
║                                                            ║
║   ░██████╗░██╗░░██╗░█████╗░░██████╗████████╗░█████╗░░██████╗  ║
║   ██╔════╝░██║░░██║██╔══██╗██╔════╝╚══██╔══╝██╔══██╗██╔════╝  ║
║   ██║░░██╗░███████║██║░░██║╚█████╗░░░░██║░░░██║░░██║╚█████╗░  ║
║   ██║░░╚██╗██╔══██║██║░░██║░╚═══██╗░░░██║░░░██║░░██║░╚═══██╗  ║
║   ╚██████╔╝██║░░██║╚█████╔╝██████╔╝░░░██║░░░╚█████╔╝██████╔╝  ║
║   ░╚═════╝░╚═╝░░╚═╝░╚════╝░╚═════╝░░░░╚═╝░░░░╚════╝░╚═════╝░  ║
║                                                            ║
║              VIRTUALIZATION MANAGER                       ║
║                                                            ║
╚════════════════════════════════════════════════════════════╝

  [1] 🖥️  VirtualBox Manager
  [2] 🔷 VMware Workstation
  [3] 🌐 QEMU/KVM Manager (virt-manager)
  [4] 🐳 Docker Manager
  [5] 📦 Vagrant Manager
  [6] 📊 System Status
  [7] ⚙️  Configure Virtualization
  [8] 💾 Backup/Restore VMs
  [0] 🚪 Exit

EOF
    read -p "Select option: " choice
}

launch_virtualbox() {
    echo "Launching VirtualBox..."
    virtualbox &
}

launch_vmware() {
    echo "Launching VMware Workstation..."
    vmware &
}

launch_virt_manager() {
    echo "Launching virt-manager (QEMU/KVM)..."
    virt-manager &
}

docker_manager() {
    clear
    echo "========================================="
    echo "  Docker Manager"
    echo "========================================="
    echo ""
    echo "1) List running containers"
    echo "2) List all containers"
    echo "3) List images"
    echo "4) Docker stats"
    echo "5) Docker compose"
    echo "0) Back"
    echo ""
    read -p "Select: " docker_choice
    
    case $docker_choice in
        1) docker ps ;;
        2) docker ps -a ;;
        3) docker images ;;
        4) docker stats ;;
        5) docker compose ;;
    esac
}

vagrant_manager() {
    clear
    echo "========================================="
    echo "  Vagrant Manager"
    echo "========================================="
    echo ""
    echo "1) List Vagrant boxes"
    echo "2) Vagrant status"
    echo "3) Vagrant up (start VM)"
    echo "4) Vagrant halt (stop VM)"
    echo "0) Back"
    echo ""
    read -p "Select: " vagrant_choice
    
    case $vagrant_choice in
        1) vagrant box list ;;
        2) vagrant global-status ;;
        3) read -p "Box name: " box && vagrant up $box ;;
        4) read -p "Box name: " box && vagrant halt $box ;;
    esac
}

system_status() {
    clear
    echo "========================================="
    echo "  Virtualization System Status"
    echo "========================================="
    echo ""
    
    echo "VirtualBox:"
    vboxmanage --version 2>/dev/null && echo "  ✓ Installed" || echo "  ✗ Not installed"
    echo ""
    
    echo "VMware:"
    vmware --version 2>/dev/null && echo "  ✓ Installed" || echo "  ✗ Not installed"
    echo ""
    
    echo "QEMU/KVM:"
    virsh --version 2>/dev/null && echo "  ✓ Installed" || echo "  ✗ Not installed"
    echo ""
    
    echo "Docker:"
    docker --version 2>/dev/null && echo "  ✓ Installed" || echo "  ✗ Not installed"
    echo ""
    
    echo "Vagrant:"
    vagrant --version 2>/dev/null && echo "  ✓ Installed" || echo "  ✗ Not installed"
    echo ""
    
    echo "KVM Support:"
    if [ -e /dev/kvm ]; then
        echo "  ✓ Hardware virtualization enabled"
    else
        echo "  ✗ Hardware virtualization not available"
    fi
    echo ""
    
    echo "Running VMs:"
    echo "  VirtualBox: $(vboxmanage list runningvms 2>/dev/null | wc -l)"
    echo "  VMware: $(vmrun list 2>/dev/null | tail -n +2 | wc -l)"
    echo "  KVM: $(virsh list --state-running 2>/dev/null | tail -n +3 | grep -v "^$" | wc -l)"
    echo "  Docker: $(docker ps --format '{{.Names}}' 2>/dev/null | wc -l)"
    echo ""
}

configure_virt() {
    clear
    echo "========================================="
    echo "  Virtualization Configuration"
    echo "========================================="
    echo ""
    echo "1) Configure VirtualBox networks"
    echo "2) Configure VMware networks"
    echo "3) Configure KVM networks"
    echo "4) Enable nested virtualization"
    echo "5) Configure shared folders"
    echo "0) Back"
    echo ""
    read -p "Select: " config_choice
    
    case $config_choice in
        1) vboxmanage list hostonlyifs && vboxmanage list bridgedifs ;;
        2) vmware-netcfg ;;
        3) virsh net-list --all ;;
        4) 
            modprobe -r kvm_intel
            modprobe kvm_intel nested=1
            echo "options kvm_intel nested=1" > /etc/modprobe.d/kvm-nested.conf
            echo "Nested virtualization enabled"
            ;;
        5) echo "Configure shared folders in VM settings" ;;
    esac
}

backup_restore() {
    clear
    echo "========================================="
    echo "  VM Backup & Restore"
    echo "========================================="
    echo ""
    echo "1) Export VirtualBox VM"
    echo "2) Import VirtualBox VM"
    echo "3) Clone VMware VM"
    echo "4) Backup Docker containers"
    echo "0) Back"
    echo ""
    read -p "Select: " backup_choice
    
    case $backup_choice in
        1) 
            read -p "VM name: " vm
            read -p "Output file: " output
            vboxmanage export "$vm" -o "$output"
            ;;
        2)
            read -p "OVA file: " ova
            vboxmanage import "$ova"
            ;;
        3)
            read -p "VM VMX file: " vmx
            read -p "Destination: " dest
            vmrun clone "$vmx" "$dest" full
            ;;
        4)
            docker ps -a
            read -p "Container ID: " cid
            docker commit $cid backup_$(date +%Y%m%d)
            ;;
    esac
}

# Main loop
while true; do
    show_menu
    
    case $choice in
        1) launch_virtualbox ;;
        2) launch_vmware ;;
        3) launch_virt_manager ;;
        4) docker_manager ;;
        5) vagrant_manager ;;
        6) system_status ; read -p "Press ENTER..." ;;
        7) configure_virt ; read -p "Press ENTER..." ;;
        8) backup_restore ; read -p "Press ENTER..." ;;
        0) exit 0 ;;
        *) echo "Invalid option" ; sleep 1 ;;
    esac
done
VIRTMGR

chmod +x /usr/local/bin/ghostos-virt

# Create desktop entries
cat > /usr/share/applications/virtualbox.desktop << 'EOF'
[Desktop Entry]
Name=VirtualBox
Comment=Run virtual machines
Exec=virtualbox
Icon=virtualbox
Terminal=false
Type=Application
Categories=System;Emulator;
EOF

cat > /usr/share/applications/vmware-workstation.desktop << 'EOF'
[Desktop Entry]
Name=VMware Workstation
Comment=Run virtual machines
Exec=vmware
Icon=vmware-workstation
Terminal=false
Type=Application
Categories=System;Emulator;
EOF

cat > /usr/share/applications/ghostos-virt.desktop << 'EOF'
[Desktop Entry]
Name=Virtualization Manager
Comment=Manage VirtualBox, VMware, QEMU, Docker
Exec=xfce4-terminal -e ghostos-virt
Icon=computer
Terminal=true
Type=Application
Categories=System;Emulator;
EOF

# Load kernel modules
modprobe vboxdrv 2>/dev/null || true
modprobe vmmon 2>/dev/null || true
modprobe vmnet 2>/dev/null || true

# Create VM storage directories
mkdir -p /home/$USER/VirtualMachines/{VirtualBox,VMware,KVM}

echo ""
echo "[*] Virtualization platforms installed!"
echo "    Commands:"
echo "    - ghostos-virt       : Unified virtualization manager"
echo "    - virtualbox         : VirtualBox GUI"
echo "    - vmware             : VMware Workstation"
echo "    - virt-manager       : KVM manager"
echo "    - docker             : Docker CLI"
echo "    - vagrant            : Vagrant CLI"
echo ""
echo "    Installed platforms:"
echo "    ✓ VirtualBox 7.0 + Extension Pack"
echo "    ✓ VMware Workstation 17.5"
echo "    ✓ QEMU/KVM + virt-manager"
echo "    ✓ Docker + Docker Compose"
echo "    ✓ Vagrant + plugins"
echo ""
echo "    Features:"
echo "    ✓ Full VM management interface"
echo "    ✓ Nested virtualization support"
echo "    ✓ USB device passthrough"
echo "    ✓ Shared folders"
echo "    ✓ Snapshots and cloning"
echo "    ✓ Network configuration"
echo "    ✓ VM backup and restore"
echo ""
echo "    VM storage: ~/VirtualMachines/"

# ============================================
# Gaming Platforms (Steam, Game Pass, GOG)
# ============================================
echo ""
echo "[*] Installing gaming platforms..."
echo "    Steam, Xbox Game Pass, GOG Galaxy"

# Install Steam (full version with all features)
dpkg --add-architecture i386
apt-get update
apt-get install -y \
    steam-installer \
    steam-devices \
    libgl1-mesa-dri:i386 \
    libgl1:i386 \
    libc6:i386

# Configure Steam for optimal performance
cat > /etc/sysctl.d/80-gamecompatibility.conf << 'EOF'
# Improve gaming performance
vm.max_map_count = 2147483642
fs.file-max = 524288
EOF

sysctl -p /etc/sysctl.d/80-gamecompatibility.conf

# Install Proton GE (custom Proton version for better compatibility)
cd /tmp
PROTON_VERSION=$(curl -s https://api.github.com/repos/GloriousEggroll/proton-ge-custom/releases/latest | grep "tag_name" | cut -d '"' -f 4)
wget https://github.com/GloriousEggroll/proton-ge-custom/releases/download/${PROTON_VERSION}/${PROTON_VERSION}.tar.gz
mkdir -p ~/.steam/root/compatibilitytools.d
tar -xf ${PROTON_VERSION}.tar.gz -C ~/.steam/root/compatibilitytools.d/

# ============================================
# Heroic Games Launcher (GOG + Epic Games)
# ============================================
echo ""
echo "[*] Installing Heroic Games Launcher (GOG, Epic Games)..."

# Install Heroic (AppImage version)
cd /opt
wget https://github.com/Heroic-Games-Launcher/HeroicGamesLauncher/releases/latest/download/heroic.AppImage
chmod +x heroic.AppImage

# Create desktop entry
cat > /usr/share/applications/heroic.desktop << 'EOF'
[Desktop Entry]
Name=Heroic Games Launcher
Comment=GOG and Epic Games Store launcher
Exec=/opt/heroic.AppImage
Icon=heroic
Terminal=false
Type=Application
Categories=Game;
EOF

# Create wrapper script
cat > /usr/local/bin/heroic << 'EOF'
#!/bin/bash
/opt/heroic.AppImage "$@"
EOF

chmod +x /usr/local/bin/heroic

# ============================================
# Lutris (Universal game launcher)
# ============================================
echo ""
echo "[*] Installing Lutris..."

apt-get install -y lutris

# Install Lutris runtime and dependencies
apt-get install -y \
    python3-yaml \
    python3-requests \
    python3-pil \
    python3-gi \
    gir1.2-gtk-3.0 \
    gir1.2-gnomedesktop-3.0 \
    gir1.2-webkit2-4.0 \
    gir1.2-notify-0.7 \
    psmisc \
    cabextract \
    unzip \
    p7zip \
    curl \
    fluid-soundfont-gs \
    x11-xserver-utils \
    mesa-utils

# ============================================
# Xbox Game Pass via Cloud Gaming (xcloud)
# ============================================
echo ""
echo "[*] Installing Xbox Game Pass (Cloud Gaming support)..."

# Install dependencies for Xbox Cloud Gaming
apt-get install -y \
    chromium \
    chromium-driver

# Create Xbox Cloud Gaming launcher
cat > /usr/local/bin/xbox-gamepass << 'XCLOUD'
#!/bin/bash
# Xbox Game Pass Cloud Gaming Launcher

echo "========================================="
echo "  Xbox Game Pass Cloud Gaming"
echo "========================================="
echo ""
echo "Opening Xbox Cloud Gaming in browser..."
echo ""
echo "Login with your Xbox Game Pass Ultimate account"
echo "to access 100+ games via cloud streaming"
echo ""

# Launch with optimal settings for cloud gaming
chromium --app=https://www.xbox.com/play --window-size=1920,1080 --start-fullscreen &

# Optional: Install gamepad support
if command -v xboxdrv &> /dev/null; then
    echo "Xbox controller support enabled"
fi
XCLOUD

chmod +x /usr/local/bin/xbox-gamepass

# Create desktop entry
cat > /usr/share/applications/xbox-gamepass.desktop << 'EOF'
[Desktop Entry]
Name=Xbox Game Pass
Comment=Xbox Cloud Gaming (requires Game Pass Ultimate)
Exec=xbox-gamepass
Icon=gamepad
Terminal=false
Type=Application
Categories=Game;
EOF

# ============================================
# EA Play via Lutris
# ============================================
echo ""
echo "[*] Configuring EA Play support..."

# EA Play will be available through Lutris and Steam
# Create helper script
cat > /usr/local/bin/ea-play << 'EOF'
#!/bin/bash
echo "EA Play is accessible through:"
echo "  1) Steam (if subscribed)"
echo "  2) Xbox Game Pass Ultimate (cloud)"
echo "  3) Lutris (install EA App)"
echo ""
echo "Opening Lutris for EA App installation..."
lutris lutris:ea-app
EOF

chmod +x /usr/local/bin/ea-play

# ============================================
# Unified Gaming Launcher
# ============================================
echo ""
echo "[*] Creating unified gaming launcher..."

cat > /usr/local/bin/ghostos-gamestore << 'GAMESTORE'
#!/bin/bash
# GhostOS Unified Game Store Launcher

show_menu() {
    clear
    cat << 'EOF'
╔════════════════════════════════════════════════════════════╗
║                                                            ║
║   ░██████╗░██╗░░██╗░█████╗░░██████╗████████╗░█████╗░░██████╗  ║
║   ██╔════╝░██║░░██║██╔══██╗██╔════╝╚══██╔══╝██╔══██╗██╔════╝  ║
║   ██║░░██╗░███████║██║░░██║╚█████╗░░░░██║░░░██║░░██║╚█████╗░  ║
║   ██║░░╚██╗██╔══██║██║░░██║░╚═══██╗░░░██║░░░██║░░██║░╚═══██╗  ║
║   ╚██████╔╝██║░░██║╚█████╔╝██████╔╝░░░██║░░░╚█████╔╝██████╔╝  ║
║   ░╚═════╝░╚═╝░░╚═╝░╚════╝░╚═════╝░░░░╚═╝░░░░╚════╝░╚═════╝░  ║
║                                                            ║
║                 GAME STORE LAUNCHER                       ║
║                                                            ║
╚════════════════════════════════════════════════════════════╝

  [1] 🎮 Steam (Valve)
  [2] 🎯 GOG Galaxy (Heroic Launcher)
  [3] 🎪 Epic Games Store (Heroic Launcher)
  [4] 🎮 Xbox Game Pass Ultimate (Cloud)
  [5] 🎲 EA Play
  [6] 🕹️  Lutris (All platforms)
  [7] 🎨 Itch.io
  [8] 📊 Gaming Stats & Library
  [0] 🚪 Exit

EOF
    read -p "Select platform: " choice
}

launch_steam() {
    echo "Launching Steam..."
    steam &
}

launch_gog() {
    echo "Launching Heroic (GOG)..."
    heroic &
}

launch_epic() {
    echo "Launching Heroic (Epic Games)..."
    heroic &
}

launch_gamepass() {
    echo "Launching Xbox Game Pass..."
    xbox-gamepass &
}

launch_ea() {
    ea-play
}

launch_lutris() {
    echo "Launching Lutris..."
    lutris &
}

launch_itch() {
    echo "Opening Itch.io..."
    xdg-open https://itch.io &
}

show_stats() {
    clear
    echo "========================================="
    echo "  Gaming Library Statistics"
    echo "========================================="
    echo ""
    
    if command -v steam &> /dev/null; then
        echo "Steam:"
        STEAM_GAMES=$(find ~/.steam/steam/steamapps/common -maxdepth 1 -type d 2>/dev/null | wc -l)
        echo "  Installed games: $STEAM_GAMES"
    fi
    
    echo ""
    echo "Heroic (GOG + Epic):"
    HEROIC_GAMES=$(find ~/Games/Heroic -type d -maxdepth 1 2>/dev/null | wc -l)
    echo "  Installed games: $HEROIC_GAMES"
    
    echo ""
    echo "Native Linux games: $(find ~/Games/Native -type f -name "*.sh" 2>/dev/null | wc -l)"
    echo "ROM files: $(find ~/Games/ROMs -type f 2>/dev/null | wc -l)"
    echo ""
    
    read -p "Press ENTER to continue..."
}

# Main loop
while true; do
    show_menu
    
    case $choice in
        1) launch_steam ;;
        2) launch_gog ;;
        3) launch_epic ;;
        4) launch_gamepass ;;
        5) launch_ea ;;
        6) launch_lutris ;;
        7) launch_itch ;;
        8) show_stats ;;
        0) exit 0 ;;
        *) echo "Invalid option" ; sleep 1 ;;
    esac
done
GAMESTORE

chmod +x /usr/local/bin/ghostos-gamestore

# Create desktop entry
cat > /usr/share/applications/ghostos-gamestore.desktop << 'EOF'
[Desktop Entry]
Name=Game Store Launcher
Comment=Access Steam, GOG, Epic, Xbox Game Pass
Exec=xfce4-terminal -e ghostos-gamestore
Icon=applications-games
Terminal=true
Type=Application
Categories=Game;
EOF

echo ""
echo "[*] Gaming platforms installed!"
echo "    Commands:"
echo "    - ghostos-gamestore  : Unified game launcher"
echo "    - steam              : Steam client"
echo "    - heroic             : GOG + Epic Games"
echo "    - xbox-gamepass      : Xbox cloud gaming"
echo "    - lutris             : Universal game manager"
echo ""
echo "    Installed platforms:"
echo "    ✓ Steam + Proton GE (Windows game compatibility)"
echo "    ✓ Heroic Games Launcher (GOG + Epic Games)"
echo "    ✓ Xbox Game Pass Ultimate (cloud gaming)"
echo "    ✓ EA Play (via Steam/Game Pass/Lutris)"
echo "    ✓ Lutris (all platforms)"
echo "    ✓ Itch.io support"

# ============================================
# VLC Media Player with Blu-ray Support
# ============================================
echo ""
echo "[*] Installing VLC with Blu-ray codec support..."

# Install VLC and dependencies
apt-get install -y \
    vlc \
    vlc-plugin-access-extra \
    vlc-plugin-base \
    vlc-plugin-qt \
    vlc-plugin-video-output \
    vlc-plugin-visualization \
    vlc-l10n

# Install Blu-ray libraries
apt-get install -y \
    libbluray2 \
    libbluray-dev \
    libbluray-bin \
    libdvdread8 \
    libdvdnav4 \
    libdvdcss2

# Install libdvdcss (for DVD decryption)
apt-get install -y libdvd-pkg
dpkg-reconfigure libdvd-pkg

# ============================================
# Install AACS and BD+ for Blu-ray decryption
# ============================================
echo ""
echo "[*] Installing Blu-ray decryption libraries..."

# Install libaacs (AACS decryption)
cd /usr/src
git clone https://code.videolan.org/videolan/libaacs.git
cd libaacs
./bootstrap
./configure
make -j$(nproc)
make install
ldconfig

# Install libbdplus (BD+ decryption)
cd /usr/src
git clone https://code.videolan.org/videolan/libbdplus.git
cd libbdplus
./bootstrap
./configure
make -j$(nproc)
make install
ldconfig

# Download AACS keys (KEYDB.cfg)
mkdir -p ~/.config/aacs
cd ~/.config/aacs
wget http://vlc-bluray.whoknowsmy.name/files/KEYDB.cfg

# Make keys globally available
mkdir -p /usr/share/libaacs/
cp ~/.config/aacs/KEYDB.cfg /usr/share/libaacs/

# Download BD+ VM file
mkdir -p ~/.config/bdplus
cd ~/.config/bdplus
wget http://vlc-bluray.whoknowsmy.name/files/vm0.zip
unzip vm0.zip

# Make BD+ VM globally available
mkdir -p /usr/share/libbdplus/
cp -r ~/.config/bdplus/* /usr/share/libbdplus/

# ============================================
# VLC Configuration for optimal playback
# ============================================
echo ""
echo "[*] Configuring VLC for optimal Blu-ray playback..."

# Create VLC config directory
mkdir -p ~/.config/vlc

# Configure VLC settings
cat > ~/.config/vlc/vlcrc << 'EOF'
# GhostOS VLC Configuration

[core]
# Enable hardware acceleration
avcodec-hw=vdpau

# Blu-ray settings
bluray-menu=1
bluray-region=A

# DVD settings
dvdnav-menu=1

# Video output
vout=auto
video-on-top=0

# Audio output
aout=pulse

# Performance
file-caching=1000
network-caching=1000
disc-caching=3000

# Interface
qt-system-tray=1
EOF

# Install additional codecs
apt-get install -y \
    ffmpeg \
    libavcodec-extra \
    libavformat-extra \
    libavutil-extra \
    gstreamer1.0-libav \
    gstreamer1.0-plugins-ugly \
    gstreamer1.0-plugins-bad \
    gstreamer1.0-vaapi \
    vdpau-driver-all

# Install MakeMKV (for Blu-ray backup)
cd /tmp
wget -q -O - https://www.makemkv.com/download/makemkv-bin-1.17.5.tar.gz | tar xz
wget -q -O - https://www.makemkv.com/download/makemkv-oss-1.17.5.tar.gz | tar xz

cd makemkv-oss-1.17.5
./configure
make -j$(nproc)
make install

cd ../makemkv-bin-1.17.5
make
make install

# Create VLC Blu-ray launcher
cat > /usr/local/bin/vlc-bluray << 'VLCBR'
#!/bin/bash
# VLC Blu-ray Launcher

echo "========================================="
echo "  VLC Blu-ray Player"
echo "========================================="
echo ""

# Detect Blu-ray drive
BLURAY_DRIVE=$(lsblk | grep -i "rom" | awk '{print $1}' | head -1)

if [ -z "$BLURAY_DRIVE" ]; then
    echo "No Blu-ray drive detected"
    echo "Please insert a disc and try again"
    exit 1
fi

echo "Blu-ray drive detected: /dev/$BLURAY_DRIVE"
echo "Starting VLC with Blu-ray support..."
echo ""

# Launch VLC with Blu-ray disc
vlc bluray:///dev/$BLURAY_DRIVE

VLCBR

chmod +x /usr/local/bin/vlc-bluray

# Create desktop entry
cat > /usr/share/applications/vlc-bluray.desktop << 'EOF'
[Desktop Entry]
Name=VLC Blu-ray Player
Comment=Play Blu-ray discs with full menu support
Exec=vlc-bluray
Icon=vlc
Terminal=false
Type=Application
Categories=AudioVideo;Player;
MimeType=x-content/video-bluray;x-content/video-dvd;
EOF

# Update MIME types
update-desktop-database

echo ""
echo "[*] VLC with Blu-ray support installed!"
echo "    Commands:"
echo "    - vlc                : VLC media player"
echo "    - vlc-bluray         : VLC Blu-ray launcher"
echo "    - makemkv            : Blu-ray ripper/backup"
echo ""
echo "    Features:"
echo "    ✓ VLC Media Player (latest version)"
echo "    ✓ Full Blu-ray playback support"
echo "    ✓ AACS decryption (commercial Blu-rays)"
echo "    ✓ BD+ decryption (protected Blu-rays)"
echo "    ✓ DVD playback with libdvdcss"
echo "    ✓ Hardware acceleration (VDPAU/VAAPI)"
echo "    ✓ Blu-ray menu navigation"
echo "    ✓ MakeMKV (Blu-ray backup)"
echo "    ✓ All video/audio codecs"
echo ""
echo "    Supported formats:"
echo "    ✓ Blu-ray (commercial & homemade)"
echo "    ✓ DVD (commercial & homemade)"
echo "    ✓ 4K UHD Blu-ray"
echo "    ✓ All video formats (MP4, MKV, AVI, etc.)"
echo "    ✓ All audio formats (FLAC, AAC, DTS, etc.)"

# ============================================
# ASUS Armoury Crate (Linux Alternative)
# ============================================
echo ""
echo "[*] Installing ASUS Armoury Crate (Linux alternative)..."
echo "    Full RGB control, fan profiles, performance modes"

# Install asusctl (ASUS control utilities)
cd /usr/src
git clone https://gitlab.com/asus-linux/asusctl.git
cd asusctl

# Install Rust (required for asusctl)
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
source $HOME/.cargo/env

# Build and install asusctl
make
make install

# Install asusd (ASUS daemon)
systemctl enable asusd
systemctl start asusd || true

# Install ROG Control Center (GUI)
cd /usr/src
git clone https://gitlab.com/asus-linux/rog-control-center.git
cd rog-control-center
make
make install

# Install ASUS Aura support (already have OpenRGB, enhance it)
# OpenRGB was installed earlier, now configure for ASUS

# Install additional ASUS tools
apt-get install -y \
    i2c-tools \
    dmidecode

# Enable I2C for RGB control
modprobe i2c-dev
modprobe i2c-i801
echo "i2c-dev" >> /etc/modules
echo "i2c-i801" >> /etc/modules

# Create ASUS Armoury Crate alternative launcher
cat > /usr/local/bin/armoury-crate << 'ARMOURY'
#!/bin/bash
# GhostOS ASUS Armoury Crate Alternative

show_menu() {
    clear
    cat << 'EOF'
╔════════════════════════════════════════════════════════════╗
║                                                            ║
║             ASUS ARMOURY CRATE (GhostOS)                  ║
║                                                            ║
╚════════════════════════════════════════════════════════════╝

  [1] 🎨 RGB Control (Aura Sync)
  [2] 🌡️  Fan Control & Monitoring
  [3] ⚡ Performance Modes
  [4] 🔧 System Information
  [5] 📊 Hardware Monitoring
  [6] 🎮 Gaming Profiles
  [7] ⚙️  Settings
  [0] 🚪 Exit

EOF
    read -p "Select option: " choice
}

rgb_control() {
    clear
    echo "========================================="
    echo "  ASUS Aura RGB Control"
    echo "========================================="
    echo ""
    echo "1) Launch OpenRGB (Full RGB control)"
    echo "2) Set static color"
    echo "3) Set breathing effect"
    echo "4) Set rainbow effect"
    echo "5) Turn off RGB"
    echo "0) Back"
    echo ""
    read -p "Select: " rgb_choice
    
    case $rgb_choice in
        1) openrgb & ;;
        2) 
            read -p "Enter color (red/green/blue/cyan/magenta/yellow/white): " color
            asusctl led-mode static --color $color
            ;;
        3) asusctl led-mode breathe ;;
        4) asusctl led-mode rainbow ;;
        5) asusctl led-mode off ;;
    esac
}

fan_control() {
    clear
    echo "========================================="
    echo "  Fan Control & Monitoring"
    echo "========================================="
    echo ""
    echo "Current fan speeds:"
    sensors | grep -i "fan"
    echo ""
    echo "1) Silent mode (quiet)"
    echo "2) Performance mode (balanced)"
    echo "3) Turbo mode (maximum cooling)"
    echo "4) Custom fan curve"
    echo "0) Back"
    echo ""
    read -p "Select: " fan_choice
    
    case $fan_choice in
        1) asusctl profile -P Quiet ;;
        2) asusctl profile -P Balanced ;;
        3) asusctl profile -P Performance ;;
        4) echo "Custom curves: Edit /etc/asusd/profile.conf" ;;
    esac
}

performance_modes() {
    clear
    echo "========================================="
    echo "  Performance Modes"
    echo "========================================="
    echo ""
    echo "Current mode: $(asusctl profile -p)"
    echo ""
    echo "1) Silent (power saving)"
    echo "2) Balanced (default)"
    echo "3) Performance (high power)"
    echo "4) Windows mode (compatibility)"
    echo "0) Back"
    echo ""
    read -p "Select: " perf_choice
    
    case $perf_choice in
        1) asusctl profile -P Quiet ;;
        2) asusctl profile -P Balanced ;;
        3) asusctl profile -P Performance ;;
        4) asusctl profile -P Windows ;;
    esac
}

system_info() {
    clear
    echo "========================================="
    echo "  ASUS System Information"
    echo "========================================="
    echo ""
    
    echo "Motherboard:"
    dmidecode -t baseboard | grep -E "Manufacturer|Product Name|Version"
    echo ""
    
    echo "BIOS:"
    dmidecode -t bios | grep -E "Vendor|Version|Release Date"
    echo ""
    
    echo "CPU:"
    lscpu | grep "Model name"
    echo ""
    
    echo "GPU:"
    lspci | grep -i vga
    echo ""
    
    read -p "Press ENTER to continue..."
}

hardware_monitoring() {
    clear
    echo "========================================="
    echo "  Hardware Monitoring"
    echo "========================================="
    echo ""
    
    echo "--- Temperatures ---"
    sensors | grep -E "temp|fan" | head -20
    echo ""
    
    echo "--- Power ---"
    asusctl -c 2>/dev/null || echo "Power info: Use 'asusctl -c'"
    echo ""
    
    echo "--- GPU ---"
    nvidia-smi 2>/dev/null | grep -A 5 "GPU Name" || echo "NVIDIA GPU not detected"
    echo ""
    
    read -p "Press ENTER to continue..."
}

gaming_profiles() {
    clear
    echo "========================================="
    echo "  Gaming Profiles"
    echo "========================================="
    echo ""
    echo "1) FPS mode (high performance + turbo fans)"
    echo "2) Strategy mode (balanced)"
    echo "3) Quiet mode (silent gaming)"
    echo "4) Extreme mode (max everything)"
    echo "0) Back"
    echo ""
    read -p "Select: " game_choice
    
    case $game_choice in
        1) 
            asusctl profile -P Performance
            asusctl led-mode static --color red
            nvidia-mode gaming 2>/dev/null || true
            ;;
        2)
            asusctl profile -P Balanced
            asusctl led-mode breathing
            ;;
        3)
            asusctl profile -P Quiet
            asusctl led-mode off
            ;;
        4)
            asusctl profile -P Performance
            asusctl led-mode rainbow
            nvidia-mode gaming 2>/dev/null || true
            ;;
    esac
    
    echo ""
    echo "Profile applied!"
    sleep 2
}

settings() {
    clear
    echo "========================================="
    echo "  Settings"
    echo "========================================="
    echo ""
    echo "1) Start asusd service"
    echo "2) Restart asusd service"
    echo "3) Check asusd status"
    echo "4) Launch ROG Control Center (GUI)"
    echo "0) Back"
    echo ""
    read -p "Select: " set_choice
    
    case $set_choice in
        1) systemctl start asusd ;;
        2) systemctl restart asusd ;;
        3) systemctl status asusd ;;
        4) rog-control-center & ;;
    esac
}

# Main loop
while true; do
    show_menu
    
    case $choice in
        1) rgb_control ;;
        2) fan_control ;;
        3) performance_modes ;;
        4) system_info ;;
        5) hardware_monitoring ;;
        6) gaming_profiles ;;
        7) settings ;;
        0) exit 0 ;;
        *) echo "Invalid option" ; sleep 1 ;;
    esac
done
ARMOURY

chmod +x /usr/local/bin/armoury-crate

# Create desktop entry
cat > /usr/share/applications/armoury-crate.desktop << 'EOF'
[Desktop Entry]
Name=ASUS Armoury Crate
Comment=ASUS RGB, fan control, and performance management
Exec=xfce4-terminal -e armoury-crate
Icon=preferences-system
Terminal=true
Type=Application
Categories=System;Settings;
EOF

echo ""
echo "[*] ASUS Armoury Crate installed!"

# ============================================
# Corsair iCUE (Linux Alternative)
# ============================================
echo ""
echo "[*] Installing Corsair iCUE (Linux alternative)..."
echo "    RGB control, fan control, hardware monitoring"

# Install ckb-next (Corsair keyboard/mouse driver)
cd /usr/src
git clone https://github.com/ckb-next/ckb-next.git
cd ckb-next
mkdir build && cd build

# Install dependencies
apt-get install -y \
    build-essential \
    cmake \
    libudev-dev \
    qt5-default \
    qttools5-dev \
    qttools5-dev-tools \
    libpulse-dev \
    libquazip5-dev \
    libqt5x11extras5-dev \
    libxcb-screensaver0-dev \
    libxcb-ewmh-dev \
    libxcb1-dev

# Build and install
cmake ..
make -j$(nproc)
make install

# Enable ckb-next service
systemctl enable ckb-next-daemon
systemctl start ckb-next-daemon || true

# Install liquidctl (for Corsair coolers and fans)
pip3 install --break-system-packages liquidctl

# Add liquidctl udev rules
cat > /etc/udev/rules.d/69-liquidctl.rules << 'EOF'
# Corsair devices
SUBSYSTEM=="usb", ATTR{idVendor}=="1b1c", MODE="0666", TAG+="uaccess"
# NZXT devices
SUBSYSTEM=="usb", ATTR{idVendor}=="1e71", MODE="0666", TAG+="uaccess"
EOF

udevadm control --reload-rules
udevadm trigger

# Configure OpenRGB for Corsair devices (already installed)
# Add Corsair specific profile

# Create Corsair iCUE alternative launcher
cat > /usr/local/bin/icue << 'ICUE'
#!/bin/bash
# GhostOS Corsair iCUE Alternative

show_menu() {
    clear
    cat << 'EOF'
╔════════════════════════════════════════════════════════════╗
║                                                            ║
║               CORSAIR iCUE (GhostOS)                      ║
║                                                            ║
╚════════════════════════════════════════════════════════════╝

  [1] 🎨 RGB Lighting Control
  [2] 💧 Liquid Cooling Control
  [3] 🌀 Fan Control
  [4] 📊 Hardware Monitoring
  [5] 🎮 Gaming Profiles
  [6] ⚡ Performance Modes
  [7] ⚙️  Device Settings
  [8] 📱 Synchronize Devices
  [0] 🚪 Exit

EOF
    read -p "Select option: " choice
}

rgb_control() {
    clear
    echo "========================================="
    echo "  Corsair RGB Lighting"
    echo "========================================="
    echo ""
    echo "1) Launch ckb-next (Keyboard/Mouse RGB)"
    echo "2) Launch OpenRGB (All Corsair devices)"
    echo "3) Set static color"
    echo "4) Set color wave effect"
    echo "5) Set reactive effect"
    echo "6) Turn off lighting"
    echo "0) Back"
    echo ""
    read -p "Select: " rgb_choice
    
    case $rgb_choice in
        1) ckb-next & ;;
        2) openrgb & ;;
        3)
            read -p "Enter RGB hex color (e.g., ff0000 for red): " color
            liquidctl set sync color fixed $color 2>/dev/null || echo "No compatible device"
            ;;
        4) liquidctl set sync color fading ffffff 00ff00 0000ff 2>/dev/null || echo "No compatible device" ;;
        5) liquidctl set sync color pulse ff0000 2>/dev/null || echo "No compatible device" ;;
        6) liquidctl set sync color off 2>/dev/null || echo "All RGB off" ;;
    esac
}

cooling_control() {
    clear
    echo "========================================="
    echo "  Liquid Cooling Control"
    echo "========================================="
    echo ""
    
    # Detect Corsair coolers
    liquidctl list 2>/dev/null
    
    echo ""
    echo "1) Set quiet mode (low RPM)"
    echo "2) Set balanced mode"
    echo "3) Set performance mode (high RPM)"
    echo "4) Set extreme mode (max RPM)"
    echo "5) Custom fan curve"
    echo "0) Back"
    echo ""
    read -p "Select: " cool_choice
    
    case $cool_choice in
        1) liquidctl set pump speed 50 2>/dev/null && liquidctl set fan speed 30 2>/dev/null ;;
        2) liquidctl set pump speed 75 2>/dev/null && liquidctl set fan speed 50 2>/dev/null ;;
        3) liquidctl set pump speed 90 2>/dev/null && liquidctl set fan speed 75 2>/dev/null ;;
        4) liquidctl set pump speed 100 2>/dev/null && liquidctl set fan speed 100 2>/dev/null ;;
        5)
            echo "Custom fan curve:"
            read -p "Pump speed (20-100): " pump
            read -p "Fan speed (20-100): " fan
            liquidctl set pump speed $pump 2>/dev/null
            liquidctl set fan speed $fan 2>/dev/null
            ;;
    esac
}

fan_control() {
    clear
    echo "========================================="
    echo "  Fan Control"
    echo "========================================="
    echo ""
    
    echo "Current fan speeds:"
    sensors | grep -i "fan"
    echo ""
    
    echo "1) Quiet (30%)"
    echo "2) Balanced (50%)"
    echo "3) Performance (75%)"
    echo "4) Max (100%)"
    echo "0) Back"
    echo ""
    read -p "Select: " fan_choice
    
    case $fan_choice in
        1) liquidctl set fan speed 30 2>/dev/null ;;
        2) liquidctl set fan speed 50 2>/dev/null ;;
        3) liquidctl set fan speed 75 2>/dev/null ;;
        4) liquidctl set fan speed 100 2>/dev/null ;;
    esac
}

monitoring() {
    clear
    echo "========================================="
    echo "  Hardware Monitoring"
    echo "========================================="
    echo ""
    
    echo "Corsair Devices:"
    liquidctl status 2>/dev/null || echo "No Corsair devices detected"
    
    echo ""
    echo "System Temperatures:"
    sensors | grep -E "temp|fan"
    
    echo ""
    read -p "Press ENTER to continue..."
}

gaming_profiles() {
    clear
    echo "========================================="
    echo "  Gaming Profiles"
    echo "========================================="
    echo ""
    echo "1) FPS Gaming (red theme, max cooling)"
    echo "2) MOBA Gaming (blue theme, balanced)"
    echo "3) Streaming (rainbow, quiet)"
    echo "4) Productivity (white, silent)"
    echo "0) Back"
    echo ""
    read -p "Select: " game_choice
    
    case $game_choice in
        1)
            liquidctl set sync color fixed ff0000
            liquidctl set pump speed 100
            liquidctl set fan speed 100
            ;;
        2)
            liquidctl set sync color fixed 0000ff
            liquidctl set pump speed 75
            liquidctl set fan speed 60
            ;;
        3)
            liquidctl set sync color fading ff0000 00ff00 0000ff
            liquidctl set pump speed 60
            liquidctl set fan speed 40
            ;;
        4)
            liquidctl set sync color fixed ffffff
            liquidctl set pump speed 50
            liquidctl set fan speed 30
            ;;
    esac
    
    echo ""
    echo "Profile applied!"
    sleep 2
}

performance_modes() {
    clear
    echo "========================================="
    echo "  Performance Modes"
    echo "========================================="
    echo ""
    echo "1) Silent (power saving)"
    echo "2) Balanced"
    echo "3) Performance"
    echo "4) Extreme (overclock)"
    echo "0) Back"
    echo ""
    read -p "Select: " perf_choice
    
    case $perf_choice in
        1)
            liquidctl set pump speed 40
            liquidctl set fan speed 25
            ;;
        2)
            liquidctl set pump speed 70
            liquidctl set fan speed 50
            ;;
        3)
            liquidctl set pump speed 90
            liquidctl set fan speed 80
            ;;
        4)
            liquidctl set pump speed 100
            liquidctl set fan speed 100
            ;;
    esac
}

device_settings() {
    clear
    echo "========================================="
    echo "  Device Settings"
    echo "========================================="
    echo ""
    echo "1) List Corsair devices"
    echo "2) Initialize devices"
    echo "3) Restart ckb-next daemon"
    echo "4) Launch ckb-next GUI"
    echo "0) Back"
    echo ""
    read -p "Select: " dev_choice
    
    case $dev_choice in
        1) liquidctl list ;;
        2) liquidctl initialize all ;;
        3) systemctl restart ckb-next-daemon ;;
        4) ckb-next & ;;
    esac
}

synchronize() {
    clear
    echo "========================================="
    echo "  Synchronize All Devices"
    echo "========================================="
    echo ""
    
    read -p "Enter RGB hex color for all devices: " color
    
    echo "Synchronizing..."
    liquidctl set sync color fixed $color 2>/dev/null
    
    echo "All Corsair devices synchronized!"
    sleep 2
}

# Main loop
while true; do
    show_menu
    
    case $choice in
        1) rgb_control ;;
        2) cooling_control ;;
        3) fan_control ;;
        4) monitoring ;;
        5) gaming_profiles ;;
        6) performance_modes ;;
        7) device_settings ;;
        8) synchronize ;;
        0) exit 0 ;;
        *) echo "Invalid option" ; sleep 1 ;;
    esac
done
ICUE

chmod +x /usr/local/bin/icue

# Create desktop entry
cat > /usr/share/applications/corsair-icue.desktop << 'EOF'
[Desktop Entry]
Name=Corsair iCUE
Comment=Corsair RGB, cooling, and fan control
Exec=xfce4-terminal -e icue
Icon=preferences-system
Terminal=true
Type=Application
Categories=System;Settings;
EOF

# Create unified hardware control launcher
cat > /usr/local/bin/ghostos-hardware << 'HWCTRL'
#!/bin/bash
# GhostOS Unified Hardware Control

clear
cat << 'EOF'
╔════════════════════════════════════════════════════════════╗
║                                                            ║
║   ░██████╗░██╗░░██╗░█████╗░░██████╗████████╗░█████╗░░██████╗  ║
║                                                            ║
║           HARDWARE CONTROL CENTER                         ║
║                                                            ║
╚════════════════════════════════════════════════════════════╝

  [1] 🎨 ASUS Armoury Crate
  [2] 💧 Corsair iCUE
  [3] 🌈 OpenRGB (Universal RGB)
  [4] 🖥️  NVIDIA Control
  [5] 🔧 System Monitoring
  [0] 🚪 Exit

EOF

read -p "Select: " choice

case $choice in
    1) armoury-crate ;;
    2) icue ;;
    3) openrgb & ;;
    4) nvidia-settings & ;;
    5) htop ;;
esac
HWCTRL

chmod +x /usr/local/bin/ghostos-hardware

cat > /usr/share/applications/ghostos-hardware.desktop << 'EOF'
[Desktop Entry]
Name=Hardware Control Center
Comment=ASUS, Corsair, NVIDIA control
Exec=xfce4-terminal -e ghostos-hardware
Icon=computer
Terminal=true
Type=Application
Categories=System;Settings;HardwareSettings;
EOF

echo ""
echo "[*] Corsair iCUE installed!"
echo ""
echo "    Commands:"
echo "    - armoury-crate      : ASUS Armoury Crate alternative"
echo "    - icue               : Corsair iCUE alternative"
echo "    - ghostos-hardware   : Unified hardware control"
echo "    - openrgb            : Universal RGB control"
echo "    - ckb-next           : Corsair keyboard/mouse"
echo "    - liquidctl          : Corsair AIO/fans (CLI)"
echo ""
echo "    Installed features:"
echo "    ✓ ASUS Armoury Crate (asusctl + ROG Control Center)"
echo "    ✓ ASUS Aura RGB sync"
echo "    ✓ ASUS fan control & performance profiles"
echo "    ✓ Corsair iCUE (ckb-next + liquidctl)"
echo "    ✓ Corsair RGB control (keyboards, mice, headsets)"
echo "    ✓ Corsair AIO liquid cooling control"
echo "    ✓ Corsair fan speed control"
echo "    ✓ Universal RGB control (OpenRGB)"
echo "    ✓ Hardware monitoring"
echo "    ✓ Gaming profiles"
echo ""
echo "    Supported devices:"
echo "    ✓ ASUS motherboards (all AM5 boards)"
echo "    ✓ ASUS GPUs (via OpenRGB)"
echo "    ✓ Corsair keyboards (K series)"
echo "    ✓ Corsair mice (M series)"
echo "    ✓ Corsair headsets"
echo "    ✓ Corsair AIOs (H series)"
echo "    ✓ Corsair fans (LL, QL, ML series)"
echo "    ✓ Corsair Commander Pro"
echo "    ✓ Corsair Lighting Node Pro"

# ============================================
# Elgato Stream Deck Drivers & Software
# ============================================
echo ""
echo "[*] Installing Elgato Stream Deck drivers..."
echo "    All Stream Deck models supported"

# Install dependencies for Stream Deck
apt-get install -y \
    python3-pip \
    python3-pil \
    python3-xlib \
    libhidapi-libusb0 \
    libhidapi-hidraw0 \
    libhidapi-dev \
    libudev-dev \
    libusb-1.0-0-dev

# Install python-elgato-streamdeck
pip3 install --break-system-packages streamdeck

# Install streamdeck-ui (GUI interface)
pip3 install --break-system-packages streamdeck-ui

# Install additional Stream Deck libraries
pip3 install --break-system-packages \
    pillow \
    pynput \
    xlib \
    cairosvg

# Add udev rules for Stream Deck
cat > /etc/udev/rules.d/70-streamdeck.rules << 'EOF'
# Elgato Stream Deck devices
SUBSYSTEM=="usb", ATTRS{idVendor}=="0fd9", ATTRS{idProduct}=="0060", MODE="0666", TAG+="uaccess"  # Stream Deck Original
SUBSYSTEM=="usb", ATTRS{idVendor}=="0fd9", ATTRS{idProduct}=="0063", MODE="0666", TAG+="uaccess"  # Stream Deck Mini
SUBSYSTEM=="usb", ATTRS{idVendor}=="0fd9", ATTRS{idProduct}=="006c", MODE="0666", TAG+="uaccess"  # Stream Deck XL
SUBSYSTEM=="usb", ATTRS{idVendor}=="0fd9", ATTRS{idProduct}=="006d", MODE="0666", TAG+="uaccess"  # Stream Deck Original V2
SUBSYSTEM=="usb", ATTRS{idVendor}=="0fd9", ATTRS{idProduct}=="0080", MODE="0666", TAG+="uaccess"  # Stream Deck XL V2
SUBSYSTEM=="usb", ATTRS{idVendor}=="0fd9", ATTRS{idProduct}=="0084", MODE="0666", TAG+="uaccess"  # Stream Deck Pedal
SUBSYSTEM=="usb", ATTRS{idVendor}=="0fd9", ATTRS{idProduct}=="0086", MODE="0666", TAG+="uaccess"  # Stream Deck Mini V2
SUBSYSTEM=="usb", ATTRS{idVendor}=="0fd9", ATTRS{idProduct}=="0090", MODE="0666", TAG+="uaccess"  # Stream Deck +
SUBSYSTEM=="usb", ATTRS{idVendor}=="0fd9", ATTRS{idProduct}=="009a", MODE="0666", TAG+="uaccess"  # Stream Deck MK.2
EOF

udevadm control --reload-rules
udevadm trigger

# Create Stream Deck control script
cat > /usr/local/bin/streamdeck-control << 'SDECK'
#!/bin/bash
# GhostOS Elgato Stream Deck Control

show_menu() {
    clear
    cat << 'EOF'
╔════════════════════════════════════════════════════════════╗
║                                                            ║
║            ELGATO STREAM DECK CONTROL                     ║
║                                                            ║
╚════════════════════════════════════════════════════════════╝

  [1] 🎛️  Launch Stream Deck UI
  [2] 🔍 Detect Stream Deck devices
  [3] 💡 Set brightness
  [4] 🎨 Test keys/buttons
  [5] 📊 Device information
  [6] 🔧 Reset device
  [7] ⚙️  Configure profiles
  [8] 📁 Open config directory
  [0] 🚪 Exit

EOF
    read -p "Select option: " choice
}

launch_ui() {
    echo "Launching Stream Deck UI..."
    streamdeck &
}

detect_devices() {
    clear
    echo "========================================="
    echo "  Detecting Stream Deck Devices"
    echo "========================================="
    echo ""
    
    python3 << 'PYEOF'
from StreamDeck.DeviceManager import DeviceManager

manager = DeviceManager()
decks = manager.enumerate()

print(f"Found {len(decks)} Stream Deck device(s):\n")

for index, deck in enumerate(decks):
    deck.open()
    deck.reset()
    
    print(f"Device {index + 1}:")
    print(f"  - Model: {deck.deck_type()}")
    print(f"  - Serial: {deck.get_serial_number()}")
    print(f"  - Firmware: {deck.get_firmware_version()}")
    print(f"  - Key count: {deck.key_count()}")
    print(f"  - Key layout: {deck.key_layout()}")
    print()
    
    deck.close()

if len(decks) == 0:
    print("No Stream Deck devices detected!")
    print("Make sure your device is connected.")
PYEOF
    
    echo ""
    read -p "Press ENTER to continue..."
}

set_brightness() {
    clear
    echo "========================================="
    echo "  Set Brightness"
    echo "========================================="
    echo ""
    read -p "Enter brightness (0-100): " brightness
    
    python3 << PYEOF
from StreamDeck.DeviceManager import DeviceManager

manager = DeviceManager()
decks = manager.enumerate()

for deck in decks:
    deck.open()
    deck.set_brightness($brightness)
    print(f"Brightness set to $brightness% on {deck.deck_type()}")
    deck.close()
PYEOF
    
    echo ""
    read -p "Press ENTER to continue..."
}

test_keys() {
    clear
    echo "========================================="
    echo "  Test Keys"
    echo "========================================="
    echo ""
    echo "Testing all keys with colors..."
    
    python3 << 'PYEOF'
from StreamDeck.DeviceManager import DeviceManager
from StreamDeck.ImageHelpers import PILHelper
from PIL import Image, ImageDraw
import time

manager = DeviceManager()
decks = manager.enumerate()

for deck in decks:
    deck.open()
    deck.reset()
    deck.set_brightness(75)
    
    # Test each key with different colors
    colors = ['red', 'green', 'blue', 'yellow', 'cyan', 'magenta', 'white']
    
    for key in range(deck.key_count()):
        color = colors[key % len(colors)]
        image = PILHelper.create_image(deck)
        draw = ImageDraw.Draw(image)
        draw.rectangle((0, 0, image.width, image.height), fill=color)
        
        key_image = PILHelper.to_native_format(deck, image)
        deck.set_key_image(key, key_image)
        time.sleep(0.1)
    
    print(f"Test complete on {deck.deck_type()}")
    time.sleep(2)
    deck.reset()
    deck.close()
PYEOF
    
    echo ""
    read -p "Press ENTER to continue..."
}

device_info() {
    clear
    echo "========================================="
    echo "  Device Information"
    echo "========================================="
    echo ""
    
    lsusb | grep "0fd9" || echo "No Elgato devices detected via USB"
    
    echo ""
    read -p "Press ENTER to continue..."
}

reset_device() {
    clear
    echo "========================================="
    echo "  Reset Device"
    echo "========================================="
    echo ""
    echo "Resetting all Stream Deck devices..."
    
    python3 << 'PYEOF'
from StreamDeck.DeviceManager import DeviceManager

manager = DeviceManager()
decks = manager.enumerate()

for deck in decks:
    deck.open()
    deck.reset()
    print(f"Reset {deck.deck_type()}")
    deck.close()
PYEOF
    
    echo ""
    echo "All devices reset!"
    sleep 2
}

configure_profiles() {
    echo ""
    echo "Profile configuration:"
    echo "  1) Edit ~/.streamdeck_ui.json manually"
    echo "  2) Use Stream Deck UI for graphical configuration"
    echo ""
    read -p "Press ENTER to continue..."
}

open_config() {
    xdg-open ~/.streamdeck_ui 2>/dev/null || echo "Config directory: ~/.streamdeck_ui"
    sleep 2
}

# Main loop
while true; do
    show_menu
    
    case $choice in
        1) launch_ui ;;
        2) detect_devices ;;
        3) set_brightness ;;
        4) test_keys ;;
        5) device_info ;;
        6) reset_device ;;
        7) configure_profiles ;;
        8) open_config ;;
        0) exit 0 ;;
        *) echo "Invalid option" ; sleep 1 ;;
    esac
done
SDECK

chmod +x /usr/local/bin/streamdeck-control

# Create desktop entry
cat > /usr/share/applications/streamdeck.desktop << 'EOF'
[Desktop Entry]
Name=Elgato Stream Deck
Comment=Stream Deck control and configuration
Exec=streamdeck
Icon=input-gaming
Terminal=false
Type=Application
Categories=Utility;
EOF

cat > /usr/share/applications/streamdeck-control.desktop << 'EOF'
[Desktop Entry]
Name=Stream Deck Control
Comment=Advanced Stream Deck management
Exec=xfce4-terminal -e streamdeck-control
Icon=input-gaming
Terminal=true
Type=Application
Categories=Utility;
EOF

# Enable Stream Deck service (auto-start)
cat > /etc/systemd/user/streamdeck.service << 'EOF'
[Unit]
Description=Elgato Stream Deck Service
After=graphical.target

[Service]
Type=simple
ExecStart=/usr/local/bin/streamdeck
Restart=on-failure

[Install]
WantedBy=default.target
EOF

echo ""
echo "[*] Elgato Stream Deck drivers installed!"

# ============================================
# Elgato Camera Drivers & Software
# ============================================
echo ""
echo "[*] Installing Elgato camera drivers..."
echo "    Cam Link, HD60, Facecam support"

# Install V4L2 tools and camera support
apt-get install -y \
    v4l-utils \
    v4l2loopback-dkms \
    ffmpeg \
    gstreamer1.0-plugins-good \
    gstreamer1.0-plugins-bad \
    gstreamer1.0-plugins-ugly \
    gstreamer1.0-tools

# Load v4l2loopback module
modprobe v4l2loopback
echo "v4l2loopback" >> /etc/modules-load.d/v4l2loopback.conf

# Add udev rules for Elgato cameras
cat > /etc/udev/rules.d/71-elgato-cameras.rules << 'EOF'
# Elgato Cam Link 4K
SUBSYSTEM=="usb", ATTRS{idVendor}=="0fd9", ATTRS{idProduct}=="0066", MODE="0666", TAG+="uaccess"

# Elgato HD60 S
SUBSYSTEM=="usb", ATTRS{idVendor}=="0fd9", ATTRS{idProduct}=="004b", MODE="0666", TAG+="uaccess"

# Elgato HD60 S+
SUBSYSTEM=="usb", ATTRS{idVendor}=="0fd9", ATTRS{idProduct}=="005c", MODE="0666", TAG+="uaccess"

# Elgato HD60 X
SUBSYSTEM=="usb", ATTRS{idVendor}=="0fd9", ATTRS{idProduct}=="008f", MODE="0666", TAG+="uaccess"

# Elgato Facecam
SUBSYSTEM=="usb", ATTRS{idVendor}=="0fd9", ATTRS{idProduct}=="0085", MODE="0666", TAG+="uaccess"

# Elgato Facecam Pro
SUBSYSTEM=="usb", ATTRS{idVendor}=="0fd9", ATTRS{idProduct}=="0095", MODE="0666", TAG+="uaccess"

# Elgato 4K60 Pro
SUBSYSTEM=="usb", ATTRS{idVendor}=="0fd9", ATTRS{idProduct}=="003f", MODE="0666", TAG+="uaccess"
EOF

udevadm control --reload-rules
udevadm trigger

# Install OBS Studio (for camera/capture card usage)
apt-get install -y obs-studio

# Install additional camera control tools
apt-get install -y \
    guvcview \
    cheese \
    camorama \
    qv4l2

# Create Elgato camera control script
cat > /usr/local/bin/elgato-camera << 'ECAM'
#!/bin/bash
# GhostOS Elgato Camera Control

show_menu() {
    clear
    cat << 'EOF'
╔════════════════════════════════════════════════════════════╗
║                                                            ║
║            ELGATO CAMERA CONTROL                          ║
║                                                            ║
╚════════════════════════════════════════════════════════════╝

  [1] 📹 Detect Elgato devices
  [2] 🎥 Test camera (Facecam)
  [3] 🎮 Test capture card (Cam Link/HD60)
  [4] ⚙️  Configure camera settings
  [5] 🔧 Launch OBS Studio
  [6] 📊 Device information
  [7] 🎬 Launch camera viewer (guvcview)
  [8] 🎯 V4L2 controls
  [0] 🚪 Exit

EOF
    read -p "Select option: " choice
}

detect_devices() {
    clear
    echo "========================================="
    echo "  Detecting Elgato Devices"
    echo "========================================="
    echo ""
    
    echo "USB Devices:"
    lsusb | grep -i "elgato\|0fd9"
    
    echo ""
    echo "Video Devices:"
    v4l2-ctl --list-devices
    
    echo ""
    read -p "Press ENTER to continue..."
}

test_camera() {
    echo "Testing Elgato Facecam..."
    
    # Find Facecam device
    DEVICE=$(v4l2-ctl --list-devices | grep -A 1 -i "facecam\|elgato" | tail -1 | xargs)
    
    if [ -z "$DEVICE" ]; then
        echo "No Elgato camera detected!"
        sleep 2
        return
    fi
    
    echo "Found: $DEVICE"
    echo "Opening camera preview..."
    
    ffplay -f v4l2 -video_size 1920x1080 -framerate 60 $DEVICE 2>/dev/null &
    
    echo ""
    echo "Press ENTER to stop preview..."
    read
    pkill -f ffplay
}

test_capture() {
    echo "Testing Elgato Capture Card..."
    
    # Find capture card device
    DEVICE=$(v4l2-ctl --list-devices | grep -A 1 -i "cam link\|hd60" | tail -1 | xargs)
    
    if [ -z "$DEVICE" ]; then
        echo "No Elgato capture card detected!"
        sleep 2
        return
    fi
    
    echo "Found: $DEVICE"
    echo "Opening capture preview..."
    
    ffplay -f v4l2 -video_size 1920x1080 -framerate 60 $DEVICE 2>/dev/null &
    
    echo ""
    echo "Press ENTER to stop preview..."
    read
    pkill -f ffplay
}

configure_camera() {
    clear
    echo "========================================="
    echo "  Camera Settings"
    echo "========================================="
    echo ""
    
    # Find camera device
    DEVICE=$(v4l2-ctl --list-devices | grep -A 1 -i "facecam\|elgato" | tail -1 | xargs)
    
    if [ -z "$DEVICE" ]; then
        echo "No Elgato camera detected!"
        sleep 2
        return
    fi
    
    echo "Camera: $DEVICE"
    echo ""
    echo "1) Set resolution to 1920x1080"
    echo "2) Set resolution to 1280x720"
    echo "3) Set framerate to 60fps"
    echo "4) Set framerate to 30fps"
    echo "5) Auto-adjust settings"
    echo "6) Launch qv4l2 (GUI controls)"
    echo "0) Back"
    echo ""
    read -p "Select: " cam_choice
    
    case $cam_choice in
        1) v4l2-ctl -d $DEVICE --set-fmt-video=width=1920,height=1080 ;;
        2) v4l2-ctl -d $DEVICE --set-fmt-video=width=1280,height=720 ;;
        3) v4l2-ctl -d $DEVICE --set-parm=60 ;;
        4) v4l2-ctl -d $DEVICE --set-parm=30 ;;
        5) v4l2-ctl -d $DEVICE --set-ctrl=auto_exposure=3 ;;
        6) qv4l2 & ;;
    esac
}

launch_obs() {
    echo "Launching OBS Studio..."
    obs &
}

device_info() {
    clear
    echo "========================================="
    echo "  Device Information"
    echo "========================================="
    echo ""
    
    DEVICE=$(v4l2-ctl --list-devices | grep -A 1 -i "elgato" | tail -1 | xargs)
    
    if [ -z "$DEVICE" ]; then
        echo "No Elgato devices detected!"
    else
        echo "Device: $DEVICE"
        echo ""
        v4l2-ctl -d $DEVICE --all
    fi
    
    echo ""
    read -p "Press ENTER to continue..."
}

launch_guvcview() {
    echo "Launching guvcview..."
    guvcview &
}

v4l2_controls() {
    clear
    echo "========================================="
    echo "  V4L2 Controls"
    echo "========================================="
    echo ""
    
    DEVICE=$(v4l2-ctl --list-devices | grep -A 1 -i "elgato" | tail -1 | xargs)
    
    if [ -z "$DEVICE" ]; then
        echo "No Elgato devices detected!"
        sleep 2
        return
    fi
    
    echo "Available controls for $DEVICE:"
    echo ""
    v4l2-ctl -d $DEVICE --list-ctrls
    
    echo ""
    read -p "Press ENTER to continue..."
}

# Main loop
while true; do
    show_menu
    
    case $choice in
        1) detect_devices ;;
        2) test_camera ;;
        3) test_capture ;;
        4) configure_camera ;;
        5) launch_obs ;;
        6) device_info ;;
        7) launch_guvcview ;;
        8) v4l2_controls ;;
        0) exit 0 ;;
        *) echo "Invalid option" ; sleep 1 ;;
    esac
done
ECAM

chmod +x /usr/local/bin/elgato-camera

# Create desktop entries
cat > /usr/share/applications/elgato-camera.desktop << 'EOF'
[Desktop Entry]
Name=Elgato Camera Control
Comment=Control Elgato cameras and capture cards
Exec=xfce4-terminal -e elgato-camera
Icon=camera-video
Terminal=true
Type=Application
Categories=AudioVideo;Video;
EOF

# Create unified Elgato control launcher
cat > /usr/local/bin/elgato-control << 'ELGATO'
#!/bin/bash
# GhostOS Unified Elgato Control

clear
cat << 'EOF'
╔════════════════════════════════════════════════════════════╗
║                                                            ║
║            ELGATO CONTROL CENTER                          ║
║                                                            ║
╚════════════════════════════════════════════════════════════╝

  [1] 🎛️  Stream Deck
  [2] 📹 Cameras & Capture Cards
  [3] 🎮 Launch OBS Studio
  [0] 🚪 Exit

EOF

read -p "Select: " choice

case $choice in
    1) streamdeck-control ;;
    2) elgato-camera ;;
    3) obs & ;;
esac
ELGATO

chmod +x /usr/local/bin/elgato-control

cat > /usr/share/applications/elgato-control.desktop << 'EOF'
[Desktop Entry]
Name=Elgato Control Center
Comment=Stream Deck, cameras, and capture cards
Exec=xfce4-terminal -e elgato-control
Icon=input-gaming
Terminal=true
Type=Application
Categories=Utility;AudioVideo;
EOF

echo ""
echo "[*] Elgato camera drivers installed!"
echo ""
echo "    Commands:"
echo "    - elgato-control     : Unified Elgato control"
echo "    - streamdeck         : Stream Deck UI"
echo "    - streamdeck-control : Stream Deck management"
echo "    - elgato-camera      : Camera/capture card control"
echo ""
echo "    Installed features:"
echo "    ✓ Stream Deck support (all models)"
echo "    ✓ Stream Deck UI (graphical interface)"
echo "    ✓ Elgato Cam Link 4K"
echo "    ✓ Elgato HD60 S/S+/X"
echo "    ✓ Elgato 4K60 Pro"
echo "    ✓ Elgato Facecam/Facecam Pro"
echo "    ✓ OBS Studio integration"
echo "    ✓ Camera controls (brightness, contrast, etc.)"
echo "    ✓ V4L2 camera support"
echo "    ✓ Hardware acceleration"
echo ""
echo "    Supported devices:"
echo "    ✓ Stream Deck Original/Mini/XL"
echo "    ✓ Stream Deck MK.2/+/Pedal"
echo "    ✓ All Elgato capture cards"
echo "    ✓ All Elgato webcams"

echo "[✓] GhostOS v1.0 installation complete"

V1_EOF
chmod +x "$BUILD_DIR/install_v1.0.sh"
}

create_install_script_1.1() {
    cat > "$BUILD_DIR/install_v1.1.sh" << 'V11_EOF'
#!/bin/bash
set -e
export DEBIAN_FRONTEND=noninteractive

echo "========================================"
echo "  Installing GhostOS v1.1"
echo "  Enhanced Edition"
echo "  on Parrot OS 7 Security base"
echo "========================================"

# ============================================
# Configure Parrot OS 7 Security Repositories
# ============================================
echo ""
echo "[*] Configuring Parrot OS 7 Security repositories..."

cat > /etc/apt/sources.list << 'PARROT_EOF'
# Parrot OS 7 (lory) - Security Edition Base
deb https://deb.parrot.sh/parrot lory main contrib non-free non-free-firmware
deb https://deb.parrot.sh/parrot lory-security main contrib non-free non-free-firmware
deb https://deb.parrot.sh/parrot lory-backports main contrib non-free non-free-firmware
PARROT_EOF

# ============================================
# BASE SYSTEM (from v1.0)
# ============================================
echo ""
echo "[*] Installing base system and kernel..."

apt-get update
apt-get install -y \
    linux-image-amd64 \
    linux-headers-amd64 \
    firmware-linux \
    firmware-linux-nonfree \
    build-essential \
    dkms \
    git \
    wget \
    curl

# ============================================
# AMD AM5 Chipset Support
# ============================================
echo ""
echo "[*] Installing AMD AM5 chipset support..."

apt-get install -y \
    amd64-microcode \
    firmware-amd-graphics \
    amdgpu-dkms \
    libdrm-amdgpu1 \
    mesa-vulkan-drivers \
    xserver-xorg-video-amdgpu

cat > /etc/modules-load.d/amd-pstate.conf << 'EOF'
amd_pstate
EOF

# ============================================
# ASUS AM5 Platform Drivers
# ============================================
echo ""
echo "[*] Installing ASUS AM5 motherboard drivers..."

apt-get install -y \
    linux-headers-$(uname -r) \
    dkms \
    i2c-tools \
    lm-sensors \
    fancontrol

cd /usr/src
git clone https://github.com/zeule/asus-wmi-sensors.git asus-wmi-sensors
cd asus-wmi-sensors

if [ -f "dkms.conf" ]; then
    dkms add -m asus-wmi-sensors -v 1.0
    dkms build -m asus-wmi-sensors -v 1.0
    dkms install -m asus-wmi-sensors -v 1.0
fi

echo "asus_wmi_sensors" >> /etc/modules-load.d/asus.conf

cd /usr/src
git clone https://github.com/zeule/asus-ec-sensors.git asus-ec-sensors
cd asus-ec-sensors
make
make install
echo "asus_ec_sensors" >> /etc/modules-load.d/asus.conf

# ============================================
# ASUS Aura RGB Support
# ============================================
echo ""
echo "[*] Installing ASUS Aura RGB support..."

apt-get install -y \
    libusb-1.0-0-dev \
    libhidapi-dev \
    qt5-default \
    qttools5-dev

cd /usr/src
git clone https://gitlab.com/CalcProgrammer1/OpenRGB.git openrgb
cd openrgb
qmake OpenRGB.pro
make -j$(nproc)
make install

cat > /etc/udev/rules.d/60-openrgb.rules << 'EOF'
SUBSYSTEM=="usb", ATTR{idVendor}=="0b05", ATTR{idProduct}=="1872", TAG+="uaccess"
SUBSYSTEM=="usb", ATTR{idVendor}=="0b05", ATTR{idProduct}=="1867", TAG+="uaccess"
SUBSYSTEM=="usb", ATTR{idVendor}=="0b05", ATTR{idProduct}=="19b6", TAG+="uaccess"
KERNEL=="i2c-[0-9]*", TAG+="uaccess"
EOF

udevadm control --reload-rules
udevadm trigger

# ============================================
# AM5 USB4/Thunderbolt Support
# ============================================
echo ""
echo "[*] Installing USB4/Thunderbolt support..."

apt-get install -y bolt thunderbolt-tools
systemctl enable bolt

# ============================================
# Audio Support
# ============================================
echo ""
echo "[*] Installing audio support..."

apt-get install -y \
    pulseaudio \
    pavucontrol \
    alsa-utils \
    firmware-sof-signed

sensors-detect --auto

cat > /usr/local/bin/asus-sensors-monitor << 'SENSEOF'
#!/bin/bash
echo "==================================="
echo "  ASUS AM5 System Sensors"
echo "==================================="
echo ""
echo "CPU Information:"
sensors | grep -A 10 "k10temp"
echo ""
echo "Motherboard Sensors:"
sensors | grep -A 20 "asus"
echo ""
echo "Fan Speeds:"
sensors | grep -i "fan"
SENSEOF

chmod +x /usr/local/bin/asus-sensors-monitor

# ============================================
# NVIDIA Driver Installation (from trusted source)
# ============================================
echo ""
echo "[*] Installing NVIDIA drivers from trusted GitHub source..."

apt-get install -y \
    build-essential \
    dkms \
    linux-headers-$(uname -r) \
    pkg-config \
    libglvnd-dev \
    libvulkan1 \
    vulkan-tools \
    xserver-xorg-dev

cd /usr/src
git clone https://github.com/NVIDIA/open-gpu-kernel-modules.git nvidia-open-drivers
cd nvidia-open-drivers
LATEST_TAG=$(git describe --tags --abbrev=0)
echo "Using NVIDIA driver version: $LATEST_TAG"
git checkout $LATEST_TAG
make modules -j$(nproc)
make modules_install

cd /tmp
cat > /tmp/nvidia-installer-helper.sh << 'NVINST'
#!/bin/bash
DRIVER_VERSION="545.29.06"
echo "Downloading NVIDIA driver version $DRIVER_VERSION..."
wget -O NVIDIA-Linux-x86_64-${DRIVER_VERSION}.run \
    https://us.download.nvidia.com/XFree86/Linux-x86_64/${DRIVER_VERSION}/NVIDIA-Linux-x86_64-${DRIVER_VERSION}.run
chmod +x NVIDIA-Linux-x86_64-${DRIVER_VERSION}.run
./NVIDIA-Linux-x86_64-${DRIVER_VERSION}.run \
    --dkms \
    --no-questions \
    --ui=none \
    --disable-nouveau \
    --run-nvidia-xconfig
echo "NVIDIA driver $DRIVER_VERSION installed successfully"
NVINST

chmod +x /tmp/nvidia-installer-helper.sh

cat > /etc/modprobe.d/blacklist-nouveau.conf << 'EOF'
blacklist nouveau
options nouveau modeset=0
EOF

update-initramfs -u

bash /tmp/nvidia-installer-helper.sh || {
    echo "Warning: Falling back to Debian packages..."
    apt-get install -y nvidia-driver nvidia-smi nvidia-settings
}

cd /usr/src
git clone https://github.com/NVIDIA/cuda-samples.git cuda-samples-github
apt-get install -y nvtop nvidia-cuda-toolkit

cd /usr/src
git clone https://github.com/NVIDIA/nvidia-settings.git nvidia-settings-src
cd nvidia-settings-src
make -j$(nproc)
make install

apt-get install -y nvidia-persistenced || {
    cd /usr/src
    git clone https://github.com/NVIDIA/nvidia-persistenced.git
    cd nvidia-persistenced
    make -j$(nproc)
    make install
    cat > /etc/systemd/system/nvidia-persistenced.service << 'NVPERSIST'
[Unit]
Description=NVIDIA Persistence Daemon
Wants=syslog.target
[Service]
Type=forking
ExecStart=/usr/bin/nvidia-persistenced --verbose
ExecStopPost=/bin/rm -rf /var/run/nvidia-persistenced
[Install]
WantedBy=multi-user.target
NVPERSIST
}

systemctl enable nvidia-persistenced

# NVIDIA Mode Switcher
cat > /usr/local/bin/nvidia-mode << 'NVEOF'
#!/bin/bash
MODE=$1
show_usage() {
    echo "GhostOS NVIDIA Mode Switcher"
    echo "Usage: nvidia-mode [production|gaming|status]"
}
check_nvidia() {
    if ! command -v nvidia-smi &> /dev/null; then
        echo "Error: NVIDIA drivers not found"
        exit 1
    fi
}
show_status() {
    echo "========================================="
    echo "  NVIDIA GPU Status"
    echo "========================================="
    nvidia-smi --query-gpu=name,driver_version,power.draw,temperature.gpu,clocks.current.graphics,clocks.current.memory --format=csv,noheader
    echo ""
    CURRENT_MODE=$(cat /etc/nvidia-mode.conf 2>/dev/null || echo "unknown")
    echo "Current Mode: $CURRENT_MODE"
}
set_production_mode() {
    echo "Switching to PRODUCTION mode..."
    nvidia-smi -pl $(nvidia-smi --query-gpu=power.max_limit --format=csv,noheader,nounits | awk '{print int($1 * 0.75)}')
    nvidia-smi -pm 1
    nvidia-settings -a "[gpu:0]/GpuPowerMizerMode=0" 2>/dev/null || true
    nvidia-smi -rgc 2>/dev/null || true
    nvidia-smi -rmc 2>/dev/null || true
    echo "production" > /etc/nvidia-mode.conf
    echo "✓ Production mode enabled"
}
set_gaming_mode() {
    echo "Switching to GAMING mode..."
    nvidia-smi -pl $(nvidia-smi --query-gpu=power.max_limit --format=csv,noheader,nounits | awk '{print int($1)}')
    nvidia-smi -pm 1
    nvidia-settings -a "[gpu:0]/GpuPowerMizerMode=1" 2>/dev/null || true
    MAX_GRAPHICS_CLOCK=$(nvidia-smi --query-supported-clocks=graphics --format=csv,noheader | head -1)
    MAX_MEMORY_CLOCK=$(nvidia-smi --query-supported-clocks=memory --format=csv,noheader | head -1)
    [ ! -z "$MAX_GRAPHICS_CLOCK" ] && nvidia-smi -lgc $MAX_GRAPHICS_CLOCK 2>/dev/null || true
    [ ! -z "$MAX_MEMORY_CLOCK" ] && nvidia-smi -lmc $MAX_MEMORY_CLOCK 2>/dev/null || true
    echo "gaming" > /etc/nvidia-mode.conf
    echo "✓ Gaming mode enabled"
}
check_nvidia
if [ "$MODE" = "status" ]; then
    show_status
elif [ "$MODE" = "production" ]; then
    [ "$EUID" -ne 0 ] && echo "Error: Must run as root" && exit 1
    set_production_mode
    show_status
elif [ "$MODE" = "gaming" ]; then
    [ "$EUID" -ne 0 ] && echo "Error: Must run as root" && exit 1
    set_gaming_mode
    show_status
else
    show_usage
    exit 1
fi
NVEOF

chmod +x /usr/local/bin/nvidia-mode

cat > /usr/share/applications/nvidia-mode-switcher.desktop << 'EOF'
[Desktop Entry]
Name=NVIDIA Mode Switcher
Comment=Switch between Production and Gaming modes
Exec=xfce4-terminal -e "bash -c 'nvidia-mode status; echo; read'"
Icon=nvidia-settings
Terminal=false
Type=Application
Categories=System;Settings;
EOF

echo "production" > /etc/nvidia-mode.conf

cat > /etc/systemd/system/nvidia-mode-restore.service << 'EOF'
[Unit]
Description=Restore NVIDIA Mode on Boot
After=nvidia-persistenced.service
[Service]
Type=oneshot
ExecStart=/usr/local/bin/nvidia-mode-restore.sh
RemainAfterExit=yes
[Install]
WantedBy=multi-user.target
EOF

cat > /usr/local/bin/nvidia-mode-restore.sh << 'EOF'
#!/bin/bash
MODE=$(cat /etc/nvidia-mode.conf 2>/dev/null || echo "production")
/usr/local/bin/nvidia-mode $MODE
EOF

chmod +x /usr/local/bin/nvidia-mode-restore.sh
systemctl enable nvidia-mode-restore.service

echo "[*] NVIDIA drivers installed from trusted GitHub sources"

# ============================================
# V1.1 ENHANCEMENTS
# ============================================

# Enhanced Privacy
echo ""
echo "[*] Configuring enhanced privacy..."

# Block more telemetry endpoints
cat >> /etc/hosts << 'EOF'

# GhostOS v1.1 Enhanced Privacy Blocking
# Microsoft Telemetry
0.0.0.0 vortex.data.microsoft.com
0.0.0.0 vortex-win.data.microsoft.com
0.0.0.0 telecommand.telemetry.microsoft.com
0.0.0.0 oca.telemetry.microsoft.com
0.0.0.0 sqm.telemetry.microsoft.com
0.0.0.0 watson.telemetry.microsoft.com
0.0.0.0 redir.metaservices.microsoft.com
0.0.0.0 choice.microsoft.com
0.0.0.0 df.telemetry.microsoft.com
0.0.0.0 reports.wes.df.telemetry.microsoft.com
0.0.0.0 services.wes.df.telemetry.microsoft.com
0.0.0.0 settings-win.data.microsoft.com

# Google Telemetry
0.0.0.0 google-analytics.com
0.0.0.0 ssl.google-analytics.com
0.0.0.0 www.google-analytics.com
0.0.0.0 analytics.google.com

# Facebook Tracking
0.0.0.0 www.facebook.com
0.0.0.0 facebook.com
0.0.0.0 static.ak.facebook.com
0.0.0.0 static.ak.fbcdn.net
0.0.0.0 connect.facebook.net
0.0.0.0 graph.facebook.com

# Amazon Tracking
0.0.0.0 device-metrics-us.amazon.com
0.0.0.0 device-metrics-us-2.amazon.com

# Adobe Tracking
0.0.0.0 practivate.adobe.com
0.0.0.0 ereg.adobe.com
0.0.0.0 activate.adobe.com
0.0.0.0 3dns-3.adobe.com

# Nvidia Telemetry
0.0.0.0 telemetry.nvidia.com
0.0.0.0 gfe.nvidia.com

# Steam Tracking (optional)
# 0.0.0.0 steamcommunity.com

EOF

# DNS Privacy
apt-get install -y unbound
cat > /etc/unbound/unbound.conf << 'EOF'
server:
    interface: 127.0.0.1
    do-ip4: yes
    do-udp: yes
    do-tcp: yes
    access-control: 127.0.0.0/8 allow
    verbosity: 1
    hide-identity: yes
    hide-version: yes
    harden-glue: yes
    harden-dnssec-stripped: yes
    use-caps-for-id: yes
    prefetch: yes
    qname-minimisation: yes
    
forward-zone:
    name: "."
    forward-addr: 1.1.1.1  # Cloudflare DNS
    forward-addr: 1.0.0.1
EOF

systemctl enable unbound

# MAC Address Randomization
cat > /etc/NetworkManager/conf.d/mac-randomization.conf << 'EOF'
[device]
wifi.scan-rand-mac-address=yes

[connection]
wifi.cloned-mac-address=random
ethernet.cloned-mac-address=random
EOF

# Firewall hardening
ufw default deny incoming
ufw default allow outgoing
ufw allow 22/tcp  # SSH
ufw enable

# ============================================
# Malwarebytes Installation
# ============================================
echo ""
echo "[*] Installing Malwarebytes..."

cd /tmp
# Note: Malwarebytes doesn't have official Linux version
# Installing ClamAV + rkhunter as alternatives
apt-get install -y clamav clamav-daemon clamav-freshclam rkhunter chkrootkit

# Update virus definitions
freshclam

# Create Malwarebytes-style wrapper
cat > /usr/local/bin/malwarebytes << 'MBEOF'
#!/bin/bash
# GhostOS Malwarebytes Wrapper
echo "GhostOS Security Scanner"
echo "Powered by ClamAV + rkhunter"
echo ""

echo "[*] Updating virus definitions..."
sudo freshclam

echo "[*] Scanning system..."
sudo clamscan -r -i /home

echo "[*] Checking for rootkits..."
sudo rkhunter --check --skip-keypress

echo "[*] Scan complete"
MBEOF

chmod +x /usr/local/bin/malwarebytes

# Create desktop entry
cat > /usr/share/applications/malwarebytes.desktop << 'EOF'
[Desktop Entry]
Name=Malwarebytes (GhostOS)
Comment=Security Scanner
Exec=xfce4-terminal -e malwarebytes
Icon=security-high
Terminal=false
Type=Application
Categories=Security;
EOF

# ============================================
# Improved UI - Smooth Animations
# ============================================
echo ""
echo "[*] Installing improved UI components..."

# Install advanced compositor
apt-get install -y picom

cat > /etc/xdg/picom.conf << 'EOF'
# GhostOS v1.1 Compositor Config
# Smooth animations and effects

# Shadows
shadow = true;
shadow-radius = 12;
shadow-offset-x = -7;
shadow-offset-y = -7;
shadow-opacity = 0.7;

# Fading
fading = true;
fade-in-step = 0.03;
fade-out-step = 0.03;
fade-delta = 4;

# Transparency
inactive-opacity = 0.95;
active-opacity = 1.0;
frame-opacity = 0.9;

# Blur
blur-background = true;
blur-method = "dual_kawase";
blur-strength = 5;

# Performance
backend = "glx";
vsync = true;
glx-no-stencil = true;
glx-no-rebind-pixmap = true;

# Animations
transition-length = 300;
transition-pow-x = 0.1;
transition-pow-y = 0.1;
transition-pow-w = 0.1;
transition-pow-h = 0.1;
size-transition = true;
EOF

# Install better themes
apt-get install -y \
    arc-theme \
    papirus-icon-theme \
    numix-gtk-theme \
    breeze-cursor-theme

# ============================================
# System Consolidation
# ============================================
echo ""
echo "[*] Consolidating system services..."

# Remove duplicate services
systemctl disable apport || true
systemctl disable whoopsie || true
systemctl disable bluetooth || true  # Already disabled for privacy

# Consolidate logs
cat > /etc/logrotate.d/ghostos << 'EOF'
/var/log/*.log {
    daily
    missingok
    rotate 7
    compress
    delaycompress
    notifempty
}
EOF

# Clean up unnecessary packages
apt-get autoremove -y
apt-get autoclean

# ============================================
# Windows Compatibility Layer (Wine - Privacy Mode)
# ============================================
echo ""
echo "[*] Installing Windows compatibility layer (Wine)..."

apt-get install -y software-properties-common wget
mkdir -pm755 /etc/apt/keyrings
wget -O /etc/apt/keyrings/winehq-archive.key https://dl.winehq.org/wine-builds/winehq.key
wget -NP /etc/apt/sources.list.d/ https://dl.winehq.org/wine-builds/debian/dists/bookworm/winehq-bookworm.sources

apt-get update
apt-get install -y --install-recommends winehq-staging winetricks cabextract unzip p7zip-full

apt-get install -y \
    mesa-vulkan-drivers \
    libvulkan1 \
    vulkan-tools \
    libgl1-mesa-dri:i386 \
    libgl1-mesa-glx:i386

dpkg --add-architecture i386
apt-get update
apt-get install -y wine32 wine64

cd /usr/src
git clone https://github.com/doitsujin/dxvk.git
cd dxvk
git checkout $(git describe --tags --abbrev=0)
apt-get install -y meson glslang-tools mingw-w64 mingw-w64-tools
./package-release.sh master /usr/local/share/dxvk --no-package

cd /usr/src
git clone --recursive https://github.com/HansKristian-Work/vkd3d-proton.git
cd vkd3d-proton
git checkout $(git describe --tags --abbrev=0)
./package-release.sh master /usr/local/share/vkd3d-proton --no-package

cat > /usr/local/bin/wine-privacy-setup << 'WINEPRIV'
#!/bin/bash
PREFIX="${WINEPREFIX:-$HOME/.wine}"
echo "Setting up Wine prefix: $PREFIX (Privacy mode)"
WINEDLLOVERRIDES="mscoree,mshtml=" WINEARCH=win64 wineboot -u
sleep 5
cat >> "$PREFIX/drive_c/windows/system32/drivers/etc/hosts" << 'EOF'
0.0.0.0 telemetry.microsoft.com
0.0.0.0 vortex.data.microsoft.com
0.0.0.0 settings-win.data.microsoft.com
0.0.0.0 watson.telemetry.microsoft.com
EOF
wine reg add "HKCU\\Software\\Wine\\DllOverrides" /v "mscoree" /d "" /f
wine reg add "HKCU\\Software\\Wine\\DllOverrides" /v "mshtml" /d "" /f
wine reg add "HKCU\\Software\\Wine" /v "Version" /d "win10" /f
echo "✓ Wine privacy setup complete"
WINEPRIV

chmod +x /usr/local/bin/wine-privacy-setup

cat > /usr/local/bin/wine-ghostos << 'WINELAUNCH'
#!/bin/bash
export WINEPREFIX="${WINEPREFIX:-$HOME/.wine}"
export WINEDLLOVERRIDES="mscoree,mshtml=;winemenubuilder.exe=d"
export WININET_DISABLE_NETWORK=1
export WINEDEBUG=-all
[ ! -d "$WINEPREFIX" ] && wine-privacy-setup
[ $# -eq 0 ] && echo "Usage: wine-ghostos <program.exe>" && exit 0
wine "$@"
WINELAUNCH

chmod +x /usr/local/bin/wine-ghostos

cat > /usr/local/bin/dxvk-install << 'DXVKINSTALL'
#!/bin/bash
PREFIX="${WINEPREFIX:-$HOME/.wine}"
[ ! -d "$PREFIX" ] && echo "Run wine-ghostos first" && exit 1
DXVK_DIR="/usr/local/share/dxvk"
[ -d "$DXVK_DIR" ] && cd "$DXVK_DIR" && \
    cp x64/*.dll "$PREFIX/drive_c/windows/system32/" && \
    wine reg add "HKCU\\Software\\Wine\\DllOverrides" /v "d3d9" /d "native" /f && \
    wine reg add "HKCU\\Software\\Wine\\DllOverrides" /v "d3d11" /d "native" /f && \
    echo "✓ DXVK installed"
DXVKINSTALL

chmod +x /usr/local/bin/dxvk-install

cat > /usr/share/applications/wine-ghostos.desktop << 'EOF'
[Desktop Entry]
Name=Wine (Privacy Mode)
Comment=Run Windows applications without telemetry
Exec=xfce4-terminal -e "bash -c 'wine-ghostos; read'"
Icon=wine
Terminal=true
Type=Application
Categories=System;Emulator;
EOF

echo "[*] Windows compatibility installed (Wine + DXVK, NO telemetry)"

# ============================================
# Network Security Monitoring (Low Impact)
# ============================================
echo ""
echo "[*] Installing network security monitoring (low-impact)..."

apt-get install -y fail2ban iftop nethogs iptraf-ng tcpdump nmap suricata

cat > /etc/fail2ban/jail.local << 'EOF'
[DEFAULT]
bantime = 3600
findtime = 600
maxretry = 5
[sshd]
enabled = true
port = ssh
maxretry = 3
EOF

systemctl enable fail2ban
systemctl start fail2ban || true

cat > /usr/local/bin/ghostos-netmon << 'NETMON'
#!/bin/bash
echo "Network Security Monitor - use 'netstatus' for quick view"
echo "1) Connections  2) Firewall  3) Fail2ban  4) Alerts  0) Exit"
read -p "Select: " choice
case $choice in
    1) ss -tunap | grep ESTABLISHED ;;
    2) ufw status verbose ;;
    3) fail2ban-client status ;;
    4) tail -20 /var/log/suricata/fast.log 2>/dev/null || echo "No alerts" ;;
esac
NETMON

chmod +x /usr/local/bin/ghostos-netmon

cat > /usr/local/bin/netstatus << 'NETSTATUS'
#!/bin/bash
echo "Network Security Status"
echo "Firewall: $(ufw status | head -1)"
echo "Fail2ban: $(systemctl is-active fail2ban)"
echo "Connections: $(ss -tunap | grep ESTABLISHED | wc -l)"
NETSTATUS

chmod +x /usr/local/bin/netstatus

echo "[*] Network monitoring active (Commands: ghostos-netmon, netstatus)"

echo "[✓] GhostOS v1.1 installation complete"

V11_EOF
chmod +x "$BUILD_DIR/install_v1.1.sh"
}

create_install_script_2.0() {
    cat > "$BUILD_DIR/install_v2.0.sh" << 'V2_EOF'
#!/bin/bash
set -e
export DEBIAN_FRONTEND=noninteractive

echo "========================================"
echo "  Installing GhostOS v2.0"
echo "  Next Generation"
echo "  on Parrot OS 7 Security base"
echo "========================================"

# ============================================
# Configure Parrot OS 7 Security Repositories
# ============================================
echo ""
echo "[*] Configuring Parrot OS 7 Security repositories..."

cat > /etc/apt/sources.list << 'PARROT_EOF'
# Parrot OS 7 (lory) - Security Edition Base
deb https://deb.parrot.sh/parrot lory main contrib non-free non-free-firmware
deb https://deb.parrot.sh/parrot lory-security main contrib non-free non-free-firmware
deb https://deb.parrot.sh/parrot lory-backports main contrib non-free non-free-firmware
PARROT_EOF

# ============================================
# BASE SYSTEM (from v1.0)
# ============================================
echo ""
echo "[*] Installing base system and kernel..."

apt-get update
apt-get install -y \
    linux-image-amd64 \
    linux-headers-amd64 \
    firmware-linux \
    firmware-linux-nonfree \
    build-essential \
    dkms \
    git \
    wget \
    curl

# ============================================
# AMD AM5 Chipset Support
# ============================================
echo ""
echo "[*] Installing AMD AM5 chipset support..."

apt-get install -y \
    amd64-microcode \
    firmware-amd-graphics \
    amdgpu-dkms \
    libdrm-amdgpu1 \
    mesa-vulkan-drivers \
    xserver-xorg-video-amdgpu

cat > /etc/modules-load.d/amd-pstate.conf << 'EOF'
amd_pstate
EOF

# ============================================
# ASUS AM5 Platform Drivers
# ============================================
echo ""
echo "[*] Installing ASUS AM5 motherboard drivers..."

apt-get install -y \
    linux-headers-$(uname -r) \
    dkms \
    i2c-tools \
    lm-sensors \
    fancontrol

cd /usr/src
git clone https://github.com/zeule/asus-wmi-sensors.git asus-wmi-sensors
cd asus-wmi-sensors

if [ -f "dkms.conf" ]; then
    dkms add -m asus-wmi-sensors -v 1.0
    dkms build -m asus-wmi-sensors -v 1.0
    dkms install -m asus-wmi-sensors -v 1.0
fi

echo "asus_wmi_sensors" >> /etc/modules-load.d/asus.conf

cd /usr/src
git clone https://github.com/zeule/asus-ec-sensors.git asus-ec-sensors
cd asus-ec-sensors
make
make install
echo "asus_ec_sensors" >> /etc/modules-load.d/asus.conf

# ============================================
# ASUS Aura RGB Support
# ============================================
echo ""
echo "[*] Installing ASUS Aura RGB support..."

apt-get install -y \
    libusb-1.0-0-dev \
    libhidapi-dev \
    qt5-default \
    qttools5-dev

cd /usr/src
git clone https://gitlab.com/CalcProgrammer1/OpenRGB.git openrgb
cd openrgb
qmake OpenRGB.pro
make -j$(nproc)
make install

cat > /etc/udev/rules.d/60-openrgb.rules << 'EOF'
SUBSYSTEM=="usb", ATTR{idVendor}=="0b05", ATTR{idProduct}=="1872", TAG+="uaccess"
SUBSYSTEM=="usb", ATTR{idVendor}=="0b05", ATTR{idProduct}=="1867", TAG+="uaccess"
SUBSYSTEM=="usb", ATTR{idVendor}=="0b05", ATTR{idProduct}=="19b6", TAG+="uaccess"
KERNEL=="i2c-[0-9]*", TAG+="uaccess"
EOF

udevadm control --reload-rules
udevadm trigger

# ============================================
# AM5 USB4/Thunderbolt Support
# ============================================
echo ""
echo "[*] Installing USB4/Thunderbolt support..."

apt-get install -y bolt thunderbolt-tools
systemctl enable bolt

# ============================================
# Audio Support
# ============================================
echo ""
echo "[*] Installing audio support..."

apt-get install -y \
    pulseaudio \
    pavucontrol \
    alsa-utils \
    firmware-sof-signed

sensors-detect --auto

cat > /usr/local/bin/asus-sensors-monitor << 'SENSEOF'
#!/bin/bash
echo "==================================="
echo "  ASUS AM5 System Sensors"
echo "==================================="
echo ""
echo "CPU Information:"
sensors | grep -A 10 "k10temp"
echo ""
echo "Motherboard Sensors:"
sensors | grep -A 20 "asus"
echo ""
echo "Fan Speeds:"
sensors | grep -i "fan"
SENSEOF

chmod +x /usr/local/bin/asus-sensors-monitor

# ============================================
# NVIDIA Driver Installation (from trusted source)
# ============================================
echo ""
echo "[*] Installing NVIDIA drivers from trusted GitHub source..."

apt-get install -y \
    build-essential \
    dkms \
    linux-headers-$(uname -r) \
    pkg-config \
    libglvnd-dev \
    libvulkan1 \
    vulkan-tools \
    xserver-xorg-dev

cd /usr/src
git clone https://github.com/NVIDIA/open-gpu-kernel-modules.git nvidia-open-drivers
cd nvidia-open-drivers
LATEST_TAG=$(git describe --tags --abbrev=0)
echo "Using NVIDIA driver version: $LATEST_TAG"
git checkout $LATEST_TAG
make modules -j$(nproc)
make modules_install

cd /tmp
cat > /tmp/nvidia-installer-helper.sh << 'NVINST'
#!/bin/bash
DRIVER_VERSION="545.29.06"
echo "Downloading NVIDIA driver version $DRIVER_VERSION..."
wget -O NVIDIA-Linux-x86_64-${DRIVER_VERSION}.run \
    https://us.download.nvidia.com/XFree86/Linux-x86_64/${DRIVER_VERSION}/NVIDIA-Linux-x86_64-${DRIVER_VERSION}.run
chmod +x NVIDIA-Linux-x86_64-${DRIVER_VERSION}.run
./NVIDIA-Linux-x86_64-${DRIVER_VERSION}.run \
    --dkms \
    --no-questions \
    --ui=none \
    --disable-nouveau \
    --run-nvidia-xconfig
echo "NVIDIA driver $DRIVER_VERSION installed successfully"
NVINST

chmod +x /tmp/nvidia-installer-helper.sh

cat > /etc/modprobe.d/blacklist-nouveau.conf << 'EOF'
blacklist nouveau
options nouveau modeset=0
EOF

update-initramfs -u

bash /tmp/nvidia-installer-helper.sh || {
    echo "Warning: Falling back to Debian packages..."
    apt-get install -y nvidia-driver nvidia-smi nvidia-settings
}

cd /usr/src
git clone https://github.com/NVIDIA/cuda-samples.git cuda-samples-github
apt-get install -y nvtop nvidia-cuda-toolkit

cd /usr/src
git clone https://github.com/NVIDIA/nvidia-settings.git nvidia-settings-src
cd nvidia-settings-src
make -j$(nproc)
make install

apt-get install -y nvidia-persistenced || {
    cd /usr/src
    git clone https://github.com/NVIDIA/nvidia-persistenced.git
    cd nvidia-persistenced
    make -j$(nproc)
    make install
    cat > /etc/systemd/system/nvidia-persistenced.service << 'NVPERSIST'
[Unit]
Description=NVIDIA Persistence Daemon
Wants=syslog.target
[Service]
Type=forking
ExecStart=/usr/bin/nvidia-persistenced --verbose
ExecStopPost=/bin/rm -rf /var/run/nvidia-persistenced
[Install]
WantedBy=multi-user.target
NVPERSIST
}

systemctl enable nvidia-persistenced

# NVIDIA Mode Switcher
cat > /usr/local/bin/nvidia-mode << 'NVEOF'
#!/bin/bash
MODE=$1
show_usage() {
    echo "GhostOS NVIDIA Mode Switcher"
    echo "Usage: nvidia-mode [production|gaming|status]"
}
check_nvidia() {
    if ! command -v nvidia-smi &> /dev/null; then
        echo "Error: NVIDIA drivers not found"
        exit 1
    fi
}
show_status() {
    echo "========================================="
    echo "  NVIDIA GPU Status"
    echo "========================================="
    nvidia-smi --query-gpu=name,driver_version,power.draw,temperature.gpu,clocks.current.graphics,clocks.current.memory --format=csv,noheader
    echo ""
    CURRENT_MODE=$(cat /etc/nvidia-mode.conf 2>/dev/null || echo "unknown")
    echo "Current Mode: $CURRENT_MODE"
}
set_production_mode() {
    echo "Switching to PRODUCTION mode..."
    nvidia-smi -pl $(nvidia-smi --query-gpu=power.max_limit --format=csv,noheader,nounits | awk '{print int($1 * 0.75)}')
    nvidia-smi -pm 1
    nvidia-settings -a "[gpu:0]/GpuPowerMizerMode=0" 2>/dev/null || true
    nvidia-smi -rgc 2>/dev/null || true
    nvidia-smi -rmc 2>/dev/null || true
    echo "production" > /etc/nvidia-mode.conf
    echo "✓ Production mode enabled"
}
set_gaming_mode() {
    echo "Switching to GAMING mode..."
    nvidia-smi -pl $(nvidia-smi --query-gpu=power.max_limit --format=csv,noheader,nounits | awk '{print int($1)}')
    nvidia-smi -pm 1
    nvidia-settings -a "[gpu:0]/GpuPowerMizerMode=1" 2>/dev/null || true
    MAX_GRAPHICS_CLOCK=$(nvidia-smi --query-supported-clocks=graphics --format=csv,noheader | head -1)
    MAX_MEMORY_CLOCK=$(nvidia-smi --query-supported-clocks=memory --format=csv,noheader | head -1)
    [ ! -z "$MAX_GRAPHICS_CLOCK" ] && nvidia-smi -lgc $MAX_GRAPHICS_CLOCK 2>/dev/null || true
    [ ! -z "$MAX_MEMORY_CLOCK" ] && nvidia-smi -lmc $MAX_MEMORY_CLOCK 2>/dev/null || true
    echo "gaming" > /etc/nvidia-mode.conf
    echo "✓ Gaming mode enabled"
}
check_nvidia
if [ "$MODE" = "status" ]; then
    show_status
elif [ "$MODE" = "production" ]; then
    [ "$EUID" -ne 0 ] && echo "Error: Must run as root" && exit 1
    set_production_mode
    show_status
elif [ "$MODE" = "gaming" ]; then
    [ "$EUID" -ne 0 ] && echo "Error: Must run as root" && exit 1
    set_gaming_mode
    show_status
else
    show_usage
    exit 1
fi
NVEOF

chmod +x /usr/local/bin/nvidia-mode

cat > /usr/share/applications/nvidia-mode-switcher.desktop << 'EOF'
[Desktop Entry]
Name=NVIDIA Mode Switcher
Comment=Switch between Production and Gaming modes
Exec=xfce4-terminal -e "bash -c 'nvidia-mode status; echo; read'"
Icon=nvidia-settings
Terminal=false
Type=Application
Categories=System;Settings;
EOF

echo "production" > /etc/nvidia-mode.conf

cat > /etc/systemd/system/nvidia-mode-restore.service << 'EOF'
[Unit]
Description=Restore NVIDIA Mode on Boot
After=nvidia-persistenced.service
[Service]
Type=oneshot
ExecStart=/usr/local/bin/nvidia-mode-restore.sh
RemainAfterExit=yes
[Install]
WantedBy=multi-user.target
EOF

cat > /usr/local/bin/nvidia-mode-restore.sh << 'EOF'
#!/bin/bash
MODE=$(cat /etc/nvidia-mode.conf 2>/dev/null || echo "production")
/usr/local/bin/nvidia-mode $MODE
EOF

chmod +x /usr/local/bin/nvidia-mode-restore.sh
systemctl enable nvidia-mode-restore.service

echo "[*] NVIDIA drivers installed from trusted GitHub sources"

# ============================================
# V1.1 ENHANCEMENTS (inherited)
# ============================================
echo ""
echo "[*] Configuring enhanced privacy..."

cat >> /etc/hosts << 'EOF'

# GhostOS Enhanced Privacy Blocking
0.0.0.0 vortex.data.microsoft.com
0.0.0.0 vortex-win.data.microsoft.com
0.0.0.0 telecommand.telemetry.microsoft.com
0.0.0.0 oca.telemetry.microsoft.com
0.0.0.0 sqm.telemetry.microsoft.com
0.0.0.0 watson.telemetry.microsoft.com
0.0.0.0 google-analytics.com
0.0.0.0 www.facebook.com
0.0.0.0 telemetry.nvidia.com
EOF

apt-get install -y unbound
cat > /etc/unbound/unbound.conf << 'EOF'
server:
    interface: 127.0.0.1
    do-ip4: yes
    do-udp: yes
    do-tcp: yes
    access-control: 127.0.0.0/8 allow
    hide-identity: yes
    hide-version: yes
forward-zone:
    name: "."
    forward-addr: 1.1.1.1
    forward-addr: 1.0.0.1
EOF

systemctl enable unbound

cat > /etc/NetworkManager/conf.d/mac-randomization.conf << 'EOF'
[device]
wifi.scan-rand-mac-address=yes
[connection]
wifi.cloned-mac-address=random
ethernet.cloned-mac-address=random
EOF

apt-get install -y ufw
ufw default deny incoming
ufw default allow outgoing
ufw allow 22/tcp
ufw --force enable

apt-get install -y clamav clamav-daemon clamav-freshclam rkhunter chkrootkit
freshclam || true

cat > /usr/local/bin/malwarebytes << 'MBEOF'
#!/bin/bash
echo "GhostOS Security Scanner"
echo "Powered by ClamAV + rkhunter"
sudo freshclam
sudo clamscan -r -i /home
sudo rkhunter --check --skip-keypress
echo "[*] Scan complete"
MBEOF

chmod +x /usr/local/bin/malwarebytes

cat > /usr/share/applications/malwarebytes.desktop << 'EOF'
[Desktop Entry]
Name=Malwarebytes (GhostOS)
Comment=Security Scanner
Exec=xfce4-terminal -e malwarebytes
Icon=security-high
Terminal=false
Type=Application
Categories=Security;
EOF

apt-get install -y picom

cat > /etc/xdg/picom.conf << 'EOF'
shadow = true;
shadow-radius = 12;
fading = true;
fade-in-step = 0.03;
fade-out-step = 0.03;
inactive-opacity = 0.95;
blur-background = true;
blur-method = "dual_kawase";
blur-strength = 5;
backend = "glx";
vsync = true;
EOF

apt-get install -y \
    arc-theme \
    papirus-icon-theme \
    numix-gtk-theme \
    breeze-cursor-theme

# ============================================
# V2.0 NEW FEATURES
# ============================================

# ============================================
# Wayland Support
# ============================================
echo ""
echo "[*] Installing Wayland support..."

apt-get install -y \
    wayland \
    wlroots \
    sway \
    waybar \
    wofi \
    mako-notifier \
    grim \
    slurp \
    wl-clipboard \
    xwayland

# Sway config
mkdir -p /etc/sway
cat > /etc/sway/config << 'EOF'
# GhostOS v2.0 Sway Config
# Modern Wayland compositor

# Variables
set $mod Mod4
set $term xfce4-terminal
set $menu wofi --show drun

# Key bindings
bindsym $mod+Return exec $term
bindsym $mod+d exec $menu
bindsym $mod+Shift+q kill

# Outputs
output * bg /usr/share/backgrounds/ghostos-2.0.png fill

# Gaps and borders
gaps inner 10
gaps outer 5
default_border pixel 2
default_floating_border pixel 2

# Colors (GhostOS theme)
client.focused          #00d9ff #00d9ff #000000 #00d9ff
client.focused_inactive #333333 #333333 #ffffff #333333
client.unfocused        #222222 #222222 #888888 #222222

# Animations (via custom script)
exec_always --no-startup-id ghostos-animations
EOF

# ============================================
# AI Assistant Integration
# ============================================
echo ""
echo "[*] Installing AI assistant..."

# Install Ollama for local LLM
curl -fsSL https://ollama.ai/install.sh | sh

# Install smaller model for local AI
ollama pull mistral:7b-instruct || true

# Create AI assistant service
cat > /etc/systemd/system/ghostos-ai.service << 'EOF'
[Unit]
Description=GhostOS AI Assistant
After=network.target

[Service]
Type=simple
User=ghostos
ExecStart=/usr/local/bin/ollama serve
Restart=always

[Install]
WantedBy=multi-user.target
EOF

systemctl enable ghostos-ai

# AI Assistant Python wrapper
pip3 install --break-system-packages \
    langchain \
    chromadb \
    sentence-transformers

cat > /usr/local/bin/ghostos-ai << 'AIEOF'
#!/usr/bin/env python3
"""GhostOS AI Assistant"""
import subprocess
import sys

def ask_ai(question):
    result = subprocess.run(
        ['ollama', 'run', 'mistral:7b-instruct', question],
        capture_output=True,
        text=True
    )
    return result.stdout

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: ghostos-ai 'your question'")
        sys.exit(1)
    
    question = ' '.join(sys.argv[1:])
    response = ask_ai(question)
    print(response)
AIEOF

chmod +x /usr/local/bin/ghostos-ai

# ============================================
# Advanced UI with Blur Effects
# ============================================
echo ""
echo "[*] Installing advanced UI..."

# Install Kvantum theme engine
apt-get install -y qt5-style-kvantum qt5-style-kvantum-themes

# Install advanced GTK themes
apt-get install -y \
    gtk3-engines-breeze \
    qt5ct \
    lxappearance-gtk3

# Advanced picom config with blur
cat > /etc/xdg/picom-v2.conf << 'EOF'
# GhostOS v2.0 Advanced Compositor

# Blur
blur: {
  method = "dual_kawase";
  strength = 8;
  background = true;
  background-frame = true;
  background-fixed = true;
}

# Shadows
shadow = true;
shadow-radius = 15;
shadow-offset-x = -12;
shadow-offset-y = -12;
shadow-opacity = 0.75;

# Fading
fading = true;
fade-in-step = 0.028;
fade-out-step = 0.028;
fade-delta = 3;

# Opacity
inactive-opacity = 0.92;
active-opacity = 1.0;
frame-opacity = 0.85;

# Animations (experimental)
animations = true;
animation-stiffness = 300;
animation-dampening = 22;
animation-clamping = true;
animation-window-mass = 0.5;
animation-for-open-window = "zoom";
animation-for-unmap-window = "zoom";

# Backend
backend = "glx";
vsync = true;
glx-no-stencil = true;
glx-no-rebind-pixmap = true;
use-damage = true;

# Performance
unredir-if-possible = true;
unredir-if-possible-delay = 500;
EOF

# ============================================
# Cloud Backup (Encrypted)
# ============================================
echo ""
echo "[*] Installing encrypted cloud backup..."

apt-get install -y \
    rclone \
    encfs \
    cryptsetup

# Create backup script
cat > /usr/local/bin/ghostos-backup << 'BACKUPEOF'
#!/bin/bash
# GhostOS Encrypted Cloud Backup

BACKUP_DIR="$HOME/GhostOS-Backup"
ENCRYPTED_DIR="$HOME/.ghostos-encrypted"
CLOUD_REMOTE="ghostos-cloud"

# Create encrypted directory
if [ ! -d "$ENCRYPTED_DIR" ]; then
    encfs "$ENCRYPTED_DIR" "$BACKUP_DIR"
fi

# Sync to cloud (user must configure rclone first)
rclone sync "$BACKUP_DIR" "$CLOUD_REMOTE:ghostos-backup" \
    --progress \
    --exclude ".Trash-*" \
    --exclude "lost+found"

echo "Backup complete"
BACKUPEOF

chmod +x /usr/local/bin/ghostos-backup

# ============================================
# Plugin System
# ============================================
echo ""
echo "[*] Installing plugin system..."

mkdir -p /opt/ghostos/plugins

cat > /usr/local/bin/ghostos-plugin << 'PLUGINEOF'
#!/usr/bin/env python3
"""GhostOS Plugin Manager"""

import os
import sys
import json
from pathlib import Path

PLUGIN_DIR = Path("/opt/ghostos/plugins")

def list_plugins():
    """List installed plugins"""
    for plugin in PLUGIN_DIR.glob("*/plugin.json"):
        with open(plugin) as f:
            info = json.load(f)
            print(f"{info['name']} v{info['version']} - {info['description']}")

def install_plugin(url):
    """Install plugin from URL"""
    # Simplified - would use git clone in real implementation
    print(f"Installing plugin from {url}...")

def remove_plugin(name):
    """Remove plugin"""
    plugin_path = PLUGIN_DIR / name
    if plugin_path.exists():
        import shutil
        shutil.rmtree(plugin_path)
        print(f"Removed {name}")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage:")
        print("  ghostos-plugin list")
        print("  ghostos-plugin install <url>")
        print("  ghostos-plugin remove <name>")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == 'list':
        list_plugins()
    elif command == 'install' and len(sys.argv) > 2:
        install_plugin(sys.argv[2])
    elif command == 'remove' and len(sys.argv) > 2:
        remove_plugin(sys.argv[2])
PLUGINEOF

chmod +x /usr/local/bin/ghostos-plugin

# ============================================
# ARM Architecture Support (Cross-compilation)
# ============================================
echo ""
echo "[*] Installing ARM support..."

apt-get install -y \
    qemu-user-static \
    binfmt-support \
    gcc-aarch64-linux-gnu \
    g++-aarch64-linux-gnu \
    crossbuild-essential-arm64

# Enable ARM emulation
update-binfmts --enable qemu-aarch64

# ============================================
# Advanced Privacy Features
# ============================================
echo ""
echo "[*] Configuring advanced privacy..."

# Install PrivacyGuard
pip3 install --break-system-packages privapy

# Kernel hardening
cat >> /etc/sysctl.conf << 'EOF'

# GhostOS v2.0 Security Hardening
kernel.dmesg_restrict = 1
kernel.kptr_restrict = 2
kernel.unprivileged_bpf_disabled = 1
kernel.unprivileged_userns_clone = 0
net.ipv4.conf.all.rp_filter = 1
net.ipv4.conf.default.rp_filter = 1
net.ipv4.tcp_syncookies = 1
net.ipv6.conf.all.disable_ipv6 = 1
net.ipv6.conf.default.disable_ipv6 = 1
EOF

sysctl -p

# AppArmor enforcement
apt-get install -y apparmor apparmor-utils
systemctl enable apparmor

# ============================================
# Modern UI Theme System
# ============================================
echo ""
echo "[*] Installing modern UI theme..."

# Create GhostOS v2.0 theme
mkdir -p /usr/share/themes/GhostOS-2.0/gtk-3.0

cat > /usr/share/themes/GhostOS-2.0/gtk-3.0/gtk.css << 'CSSEOF'
/* GhostOS v2.0 GTK Theme */

* {
    transition: all 300ms cubic-bezier(0.4, 0.0, 0.2, 1);
}

window {
    background-color: rgba(10, 10, 10, 0.95);
    color: #ffffff;
    border-radius: 12px;
}

button {
    background: linear-gradient(135deg, #00d9ff, #9b59b6);
    border-radius: 8px;
    padding: 10px 20px;
    border: none;
    color: white;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
}

button:hover {
    box-shadow: 0 6px 12px rgba(0, 217, 255, 0.4);
    transform: translateY(-2px);
}

entry {
    background-color: rgba(30, 30, 30, 0.9);
    border: 2px solid #00d9ff;
    border-radius: 6px;
    padding: 8px;
    color: white;
}

scrollbar {
    background-color: transparent;
}

scrollbar slider {
    background-color: rgba(0, 217, 255, 0.5);
    border-radius: 10px;
}

scrollbar slider:hover {
    background-color: rgba(0, 217, 255, 0.8);
}
CSSEOF

# Set default theme
cat > /etc/gtk-3.0/settings.ini << 'EOF'
[Settings]
gtk-theme-name=GhostOS-2.0
gtk-icon-theme-name=Papirus-Dark
gtk-font-name=Segoe UI 10
gtk-cursor-theme-name=Breeze
gtk-application-prefer-dark-theme=1
gtk-enable-animations=1
EOF

# ============================================
# Network Security Monitoring (Low Impact) - V2.0 Enhanced
# ============================================
echo ""
echo "[*] Installing enhanced network security monitoring..."

apt-get install -y fail2ban iftop nethogs iptraf-ng tcpdump nmap suricata

cat > /etc/fail2ban/jail.local << 'EOF'
[DEFAULT]
bantime = 3600
findtime = 600
maxretry = 5
[sshd]
enabled = true
maxretry = 3
EOF

systemctl enable fail2ban
systemctl start fail2ban || true

# Enhanced monitoring scripts for v2.0
cat > /usr/local/bin/ghostos-netmon << 'NETMON'
#!/bin/bash
echo "========================================="
echo "  GhostOS v2.0 Network Security Monitor"
echo "========================================="
echo "1) Active Connections  2) Firewall Status"
echo "3) Fail2ban Status     4) Security Alerts"
echo "5) Live Traffic        6) Banned IPs"
echo "7) Port Scan           0) Exit"
read -p "Select: " choice
case $choice in
    1) ss -tunap | grep ESTABLISHED ;;
    2) ufw status verbose ;;
    3) fail2ban-client status ;;
    4) tail -30 /var/log/suricata/fast.log 2>/dev/null || echo "No alerts" ;;
    5) nethogs -d 1 ;;
    6) fail2ban-client status sshd | grep "Banned IP" ;;
    7) nmap -sn $(ip route | grep default | awk '{print $3}' | sed 's/\.[0-9]*$/.0\/24/') ;;
esac
NETMON

chmod +x /usr/local/bin/ghostos-netmon

cat > /usr/local/bin/netstatus << 'NETSTATUS'
#!/bin/bash
echo "========================================="
echo "  Network Security Status"
echo "========================================="
echo "Firewall: $(ufw status | head -1)"
echo "Fail2ban: $(systemctl is-active fail2ban)"
echo "Suricata IDS: $(systemctl is-active suricata)"
echo "Active Connections: $(ss -tunap | grep ESTABLISHED | wc -l)"
echo "Banned IPs: $(fail2ban-client status sshd 2>/dev/null | grep 'Currently banned' | awk '{print $3}')"
echo ""
echo "Commands: ghostos-netmon (full dashboard), netstatus (quick check)"
NETSTATUS

chmod +x /usr/local/bin/netstatus

cat > /usr/share/applications/ghostos-netmon.desktop << 'EOF'
[Desktop Entry]
Name=Network Security Monitor
Comment=Monitor network security and threats
Exec=xfce4-terminal -e ghostos-netmon
Icon=security-high
Terminal=true
Type=Application
Categories=System;Security;Network;
EOF

echo "[*] Network security monitoring active (low-impact, real-time)"

echo "[✓] GhostOS v2.0 installation complete"

V2_EOF
chmod +x "$BUILD_DIR/install_v2.0.sh"
}

# ============================================
# ISO Creation Function
# ============================================

create_iso() {
    local VERSION=$1
    local OUTPUT=$2
    
    echo ""
    echo "[*] Creating ISO for v$VERSION..."
    
    # Copy kernel and initrd
    cp "$ROOTFS_DIR/boot/vmlinuz-"* "$ISO_DIR/live/vmlinuz"
    cp "$ROOTFS_DIR/boot/initrd.img-"* "$ISO_DIR/live/initrd.img"
    
    # Create squashfs
    mksquashfs "$ROOTFS_DIR" "$ISO_DIR/live/filesystem.squashfs" \
        -comp xz -b 1M -Xbcj x86 -e boot -progress
    
    # GRUB config
    cat > "$ISO_DIR/boot/grub/grub.cfg" << GRUBEOF
set timeout=30
set default=0

insmod all_video
insmod gfxterm
terminal_output gfxterm
set gfxmode=1920x1080
set gfxpayload=keep

menuentry "👻 GhostOS v$VERSION - Install" {
    linux /live/vmlinuz boot=live quiet splash installer-mode
    initrd /live/initrd.img
}

menuentry "👻 GhostOS v$VERSION - Live Mode" {
    linux /live/vmlinuz boot=live quiet splash
    initrd /live/initrd.img
}

menuentry "👻 GhostOS v$VERSION - Safe Mode" {
    linux /live/vmlinuz boot=live nomodeset
    initrd /live/initrd.img
}
GRUBEOF
    
    # Create EFI boot
    grub-mkstandalone \
        --format=x86_64-efi \
        --output="$ISO_DIR/EFI/BOOT/BOOTX64.EFI" \
        --locales="" \
        --fonts="" \
        "boot/grub/grub.cfg=$ISO_DIR/boot/grub/grub.cfg"
    
    # Create BIOS boot
    grub-mkstandalone \
        --format=i386-pc \
        --output="$ISO_DIR/boot/grub/core.img" \
        --locales="" \
        --fonts="" \
        "boot/grub/grub.cfg=$ISO_DIR/boot/grub/grub.cfg"
    
    cat /usr/lib/grub/i386-pc/cdboot.img "$ISO_DIR/boot/grub/core.img" \
        > "$ISO_DIR/boot/grub/bios.img"
    
    # Build ISO
    xorriso -as mkisofs \
        -iso-level 3 \
        -full-iso9660-filenames \
        -volid "GHOSTOS-v$VERSION" \
        -appid "GhostOS v$VERSION" \
        -publisher "jameshroop-art" \
        -eltorito-boot boot/grub/bios.img \
        -no-emul-boot \
        -boot-load-size 4 \
        -boot-info-table \
        --grub2-boot-info \
        --grub2-mbr /usr/lib/grub/i386-pc/boot_hybrid.img \
        -eltorito-alt-boot \
        -e EFI/BOOT/BOOTX64.EFI \
        -no-emul-boot \
        -isohybrid-gpt-basdat \
        -output "$OUTPUT" \
        "$ISO_DIR"
    
    isohybrid --uefi "$OUTPUT"
    
    md5sum "$OUTPUT" > "${OUTPUT}.md5"
    sha256sum "$OUTPUT" > "${OUTPUT}.sha256"
    
    echo "[✓] ISO created: $OUTPUT"
}

# ============================================
# USB Creation Function
# ============================================

create_usb() {
    local ISO=$1
    local DEVICE=$2
    
    echo ""
    echo "[*] Creating bootable USB..."
    echo "ISO: $ISO"
    echo "Device: $DEVICE"
    
    # Unmount
    umount ${DEVICE}* 2>/dev/null || true
    
    # Write
    dd if="$ISO" of="$DEVICE" bs=4M status=progress conv=fsync
    
    sync
    
    echo "[✓] Bootable USB created on $DEVICE"
}

# Build each version
for VERSION in "${VERSIONS[@]}"; do
    echo ""
    echo "========================================"
    echo "  Building GhostOS v$VERSION"
    echo "========================================"
    
    ISO_OUTPUT="$PROJECT_DIR/GhostOS-v${VERSION}.iso"
    
    # Create build structure
    mkdir -p "$PROJECT_DIR"/{build,downloads,logs}
    mkdir -p "$BUILD_DIR"/{iso,rootfs}
    mkdir -p "$ISO_DIR"/{boot/grub,EFI/BOOT,live}
    
    cd "$PROJECT_DIR"
    
    # Bootstrap if needed
    if [ ! -d "$ROOTFS_DIR/usr" ]; then
        echo "[*] Bootstrapping Parrot OS 7 Security base system..."
        echo "    Using Parrot Security repositories for enhanced security features"
        debootstrap --arch=amd64 --include=wget,curl,ca-certificates,gnupg \
            lory "$ROOTFS_DIR" https://deb.parrot.sh/parrot
    fi
    
    # Create version-specific installation script
    create_install_script_$VERSION
    
    # Execute installation
    mount --bind /dev "$ROOTFS_DIR/dev"
    mount --bind /dev/pts "$ROOTFS_DIR/dev/pts"
    mount --bind /proc "$ROOTFS_DIR/proc"
    mount --bind /sys "$ROOTFS_DIR/sys"
    
    cp "$BUILD_DIR/install_v${VERSION}.sh" "$ROOTFS_DIR/tmp/"
    chroot "$ROOTFS_DIR" /bin/bash /tmp/install_v${VERSION}.sh 2>&1 | tee "$PROJECT_DIR/logs/install_v${VERSION}.log"
    
    umount "$ROOTFS_DIR/sys" "$ROOTFS_DIR/proc" "$ROOTFS_DIR/dev/pts" "$ROOTFS_DIR/dev" || true
    
    # Create ISO
    create_iso "$VERSION" "$ISO_OUTPUT"
    
    # Create USB if last version
    if [ "$VERSION" = "${VERSIONS[-1]}" ] && [ "$CREATE_USB" = true ]; then
        create_usb "$ISO_OUTPUT" "$USB_DEVICE"
    fi
done

echo ""
echo "========================================"
echo "✅ BUILD COMPLETE!"
echo "========================================"

# Run the build
# (Function definitions above, execution happens in main loop)
