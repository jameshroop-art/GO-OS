# Parrot Security OS 7.0 ISO Download Guide

## ⚠️ Important Note

The Parrot Security OS 7.0 ISO is **approximately 8GB** and **cannot be stored on GitHub** due to file size limits (2GB maximum per file with Git LFS).

**Note:** The GhostOS build script uses `debootstrap` to download and create Parrot OS directly from official repositories. **You do NOT need to download the ISO to build GhostOS.**

**However, you may want to download the ISO if you:**
- Want to test Parrot Security OS before building GhostOS
- Need to install Parrot OS manually on a system
- Want a reference copy of the official Parrot Security distribution
- Need to create Parrot OS bootable media separately

---

## 📥 Download Options

### Option 1: Direct Download (Recommended)

```bash
# Navigate to your GO-OS directory
cd ~/GO-OS

# Download the ISO (8GB, may take time)
wget https://deb.parrot.sh/parrot/iso/7.0/Parrot-security-7.0_amd64.iso

# Or with resume capability if interrupted
wget -c https://deb.parrot.sh/parrot/iso/7.0/Parrot-security-7.0_amd64.iso
```

**Download Time Estimates:**
- 100 Mbps: ~10-15 minutes
- 50 Mbps: ~20-30 minutes
- 25 Mbps: ~40-60 minutes
- 10 Mbps: ~2 hours

### Option 2: Torrent Download (Better for slow connections)

Torrent downloads are more resilient and can be paused/resumed:

```bash
# Install BitTorrent client
sudo apt install transmission-cli

# Get torrent file from official Parrot website
# Visit: https://www.parrotsec.org/download/
# Download the .torrent file

# Start download
transmission-cli Parrot-security-7.0_amd64.iso.torrent
```

### Option 3: Official Website Manual Download

1. Visit: **https://www.parrotsec.org/download/**
2. Select: **Security Edition**
3. Architecture: **AMD64**
4. Click download and save to your GO-OS directory

---

## ✅ Verify Your Download

**CRITICAL: Always verify ISO integrity before use!**

### Step 1: Check File Size

```bash
ls -lh Parrot-security-7.0_amd64.iso
```

**Expected size:** Approximately 7.5-8.5 GB

If it shows 0 bytes or a very small size, the download failed - delete and re-download.

### Step 2: Verify File Type

```bash
file Parrot-security-7.0_amd64.iso
```

**Expected output:** `ISO 9660 CD-ROM filesystem data`

### Step 3: Verify SHA256 Checksum

```bash
sha256sum Parrot-security-7.0_amd64.iso
```

Compare the output with the official checksum from:
**https://www.parrotsec.org/download/**

### Automated Verification Script

Use the included verification script:

```bash
cd Go-OS
./verify-iso.sh ../Parrot-security-7.0_amd64.iso
```

This will automatically:
- Check file size
- Verify file type
- Validate checksum (if available)
- Confirm ISO is ready for GhostOS build

---

## 🚀 Using the ISO

Once your ISO is downloaded and verified, you can:

### Option 1: Test Parrot Security OS in a Virtual Machine

```bash
# Using QEMU
qemu-system-x86_64 -enable-kvm -m 4096 -cdrom Parrot-security-7.0_amd64.iso

# Using VirtualBox
# Create new VM and attach the ISO as optical drive
```

### Option 2: Create Bootable USB for Parrot OS

```bash
# Write ISO to USB drive (replace sdX with your USB device)
sudo dd if=Parrot-security-7.0_amd64.iso of=/dev/sdX bs=4M status=progress
sync
```

### Option 3: Continue with GhostOS Build

The GhostOS build script doesn't require the ISO - it uses `debootstrap` to download Parrot OS:

```bash
cd Go-OS
sudo ./ghostos-build.sh
# The script will download Parrot OS automatically from repositories
```

---

## 🐛 Troubleshooting

### Download Keeps Failing

**Use wget with resume:**
```bash
wget -c https://deb.parrot.sh/parrot/iso/7.0/Parrot-security-7.0_amd64.iso
```

The `-c` flag resumes interrupted downloads.

### File Shows as Empty (0 bytes)

Your download failed completely:

```bash
# Delete the broken file
rm Parrot-security-7.0_amd64.iso

# Re-download
wget https://deb.parrot.sh/parrot/iso/7.0/Parrot-security-7.0_amd64.iso
```

### Checksum Doesn't Match

**DO NOT USE THE ISO!** It may be corrupted or compromised.

```bash
# Delete the suspicious file
rm Parrot-security-7.0_amd64.iso

# Download from official source only
wget https://deb.parrot.sh/parrot/iso/7.0/Parrot-security-7.0_amd64.iso
```

### "Cannot stat" or "File not found" Error

The ISO is not in the expected location. Either:

**Option A:** Move it to the GO-OS root directory for testing/manual use:
```bash
cp /path/to/Parrot-security-7.0_amd64.iso ~/GO-OS/
```

**Option B:** Use the ISO for testing or manual installation:
```bash
# Test in VM
qemu-system-x86_64 -enable-kvm -m 4096 -cdrom /path/to/Parrot-security-7.0_amd64.iso

# Or create bootable USB
sudo dd if=/path/to/Parrot-security-7.0_amd64.iso of=/dev/sdX bs=4M status=progress
```

**Note:** The GhostOS build script downloads Parrot OS automatically via `debootstrap` and does not require the ISO file.

### ISO Won't Mount or Extract

The file is corrupted:
1. Delete the ISO
2. Re-download from official sources
3. Verify checksum before using

---

## 📊 Storage Requirements

### During Download
- **8GB** for the ISO file

### During Build
- **8GB** for the ISO (kept)
- **10-15GB** for extraction and customization
- **10-12GB** for the final GhostOS ISO
- **Total: 30-35GB free space recommended**

### After Build
You can optionally delete the original Parrot ISO to save space:
```bash
# After successful GhostOS build
rm Parrot-security-7.0_amd64.iso
```

Your custom GhostOS ISO will be in:
`$HOME/ghostos-ultimate/GhostOS-v*.iso`

---

## ⚠️ Security Notes

1. **Only download from official Parrot sources:**
   - https://www.parrotsec.org/download/
   - https://deb.parrot.sh/parrot/iso/

2. **Always verify checksums** - this protects against:
   - Corrupted downloads
   - Man-in-the-middle attacks
   - Compromised mirrors

3. **Never use an ISO with a mismatched checksum**

4. **Keep your ISO in a safe location** - it contains a clean base system

---

## 📚 Additional Resources

- [Parrot Security Official Site](https://www.parrotsec.org/)
- [GhostOS Build README](GHOSTOS_BUILD_README.md)
- [GhostOS Quick Reference](GHOSTOS_QUICK_REFERENCE.md)
- [FAQ](FAQ.md)

---

**Questions?** Open an issue: https://github.com/jameshroop-art/GO-OS/issues
