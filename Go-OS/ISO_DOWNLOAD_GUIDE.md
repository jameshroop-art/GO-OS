# Parrot Security OS 7.0 ISO Download Guide

## ⚠️ Important: Large File Warning

The Parrot Security OS 7.0 ISO is **approximately 8GB** and **cannot be stored on GitHub** due to file size limits (2GB maximum per file with Git LFS).

**You MUST download the ISO separately before building GhostOS.**

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

## 🚀 After Download & Verification

Once your ISO is downloaded and verified:

```bash
cd Go-OS

# Run the GhostOS build script
sudo ./ghostos-build.sh ../Parrot-security-7.0_amd64.iso

# Or if ISO is in the same directory
sudo ./ghostos-build.sh Parrot-security-7.0_amd64.iso
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

**Option A:** Move it to the GO-OS root directory:
```bash
cp /path/to/Parrot-security-7.0_amd64.iso ~/GO-OS/
```

**Option B:** Provide the full path to the build script:
```bash
sudo ./ghostos-build.sh /path/to/Parrot-security-7.0_amd64.iso
```

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
