# GhostOS - Multi-Platform Operating System

Complete operating system distribution available for multiple platforms with advanced privacy features, driver support, and full customization.

## 🚀 Platforms

### 🐧 Desktop/Server (Linux ISO)
Full-featured **Parrot OS 7 Security**-based distribution with multiple versions:
- **v1.0 - Stable Release**: Complete base system with Parrot Security tools (~10GB)
- **v1.1 - Enhanced Edition**: Privacy-focused with Malwarebytes-style security (~11GB)
- **v2.0 - Next Generation**: Wayland, AI assistant, cloud backup, plugin system (~12GB)

**Base Operating System:** Parrot OS 7 Security Edition (Debian-based security-focused distribution)

**GhostOS Features:**
- ✅ BIOS/UEFI boot support
- ✅ AMD AM5/ASUS platform optimizations
- ✅ Gaming and AI/ML tools
- ✅ Enhanced privacy controls
- ✅ Security tools and hardening (Parrot + GhostOS)
- ✅ Custom GhostOS GUI and desktop environment

**Documentation:** See [`GHOSTOS_BUILD_README.md`](Go-OS/GHOSTOS_BUILD_README.md) and [`GHOSTOS_QUICK_REFERENCE.md`](Go-OS/GHOSTOS_QUICK_REFERENCE.md)

## 📥 Getting the Parrot Security OS ISO (Optional)

**Note:** The GhostOS build script uses `debootstrap` to download Parrot OS automatically from official repositories. **You do NOT need to download the ISO to build GhostOS.**

**However, you may want to download the Parrot Security OS 7.0 ISO (~8GB) if you:**
- Want to test Parrot Security OS before building GhostOS
- Need to manually install Parrot OS on a system
- Want a reference copy of the official Parrot distribution

**Due to GitHub's 2GB file size limit, the ISO cannot be stored in this repository.**

### Quick Download

```bash
cd ~/GO-OS
wget https://deb.parrot.sh/parrot/iso/7.0/Parrot-security-7.0_amd64.iso
```

### Verify Your Download

```bash
# Check file size (~8GB expected)
ls -lh Parrot-security-7.0_amd64.iso

# Verify it's a valid ISO
file Parrot-security-7.0_amd64.iso

# Verify checksum
sha256sum Parrot-security-7.0_amd64.iso
# Compare with official checksum from parrotsec.org
```

### Automated Verification

```bash
cd Go-OS
./verify-iso.sh ../Parrot-security-7.0_amd64.iso
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
wget https://raw.githubusercontent.com/jameshroop-art/GO-OS/main/Go-OS/ghostos-build.sh
chmod +x ghostos-build.sh
sudo ./ghostos-build.sh
```

Builds bootable ISO with:
- Parrot OS 7 Security Edition base
- GhostOS custom GUI and desktop environment
- Complete Linux system with security tools
- Hardware drivers (AMD, NVIDIA, Intel)
- Privacy and security tools (Parrot + GhostOS)
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
wget https://raw.githubusercontent.com/jameshroop-art/GO-OS/main/Go-OS/ghostos-android.sh
chmod +x ghostos-android.sh
bash ghostos-android.sh
source ~/.bashrc
ghostos
```

Installs:
- Parrot Security OS proot environment
- WiFi management tools (non-root)
- Bluetooth management tools (non-root)
- Driver optimization utilities
- Full Linux command-line tools

## 📚 Documentation

**👉 [Complete Documentation Index](Go-OS/DOCUMENTATION_INDEX.md)** - Full documentation listing

### Desktop/Server
- **[Build System README](Go-OS/GHOSTOS_BUILD_README.md)** - Complete build guide
- **[Quick Reference](Go-OS/GHOSTOS_QUICK_REFERENCE.md)** - Fast command reference
- **[Build Script](Go-OS/ghostos-build.sh)** - Main build script
- **[Files Report](Go-OS/GHOST_OS_FILES_REPORT.md)** - Project structure
- **[Security Notes](Go-OS/VERIFICATION_TOOL_SECURITY_NOTES.md)** - Security documentation

### Android
- **[Installation Guide](Go-OS/ANDROID_INSTALLATION.md)** - Complete setup instructions
- **[Quick Reference](Go-OS/ANDROID_QUICK_REFERENCE.md)** - Command cheat sheet
- **[Technical Details](Go-OS/ANDROID_TECHNICAL_DETAILS.md)** - Architecture and compatibility
- **[Install Script](Go-OS/ghostos-android.sh)** - Android installer

### General
- **[FAQ](Go-OS/FAQ.md)** - Frequently Asked Questions
- **[Architecture](Go-OS/ARCHITECTURE.md)** - System architecture and diagrams

## 🎯 Features Comparison

### Desktop/Server GhostOS

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

### Android GhostOS

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
- **Base OS**: Parrot OS 7 Security Edition (automatically bootstrapped)
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
ghostos-wifi status
ghostos-bluetooth status

# Scan networks/devices
ghostos-wifi scan
ghostos-bluetooth scan

# Optimize performance
ghostos-driver-optimizer

# Launch Linux environment
ghostos-debian

# Get help
ghostos-help
```

## 🖥️ Desktop Commands

```bash
# Build specific version
sudo ./ghostos-build.sh
# Select: 1 (v1.0), 2 (v1.1), 3 (v2.0), or 4 (all)

# Create bootable USB
sudo dd if=$HOME/ghostos-ultimate/GhostOS-v2.0.iso of=/dev/sdX bs=4M status=progress

# Test in VM
qemu-system-x86_64 -enable-kvm -m 4096 -cdrom GhostOS-v2.0.iso
```

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

GhostOS build system and Android tools are provided as-is for educational and development purposes.

Based on:
- **Parrot OS 7 Security Edition** (Desktop) - GPLv3 and various licenses
- **Debian GNU/Linux** - Various licenses (Parrot base)
- **Termux** (Android) - GPLv3
- **proot** (Android) - GPL
- Numerous open-source packages with individual licenses

Please respect all applicable licenses.

## 🔗 Links

- **GitHub Repository**: https://github.com/jameshroop-art/GO-OS
- **Issues/Support**: https://github.com/jameshroop-art/GO-OS/issues
- **Parrot Security**: https://www.parrotsec.org
- **Termux**: https://termux.com
- **F-Droid**: https://f-droid.org
- **Debian**: https://www.debian.org

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
- **v2.0** (2025): Parrot OS 7 base, Wayland, AI assistant, ARM support, plugin system
- **v1.1** (2025): Parrot OS 7 base, Enhanced privacy, security tools, improved UI
- **v1.0** (2025): Initial stable release, Parrot OS 7 Security base with GhostOS GUI

### Android
- **v1.0-android** (2026-01): Initial Android release
  - Android 9+ support
  - Non-root WiFi/Bluetooth
  - Parrot Security OS proot environment
  - Driver optimization tools

---

**GhostOS** - Security-focused, feature-rich operating system built on Parrot OS 7 Security Edition with custom GhostOS GUI. For desktop and mobile platforms. Build it, customize it, own it. 👻🦜
