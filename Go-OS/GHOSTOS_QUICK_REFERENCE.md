#GhostOS Build System - Quick Reference

**Base OS:** Parrot OS 7 Security Edition
**GUI:** GhostOS Custom Desktop Environment

## Quick Start

```bash
# 1. Make script executable
chmod +x ghostos-build.sh

# 2. Run as root
sudo ./ghostos-build.sh

# 3. Select version (1-4)
# 4. Choose whether to create bootable USB
# 5. Wait for build to complete
```

## Version Selection Quick Guide

| Option | Version | Features | ISO Size |
|--------|---------|----------|----------|
| 1 | v1.0 | Parrot OS 7 base, GhostOS GUI, core features | ~10GB |
| 2 | v1.1 | Parrot OS 7 base, enhanced privacy, Malwarebytes, improved UI | ~11GB |
| 3 | v2.0 | Parrot OS 7 base, Wayland, AI, cloud backup, plugins, ARM | ~12GB |
| 4 | All | Build all three versions | ~33GB total |

## Command Reference

### Build Specific Version
```bash
# v1.0 only
sudo ./ghostos-build.sh
# Then select option 1

# v1.1 only
sudo ./ghostos-build.sh
# Then select option 2

# v2.0 only
sudo ./ghostos-build.sh
# Then select option 3

# All versions
sudo ./ghostos-build.sh
# Then select option 4
```

### Create Bootable USB
```bash
# Manual method (after ISO is built)
sudo dd if=$HOME/ghostos-ultimate/GhostOS-v2.0.iso of=/dev/sdX bs=4M status=progress conv=fsync
sudo sync
```

### Verify ISO
```bash
cd $HOME/ghostos-ultimate
md5sum -c GhostOS-v2.0.iso.md5
sha256sum -c GhostOS-v2.0.iso.sha256
```

### Clean Build Directory
```bash
# Remove rootfs to force rebuild
sudo rm -rf $HOME/ghostos-ultimate/build/rootfs

# Remove everything
sudo rm -rf $HOME/ghostos-ultimate
```

## Output Locations

- **ISOs**: `$HOME/ghostos-ultimate/GhostOS-v*.iso`
- **Logs**: `$HOME/ghostos-ultimate/logs/install_v*.log`
- **Checksums**: `$HOME/ghostos-ultimate/GhostOS-v*.iso.{md5,sha256}`

## USB Device Detection

```bash
# List all block devices
lsblk

# List USB devices only
lsblk -d -o NAME,SIZE,TYPE,TRAN | grep usb

# Get detailed info about specific device
lsblk /dev/sdX
```

## System Requirements

- **OS**: Debian-based Linux (Debian, Ubuntu, Linux Mint, etc.)
- **RAM**: 8GB minimum, 16GB recommended
- **Disk**: 
  - v1.0: 50GB
  - v1.1: 60GB
  - v2.0: 70GB
  - All versions: 100GB+
- **Root**: Must run with sudo/root privileges

## Build Time Estimates

| Version | Typical Build Time* |
|---------|-------------------|
| v1.0 | 2-3 hours |
| v1.1 | 2.5-3.5 hours |
| v2.0 | 3-4 hours |
| All | 6-8 hours |

*Times vary based on CPU, disk speed, and internet connection

## Troubleshooting Quick Fixes

### Error: "Must run as root"
```bash
sudo ./ghostos-build.sh
```

### Error: Insufficient disk space
```bash
df -h $HOME
# Free up space or change PROJECT_DIR in script
```

### Error: Network issues during debootstrap
```bash
# Check internet connection
ping -c 4 deb.debian.org

# Try again - network issues are often temporary
sudo ./ghostos-build.sh
```

### Error: GRUB installation fails
```bash
sudo apt-get install grub-pc-bin grub-efi-amd64-bin
sudo ./ghostos-build.sh
```

### Script hangs or freezes
```bash
# Check logs in another terminal
tail -f $HOME/ghostos-ultimate/logs/install_v*.log

# If necessary, stop and restart
sudo pkill -f ghostos-build.sh
sudo ./ghostos-build.sh
```

## Feature Comparison Matrix

| Feature | v1.0 | v1.1 | v2.0 |
|---------|------|------|------|
| Base System | ✅ | ✅ | ✅ |
| BIOS/UEFI Boot | ✅ | ✅ | ✅ |
| Enhanced Privacy | ❌ | ✅ | ✅ |
| Malwarebytes Scanner | ❌ | ✅ | ✅ |
| Smooth Animations | ❌ | ✅ | ✅ |
| Wayland Support | ❌ | ❌ | ✅ |
| AI Assistant | ❌ | ❌ | ✅ |
| Cloud Backup | ❌ | ❌ | ✅ |
| Plugin System | ❌ | ❌ | ✅ |
| ARM Support | ❌ | ❌ | ✅ |

## Privacy Features by Version

### v1.0
- Basic privacy configuration

### v1.1
- Extended telemetry blocking
- DNS privacy (Unbound + Cloudflare)
- MAC address randomization
- UFW firewall hardening

### v2.0
- All v1.1 features plus:
- Kernel hardening (sysctl)
- AppArmor enforcement
- IPv6 disabled
- Advanced BPF restrictions

## Customization

### Add Custom Packages

1. Stop script after it generates installation scripts
2. Edit `$HOME/ghostos-ultimate/build/install_v*.sh`
3. Add packages to `apt-get install -y` lines
4. Re-run build script

### Change ISO Name

Edit the script line:
```bash
ISO_OUTPUT="$PROJECT_DIR/GhostOS-v${VERSION}.iso"
```

To:
```bash
ISO_OUTPUT="$PROJECT_DIR/MyCustomOS-v${VERSION}.iso"
```

### Change Build Directory

Edit the script line:
```bash
PROJECT_DIR="$HOME/ghostos-ultimate"
```

To:
```bash
PROJECT_DIR="/path/to/your/build/directory"
```

## Testing ISOs

### QEMU (Quick Test)
```bash
qemu-system-x86_64 -enable-kvm -m 4096 -cdrom GhostOS-v2.0.iso
```

### VirtualBox (Full Test)
```bash
VBoxManage createvm --name "GhostOS-Test" --ostype "Debian_64" --register
VBoxManage modifyvm "GhostOS-Test" --memory 4096 --vram 128
VBoxManage storagectl "GhostOS-Test" --name "IDE" --add ide
VBoxManage storageattach "GhostOS-Test" --storagectl "IDE" --port 0 --device 0 --type dvddrive --medium GhostOS-v2.0.iso
VBoxManage startvm "GhostOS-Test"
```

## Common Use Cases

### Build for Daily Use (Recommended: v1.1)
```bash
sudo ./ghostos-build.sh
# Select: 2 (v1.1)
# USB: yes (if available)
```

### Build for Development (Recommended: v2.0)
```bash
sudo ./ghostos-build.sh
# Select: 3 (v2.0)
# USB: yes (if available)
```

### Build for Testing/Comparison (All versions)
```bash
sudo ./ghostos-build.sh
# Select: 4 (All versions)
# USB: yes (for last built version)
```

### Build for Offline Distribution
```bash
# Build the ISO
sudo ./ghostos-build.sh

# Create multiple USB drives
for i in 1 2 3; do
    echo "Insert USB drive $i and press Enter"
    read
    sudo dd if=$HOME/ghostos-ultimate/GhostOS-v2.0.iso of=/dev/sdX bs=4M status=progress
    sudo sync
    echo "USB $i complete"
done
```

## Safety Checklist

Before running the build:
- [ ] Running on a Debian-based system
- [ ] Have sufficient disk space (check with `df -h`)
- [ ] Have stable internet connection
- [ ] Have 2-4 hours of available time
- [ ] Running with sudo/root privileges

Before creating USB:
- [ ] USB drive is backed up (will be erased!)
- [ ] Verified correct device name with `lsblk`
- [ ] USB drive has sufficient capacity (16GB+ for v1.0/v1.1, 32GB+ for v2.0)
- [ ] Ready to type 'YES' to confirm (case-sensitive)

## Additional Resources

- Full documentation: `GHOSTOS_BUILD_README.md`
- Script source: `ghostos-build.sh`
- Project repository: https://github.com/jameshroop-art/Experimental-UI

---

**Remember**: Always verify the ISO with checksums before deploying to production or creating multiple USB copies!
