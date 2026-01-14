# HeckOS Build Guide

## Safe Build Process

To build HeckOS without breaking linked files, use the safe build wrapper:

```bash
cd Go-OS
sudo bash build-heckos.sh
```

This wrapper:
- ✓ Backs up all symbolic links before build
- ✓ Protects linked files during build process
- ✓ Verifies links after build completion
- ✓ Provides link restoration info if needed

## Quick Build Commands

### Standard Build
```bash
cd Go-OS
sudo bash build-heckos.sh
```

### Build Specific Version
```bash
# The script will prompt you to select:
# 1) HeckOS v1.0 - Stable Release (~10GB)
# 2) HeckOS v1.1 - Enhanced Edition (~11GB)
# 3) HeckOS v2.0 - Next Generation (~12GB)
# 4) Build ALL versions
```

## Build Requirements

### System Requirements
- **OS**: Debian-based Linux (for building)
- **RAM**: 8GB minimum, 16GB recommended
- **Disk Space**: 50-100GB free
- **Root Access**: Required (`sudo`)
- **Architecture**: x86_64

### Required Packages
Automatically installed by build script:
- debootstrap
- squashfs-tools
- xorriso
- grub-pc-bin
- grub-efi-amd64-bin
- mtools
- dosfstools
- isolinux
- syslinux

## Build Output

### ISO Files Location
```bash
~/heckos-ultimate/HeckOS-v1.0.iso
~/heckos-ultimate/HeckOS-v1.1.iso
~/heckos-ultimate/HeckOS-v2.0.iso
```

### Build Logs
```bash
~/heckos-ultimate/build/build.log
```

## Testing Your Build

### Test in Virtual Machine (QEMU)
```bash
# Test v2.0 ISO
qemu-system-x86_64 \
    -enable-kvm \
    -m 4096 \
    -cdrom ~/heckos-ultimate/HeckOS-v2.0.iso \
    -boot d
```

### Test in VirtualBox
1. Create new VM
2. Select Linux, Debian 64-bit
3. Allocate 4GB RAM, 32GB disk
4. Attach ISO to optical drive
5. Boot and test

### Create Bootable USB
```bash
cd Go-OS
sudo bash ghostos-installation-setup.sh
# Select: Bootable USB option
```

## Preventing Broken Links

### What the Safe Build Does

1. **Pre-Build Check**
   - Scans repository for all symbolic links
   - Creates registry of link paths and targets
   - Saves to `/tmp/heckos-link-backup-*/`

2. **During Build**
   - Sets `HECKOS_BUILD_SAFE_MODE=1`
   - Sets `HECKOS_PRESERVE_LINKS=1`
   - Build operates in isolated directory

3. **Post-Build Verification**
   - Checks all registered links
   - Reports any broken links
   - Provides restoration information

### Manual Link Verification

If you need to verify links manually:

```bash
# Find all symbolic links
find /home/runner/work/GO-OS/GO-OS -type l

# Check for broken links
find /home/runner/work/GO-OS/GO-OS -type l ! -exec test -e {} \; -print

# View link target
readlink /path/to/link
ls -l /path/to/link
```

### Restoring Broken Links

If a link breaks during build:

```bash
# Check the backup registry
cat /tmp/heckos-link-backup-*/link-registry.txt

# Manually restore a link
ln -sf /path/to/target /path/to/link
```

## Build Process Details

### What Happens During Build

1. **Preparation**
   - Install build dependencies
   - Create build directories
   - Set up build environment

2. **Base System**
   - Bootstrap Debian 12 (Bookworm) with debootstrap
   - Install core packages
   - Configure base system

3. **Desktop Environment**
   - Install HeckOS custom GUI
   - Configure MATE/XFCE/KDE (based on version)
   - Set up themes and icons

4. **Hardware Support**
   - AMD AM5 drivers
   - NVIDIA proprietary drivers
   - Intel graphics drivers
   - USB4/Thunderbolt support

5. **Software Installation**
   - Development tools
   - Gaming support (Steam, Lutris)
   - Privacy tools
   - Security tools (based on version)

6. **System Configuration**
   - Network setup (NetworkManager)
   - Power management
   - User configuration
   - Boot configuration (GRUB)

7. **ISO Creation**
   - Compress rootfs with squashfs
   - Create ISO filesystem
   - Add bootloader (GRUB)
   - Make ISO hybrid (USB bootable)

8. **USB Creation** (optional)
   - Write ISO to USB drive
   - Make USB bootable
   - Verify USB integrity

## Troubleshooting

### Build Fails

**Check disk space:**
```bash
df -h
# Need 50GB+ free in /home
```

**Check build log:**
```bash
tail -100 ~/heckos-ultimate/build/build.log
```

**Clean and retry:**
```bash
rm -rf ~/heckos-ultimate/build
sudo bash build-heckos.sh
```

### Broken Links After Build

**View backup registry:**
```bash
ls /tmp/heckos-link-backup-*/
cat /tmp/heckos-link-backup-*/link-registry.txt
```

**Restore links:**
```bash
# From registry:
# /path/to/link -> /path/to/target
ln -sf /path/to/target /path/to/link
```

### Permission Errors

**Ensure running as root:**
```bash
sudo bash build-heckos.sh
```

**Check file permissions:**
```bash
ls -la Go-OS/build-heckos.sh
# Should show: -rwxr-xr-x
```

### Debootstrap Fails

**Update package lists:**
```bash
sudo apt-get update
sudo apt-get install debootstrap
```

**Check mirror availability:**
```bash
ping deb.debian.org
# If fails, edit /etc/apt/sources.list to use different mirror
```

### Out of Memory

**Increase swap:**
```bash
sudo fallocate -l 8G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

**Or build with less RAM:**
Edit `ghostos-build.sh` and reduce package set

## Build Time Estimates

- **v1.0**: ~20-30 minutes (fast system)
- **v1.1**: ~30-40 minutes
- **v2.0**: ~40-60 minutes
- **All versions**: ~90-120 minutes

Time varies based on:
- CPU speed
- Disk I/O (SSD vs HDD)
- Internet connection (package downloads)
- RAM available

## After Build

### Verify ISO

```bash
# Check ISO file
file ~/heckos-ultimate/HeckOS-v2.0.iso
# Should show: ISO 9660 CD-ROM filesystem

# Check size
ls -lh ~/heckos-ultimate/*.iso

# Verify bootable
fdisk -l ~/heckos-ultimate/HeckOS-v2.0.iso
```

### Distribution

**Create checksums:**
```bash
cd ~/heckos-ultimate
sha256sum HeckOS-*.iso > SHA256SUMS
md5sum HeckOS-*.iso > MD5SUMS
```

**Compress for sharing:**
```bash
# Optional: compress ISO
xz -9 -T0 HeckOS-v2.0.iso
# Creates: HeckOS-v2.0.iso.xz (smaller for download)
```

## Next Steps

1. **Test ISO**: Boot in VM
2. **Create USB**: Use installation setup GUI
3. **Install**: Boot from USB and run installer
4. **Customize**: Use ISO Builder for further customization

## Additional Resources

- **Build System Details**: `GHOSTOS_BUILD_README.md`
- **Installation Guide**: `INSTALLATION_SETUP_GUIDE.md`
- **ISO Customization**: `gui/ghostos-iso-builder/README.md`
- **Troubleshooting**: `FAQ.md`

---

**Safe Building!** 🛡️

Always use `build-heckos.sh` to protect your repository's symbolic links during the build process.
