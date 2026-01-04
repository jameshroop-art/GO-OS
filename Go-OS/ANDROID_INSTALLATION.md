# GhostOS for Android - Installation Guide

Complete guide for installing GhostOS on Android 9+ devices without root access.

## Overview

GhostOS for Android provides a full Linux environment on your Android device using Termux and proot. It includes non-root WiFi and Bluetooth management tools that work with Android 9+ (API 28+).

## Requirements

### Minimum Requirements
- **Android Version**: Android 9.0 (Pie) or higher (API 28+)
- **Storage**: 2GB free space minimum, 5GB recommended
- **RAM**: 2GB minimum, 4GB recommended
- **Architecture**: ARM, ARM64, x86, or x86_64

### Required Apps
1. **Termux** (from F-Droid, NOT Google Play)
   - Download: https://f-droid.org/en/packages/com.termux/
   - Version: Latest stable

2. **Termux:API** (from F-Droid)
   - Download: https://f-droid.org/en/packages/com.termux.api/
   - Required for WiFi/Bluetooth control

### Permissions Required
Grant these permissions to Termux in Android Settings → Apps → Termux:
- ✅ Storage (for file access)
- ✅ Location (for WiFi/Bluetooth scanning)
- ✅ Network (automatic)

## Installation Steps

### Step 1: Install Termux

1. Open F-Droid app store
2. Search for "Termux"
3. Install Termux (NOT from Google Play - outdated version)
4. Open Termux to initialize

### Step 2: Install Termux:API

1. In F-Droid, search for "Termux:API"
2. Install Termux:API
3. Keep both apps installed

### Step 3: Grant Permissions

1. Go to Android Settings
2. Navigate to Apps → Termux
3. Tap Permissions
4. Grant:
   - Storage: Allow
   - Location: Allow (for Bluetooth/WiFi scanning)

### Step 4: Download GhostOS Installer

Open Termux and run:

```bash
# Update Termux
pkg update -y && pkg upgrade -y

# Install wget if not present
pkg install wget -y

# Download GhostOS installer
cd ~
wget https://raw.githubusercontent.com/jameshroop-art/GO-OS/main/Go-OS/ghostos-android.sh

# Make executable
chmod +x ghostos-android.sh
```

### Step 5: Run Installer

```bash
bash ghostos-android.sh
```

The installer will:
- Check Android version compatibility
- Install required Termux packages
- Set up Debian proot environment
- Install WiFi/Bluetooth management tools
- Create GhostOS commands
- Configure PATH

Installation takes 10-30 minutes depending on internet speed.

### Step 6: Activate GhostOS

After installation completes:

```bash
# Reload shell configuration
source ~/.bashrc

# Test GhostOS
ghostos

# View help
ghostos-help
```

## Features

### Non-Root WiFi Management

GhostOS provides WiFi control without root access using Android's Termux-API:

```bash
# Scan for networks
ghostos-wifi scan

# Show current connection
ghostos-wifi info

# Check WiFi status
ghostos-wifi status

# Enable/disable WiFi
ghostos-wifi enable
ghostos-wifi disable
```

### Non-Root Bluetooth Management

Control Bluetooth without root:

```bash
# Scan for devices
ghostos-bluetooth scan

# Show paired devices
ghostos-bluetooth devices

# Check Bluetooth status
ghostos-bluetooth status

# Enable/disable Bluetooth
ghostos-bluetooth enable
ghostos-bluetooth disable
```

### Driver Optimization

Optimize WiFi and Bluetooth performance:

```bash
ghostos-driver-optimizer
```

This tool:
- Analyzes WiFi signal strength
- Checks connection quality
- Provides optimization suggestions
- Works entirely in userspace (no root needed)

### Debian Linux Environment

Full Debian Linux with apt package manager:

```bash
# Launch Debian environment
ghostos-debian

# Inside Debian, you can:
apt update
apt install python3 nodejs gcc git nano vim
```

### System Information

```bash
ghostos-system
```

Shows:
- Android version and device info
- Termux configuration
- GhostOS installation details
- Hardware information

## How It Works Without Root

### WiFi/Bluetooth Control

GhostOS uses Android's official APIs through Termux:API:

1. **Termux:API Bridge**: Provides access to Android APIs
2. **Android Intent System**: Communicates with system services
3. **Standard Permissions**: Uses only user-granted permissions
4. **No Root Required**: Works within Android's security model

### Limitations Without Root

Since GhostOS runs without root access:

❌ **Cannot do:**
- Modify system WiFi/Bluetooth drivers directly
- Access raw hardware interfaces (e.g., monitor mode)
- Change system-level network configuration
- Install kernel modules
- Modify /system partition

✅ **Can do:**
- Control WiFi on/off
- Scan for networks
- View connection info
- Control Bluetooth on/off
- Scan for Bluetooth devices
- Optimize connection quality (userspace)
- Full Linux environment (proot)
- Install Linux packages

### Driver "Patching" Explained

The term "patching" in non-root context means:

1. **Optimization**: Tuning performance within userspace
2. **Monitoring**: Analyzing signal strength and quality
3. **Configuration**: Adjusting available settings
4. **Diagnostics**: Identifying and reporting issues

**Not** actual driver modification (requires root/kernel access).

## Usage Examples

### Example 1: Check WiFi Signal

```bash
# Run optimizer to see signal strength
ghostos-driver-optimizer

# Output shows:
# - Signal strength (dBm)
# - Link speed
# - Frequency
# - Optimization tips
```

### Example 2: Manage Bluetooth Devices

```bash
# Enable Bluetooth
ghostos-bluetooth enable

# Scan for devices
ghostos-bluetooth scan

# View paired devices
ghostos-bluetooth devices
```

### Example 3: Install Development Tools

```bash
# Launch Debian
ghostos-debian

# Inside Debian environment:
apt update
apt install -y python3 python3-pip nodejs npm git

# Install Python packages
pip3 install requests flask numpy

# Install Node.js packages
npm install -g express

# Clone and develop projects
git clone https://github.com/user/project.git
cd project
```

### Example 4: Monitor Network Performance

```bash
# Check WiFi status
ghostos-wifi status

# Run full optimization
ghostos-driver-optimizer

# View system details
ghostos-system
```

## Troubleshooting

### Issue: "Command not found"

**Solution:**
```bash
# Reload shell
source ~/.bashrc

# Or use full path
~/ghostos-android/bin/ghostos
```

### Issue: WiFi/Bluetooth commands don't work

**Cause:** Termux:API not installed or permissions not granted

**Solution:**
1. Install Termux:API from F-Droid
2. Grant Location permission to Termux
3. Restart Termux

### Issue: "Android 9+ required" error

**Solution:**
- Check Android version: Settings → About Phone
- GhostOS requires Android 9.0+ (API 28+)
- Upgrade Android if possible

### Issue: Installation fails during package download

**Solution:**
```bash
# Clear package cache
pkg clean

# Try again
pkg update -y && pkg upgrade -y
bash ghostos-android.sh
```

### Issue: Debian environment won't start

**Solution:**
```bash
# Reinstall proot-distro
pkg reinstall proot-distro

# Reinstall Debian
proot-distro remove debian
proot-distro install debian
```

### Issue: Permission denied errors

**Solution:**
1. Go to Android Settings → Apps → Termux → Permissions
2. Enable Storage and Location
3. Restart Termux
4. Try command again

## Advanced Configuration

### Custom Debian Configuration

Edit Debian startup script:

```bash
nano ~/ghostos-android/config/debian-startup.sh
```

### Add Custom Commands

Create scripts in:
```bash
~/ghostos-android/bin/
```

Make executable:
```bash
chmod +x ~/ghostos-android/bin/my-command
```

### Update GhostOS

```bash
# Re-run installer
bash ~/ghostos-android.sh

# Or use alias
ghostos-update
```

## Uninstallation

To remove GhostOS:

```bash
# Remove Debian environment
proot-distro remove debian

# Remove GhostOS directory
rm -rf ~/ghostos-android

# Remove from PATH (edit ~/.bashrc)
nano ~/.bashrc
# Delete GhostOS lines

# Reload shell
source ~/.bashrc
```

## Comparison: Root vs Non-Root

| Feature | With Root | Without Root (GhostOS) |
|---------|-----------|------------------------|
| WiFi On/Off | ✅ | ✅ |
| WiFi Scanning | ✅ | ✅ |
| WiFi Info | ✅ | ✅ |
| Monitor Mode | ✅ | ❌ |
| Packet Injection | ✅ | ❌ |
| Bluetooth On/Off | ✅ | ✅ |
| Bluetooth Scanning | ✅ | ✅ |
| BLE Control | ✅ | ✅ (limited) |
| Driver Modification | ✅ | ❌ |
| Kernel Modules | ✅ | ❌ |
| Linux Environment | ✅ | ✅ (proot) |
| System Files | ✅ | ❌ |

## Security Considerations

### GhostOS is Safe

- ✅ No root access required
- ✅ Uses only standard Android APIs
- ✅ Respects Android security model
- ✅ No system modifications
- ✅ Sandboxed environment (proot)
- ✅ Can be fully removed

### Permissions Explained

1. **Storage**: Access files in Termux home directory
2. **Location**: Required by Android for WiFi/Bluetooth scanning (hardware limitation)
3. **Network**: Standard network access

GhostOS does NOT:
- ❌ Collect or transmit data
- ❌ Modify system files
- ❌ Require root/bootloader unlock
- ❌ Access other apps' data
- ❌ Phone home or track usage

## FAQ

**Q: Does this require root?**  
A: No! GhostOS works entirely without root access.

**Q: Will this void my warranty?**  
A: No. GhostOS doesn't modify system files or unlock bootloader.

**Q: Can I use this for WiFi hacking?**  
A: No. Without root, advanced WiFi features (monitor mode, packet injection) are not available.

**Q: Why can't I modify drivers?**  
A: Android's security model prevents non-root apps from accessing kernel drivers directly.

**Q: Is this like Linux Deploy or Andronix?**  
A: Similar concept (proot-based Linux), but GhostOS adds custom WiFi/Bluetooth management tools.

**Q: Can I use this with other Linux distros?**  
A: Yes! You can install other distros via proot-distro (Ubuntu, Arch, Alpine, etc.)

**Q: Does this work on all Android devices?**  
A: Works on most Android 9+ devices. Some manufacturer-specific restrictions may apply.

**Q: How much battery does this use?**  
A: Minimal when idle. Active use similar to running any app.

**Q: Can I access Android files from Debian?**  
A: Yes! Android storage is accessible at `/sdcard` in Termux/Debian.

## Support

### Getting Help

1. **Documentation**: Read this guide and ghostos-help
2. **GitHub Issues**: https://github.com/jameshroop-art/GO-OS/issues
3. **Termux Wiki**: https://wiki.termux.com
4. **Community**: Termux Reddit, F-Droid forums

### Reporting Issues

Include:
- Android version and device model
- Termux version
- Error message (full output)
- Steps to reproduce

### Contributing

Contributions welcome! See repository for guidelines.

## Resources

- **GhostOS Repository**: https://github.com/jameshroop-art/GO-OS
- **Termux**: https://termux.com
- **Termux Wiki**: https://wiki.termux.com
- **F-Droid**: https://f-droid.org
- **proot-distro**: https://github.com/termux/proot-distro

## Version History

- **1.0-android** (2026-01-04): Initial Android release
  - Android 9+ support
  - Non-root WiFi/Bluetooth management
  - Debian proot environment
  - Driver optimization tools

---

**Note**: GhostOS for Android provides a powerful Linux environment and WiFi/Bluetooth management tools without requiring root access. While some advanced features are limited compared to rooted devices, it offers a secure, reversible, and warranty-safe way to run Linux on Android.

For the full desktop GhostOS experience, see `GHOSTOS_BUILD_README.md` for building bootable ISOs.
