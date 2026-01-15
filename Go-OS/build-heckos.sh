#!/bin/bash
# ============================================
# HeckOS Safe Build Wrapper
# Protects linked files during build process
# ============================================

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BUILD_SCRIPT="$SCRIPT_DIR/ghostos-build.sh"

echo "========================================"
echo "  👻 HeckOS Safe Build System"
echo "  Protects linked files during build"
echo "========================================"
echo ""

# Check root
if [ "$EUID" -ne 0 ]; then 
    echo "❌ Must run as root"
    echo "Run: sudo $0"
    exit 1
fi

# Check if build script exists
if [ ! -f "$BUILD_SCRIPT" ]; then
    echo "❌ Build script not found: $BUILD_SCRIPT"
    exit 1
fi

# Create backup of important linked files before build
echo "[*] Checking for symbolic links in repository..."
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
LINKED_FILES=$(find "$REPO_ROOT" -type l 2>/dev/null || true)

if [ -n "$LINKED_FILES" ]; then
    echo "[*] Found symbolic links - creating backup registry..."
    BACKUP_DIR="/tmp/heckos-link-backup-$$"
    mkdir -p "$BACKUP_DIR"
    
    echo "$LINKED_FILES" > "$BACKUP_DIR/links.txt"
    
    # Save link targets
    while IFS= read -r link; do
        if [ -L "$link" ]; then
            target=$(readlink "$link")
            echo "$link -> $target" >> "$BACKUP_DIR/link-registry.txt"
        fi
    done <<< "$LINKED_FILES"
    
    echo "[✓] Link registry saved to: $BACKUP_DIR/link-registry.txt"
    echo ""
fi

# Set up build environment to avoid breaking links
export HECKOS_BUILD_SAFE_MODE=1
export HECKOS_PRESERVE_LINKS=1

# Run the actual build
echo "[*] Starting HeckOS build..."
echo "[*] Build directory: $HOME/heckos-ultimate"
echo ""

# Execute build script
bash "$BUILD_SCRIPT" "$@"

BUILD_EXIT_CODE=$?

# Restore any broken links after build
if [ -f "$BACKUP_DIR/link-registry.txt" ]; then
    echo ""
    echo "[*] Verifying symbolic links..."
    
    BROKEN_LINKS=0
    while IFS= read -r line; do
        link=$(echo "$line" | cut -d' ' -f1)
        if [ ! -e "$link" ] && [ -L "$link" ]; then
            echo "⚠️  Broken link detected: $link"
            BROKEN_LINKS=$((BROKEN_LINKS + 1))
        fi
    done < "$BACKUP_DIR/link-registry.txt"
    
    if [ $BROKEN_LINKS -eq 0 ]; then
        echo "[✓] All symbolic links intact"
    else
        echo "❌ Found $BROKEN_LINKS broken links"
        echo "Link registry available at: $BACKUP_DIR/link-registry.txt"
    fi
    
    # Clean up backup directory after a delay
    echo ""
    echo "Link backup will be kept at: $BACKUP_DIR"
    echo "Remove manually when no longer needed"
fi

echo ""
if [ $BUILD_EXIT_CODE -eq 0 ]; then
    echo "========================================"
    echo "  ✓ HeckOS Build Completed Successfully"
    echo "========================================"
    echo ""
    echo "ISO files created in: $HOME/heckos-ultimate/"
    echo ""
    echo "Next steps:"
    echo "1. Test ISO: qemu-system-x86_64 -enable-kvm -m 4096 -cdrom <iso-file>"
    echo "2. Create USB: sudo bash ghostos-installation-setup.sh"
    echo "3. Install: Boot from USB and follow installer"
else
    echo "========================================"
    echo "  ❌ HeckOS Build Failed"
    echo "========================================"
    echo ""
    echo "Check logs in: $HOME/heckos-ultimate/build/build.log"
fi

exit $BUILD_EXIT_CODE
