#!/bin/bash
# GhostOS ISO Verification Script
# Verifies Parrot Security OS ISO integrity before using

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

ISO_PATH="$1"
EXPECTED_SIZE_MIN=7000000000  # ~7GB minimum
EXPECTED_SIZE_MAX=9000000000  # ~9GB maximum

echo "=========================================="
echo "  GhostOS ISO Verification Tool"
echo "=========================================="
echo ""

# Check dependencies
if ! command -v bc &> /dev/null; then
    echo -e "${YELLOW}Warning: 'bc' not found. Installing...${NC}"
    if command -v apt-get &> /dev/null; then
        sudo apt-get install -y bc
    elif command -v yum &> /dev/null; then
        sudo yum install -y bc
    else
        echo -e "${RED}Error: Cannot install bc. Please install it manually.${NC}"
        echo "  Debian/Ubuntu: sudo apt-get install bc"
        echo "  RHEL/CentOS: sudo yum install bc"
        exit 1
    fi
fi

# Check if ISO path provided
if [ -z "$ISO_PATH" ]; then
    echo -e "${RED}Error: No ISO file specified${NC}"
    echo "Usage: $0 /path/to/Parrot-security-7.0_amd64.iso"
    exit 1
fi

# Check if file exists
if [ ! -f "$ISO_PATH" ]; then
    echo -e "${RED}Error: ISO file not found: $ISO_PATH${NC}"
    echo ""
    echo "Please download the ISO first:"
    echo "  wget https://deb.parrot.sh/parrot/iso/7.0/Parrot-security-7.0_amd64.iso"
    exit 1
fi

echo -e "${YELLOW}Verifying: $ISO_PATH${NC}"
echo ""

# Check 1: File Size
echo "[1/3] Checking file size..."
ISO_SIZE=$(stat -c%s "$ISO_PATH" 2>/dev/null || stat -f%z "$ISO_PATH" 2>/dev/null)
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
echo "  Visit the official Parrot download page to get the expected checksum:"
echo "  https://www.parrotsec.org/download/"
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
echo "  • Test Parrot Security OS in a VM"
echo "  • Create a bootable USB for Parrot OS installation"
echo "  • Keep as a reference for the official Parrot distribution"
echo ""
echo "Note: The GhostOS build script (ghostos-build.sh) downloads"
echo "Parrot OS automatically via debootstrap and doesn't require the ISO."
echo ""
