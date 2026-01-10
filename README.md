# Heck-CheckOS - Multi-Platform Operating System

Complete operating system distribution available for multiple platforms with advanced privacy features, driver support, and full customization.

> ⚖️ **Legal Notice:** This is an independent project based on Debian 12 (Bookworm). Not affiliated with, endorsed by, or officially associated with Debian, Ghost Foundation, or any other "Ghost" branded software. See [LEGAL_COMPLIANCE.md](LEGAL_COMPLIANCE.md) for complete legal information.

## 🚀 Platforms

### 🐧 Desktop/Server (Linux ISO) THIS REPO DOES NOT CONTAIN THE ISO YOU CAN GET IT HERE: https://www.debian.org
Full-featured **Debian 12 (Bookworm)**-based distribution with multiple versions:
- **v1.0 - Stable Release**: Complete base system with security tools (~10GB)
- **v1.1 - Enhanced Edition**: Privacy-focused with enhanced security (~11GB)
- **v2.0 - Next Generation**: Wayland, AI assistant, cloud backup, plugin system (~12GB)

**Base Operating System:** Debian 12 (Bookworm) - Stable Linux distribution

**Heck-CheckOS Features:**
- ✅ BIOS/UEFI boot support
- ✅ AMD AM5/ASUS platform optimizations
- ✅ Gaming and AI/ML tools
- ✅ Enhanced privacy controls
- ✅ Security tools and hardening (Kali + Heck-CheckOS)
- ✅ Custom Heck-CheckOS GUI and desktop environment

**Documentation:** See [`GHOSTOS_BUILD_README.md`](Go-OS/GHOSTOS_BUILD_README.md) and [`GHOSTOS_QUICK_REFERENCE.md`](Go-OS/GHOSTOS_QUICK_REFERENCE.md)

## 📥 Getting the Debian 12 ISO (Optional)

**Note:** The Heck-CheckOS build script uses `debootstrap` to download Debian 12 automatically from official repositories. **You do NOT need to download the ISO to build Heck-CheckOS.**

**However, you may want to download the Debian 12 ISO (~600MB for netinst, ~4GB for full DVD) if you:**
- Want to test Debian 12 before building Heck-CheckOS
- Need to manually install Debian 12 on a system
- Want a reference copy of the official Debian distribution

**Due to GitHub's 2GB file size limit, the ISO cannot be stored in this repository.**

### Quick Download

```bash
cd ~/GO-OS
wget https://cdimage.debian.org/debian-cd/current/amd64/iso-cd/debian-12.8.0-amd64-netinst.iso
```

### Verify Your Download

```bash
# Check file size (~600MB for netinst expected)
ls -lh debian-12.8.0-amd64-netinst.iso

# Verify it's a valid ISO
file debian-12.8.0-amd64-netinst.iso

# Verify checksum
sha256sum debian-12.8.0-amd64-netinst.iso
# Compare with official checksum from debian.org
```

### Automated Verification

```bash
cd Go-OS
./verify-iso.sh ../debian-12.8.0-amd64-netinst.iso
```

**📖 For detailed download instructions, troubleshooting, and verification:**  
**👉 See [Go-OS/ISO_DOWNLOAD_GUIDE.md](Go-OS/ISO_DOWNLOAD_GUIDE.md)**

### 📱 Android 9+ (NEW!)
Lightweight Linux environment for Android with non-root WiFi/Bluetooth management:
- **Minimum**: Android 9.0 (API 28+)
- **No Root Required**: Works with standard permissions
- **Full Linux**: Debian environment via proot
- **Driver Management**: WiFi/Bluetooth control without root

**Features:**
- ✅ Non-root WiFi scanning and control
- ✅ Non-root Bluetooth management
- ✅ Driver optimization tools
- ✅ Full Debian Linux environment
- ✅ Works on Android 9, 10, 11, 12, 13, 14+

**Documentation:** See [`ANDROID_INSTALLATION.md`](Go-OS/ANDROID_INSTALLATION.md) and [`ANDROID_QUICK_REFERENCE.md`](Go-OS/ANDROID_QUICK_REFERENCE.md)

## 📦 Quick Start

### Desktop/Server Installation

```bash
# Download and run
wget https://raw.githubusercontent.com/jameshroop-art/GO-OS/main/Go-OS/heckcheckos-build.sh
chmod +x heckcheckos-build.sh
sudo ./heckcheckos-build.sh
```

Builds bootable ISO with:
- Debian 12 (Bookworm) base
- Heck-CheckOS custom GUI and desktop environment
- Complete Linux system with security tools
- Hardware drivers (AMD, NVIDIA, Intel)
- Privacy and security tools (Kali + Heck-CheckOS)
- Gaming support
- Development tools

### Android Installation

```bash
# Install Termux from F-Droid (NOT Google Play)
# Install Termux:API from F-Droid
# Grant Storage + Location permissions

# In Termux:
pkg update -y && pkg upgrade -y
pkg install wget -y
wget https://raw.githubusercontent.com/jameshroop-art/GO-OS/main/Go-OS/heckcheckos-android.sh
chmod +x heckcheckos-android.sh
bash heckcheckos-android.sh
source ~/.bashrc
ghostos
```

Installs:
- Debian 12 (Bookworm) proot environment
- WiFi management tools (non-root)
- Bluetooth management tools (non-root)
- Driver optimization utilities
- Full Linux command-line tools

## 📚 Documentation

**👉 [Complete Documentation Index](Go-OS/DOCUMENTATION_INDEX.md)** - Full documentation listing

### Desktop/Server
- **[Build System README](Go-OS/GHOSTOS_BUILD_README.md)** - Complete build guide
- **[Quick Reference](Go-OS/GHOSTOS_QUICK_REFERENCE.md)** - Fast command reference
- **[Build Script](Go-OS/heckcheckos-build.sh)** - Main build script
- **[Files Report](Go-OS/GHOST_OS_FILES_REPORT.md)** - Project structure
- **[Security Notes](Go-OS/VERIFICATION_TOOL_SECURITY_NOTES.md)** - Security documentation

### Android
- **[Installation Guide](Go-OS/ANDROID_INSTALLATION.md)** - Complete setup instructions
- **[Quick Reference](Go-OS/ANDROID_QUICK_REFERENCE.md)** - Command cheat sheet
- **[Technical Details](Go-OS/ANDROID_TECHNICAL_DETAILS.md)** - Architecture and compatibility
- **[Install Script](Go-OS/heckcheckos-android.sh)** - Android installer

### General
- **[FAQ](Go-OS/FAQ.md)** - Frequently Asked Questions
- **[Architecture](Go-OS/ARCHITECTURE.md)** - System architecture and diagrams

## 🎯 Features Comparison

### Desktop/Server Heck-CheckOS

| Feature | v1.0 | v1.1 | v2.0 |
|---------|------|------|------|
| Base System | ✅ | ✅ | ✅ |
| BIOS/UEFI Boot | ✅ | ✅ | ✅ |
| AMD AM5 Support | ✅ | ✅ | ✅ |
| Gaming Tools | ✅ | ✅ | ✅ |
| Enhanced Privacy | ❌ | ✅ | ✅ |
| Security Scanner | ❌ | ✅ | ✅ |
| Smooth UI | ❌ | ✅ | ✅ |
| Wayland | ❌ | ❌ | ✅ |
| AI Assistant | ❌ | ❌ | ✅ |
| Cloud Backup | ❌ | ❌ | ✅ |
| Plugin System | ❌ | ❌ | ✅ |
| ARM Support | ❌ | ❌ | ✅ |

### Android Heck-CheckOS

| Feature | Status | Notes |
|---------|--------|-------|
| WiFi Control | ✅ | On/off, scan, info |
| WiFi Monitor Mode | ❌ | Requires root |
| Bluetooth Control | ✅ | On/off, scan, devices |
| Bluetooth HCI Access | ❌ | Requires root |
| Linux Environment | ✅ | Full Debian via proot |
| Package Manager | ✅ | apt (Debian) + pkg (Termux) |
| Python/Node.js | ✅ | Full development environment |
| Driver Optimization | ✅ | Userspace analysis |
| Driver Modification | ❌ | Requires root |
| Works Without Root | ✅ | All features non-root |

## 🔧 Requirements

### Desktop/Server
- **Build OS**: Debian-based Linux (for building the ISO)
- **Base OS**: Debian 12 (Bookworm) - automatically bootstrapped
- **RAM**: 8GB minimum, 16GB recommended
- **Disk**: 50-100GB (depending on version)
- **Root**: Required for building
- **Target**: x86_64, ARM64 (v2.0)

### Android
- **Android**: 9.0+ (API 28+)
- **Storage**: 2GB minimum, 5GB recommended
- **RAM**: 2GB minimum, 4GB recommended
- **Root**: NOT required
- **Apps**: Termux + Termux:API (from F-Droid)
- **Permissions**: Storage, Location

## 🌟 Key Features

### Privacy & Security
- **Telemetry Blocking**: Microsoft, Google, Facebook, Amazon, Adobe, Nvidia
- **DNS Privacy**: Unbound + Cloudflare DNS
- **MAC Randomization**: Network privacy protection
- **Firewall**: UFW with secure defaults
- **Security Tools**: ClamAV, rkhunter, chkrootkit
- **Kernel Hardening**: sysctl, AppArmor (v2.0+)

### Hardware Support (Desktop)
- **AMD AM5**: Full chipset support, sensors, RGB
- **ASUS Boards**: WMI sensors, EC sensors, Aura Sync
- **NVIDIA**: Driver support, CUDA tools
- **Intel**: Full support including Arc GPUs
- **USB4/Thunderbolt**: Complete support

### Android Features
- **Non-Root WiFi**: Full WiFi control via Android APIs
- **Non-Root Bluetooth**: Complete Bluetooth management
- **Driver Analysis**: Signal strength, connection quality
- **Performance Tips**: Automated optimization suggestions
- **Linux Apps**: Run any Linux software via Debian

### Development Tools
- **Desktop**: Full IDE support, compilers, debuggers
- **Android**: Python, Node.js, Java, C/C++, Go
- **AI/ML**: TensorFlow, PyTorch, Ollama (desktop v2.0)
- **Gaming**: Steam, Lutris, Wine, Proton

## 📱 Android Commands

```bash
# Quick status
heckcheckos-wifi status
heckcheckos-bluetooth status

# Scan networks/devices
heckcheckos-wifi scan
heckcheckos-bluetooth scan

# Optimize performance
heckcheckos-driver-optimizer

# Launch Linux environment
heckcheckos-debian

# Get help
heckcheckos-help
```

## 🖥️ Desktop Commands

```bash
# Build specific version
sudo ./heckcheckos-build.sh
# Select: 1 (v1.0), 2 (v1.1), 3 (v2.0), or 4 (all)

# Create bootable USB
sudo dd if=$HOME/heckcheckos-ultimate/Heck-CheckOS-v2.0.iso of=/dev/sdX bs=4M status=progress

# Test in VM
qemu-system-x86_64 -enable-kvm -m 4096 -cdrom Heck-CheckOS-v2.0.iso
```

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License & Legal

**Heck-CheckOS build scripts and configuration** are licensed under the MIT License. See [LICENSE](LICENSE) file.

**Important Legal Information:**
- 📋 **Full Legal Compliance**: See [LEGAL_COMPLIANCE.md](LEGAL_COMPLIANCE.md)
- ⚖️ **Trademark Notice**: Not affiliated with Ghost Foundation
- 🔓 **Open Source**: Based on Debian 12 (Bookworm) and various open-source licenses
- 📦 **Third-Party Components**: All upstream packages retain their original licenses

**This is a derivative work based on:**
- **Debian 12 (Bookworm)** (Desktop) - Various open-source licenses
- **Debian GNU/Linux** - Various licenses
- **Termux** (Android) - GPLv3
- **proot** (Android) - GPL
- Numerous other open-source packages with individual licenses

**Disclaimer:** This project is NOT an official Debian release and is NOT endorsed by Debian. Build responsibly and respect all applicable licenses and trademark rights.

Please respect all applicable licenses and trademark rights.

## 🔗 Links

- **GitHub Repository**: https://github.com/jameshroop-art/GO-OS
- **Issues/Support**: https://github.com/jameshroop-art/GO-OS/issues
- **Debian**: https://www.debian.org
- **Kali Linux**: https://www.kali.org
- **Termux**: https://termux.com
- **F-Droid**: https://f-droid.org

## 🆘 Support

### Desktop Issues
See [GHOSTOS_BUILD_README.md](Go-OS/GHOSTOS_BUILD_README.md) troubleshooting section

### Android Issues
See [ANDROID_INSTALLATION.md](Go-OS/ANDROID_INSTALLATION.md) troubleshooting section

### General Support
- Check documentation first
- Search existing GitHub issues
- Create new issue with details:
  - Platform (Desktop/Android)
  - Version/Build
  - Error message
  - Steps to reproduce

## ⚠️ Important Notes

### Desktop/Server
- Building ISOs requires significant disk space and time
- Root access required for build process
- Test in VM before deploying to hardware
- ISOs are large (10-12GB) - use USB drives, not DVDs

### Android
- **NO ROOT REQUIRED** - works with standard permissions
- Install Termux from F-Droid, NOT Google Play
- Grant required permissions (Storage, Location)
- Some advanced features limited without root (by design)
- Driver "patching" = userspace optimization, not kernel modification

## 🎉 Version History

### Desktop
- **v2.0** (2025): Debian 12 base, Wayland, AI assistant, ARM support, plugin system
- **v1.1** (2025): Debian 12 base, Enhanced privacy, security tools, improved UI
- **v1.0** (2025): Initial stable release, Debian 12 (Bookworm) base with Heck-CheckOS GUI

### Android
- **v1.0-android** (2026-01): Initial Android release
  - Android 9+ support
  - Non-root WiFi/Bluetooth
  - Debian 12 (Bookworm) proot environment
  - Driver optimization tools

---

**Heck-CheckOS** - Security-focused, feature-rich operating system built on Debian 12 (Bookworm) with custom Heck-CheckOS GUI. For desktop and mobile platforms. Build it, customize it, own it. 👻🐧
