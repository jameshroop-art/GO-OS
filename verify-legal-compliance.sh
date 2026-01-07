#!/bin/bash
# Legal Compliance Verification Script
# Verifies that all legal documentation is in place

echo "=========================================="
echo "  Heck-CheckOS Legal Compliance Verification"
echo "=========================================="
echo ""

EXIT_CODE=0

# Check for required legal files
echo "Checking for required legal files..."
REQUIRED_FILES=(
    "LICENSE"
    "LEGAL_COMPLIANCE.md"
    "TRADEMARK_NOTICE.md"
    "THIRD_PARTY_LICENSES.md"
    "INFRINGEMENT_CHECK_SUMMARY.md"
)

for file in "${REQUIRED_FILES[@]}"; do
    if [ -f "$file" ]; then
        SIZE=$(stat -c%s "$file" 2>/dev/null || stat -f%z "$file" 2>/dev/null)
        echo "  ✓ $file (${SIZE} bytes)"
    else
        echo "  ✗ $file - MISSING!"
        EXIT_CODE=1
    fi
done

echo ""
echo "Checking README.md legal notice..."
if grep -q "Legal Notice" README.md; then
    echo "  ✓ Legal notice found in README.md"
else
    echo "  ✗ Legal notice missing from README.md"
    EXIT_CODE=1
fi

echo ""
echo "Checking for legal headers in scripts..."
SCRIPTS=(
    "Go-OS/heckcheckos-build.sh"
    "Go-OS/heckcheckos-android.sh"
    "Go-OS/verify-iso.sh"
    "Go-OS/heckcheckos-installer-gui.sh"
)

for script in "${SCRIPTS[@]}"; do
    if [ -f "$script" ]; then
        if grep -q "LEGAL NOTICE" "$script"; then
            echo "  ✓ $script has legal header"
        else
            echo "  ✗ $script missing legal header"
            EXIT_CODE=1
        fi
    else
        echo "  ? $script not found (may be optional)"
    fi
done

echo ""
echo "Checking Python files..."
PYTHON_FILES=(
    "Go-OS/heckcheckos-installer-gui.py"
    "gui/heckcheckos-iso-builder/main.py"
    "windows_driver_emulator/emulator.py"
)

for pyfile in "${PYTHON_FILES[@]}"; do
    if [ -f "$pyfile" ]; then
        if grep -q "LEGAL NOTICE" "$pyfile"; then
            echo "  ✓ $pyfile has legal header"
        else
            echo "  ✗ $pyfile missing legal header"
            EXIT_CODE=1
        fi
    else
        echo "  ? $pyfile not found (may be optional)"
    fi
done

echo ""
echo "=========================================="
if [ $EXIT_CODE -eq 0 ]; then
    echo "  ✓ All legal compliance checks PASSED"
    echo "=========================================="
else
    echo "  ✗ Some legal compliance checks FAILED"
    echo "=========================================="
fi

exit $EXIT_CODE
