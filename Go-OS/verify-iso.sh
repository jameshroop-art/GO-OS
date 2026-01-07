#!/bin/bash
# ============================================
# Heck-CheckOS ISO Verification Script
# Verifies Debian 12 ISO integrity before using
# ============================================
# LICENSE: MIT (see LICENSE file in repository root)
# 
# LEGAL NOTICE:
# This script is part of Heck-CheckOS, a derivative work based on Debian 12.
# NOT an official Debian release. See LEGAL_COMPLIANCE.md.
# ============================================

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

ISO_PATH="$1"
EXPECTED_SIZE_MIN=500000000   # ~500MB minimum (netinst)
EXPECTED_SIZE_MAX=5000000000  # ~5GB maximum (full DVD)

echo "=========================================="
echo "  Heck-CheckOS ISO Verification Tool"
echo "=========================================="
echo ""

# Check dependencies
if ! command -v bc &> /dev/null; then
    echo -e "${YELLOW}Warning: 'bc' not found. Installing...${NC}"
    if command -v apt-get &> /dev/null; then
        sudo apt-get install -y bc
    elif command -v dnf &> /dev/null; then
        sudo dnf install -y bc
    elif command -v yum &> /dev/null; then
        sudo yum install -y bc
    elif command -v pacman &> /dev/null; then
        sudo pacman -S --noconfirm bc
    elif command -v zypper &> /dev/null; then
        sudo zypper install -y bc
    else
        echo -e "${RED}Error: Cannot install bc. Please install it manually.${NC}"
        echo "  Debian/Ubuntu: sudo apt-get install bc"
        echo "  Fedora: sudo dnf install bc"
        echo "  RHEL/CentOS: sudo yum install bc"
        echo "  Arch: sudo pacman -S bc"
        echo "  openSUSE: sudo zypper install bc"
        exit 1
    fi
fi

# Check if ISO path provided
if [ -z "$ISO_PATH" ]; then
    echo -e "${RED}Error: No ISO file specified${NC}"
    echo "Usage: $0 /path/to/debian-12.8.0-amd64-netinst.iso"
    exit 1
fi

# Check if file exists
if [ ! -f "$ISO_PATH" ]; then
    echo -e "${RED}Error: ISO file not found: $ISO_PATH${NC}"
    echo ""
    echo "Please download the ISO first:"
    echo "  wget https://cdimage.debian.org/debian-cd/current/amd64/iso-cd/debian-12.8.0-amd64-netinst.iso"
    exit 1
fi

echo -e "${YELLOW}Verifying: $ISO_PATH${NC}"
echo ""

# Check 1: File Size
echo "[1/3] Checking file size..."

# Try GNU stat first (Linux), then BSD stat (macOS), with error handling
if ISO_SIZE=$(stat -c%s "$ISO_PATH" 2>/dev/null); then
    # GNU stat (Linux)
    :
elif ISO_SIZE=$(stat -f%z "$ISO_PATH" 2>/dev/null); then
    # BSD stat (macOS)
    :
else
    echo -e "${RED}✗ FAIL: Cannot determine file size${NC}"
    echo "  Your system's stat command is not supported"
    echo "  Please check the file manually with: ls -lh $ISO_PATH"
    exit 1
fi

ISO_SIZE_GB=$(echo "scale=2; $ISO_SIZE / 1024 / 1024 / 1024" | bc)

if [ "$ISO_SIZE" -lt "$EXPECTED_SIZE_MIN" ]; then
    echo -e "${RED}✗ FAIL: File too small ($ISO_SIZE_GB GB)${NC}"
    echo "  Expected: ~7-9 GB"
    echo "  The download may have failed or been interrupted"
    exit 1
elif [ "$ISO_SIZE" -gt "$EXPECTED_SIZE_MAX" ]; then
    echo -e "${YELLOW}⚠ WARNING: File larger than expected ($ISO_SIZE_GB GB)${NC}"
    echo "  This may be a newer version"
else
    echo -e "${GREEN}✓ PASS: File size OK ($ISO_SIZE_GB GB)${NC}"
fi

# Check 2: File Type
echo "[2/3] Checking file type..."
FILE_TYPE=$(file -b "$ISO_PATH")

if echo "$FILE_TYPE" | grep -qi "ISO 9660"; then
    echo -e "${GREEN}✓ PASS: Valid ISO 9660 filesystem${NC}"
elif echo "$FILE_TYPE" | grep -qi "empty"; then
    echo -e "${RED}✗ FAIL: File is empty${NC}"
    echo "  The download failed completely"
    echo "  Delete the file and re-download"
    exit 1
else
    echo -e "${RED}✗ FAIL: Not a valid ISO file${NC}"
    echo "  Detected type: $FILE_TYPE"
    exit 1
fi

# Check 3: SHA256 Checksum
echo "[3/3] Calculating SHA256 checksum..."
echo "  (This may take a minute for an 8GB file...)"
echo ""

ACTUAL_SHA256=$(sha256sum "$ISO_PATH" | awk '{print $1}')

echo "  Calculated SHA256: $ACTUAL_SHA256"
echo ""
echo -e "${YELLOW}⚠ IMPORTANT: Manual checksum verification required${NC}"
echo ""
echo "  Visit the official Debian download page to get the expected checksum:"
echo "  https://www.debian.org/CD/verify"
echo ""
echo "  Compare the checksum above with the official one."
echo "  If they match, your ISO is authentic and uncorrupted."
echo "  If they DON'T match, DELETE the file and re-download from official sources."
echo ""

# Summary
echo "=========================================="
echo "  Verification Summary"
echo "=========================================="
echo -e "File: ${GREEN}$ISO_PATH${NC}"
echo -e "Size: ${GREEN}$ISO_SIZE_GB GB${NC}"
echo -e "Type: ${GREEN}ISO 9660${NC}"
echo "SHA256: $ACTUAL_SHA256"
echo ""
echo -e "${GREEN}✓ Basic checks passed${NC}"
echo -e "${YELLOW}⚠ Please verify checksum manually before using${NC}"
echo ""
echo "You can now use the ISO to:"
echo "  • Test Debian 12 in a VM"
echo "  • Create a bootable USB for Debian 12 installation"
echo "  • Keep as a reference for the official Debian distribution"
echo ""
echo "Note: The Heck-CheckOS build script (heckcheckos-build.sh) downloads"
echo "Debian 12 automatically via debootstrap and doesn't require the ISO."
echo ""
