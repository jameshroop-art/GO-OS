# GhostOS Build System

A complete build system for creating GhostOS Linux distribution ISOs built on Debian 12 (Bookworm) with custom GhostOS GUI and settings, featuring multiple version support and bootable USB creation.

## Overview

The GhostOS Build System allows you to build custom Linux distributions with advanced features including:

- **Version 1.0 (Stable Release)**: Debian 12 (Bookworm) base with GhostOS GUI and core features (~10GB ISO)
- **Version 1.1 (Enhanced Edition)**: Improved UI with smooth animations, enhanced privacy controls, Malwarebytes-style security scanner, and system consolidation (~11GB ISO)
- **Version 2.0 (Next Generation)**: Modern Wayland support, AI assistant integration, advanced UI with blur effects, encrypted cloud backup, plugin system, and ARM architecture support (~12GB ISO)

## Features

### All Versions Include:
- **Debian 12 (Bookworm) base** (Bookworm codename)
- **GhostOS Custom GUI** and desktop environment
- Kali Security tools (penetration testing, forensics, etc.)
- Complete offline installation capability
- BIOS and UEFI boot support
- Hybrid ISO (can be written to USB)
- MD5 and SHA256 checksums

### Version-Specific Features:

#### v1.0 - Stable Release
- Debian 12 (Bookworm) base system
- GhostOS custom GUI and settings
- Complete base system
- All core features
- Kernel and drivers (AMD, NVIDIA)
- Gaming support
- AI/ML tools
- Security tools (Parrot + GhostOS)

#### v1.1 - Enhanced Edition
All v1.0 features plus:
- **Enhanced Privacy**: Extended telemetry blocking (Microsoft, Google, Facebook, Amazon, Adobe, Nvidia)
- **DNS Privacy**: Unbound DNS with Cloudflare DNS forwarding
- **MAC Address Randomization**: Network privacy protection
- **Firewall Hardening**: UFW with secure defaults
- **Malwarebytes-style Scanner**: ClamAV + rkhunter wrapper
- **Improved UI**: Picom compositor with smooth animations and blur effects
- **Better Themes**: Arc, Papirus, Numix, Breeze
- **System Consolidation**: Optimized services and log management

#### v2.0 - Next Generation
All v1.1 features plus:
- **Wayland Support**: Modern compositor (Sway) with waybar, wofi, mako
- **AI Assistant**: Local LLM with Ollama (Mistral 7B)
- **Advanced UI**: Kvantum theme engine, enhanced blur effects, modern animations
- **Encrypted Cloud Backup**: rclone + encfs for secure backups
- **Plugin System**: Extensible plugin manager
- **ARM Support**: Cross-compilation tools and QEMU emulation
- **Advanced Privacy**: Kernel hardening, AppArmor enforcement
- **Modern GTK Theme**: Custom GhostOS v2.0 theme with gradients and effects

## Requirements

### System Requirements:
- **Build Operating System**: Debian-based Linux (Debian, Ubuntu, etc.)
- **Target Operating System**: Debian 12 (Bookworm) (automatically bootstrapped)
- **RAM**: 8GB minimum, 16GB recommended
- **Disk Space**: 
  - 50GB for building v1.0
  - 60GB for building v1.1
  - 70GB for building v2.0
  - 100GB+ for building all versions
- **Privileges**: Must run as root (sudo)

### Software Dependencies (installed automatically):
- debootstrap (for Debian 12 bootstrap)
- squashfs-tools
- xorriso
- grub-pc-bin
- grub-efi-amd64-bin
- mtools
- dosfstools
- isolinux
- syslinux
- git, wget, curl, rsync

## Usage

### Basic Usage

1. **Download the script**:
   ```bash
   wget https://raw.githubusercontent.com/jameshroop-art/Experimental-UI/main/ghostos-build.sh
   chmod +x ghostos-build.sh
   ```

2. **Run as root**:
   ```bash
   sudo ./ghostos-build.sh
   ```

3. **Select version**:
   - Choose option 1 for v1.0 only
   - Choose option 2 for v1.1 only
   - Choose option 3 for v2.0 only
   - Choose option 4 to build all versions

4. **USB Creation (optional)**:
   - If USB drives are detected, you'll be prompted to create a bootable USB
   - Confirm the device to ensure you don't erase the wrong drive
   - Type 'YES' to confirm (case-sensitive)

### Example Session

```bash
$ sudo ./ghostos-build.sh

========================================
  👻 GhostOS Build System
  Multi-Version Builder
========================================

Select GhostOS version to build:

  1) GhostOS v1.0 - Stable Release
     • Complete base system
     • All core features
     • ~10GB ISO

  2) GhostOS v1.1 - Enhanced Edition
     • Improved UI (smooth animations)
     • Enhanced privacy controls
     • Malwarebytes Premium
     • System consolidation
     • ~11GB ISO

  3) GhostOS v2.0 - Next Generation
     • Modern Wayland support
     • AI assistant integration
     • Advanced UI (blur effects, transitions)
     • Cloud backup (encrypted)
     • Plugin system
     • ARM architecture support
     • ~12GB ISO

  4) Build ALL versions

Enter choice [1-4]: 2

Detecting USB drives...

Available USB drives:
NAME   SIZE   TYPE TRAN  MODEL
sdb    32G    disk usb   SanDisk Ultra

Create bootable USB after build? (yes/no): yes
Enter USB drive (e.g., sdb): sdb

⚠️  WARNING: /dev/sdb will be ERASED!
NAME   SIZE   TYPE TRAN  MODEL
sdb    32G    disk usb   SanDisk Ultra

Type 'YES' to confirm: YES

[*] Installing build dependencies...
...
```

## Output

### ISO Files
ISOs are created in `$HOME/ghostos-ultimate/`:
- `GhostOS-v1.0.iso` (≈10GB)
- `GhostOS-v1.1.iso` (≈11GB)
- `GhostOS-v2.0.iso` (≈12GB)

Each ISO includes:
- `.md5` checksum file
- `.sha256` checksum file

### Log Files
Build logs are stored in `$HOME/ghostos-ultimate/logs/`:
- `install_v1.0.log`
- `install_v1.1.log`
- `install_v2.0.log`

### Directory Structure
```
$HOME/ghostos-ultimate/
├── build/
│   ├── iso/                    # ISO staging directory
│   │   ├── boot/grub/         # GRUB bootloader
│   │   ├── EFI/BOOT/          # UEFI boot files
│   │   └── live/              # Live system files
│   ├── rootfs/                # Root filesystem
│   ├── install_v1.0.sh        # v1.0 installation script
│   ├── install_v1.1.sh        # v1.1 installation script
│   └── install_v2.0.sh        # v2.0 installation script
├── downloads/                 # Downloaded packages
├── logs/                      # Build logs
├── GhostOS-v1.0.iso
├── GhostOS-v1.0.iso.md5
├── GhostOS-v1.0.iso.sha256
├── GhostOS-v1.1.iso
├── GhostOS-v1.1.iso.md5
├── GhostOS-v1.1.iso.sha256
├── GhostOS-v2.0.iso
├── GhostOS-v2.0.iso.md5
└── GhostOS-v2.0.iso.sha256
```

## Bootable USB Creation

The script can automatically create bootable USB drives using the generated ISOs.

### Manual USB Creation

If you want to create a bootable USB manually:

```bash
# Find your USB device
lsblk

# Write ISO to USB (replace sdX with your device)
sudo dd if=$HOME/ghostos-ultimate/GhostOS-v2.0.iso of=/dev/sdX bs=4M status=progress conv=fsync
sudo sync
```

**⚠️ WARNING**: Double-check your device name! Writing to the wrong device will erase it permanently.

## Verification

### Verify ISO Integrity

```bash
# MD5 checksum
md5sum -c GhostOS-v2.0.iso.md5

# SHA256 checksum
sha256sum -c GhostOS-v2.0.iso.sha256
```

### Test ISO in Virtual Machine

Before burning to USB, test the ISO in a virtual machine:

```bash
# Using QEMU
qemu-system-x86_64 -enable-kvm -m 4096 -cdrom GhostOS-v2.0.iso

# Using VirtualBox
VBoxManage createvm --name "GhostOS-Test" --ostype "Debian_64" --register
VBoxManage modifyvm "GhostOS-Test" --memory 4096 --vram 128
VBoxManage storagectl "GhostOS-Test" --name "IDE" --add ide
VBoxManage storageattach "GhostOS-Test" --storagectl "IDE" --port 0 --device 0 --type dvddrive --medium GhostOS-v2.0.iso
VBoxManage startvm "GhostOS-Test"
```

## Troubleshooting

### Common Issues

1. **"Must run as root" error**
   - Solution: Run with `sudo ./ghostos-build.sh`

2. **Insufficient disk space**
   - Check available space: `df -h $HOME`
   - Solution: Free up space or use a different directory

3. **Debootstrap fails**
   - Check internet connection
   - Try a different Debian mirror
   - Solution: Edit the debootstrap line in the script

4. **GRUB installation fails**
   - Ensure grub packages are installed
   - Solution: `sudo apt-get install grub-pc-bin grub-efi-amd64-bin`

5. **ISO too large for DVD**
   - GhostOS ISOs are designed for USB, not DVD
   - Solution: Use USB drive (16GB+ for v1.0, 32GB+ for v2.0)

### Debug Mode

To enable verbose output, add `set -x` to the script:

```bash
#!/bin/bash
set -e
set -x  # Enable debug mode
```

### Clean Build

To start fresh:

```bash
sudo rm -rf $HOME/ghostos-ultimate/build/rootfs
```

This will force a complete rebuild on the next run.

## Security Considerations

### Privacy Features

All versions include privacy-focused configurations:
- Telemetry blocking (v1.1+)
- DNS privacy with Cloudflare (v1.1+)
- MAC address randomization (v1.1+)
- Kernel hardening (v2.0+)
- AppArmor enforcement (v2.0+)

### Security Tools

- **v1.0+**: Basic firewall, security updates
- **v1.1+**: ClamAV antivirus, rkhunter, chkrootkit, UFW firewall
- **v2.0+**: Enhanced kernel security, AppArmor, advanced privacy controls

### Offline Operation

GhostOS is designed for offline operation after build:
- No telemetry or phone-home features
- Local AI models (v2.0+)
- Encrypted local backups (v2.0+)

## Advanced Usage

### Customization

Edit the installation scripts before building:

1. Run the script once to generate installation scripts
2. Stop the build (Ctrl+C) after script generation
3. Edit `$HOME/ghostos-ultimate/build/install_v*.sh`
4. Re-run the build script

### Custom Packages

Add packages to the installation scripts:

```bash
# In the installation script, add to apt-get install
apt-get install -y \
    your-package-here \
    another-package
```

### Multiple Builds

Build different configurations in parallel by using different PROJECT_DIR values:

```bash
# Edit the script
PROJECT_DIR="$HOME/ghostos-privacy"  # For privacy-focused build
PROJECT_DIR="$HOME/ghostos-gaming"   # For gaming-focused build
```

## Contributing

Contributions are welcome! Please submit issues and pull requests to:
https://github.com/jameshroop-art/Experimental-UI

## License

This build system is provided as-is for educational and development purposes.

GhostOS and its components are based on Debian GNU/Linux and include numerous open-source packages, each with their own licenses. Please respect all applicable licenses.

## Credits

- **Base System**: Debian GNU/Linux
- **Build Tools**: debootstrap, squashfs-tools, xorriso, GRUB
- **Compositor**: Picom (v1.1+), Sway (v2.0+)
- **AI Assistant**: Ollama (v2.0+)
- **Security Tools**: ClamAV, rkhunter, UFW, AppArmor

## Support

For issues, questions, or suggestions:
- GitHub Issues: https://github.com/jameshroop-art/Experimental-UI/issues
- Documentation: https://github.com/jameshroop-art/Experimental-UI

---

**Note**: This is a comprehensive build system that creates large ISOs. Ensure you have sufficient disk space, time, and bandwidth before starting a build. Building all three versions can take several hours depending on your system and internet connection.
