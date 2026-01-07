# Debian 12 (Bookworm) ISO Download Guide

## ⚠️ Important Note

The Debian 12 ISO is available in different sizes and **cannot be stored on GitHub** due to file size limits (2GB maximum per file with Git LFS).

**Note:** The Heck-CheckOS build script uses `debootstrap` to download and create Debian 12 directly from official repositories. **You do NOT need to download the ISO to build Heck-CheckOS.**

**However, you may want to download the ISO if you:**
- Want to test Debian 12 before building Heck-CheckOS
- Need to install Debian 12 manually on a system
- Want a reference copy of the official Debian distribution
- Need to create Debian 12 bootable media separately

---

## 📥 Download Options

### Option 1: Direct Download (Recommended)

#### Netinst ISO (~600MB) - Recommended for most users
```bash
cd ~/GO-OS
wget https://cdimage.debian.org/debian-cd/current/amd64/iso-cd/debian-12.8.0-amd64-netinst.iso
```

**Note:** The Heck-CheckOS build script (`heckcheckos-build.sh`) downloads Debian 12 automatically via `debootstrap` and does not require the ISO file.
