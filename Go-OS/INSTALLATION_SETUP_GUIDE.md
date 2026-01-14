# HeckOS Installation Setup Guide

## Overview

The HeckOS Installation Setup provides a streamlined, user-friendly way to install HeckOS on various device types. This guide covers the device type selection process and installation options.

## Quick Start

```bash
cd Go-OS
sudo bash ghostos-installation-setup.sh
```

This launches the Installation Setup GUI where you can select your target device type.

## Supported Device Types

### 1. 🖥️ Standard PC (BIOS/UEFI)

**Description:** Standard desktop or workstation installation with automatic hardware detection.

**Requirements:**
- 64-bit x86_64 processor (Intel or AMD)
- 8GB RAM minimum (16GB recommended)
- 32GB available storage
- BIOS or UEFI firmware
- Network connection (recommended)

**Features:**
- Full Debian 12 (Bookworm) installation
- Automatic hardware detection
- Support for AMD AM5, Intel, and NVIDIA hardware
- Gaming and development tools
- Privacy and security features

**Installation Process:**
1. Automatic hardware detection
2. Disk partitioning and formatting
3. Base system installation
4. Bootloader configuration (GRUB)
5. Driver installation
6. Desktop environment setup

### 2. 🖥️ PC with Grub2 (Multi-boot)

**Description:** Install alongside other operating systems using Grub2 bootloader.

**Requirements:**
- 64-bit x86_64 processor
- 8GB RAM minimum (16GB recommended)
- 32GB available storage (separate partition or free space)
- UEFI firmware (recommended) or BIOS
- Existing operating system(s)

**Features:**
- Install alongside Windows, Linux, or other OS
- Grub2 bootloader for multi-boot menu
- Automatic detection of existing OS installations
- Chain-loading support
- Safe installation without affecting other systems

**Installation Process:**
1. Detect existing operating systems
2. Resize partitions or use free space
3. Install HeckOS
4. Configure Grub2 with all OS options
5. Set boot order and timeout
6. Verify multi-boot functionality

⚠️ **Recommended:** Backup important data before installation

### 3. 💻 Laptop

**Description:** Optimized installation for laptops with power management, touchpad, and WiFi support.

**Requirements:**
- 64-bit x86_64 laptop processor
- 8GB RAM minimum (16GB recommended)
- 32GB available storage
- UEFI firmware (most modern laptops)
- WiFi adapter

**Features:**
- Optimized power management (TLP, laptop-mode-tools)
- Touchpad gesture support
- WiFi and Bluetooth drivers
- Battery monitoring and optimization
- Screen brightness controls
- Suspend/hibernate support
- Laptop-specific thermal management

**Supported Laptop Brands:**
- Dell, HP, Lenovo, ASUS, Acer
- Apple MacBook (Intel-based)
- System76, Framework
- Most other x86_64 laptops

### 4. 💾 Bootable USB (with SD Card option)

**Description:** Create portable bootable USB drive with optional SD card persistence.

**Requirements:**
- USB drive (16GB minimum, 32GB+ recommended)
- Optional: SD card for additional storage/persistence
- USB 3.0+ for best performance
- Target system: Any PC with USB boot support

**Features:**
- Portable HeckOS installation
- Boot from any compatible PC
- Optional persistence (save changes)
- SD card support for extended storage
- Live environment or persistent mode
- No installation required on host PC

**Usage Modes:**
- **Live Mode:** No changes saved (reset on reboot)
- **Persistent Mode:** Changes saved to USB/SD card
- **Full Installation:** USB as primary drive

⚠️ **Warning:** All data on USB and SD card will be erased!

### 5. 📱 Android Device (Termux - Android 9+)

**Description:** Install Debian environment via Termux on Android 9+ devices (no root required).

**Requirements:**
- Android 9.0+ (API 28 or higher)
- 2GB RAM minimum (4GB recommended)
- 5GB available storage
- Termux app (from F-Droid, NOT Google Play)
- Termux:API app (from F-Droid)
- Storage and Location permissions
- Network connection

**Features:**
- Full Debian 12 environment via proot
- No root access required
- WiFi management (non-root)
- Bluetooth management (non-root)
- Linux package ecosystem (apt)
- Development tools (Python, Node.js, etc.)
- Driver optimization utilities

**Android Installation Options:**
1. **USB Storage:** Install from USB drive connected via OTG
2. **SD Card:** Install from SD card
3. **Network Download:** Download directly via internet

**Android-Specific Features:**
- Device make/model detection for driver bridging
- Controller/root access configuration (for advanced features)
- Termux integration for hardware access
- Device-specific driver configuration

⚠️ **Important:** Install Termux from F-Droid, NOT Google Play! The Google Play version is outdated and incompatible.

**Note:** Device-specific driver bridging will be configured during installation based on your phone's make, model, and Android version. This includes:
- Hardware controller bridging
- Driver version compatibility
- Root access configuration (optional)
- Termux API integration

## Installation Flow

### Step 1: Device Type Selection

1. Launch the Installation Setup:
   ```bash
   sudo bash ghostos-installation-setup.sh
   ```

2. The GUI will present all supported device types

3. Select your target device type

4. Review device-specific requirements and features

5. For Android, choose installation source (USB/SD/Network)

6. Click "Continue to Installation"

### Step 2: Device-Specific Installation

The setup will launch the appropriate installer based on your selection:

- **PC/Laptop:** Opens main installer GUI with appropriate options
- **USB:** Opens bootable USB creator
- **Android:** Provides instructions and script for Termux installation

## Usage Examples

### Installing on Standard PC

```bash
cd Go-OS
sudo bash ghostos-installation-setup.sh
# Select: Standard PC (BIOS/UEFI)
# Follow GUI prompts
```

### Creating Bootable USB

```bash
cd Go-OS
sudo bash ghostos-installation-setup.sh
# Select: Bootable USB (with SD Card option)
# Choose USB drive
# Configure persistence options
# Start creation
```

### Installing on Android

```bash
# On desktop/laptop:
cd Go-OS
bash ghostos-installation-setup.sh
# Select: Android Device (Termux - Android 9+)
# Choose installation source
# Follow on-screen instructions

# On Android device in Termux:
pkg update && pkg upgrade -y
pkg install wget -y
wget https://raw.githubusercontent.com/jameshroop-art/GO-OS/main/Go-OS/ghostos-android.sh
chmod +x ghostos-android.sh
bash ghostos-android.sh --source=network
```

## Driver Controller VM Integration

For PC and Laptop installations, the Driver Controller VM is available for Windows driver compatibility:

**Features:**
- Lightweight Windows 10 VM for driver management
- Minimal resource usage (512MB RAM, 1 CPU core)
- Process isolation (only driver-essential services)
- RPC communication between Linux and Windows VM
- Native Windows driver handling

**See Also:**
- `/windows_driver_emulator/VM_ARCHITECTURE.md` - VM architecture details
- `/windows_driver_emulator/README.md` - Driver VM usage guide

## Android Driver Bridging

Android installations include device-specific driver bridging:

1. **Detection Phase:**
   - Device make and model identification
   - Android version detection
   - Hardware capabilities assessment

2. **Bridge Configuration:**
   - Termux API integration
   - Hardware controller access
   - Driver version compatibility
   - Root access setup (if available)

3. **Driver Installation:**
   - Device-specific drivers
   - Termux-native tools
   - Hardware optimization
   - Performance tuning

**Note:** The Android driver bridging system will be expanded in future versions to support more device makes and models.

## Troubleshooting

### GUI Won't Launch

**Problem:** "No graphical display detected"

**Solution:**
- Ensure you're in a desktop environment (not SSH)
- Check DISPLAY variable: `echo $DISPLAY`
- Try: `export DISPLAY=:0`

### Missing Dependencies

**Problem:** "tkinter not found"

**Solution:**
```bash
# Debian/Ubuntu
sudo apt-get install python3-tk

# Fedora/RedHat
sudo dnf install python3-tkinter

# Arch
sudo pacman -Sy python-tk
```

### Android Installation Issues

**Problem:** Termux installation fails

**Solution:**
1. Verify Termux is from F-Droid (not Google Play)
2. Grant all required permissions
3. Update packages: `pkg update && pkg upgrade`
4. Check storage space: `df -h`
5. Try alternative installation source

### USB Creation Fails

**Problem:** USB creation failed or verification error

**Solution:**
1. Verify ISO file integrity
2. Use USB 3.0 port
3. Try different USB drive
4. Run as root: `sudo bash ghostos-installation-setup.sh`
5. Check drive isn't mounted: `umount /dev/sdX`

## System Requirements Summary

| Device Type | CPU | RAM | Storage | Notes |
|-------------|-----|-----|---------|-------|
| Standard PC | x86_64 | 8GB | 32GB | BIOS/UEFI |
| PC with Grub2 | x86_64 | 8GB | 32GB | Existing OS required |
| Laptop | x86_64 | 8GB | 32GB | WiFi required |
| Bootable USB | - | - | 16GB USB | Host PC needed |
| Android | ARM/ARM64 | 2GB | 5GB | Android 9+ |

## Security Notes

- PC installations require root privileges
- USB creation erases all data on target drive
- Android installation does NOT require root
- Backup important data before any installation
- Verify ISO checksums before installation

## Additional Resources

- **Main Repository:** https://github.com/jameshroop-art/GO-OS
- **Installation Issues:** https://github.com/jameshroop-art/GO-OS/issues
- **Documentation:** See Go-OS/DOCUMENTATION_INDEX.md
- **Android Guide:** See Go-OS/ANDROID_INSTALLATION.md
- **Driver VM Guide:** See windows_driver_emulator/VM_ARCHITECTURE.md

## Future Enhancements

Planned features for future releases:

1. **Additional Device Types:**
   - Raspberry Pi and ARM devices
   - Virtual machine templates
   - Cloud deployment options

2. **Enhanced Android Support:**
   - Expanded device make/model database
   - Automatic driver version detection
   - Root-enabled advanced features
   - Custom kernel support

3. **Improved Driver VM:**
   - Additional device controllers
   - GPU passthrough support
   - Enhanced process isolation
   - Performance optimizations

4. **Installation Features:**
   - Automated backup before installation
   - Recovery partition creation
   - Network installation support
   - Remote installation management

---

**Version:** 1.0  
**Last Updated:** January 2026  
**License:** MIT (See LICENSE file)
