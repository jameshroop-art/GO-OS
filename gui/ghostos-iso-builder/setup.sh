#!/usr/bin/env bash
#
# HeckOS Builder - Comprehensive Installation Setup
# Creates virtual environment, installs dependencies, and validates installation
#
# Usage: sudo bash setup.sh

set -e  # Exit on error

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$SCRIPT_DIR/venv"
LOG_FILE="/tmp/heckos-builder-setup.log"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging function
log() {
    echo -e "${GREEN}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $1" | tee -a "$LOG_FILE"
}

log_error() {
    echo -e "${RED}[$(date '+%Y-%m-%d %H:%M:%S')] ERROR:${NC} $1" | tee -a "$LOG_FILE"
}

log_warn() {
    echo -e "${YELLOW}[$(date '+%Y-%m-%d %H:%M:%S')] WARNING:${NC} $1" | tee -a "$LOG_FILE"
}

log_info() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')] INFO:${NC} $1" | tee -a "$LOG_FILE"
}

# Banner
echo -e "${GREEN}"
cat << 'EOF'
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║              HeckOS Builder - Setup                       ║
║                                                           ║
║       Comprehensive Installation & Configuration          ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}"

log "Starting HeckOS Builder installation..."

# Check if running as root for system dependencies
if [ "$EUID" -eq 0 ]; then
    log_warn "Running as root. Will install system dependencies."
    SUDO=""
else
    log_info "Not running as root. Will use sudo for system dependencies."
    SUDO="sudo"
fi

# Step 1: Check system requirements
log "Step 1/8: Checking system requirements..."

# Check Python version
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | awk '{print $2}')
    PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
    PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)
    
    if [ "$PYTHON_MAJOR" -ge 3 ] && [ "$PYTHON_MINOR" -ge 8 ]; then
        log "✓ Python $PYTHON_VERSION found (requirement: 3.8+)"
    else
        log_error "Python 3.8+ required. Found: $PYTHON_VERSION"
        exit 1
    fi
else
    log_error "Python 3 not found. Please install Python 3.8 or later."
    exit 1
fi

# Check available memory
TOTAL_MEM=$(free -m | awk '/^Mem:/{print $2}')
if [ "$TOTAL_MEM" -lt 4096 ]; then
    log_warn "Only ${TOTAL_MEM}MB RAM available (recommended: 4096MB+)"
else
    log "✓ Sufficient RAM: ${TOTAL_MEM}MB"
fi

# Check disk space
AVAILABLE_SPACE=$(df -BM "$SCRIPT_DIR" | awk 'NR==2 {print $4}' | sed 's/M//')
if [ "$AVAILABLE_SPACE" -lt 20480 ]; then
    log_warn "Only ${AVAILABLE_SPACE}MB disk space available (recommended: 20GB+)"
else
    log "✓ Sufficient disk space: ${AVAILABLE_SPACE}MB"
fi

# Step 2: Install system dependencies
log "Step 2/8: Installing system dependencies..."

REQUIRED_PACKAGES=(
    "python3-venv"
    "python3-pip"
    "python3-dev"
    "build-essential"
    "genisoimage"
    "squashfs-tools"
    "xorriso"
    "grub2-common"
    "grub-pc-bin"
    "grub-efi-amd64-bin"
    "mtools"
    "dosfstools"
    "git"
    "wget"
    "curl"
)

MISSING_PACKAGES=()

for pkg in "${REQUIRED_PACKAGES[@]}"; do
    if ! dpkg -l | grep -q "^ii  $pkg"; then
        MISSING_PACKAGES+=("$pkg")
    fi
done

if [ ${#MISSING_PACKAGES[@]} -gt 0 ]; then
    log "Installing missing packages: ${MISSING_PACKAGES[*]}"
    $SUDO apt-get update -qq
    $SUDO apt-get install -y "${MISSING_PACKAGES[@]}" 2>&1 | tee -a "$LOG_FILE"
    log "✓ System dependencies installed"
else
    log "✓ All system dependencies already installed"
fi

# Step 3: Create virtual environment
log "Step 3/8: Creating Python virtual environment..."

if [ -d "$VENV_DIR" ]; then
    log_warn "Virtual environment already exists at $VENV_DIR"
    read -p "Remove and recreate? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm -rf "$VENV_DIR"
        log "Removed existing virtual environment"
    else
        log "Keeping existing virtual environment"
    fi
fi

if [ ! -d "$VENV_DIR" ]; then
    python3 -m venv "$VENV_DIR"
    log "✓ Virtual environment created at $VENV_DIR"
else
    log "✓ Using existing virtual environment"
fi

# Step 4: Activate virtual environment and upgrade pip
log "Step 4/8: Activating virtual environment and upgrading pip..."

source "$VENV_DIR/bin/activate"

pip install --upgrade pip setuptools wheel 2>&1 | tee -a "$LOG_FILE"
log "✓ pip upgraded to latest version"

# Step 5: Install Python dependencies
log "Step 5/8: Installing Python dependencies..."

if [ -f "$SCRIPT_DIR/requirements.txt" ]; then
    pip install -r "$SCRIPT_DIR/requirements.txt" 2>&1 | tee -a "$LOG_FILE"
    log "✓ Python dependencies installed from requirements.txt"
else
    log_error "requirements.txt not found at $SCRIPT_DIR"
    exit 1
fi

# Step 6: Validate installation
log "Step 6/8: Validating installation..."

VALIDATION_PASSED=true

# Check PyQt6
if python3 -c "import PyQt6" 2>/dev/null; then
    log "✓ PyQt6 installed correctly"
else
    log_error "PyQt6 installation failed"
    VALIDATION_PASSED=false
fi

# Check other critical modules
CRITICAL_MODULES=("yaml" "requests" "cryptography" "git")
for module in "${CRITICAL_MODULES[@]}"; do
    if python3 -c "import $module" 2>/dev/null; then
        log "✓ $module installed correctly"
    else
        log_error "$module installation failed"
        VALIDATION_PASSED=false
    fi
done

if [ "$VALIDATION_PASSED" = false ]; then
    log_error "Installation validation failed. Check $LOG_FILE for details."
    exit 1
fi

# Step 7: Create launcher scripts
log "Step 7/8: Creating launcher scripts..."

# Create start.sh launcher
cat > "$SCRIPT_DIR/start.sh" << 'LAUNCHER_EOF'
#!/usr/bin/env bash
#
# HeckOS Builder - Launcher Script
# Automatically activates venv and starts the GUI
#

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$SCRIPT_DIR/venv"

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

# Check if venv exists
if [ ! -d "$VENV_DIR" ]; then
    echo -e "${RED}Error: Virtual environment not found.${NC}"
    echo "Please run: sudo bash setup.sh"
    exit 1
fi

# Activate venv
source "$VENV_DIR/bin/activate"

# Check if main.py exists
if [ ! -f "$SCRIPT_DIR/main.py" ]; then
    echo -e "${RED}Error: main.py not found.${NC}"
    exit 1
fi

echo -e "${GREEN}Starting HeckOS Builder...${NC}"

# Launch GUI with hardware detection and scaling
python3 "$SCRIPT_DIR/main.py" "$@"

EXIT_CODE=$?

if [ $EXIT_CODE -ne 0 ]; then
    echo -e "${RED}HeckOS Builder exited with error code: $EXIT_CODE${NC}"
fi

deactivate 2>/dev/null || true

exit $EXIT_CODE
LAUNCHER_EOF

chmod +x "$SCRIPT_DIR/start.sh"
log "✓ Created start.sh launcher"

# Create desktop entry
DESKTOP_FILE="$HOME/.local/share/applications/heckos-builder.desktop"
mkdir -p "$HOME/.local/share/applications"

cat > "$DESKTOP_FILE" << DESKTOP_EOF
[Desktop Entry]
Name=HeckOS Builder
Comment=Advanced ISO Builder and OS Customization Tool
Exec=$SCRIPT_DIR/start.sh
Icon=$SCRIPT_DIR/icon.png
Terminal=false
Type=Application
Categories=Development;Utility;System;
StartupNotify=true
DESKTOP_EOF

log "✓ Created desktop entry at $DESKTOP_FILE"

# Step 8: Test installation
log "Step 8/8: Testing installation..."

# Dry run test
if python3 "$SCRIPT_DIR/main.py" --version 2>/dev/null; then
    log "✓ Application launches successfully"
else
    log_warn "Could not test application launch (might require display)"
fi

# Deactivate venv
deactivate 2>/dev/null || true

# Success message
echo
echo -e "${GREEN}╔═══════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║                                                           ║${NC}"
echo -e "${GREEN}║         Installation Complete! ✓                          ║${NC}"
echo -e "${GREEN}║                                                           ║${NC}"
echo -e "${GREEN}╚═══════════════════════════════════════════════════════════╝${NC}"
echo
log_info "HeckOS Builder successfully installed!"
echo
echo -e "${BLUE}To start the builder:${NC}"
echo -e "  ${GREEN}cd $SCRIPT_DIR${NC}"
echo -e "  ${GREEN}./start.sh${NC}"
echo
echo -e "${BLUE}Or from applications menu:${NC}"
echo -e "  ${GREEN}HeckOS Builder${NC}"
echo
log_info "Installation log saved to: $LOG_FILE"
echo

exit 0
