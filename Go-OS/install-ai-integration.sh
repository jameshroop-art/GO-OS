#!/bin/bash
# ============================================
# HeckOS AI Integration Installer
# Installs Ollama and LM Studio with shared model access
# With AI-assisted error correction during setup
# To be run during OS installation on localhost
# ============================================

set -e

echo "========================================"
echo "  🤖 HeckOS AI Integration Setup"
echo "  Installing Ollama + LM Studio"
echo "  With AI-Assisted Error Correction"
echo "========================================"
echo ""

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    echo "⚠️  Not running as root, will use sudo for system operations"
    SUDO="sudo"
else
    SUDO=""
fi

# Enable AI correction mode
AI_CORRECTION_ENABLED=true
CORRECTION_LOG="/tmp/heckos-ai-corrections.log"
touch "$CORRECTION_LOG"

# Port configuration
PORT_RANGE_START=51511
PORT_RANGE_END=51611
OLLAMA_PORT=""
LMSTUDIO_PORT=""
PORT_REGISTRY="/var/run/heckos-ports.registry"
PORT_CLEANUP_SCRIPT="/opt/heckos/ai-models/port-cleanup.sh"

# Initialize port registry
init_port_registry() {
    $SUDO mkdir -p "$(dirname "$PORT_REGISTRY")"
    if [ ! -f "$PORT_REGISTRY" ]; then
        $SUDO touch "$PORT_REGISTRY"
        $SUDO chmod 644 "$PORT_REGISTRY"
    fi
}

# Register a port allocation
register_port() {
    local service=$1
    local port=$2
    local pid=${3:-$$}
    local timestamp=$(date +%s)
    
    # Format: service|port|pid|timestamp|config_path
    local entry="$service|$port|$pid|$timestamp|"
    
    # Add configuration path based on service
    if [ "$service" = "ollama" ]; then
        entry="${entry}/etc/systemd/system/ollama.service.d/environment.conf"
    elif [ "$service" = "lmstudio" ]; then
        entry="${entry}$HOME/.cache/lm-studio/settings.json"
    fi
    
    $SUDO bash -c "echo '$entry' >> $PORT_REGISTRY"
    echo "[✓] Registered port $port for $service"
}

# Unregister a port (called on cleanup)
unregister_port() {
    local service=$1
    local port=$2
    
    if [ -f "$PORT_REGISTRY" ]; then
        $SUDO sed -i "/^$service|$port|/d" "$PORT_REGISTRY"
        echo "[✓] Unregistered port $port for $service"
    fi
}

# Check if port is registered
is_port_registered() {
    local port=$1
    if [ -f "$PORT_REGISTRY" ]; then
        grep -q "|$port|" "$PORT_REGISTRY"
        return $?
    fi
    return 1
}

# Get registered service for a port
get_port_service() {
    local port=$1
    if [ -f "$PORT_REGISTRY" ]; then
        grep "|$port|" "$PORT_REGISTRY" | cut -d'|' -f1 | head -1
    fi
}

# Clean up stale port registrations (where process no longer exists)
cleanup_stale_ports() {
    if [ ! -f "$PORT_REGISTRY" ]; then
        return
    fi
    
    echo "[*] Cleaning up stale port registrations..."
    local cleaned=0
    
    while IFS='|' read -r service port pid timestamp config_path; do
        # Skip empty lines
        [ -z "$service" ] && continue
        
        # Check if process still exists
        if [ -n "$pid" ] && ! kill -0 "$pid" 2>/dev/null && ! systemctl is-active --quiet "$service" 2>/dev/null; then
            echo "[*] Cleaning stale registration: $service on port $port (PID $pid no longer exists)"
            unregister_port "$service" "$port"
            cleaned=$((cleaned + 1))
        fi
    done < "$PORT_REGISTRY"
    
    if [ $cleaned -gt 0 ]; then
        echo "[✓] Cleaned $cleaned stale port registrations"
    else
        echo "[✓] No stale ports found"
    fi
}

# Function to find an unused port in the range
find_unused_port() {
    local start=$1
    local end=$2
    
    for port in $(seq $start $end); do
        # Check if port is in use
        if ! $SUDO netstat -tuln 2>/dev/null | grep -q ":$port " && \
           ! $SUDO ss -tuln 2>/dev/null | grep -q ":$port " && \
           ! is_port_registered "$port"; then
            echo "$port"
            return 0
        fi
    done
    
    return 1
}

# Function to kill process using a specific port
kill_process_on_port() {
    local port=$1
    local force=${2:-false}
    
    echo "[*] Checking for processes on port $port..."
    
    # Find PIDs using the port
    local pids=$(lsof -ti:$port 2>/dev/null || $SUDO lsof -ti:$port 2>/dev/null || \
                 $SUDO fuser $port/tcp 2>/dev/null)
    
    if [ -z "$pids" ]; then
        echo "[✓] Port $port is available"
        return 0
    fi
    
    echo "[!] Found process(es) using port $port: $pids"
    
    if [ "$force" = "true" ]; then
        echo "[*] Killing process(es) on port $port..."
        for pid in $pids; do
            $SUDO kill -9 $pid 2>/dev/null && echo "[✓] Killed process $pid"
        done
        sleep 1
        return 0
    else
        echo ""
        echo "Process(es) are using port $port"
        read -p "Kill these processes? (y/n): " kill_choice
        if [ "$kill_choice" = "y" ]; then
            for pid in $pids; do
                $SUDO kill -9 $pid 2>/dev/null && echo "[✓] Killed process $pid"
            done
            sleep 1
            return 0
        else
            return 1
        fi
    fi
}

# Function to allocate port with options
allocate_port() {
    local service_name=$1
    local preferred_port=$2
    local use_range=${3:-true}
    
    echo ""
    echo "[*] Allocating port for $service_name..."
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
    # First, try preferred port
    if [ -n "$preferred_port" ]; then
        echo "[*] Checking preferred port $preferred_port..."
        if ! $SUDO netstat -tuln 2>/dev/null | grep -q ":$preferred_port " && \
           ! $SUDO ss -tuln 2>/dev/null | grep -q ":$preferred_port "; then
            echo "[✓] Using preferred port: $preferred_port"
            echo "$preferred_port"
            return 0
        else
            echo "[!] Preferred port $preferred_port is in use"
            echo ""
            echo "Options:"
            echo "  1) Kill process on port $preferred_port and use it"
            echo "  2) Find unused port in range $PORT_RANGE_START-$PORT_RANGE_END"
            echo "  3) Enter custom port number"
            echo ""
            read -p "Choose option [1-3]: " port_choice
            
            case $port_choice in
                1)
                    if kill_process_on_port "$preferred_port"; then
                        echo "[✓] Using port: $preferred_port"
                        echo "$preferred_port"
                        return 0
                    else
                        echo "[!] Could not free port $preferred_port"
                        # Fall through to find another port
                    fi
                    ;;
                2)
                    # Use range - handled below
                    ;;
                3)
                    read -p "Enter port number: " custom_port
                    if [ -n "$custom_port" ] && [ "$custom_port" -ge 1024 ] && [ "$custom_port" -le 65535 ]; then
                        if kill_process_on_port "$custom_port"; then
                            echo "[✓] Using custom port: $custom_port"
                            echo "$custom_port"
                            return 0
                        fi
                    else
                        echo "[!] Invalid port number"
                    fi
                    ;;
            esac
        fi
    fi
    
    # Find unused port in range
    if [ "$use_range" = "true" ]; then
        echo "[*] Searching for unused port in range $PORT_RANGE_START-$PORT_RANGE_END..."
        local found_port=$(find_unused_port $PORT_RANGE_START $PORT_RANGE_END)
        
        if [ -n "$found_port" ]; then
            echo "[✓] Found unused port: $found_port"
            echo "$found_port"
            return 0
        else
            echo "[!] No unused ports found in range"
            echo "[!] All ports $PORT_RANGE_START-$PORT_RANGE_END are in use"
            return 1
        fi
    fi
    
    return 1
}

# Function to ask AI for correction
ask_ai_for_correction() {
    local error_msg="$1"
    local context="$2"
    local step="$3"
    
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "  🤖 AI Error Correction Activated"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "Error occurred in: $step"
    echo "Error message: $error_msg"
    echo ""
    
    # Log the error
    echo "[$(date)] Step: $step | Error: $error_msg | Context: $context" >> "$CORRECTION_LOG"
    
    if [ "$AI_CORRECTION_ENABLED" = true ]; then
        echo "[*] Consulting AI for correction suggestions..."
        echo ""
        
        # Try to get AI suggestion if Ollama is already running
        if command -v ollama &> /dev/null && systemctl is-active --quiet ollama 2>/dev/null; then
            echo "[AI] Analyzing error with local AI model..."
            
            local ai_prompt="You are a Linux system administrator AI assistant. An error occurred during HeckOS AI integration setup.

Step: $step
Error: $error_msg
Context: $context

Provide a concise fix suggestion (max 3 bullet points) that can be executed in bash. Focus on common causes and solutions."

            # Query local AI for suggestions (non-blocking)
            local ai_response=$(timeout 10 ollama run llama2 "$ai_prompt" 2>/dev/null | head -20 || echo "")
            
            if [ -n "$ai_response" ]; then
                echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
                echo "AI Suggestion:"
                echo "$ai_response"
                echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
                echo ""
                echo "$ai_response" >> "$CORRECTION_LOG"
            else
                show_fallback_suggestions "$step" "$error_msg"
            fi
        else
            show_fallback_suggestions "$step" "$error_msg"
        fi
        
        echo ""
        echo "Options:"
        echo "  1) Retry the step"
        echo "  2) Skip this step and continue"
        echo "  3) Apply suggested fix and retry"
        echo "  4) Exit setup"
        echo ""
        read -p "Choose option [1-4]: " choice
        
        return $choice
    else
        return 1
    fi
}

# Function to show fallback suggestions when AI is not available
show_fallback_suggestions() {
    local step="$1"
    local error="$2"
    
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "Common Solutions:"
    
    case "$step" in
        "ollama_install")
            echo "  • Check internet connection: ping -c 3 ollama.com"
            echo "  • Verify curl is installed: apt-get install curl"
            echo "  • Try manual download from: https://ollama.com/"
            ;;
        "lmstudio_download")
            echo "  • Check internet connection: ping -c 3 lmstudio.ai"
            echo "  • Verify wget is installed: apt-get install wget"
            echo "  • Try manual download from: https://lmstudio.ai/"
            echo "  • Check disk space: df -h"
            ;;
        "service_start")
            echo "  • Port may be in use (script auto-allocates from $PORT_RANGE_START-$PORT_RANGE_END)"
            echo "  • Check allocated port: cat /etc/systemd/system/ollama.service.d/environment.conf"
            echo "  • Review service logs: journalctl -u ollama -n 50"
            echo "  • Kill process on port: sudo kill -9 \$(sudo lsof -ti:<port>)"
            echo "  • Try manual start: ollama serve"
            ;;
        "permissions")
            echo "  • Check directory permissions: ls -la /opt/heckos/ai-models/"
            echo "  • Fix ownership: chown -R $USER:$USER /opt/heckos/ai-models/"
            echo "  • Verify SELinux/AppArmor: sestatus or aa-status"
            ;;
        *)
            echo "  • Check system logs: journalctl -xe"
            echo "  • Verify disk space: df -h"
            echo "  • Check for conflicting services: systemctl list-units --state=failed"
            ;;
    esac
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
}

# Function to handle errors with AI correction
handle_error() {
    local exit_code=$?
    local step="$1"
    local error_msg="$2"
    local context="$3"
    
    if [ $exit_code -ne 0 ]; then
        ask_ai_for_correction "$error_msg" "$context" "$step"
        local user_choice=$?
        
        case $user_choice in
            1)  # Retry
                echo "[*] Retrying step: $step"
                return 10  # Signal to retry
                ;;
            2)  # Skip
                echo "[⚠️] Skipping step: $step"
                return 0
                ;;
            3)  # Apply fix
                echo "[*] Please apply the suggested fix, then press Enter to retry"
                read -p "Press Enter when ready..."
                return 10  # Signal to retry
                ;;
            4)  # Exit
                echo "[!] Setup cancelled by user"
                exit 1
                ;;
            *)
                return 1
                ;;
        esac
    fi
    return 0
}

# Create shared models directory
MODELS_DIR="/opt/heckos/ai-models"
echo "[*] Creating shared AI models directory: $MODELS_DIR"
$SUDO mkdir -p "$MODELS_DIR"
$SUDO chmod 755 "$MODELS_DIR"

# Initialize port registry
init_port_registry
cleanup_stale_ports

# Create port cleanup script
echo "[*] Creating port lifecycle management script..."
cat > /tmp/port-cleanup.sh << 'CLEANUP_SCRIPT_EOF'
#!/bin/bash
# Port Lifecycle Management and Cleanup Script
# Automatically releases ports when services stop

PORT_REGISTRY="/var/run/heckos-ports.registry"

cleanup_port() {
    local service=$1
    local port=$2
    
    echo "[$(date)] Cleaning up port $port for $service"
    
    # Remove from registry
    if [ -f "$PORT_REGISTRY" ]; then
        sed -i "/^$service|$port|/d" "$PORT_REGISTRY"
    fi
    
    # Log cleanup
    logger -t heckos-port-cleanup "Released port $port for $service"
}

# Check service status and cleanup if stopped
check_and_cleanup() {
    if [ ! -f "$PORT_REGISTRY" ]; then
        return
    fi
    
    while IFS='|' read -r service port pid timestamp config_path; do
        [ -z "$service" ] && continue
        
        # Check if service is running
        if ! systemctl is-active --quiet "$service" 2>/dev/null; then
            # Service stopped, cleanup port
            cleanup_port "$service" "$port"
        fi
    done < "$PORT_REGISTRY"
}

# Main cleanup function
case "${1:-check}" in
    check)
        check_and_cleanup
        ;;
    cleanup)
        service=$2
        port=$3
        if [ -n "$service" ] && [ -n "$port" ]; then
            cleanup_port "$service" "$port"
        fi
        ;;
    *)
        echo "Usage: $0 {check|cleanup service port}"
        exit 1
        ;;
esac
CLEANUP_SCRIPT_EOF

$SUDO mv /tmp/port-cleanup.sh "$PORT_CLEANUP_SCRIPT"
$SUDO chmod +x "$PORT_CLEANUP_SCRIPT"
echo "[✓] Port cleanup script created"

# ============================================
# Install Ollama
# ============================================
echo ""
echo "[1/4] Installing Ollama..."

install_ollama() {
    if command -v ollama &> /dev/null; then
        echo "[✓] Ollama already installed"
        ollama --version
        return 0
    else
        echo "[*] Downloading and installing Ollama..."
        if curl -fsSL https://ollama.com/install.sh | sh; then
            echo "[✓] Ollama installed successfully"
            return 0
        else
            return 1
        fi
    fi
}

# Try to install with error handling
while true; do
    if install_ollama; then
        break
    else
        handle_error "ollama_install" "Failed to install Ollama" "Downloading from ollama.com"
        local retry_code=$?
        if [ $retry_code -ne 10 ]; then
            break
        fi
    fi
done

# Configure Ollama to use shared models directory
echo "[*] Configuring Ollama for shared models..."

# Allocate port for Ollama (prefer 11434, but can use range)
OLLAMA_PORT=$(allocate_port "Ollama" "11434" true)
if [ -z "$OLLAMA_PORT" ]; then
    echo "[!] Could not allocate port for Ollama"
    echo "[!] Installation will continue but Ollama may not start correctly"
    OLLAMA_PORT="11434"  # Fallback
fi

echo "[✓] Ollama will use port: $OLLAMA_PORT"

# Register port allocation
register_port "ollama" "$OLLAMA_PORT"

$SUDO mkdir -p /etc/systemd/system/ollama.service.d/
$SUDO tee /etc/systemd/system/ollama.service.d/environment.conf > /dev/null << EOF
[Service]
Environment="OLLAMA_MODELS=$MODELS_DIR/ollama"
Environment="OLLAMA_HOST=127.0.0.1:$OLLAMA_PORT"
ExecStopPost=$PORT_CLEANUP_SCRIPT cleanup ollama $OLLAMA_PORT
EOF

# Create Ollama models directory
$SUDO mkdir -p "$MODELS_DIR/ollama"
$SUDO chown -R ollama:ollama "$MODELS_DIR/ollama" 2>/dev/null || true

# Enable and start Ollama service
echo "[*] Starting Ollama service..."

start_ollama_service() {
    $SUDO systemctl daemon-reload
    $SUDO systemctl enable ollama
    $SUDO systemctl restart ollama
    sleep 3
    
    if systemctl is-active --quiet ollama; then
        echo "[✓] Ollama service is running"
        echo "[✓] Port $OLLAMA_PORT is now active for Ollama (will auto-release on stop)"
        return 0
    else
        echo "⚠️  Ollama service not running"
        return 1
    fi
}

# Try to start with error handling
while true; do
    if start_ollama_service; then
        break
    else
        handle_error "service_start" "Failed to start Ollama service" "systemctl start ollama"
        local retry_code=$?
        if [ $retry_code -ne 10 ]; then
            echo "[⚠️] Continuing without Ollama service running"
            break
        fi
    fi
done

# ============================================
# Install LM Studio
# ============================================
echo ""
echo "[2/4] Installing LM Studio..."

LM_STUDIO_DIR="/opt/lmstudio"
LM_STUDIO_VERSION="0.2.9"  # Update as needed

if [ -d "$LM_STUDIO_DIR" ]; then
    echo "[✓] LM Studio directory exists"
else
    echo "[*] Creating LM Studio installation directory..."
    $SUDO mkdir -p "$LM_STUDIO_DIR"
fi

# Download LM Studio (AppImage format for Linux)
echo "[*] Downloading LM Studio..."
LM_STUDIO_URL="https://releases.lmstudio.ai/linux/x86/0.2.9/LM-Studio-0.2.9.AppImage"
LM_STUDIO_APPIMAGE="$LM_STUDIO_DIR/LMStudio.AppImage"

download_lmstudio() {
    if [ -f "$LM_STUDIO_APPIMAGE" ]; then
        echo "[✓] LM Studio AppImage already exists"
        return 0
    fi
    
    if $SUDO wget -O "$LM_STUDIO_APPIMAGE" "$LM_STUDIO_URL"; then
        $SUDO chmod +x "$LM_STUDIO_APPIMAGE"
        echo "[✓] LM Studio downloaded"
        return 0
    else
        return 1
    fi
}

# Try to download with error handling
while true; do
    if download_lmstudio; then
        break
    else
        handle_error "lmstudio_download" "Failed to download LM Studio" "Downloading from lmstudio.ai"
        local retry_code=$?
        if [ $retry_code -ne 10 ]; then
            echo "[⚠️] LM Studio download skipped. You can manually download from: https://lmstudio.ai/"
            echo "    Place the AppImage at: $LM_STUDIO_APPIMAGE"
            break
        fi
    fi
done

# Configure LM Studio to use shared models
echo "[*] Configuring LM Studio for shared models..."
$SUDO mkdir -p "$MODELS_DIR/lmstudio"

# Allocate port for LM Studio (prefer 1234, but can use range)
LMSTUDIO_PORT=$(allocate_port "LM Studio" "1234" true)
if [ -z "$LMSTUDIO_PORT" ]; then
    echo "[!] Could not allocate port for LM Studio"
    echo "[!] Installation will continue but LM Studio may not start correctly"
    LMSTUDIO_PORT="1234"  # Fallback
fi

echo "[✓] LM Studio will use port: $LMSTUDIO_PORT"

# Register port allocation for LM Studio
register_port "lmstudio" "$LMSTUDIO_PORT"

# Create LM Studio configuration
LMSTUDIO_CONFIG_DIR="$HOME/.cache/lm-studio"
mkdir -p "$LMSTUDIO_CONFIG_DIR"

cat > "$LMSTUDIO_CONFIG_DIR/settings.json" << EOF
{
  "modelsPath": "$MODELS_DIR/lmstudio",
  "serverPort": $LMSTUDIO_PORT,
  "ollamaCompatibility": true,
  "enableCors": true,
  "allowedOrigins": ["http://localhost:$OLLAMA_PORT"]
}
EOF

# Create LM Studio wrapper script with port lifecycle management
cat > "$MODELS_DIR/lmstudio-wrapper.sh" << WRAPPER_EOF
#!/bin/bash
# LM Studio Wrapper with Port Lifecycle Management

PORT_REGISTRY="/var/run/heckos-ports.registry"
LMSTUDIO_PORT=$LMSTUDIO_PORT
LMSTUDIO_APPIMAGE="$LM_STUDIO_APPIMAGE"
CLEANUP_SCRIPT="$PORT_CLEANUP_SCRIPT"

# Trap to cleanup on exit
cleanup() {
    echo "LM Studio stopped, releasing port \$LMSTUDIO_PORT"
    bash "\$CLEANUP_SCRIPT" cleanup lmstudio \$LMSTUDIO_PORT
}

trap cleanup EXIT INT TERM

echo "Starting LM Studio on port \$LMSTUDIO_PORT"
echo "Port will be automatically released when LM Studio exits"

# Run LM Studio
"\$LMSTUDIO_APPIMAGE" "\$@"

# Cleanup is handled by trap
WRAPPER_EOF

chmod +x "$MODELS_DIR/lmstudio-wrapper.sh"

echo "[✓] LM Studio configured with auto port release"

# ============================================
# Create Model Sharing Bridge
# ============================================
echo ""
echo "[3/4] Setting up model sharing between Ollama and LM Studio..."

# Create symlinks to allow both systems to access each other's models
$SUDO mkdir -p "$MODELS_DIR/shared"

# Create model bridge script
cat > "$MODELS_DIR/sync-models.sh" << 'BRIDGE_EOF'
#!/bin/bash
# Model Sync Bridge - Allows Ollama and LM Studio to share models

OLLAMA_DIR="/opt/heckos/ai-models/ollama"
LMSTUDIO_DIR="/opt/heckos/ai-models/lmstudio"
SHARED_DIR="/opt/heckos/ai-models/shared"

echo "Syncing AI models between Ollama and LM Studio..."

# Create shared directory if not exists
mkdir -p "$SHARED_DIR"

# Link Ollama models to shared
if [ -d "$OLLAMA_DIR" ]; then
    for model in "$OLLAMA_DIR"/*; do
        if [ -f "$model" ]; then
            model_name=$(basename "$model")
            if [ ! -e "$SHARED_DIR/$model_name" ]; then
                ln -sf "$model" "$SHARED_DIR/$model_name"
                echo "  ✓ Linked Ollama model: $model_name"
            fi
        fi
    done
fi

# Link LM Studio models to shared
if [ -d "$LMSTUDIO_DIR" ]; then
    for model in "$LMSTUDIO_DIR"/*; do
        if [ -f "$model" ] || [ -d "$model" ]; then
            model_name=$(basename "$model")
            if [ ! -e "$SHARED_DIR/$model_name" ]; then
                ln -sf "$model" "$SHARED_DIR/$model_name"
                echo "  ✓ Linked LM Studio model: $model_name"
            fi
        fi
    done
fi

# Allow Ollama to access LM Studio models
if [ -d "$LMSTUDIO_DIR" ]; then
    for model in "$LMSTUDIO_DIR"/*; do
        if [ -f "$model" ] || [ -d "$model" ]; then
            model_name=$(basename "$model")
            ollama_link="$OLLAMA_DIR/$model_name"
            if [ ! -e "$ollama_link" ]; then
                ln -sf "$model" "$ollama_link"
                echo "  ✓ Ollama can access: $model_name"
            fi
        fi
    done
fi

# Allow LM Studio to access Ollama models
if [ -d "$OLLAMA_DIR" ]; then
    for model in "$OLLAMA_DIR"/*; do
        if [ -f "$model" ]; then
            model_name=$(basename "$model")
            lmstudio_link="$LMSTUDIO_DIR/$model_name"
            if [ ! -e "$lmstudio_link" ]; then
                ln -sf "$model" "$lmstudio_link"
                echo "  ✓ LM Studio can access: $model_name"
            fi
        fi
    done
fi

echo "Model sync complete!"
BRIDGE_EOF

chmod +x "$MODELS_DIR/sync-models.sh"
echo "[✓] Model sharing bridge created"

# Run initial sync
echo "[*] Running initial model sync..."

sync_models() {
    if bash "$MODELS_DIR/sync-models.sh"; then
        echo "[✓] Model sync successful"
        return 0
    else
        return 1
    fi
}

# Try to sync with error handling
while true; do
    if sync_models; then
        break
    else
        handle_error "permissions" "Failed to sync models" "Running sync-models.sh script"
        local retry_code=$?
        if [ $retry_code -ne 10 ]; then
            echo "[⚠️] Model sync skipped. You can manually run: $MODELS_DIR/sync-models.sh"
            break
        fi
    fi
done

# ============================================
# Create Desktop Shortcuts and Menu Entries
# ============================================
echo ""
echo "[4/4] Creating desktop shortcuts..."

# Ollama CLI wrapper desktop file
$SUDO tee /usr/share/applications/ollama.desktop > /dev/null << EOF
[Desktop Entry]
Name=Ollama
Comment=Run and manage AI models locally
Exec=x-terminal-emulator -e "bash -c 'ollama run llama2; exec bash'"
Icon=ai-ollama
Type=Application
Categories=Development;AI;
Terminal=true
EOF

# LM Studio desktop file
if [ -f "$LM_STUDIO_APPIMAGE" ]; then
    $SUDO tee /usr/share/applications/lmstudio.desktop > /dev/null << EOF
[Desktop Entry]
Name=LM Studio (Port $LMSTUDIO_PORT)
Comment=Discover, download, and run local LLMs - Port auto-releases on exit
Exec=$MODELS_DIR/lmstudio-wrapper.sh
Icon=ai-lmstudio
Type=Application
Categories=Development;AI;
Terminal=false
EOF
fi

# Port Manager desktop file
$SUDO tee /usr/share/applications/port-manager.desktop > /dev/null << EOF
[Desktop Entry]
Name=AI Port Manager
Comment=View and manage AI service port allocations
Exec=x-terminal-emulator -e "bash -c 'echo \"=== Active Port Allocations ===\"  && cat /var/run/heckos-ports.registry 2>/dev/null || echo \"No active ports\"; echo \"\"; echo \"Press Enter to exit\"; read'"
Icon=network-server
Type=Application
Categories=System;AI;
Terminal=true
EOF

# AI Models Manager desktop file
$SUDO tee /usr/share/applications/ai-models-manager.desktop > /dev/null << EOF
[Desktop Entry]
Name=AI Models Manager
Comment=Manage shared AI models for Ollama and LM Studio
Exec=x-terminal-emulator -e "bash -c '$MODELS_DIR/sync-models.sh; exec bash'"
Icon=folder-ai
Type=Application
Categories=System;AI;
Terminal=true
EOF

echo "[✓] Desktop shortcuts created with port lifecycle management"

# ============================================
# Create Quick Start Guide
# ============================================
cat > "$MODELS_DIR/README.md" << EOF
# HeckOS AI Integration - Quick Start Guide

## Installed Components

- **Ollama**: Local AI model runtime
  - Service: \`systemctl status ollama\`
  - CLI: \`ollama\` command
  - API: http://localhost:$OLLAMA_PORT
  
- **LM Studio**: Visual AI model manager
  - Location: \`/opt/lmstudio/LMStudio.AppImage\`
  - API: http://localhost:$LMSTUDIO_PORT
  - Models: \`/opt/heckos/ai-models/lmstudio\`

- **AI Monitoring Service**: Automatic error detection and correction
  - Service: \`systemctl status ai-monitor\`
  - Logs: \`/var/log/heckos-ai-monitor.log\`

## Port Configuration

- **Ollama Port**: $OLLAMA_PORT (Service-managed, auto-releases on stop)
- **LM Studio Port**: $LMSTUDIO_PORT (Wrapper-managed, auto-releases on exit)
- **Port Range**: $PORT_RANGE_START-$PORT_RANGE_END (sequential allocation)
- **Port Registry**: \`/var/run/heckos-ports.registry\`

### Port Lifecycle Management

**Automatic Port Release:**
- Ollama: Port automatically released when service stops (systemd ExecStopPost hook)
- LM Studio: Port automatically released when application exits (wrapper script trap)

**Port Registry:**
All active port allocations are tracked in \`/var/run/heckos-ports.registry\`

Format: \`service|port|pid|timestamp|config_path\`

**View Active Ports:**
\`\`\`bash
cat /var/run/heckos-ports.registry
# Or use GUI: Applications > System > AI Port Manager
\`\`\`

**Manual Port Cleanup:**
\`\`\`bash
# Cleanup specific service
sudo $PORT_CLEANUP_SCRIPT cleanup ollama $OLLAMA_PORT

# Cleanup all stale ports
sudo $PORT_CLEANUP_SCRIPT check
\`\`\`

**How It Works:**
1. Port allocated during installation/startup
2. Port registered in registry with service info
3. Configuration follows the port (environment vars, JSON config)
4. Port automatically released when service stops/exits
5. Registry cleaned up to make port available for reuse

The installation automatically finds unused ports in the range $PORT_RANGE_START-$PORT_RANGE_END
and can kill conflicting processes if needed. Ports are only active during service runtime.

## AI-Assisted Error Correction

During installation, the setup script uses AI to help diagnose and fix issues:

### How It Works

1. **Error Detection**: When a step fails, the script captures the error
2. **AI Analysis**: Ollama (if running) or fallback logic analyzes the error
3. **Correction Suggestions**: Provides actionable fixes
4. **Interactive Options**:
   - Retry the step
   - Skip and continue
   - Apply suggested fix manually
   - Exit setup

### Example Correction Flow

```
❌ Error: Failed to start Ollama service

🤖 AI Analyzing...

Suggested Fix:
  • Port 11434 might be in use
  • Check: netstat -tulpn | grep 11434
  • Kill conflicting process or change port

Options:
  1) Retry
  2) Skip
  3) Apply fix and retry
  4) Exit

Your choice: 3
```

### Ongoing Monitoring

If enabled, the AI monitoring service continuously checks:
- Ollama service health
- Model availability
- Disk space
- API responsiveness

It automatically attempts corrections and logs all actions.

### View Correction Logs

```bash
# Installation-time corrections
cat /tmp/heckos-ai-corrections.log

# Ongoing monitoring logs
tail -f /var/log/heckos-ai-monitor.log

# Service status
systemctl status ai-monitor
```

## Shared Models Directory

All models are stored in: `/opt/heckos/ai-models/`

- `ollama/` - Ollama models
- `lmstudio/` - LM Studio models  
- `shared/` - Symlinks to all available models

Both Ollama and LM Studio can access each other's models through symlinks.

## Quick Commands

### Ollama

```bash
# List available models
ollama list

# Pull a new model
ollama pull llama2

# Run a model
ollama run llama2

# Stop Ollama service
sudo systemctl stop ollama

# Start Ollama service
sudo systemctl start ollama
```

### LM Studio

```bash
# Launch LM Studio GUI
/opt/lmstudio/LMStudio.AppImage

# Or use desktop shortcut:
# Applications > Development > LM Studio
```

### Model Sharing

```bash
# Sync models between Ollama and LM Studio
/opt/heckos/ai-models/sync-models.sh

# Check shared models
ls -la /opt/heckos/ai-models/shared/
```

## API Compatibility

Both systems expose OpenAI-compatible APIs:

- **Ollama**: `http://localhost:11434/v1/chat/completions`
- **LM Studio**: `http://localhost:1234/v1/chat/completions`

Example using curl:

```bash
curl http://localhost:11434/api/generate -d '{
  "model": "llama2",
  "prompt": "Why is the sky blue?"
}'
```

## Downloading Models

### Via Ollama
```bash
ollama pull llama2
ollama pull codellama
ollama pull mistral
ollama pull phi
```

### Via LM Studio
1. Launch LM Studio
2. Go to "Discover" tab
3. Search for models
4. Click "Download"

Models downloaded by either tool will be accessible to both after running the sync script.

## Troubleshooting

### Ollama not responding
```bash
sudo systemctl restart ollama
sudo systemctl status ollama
```

### LM Studio won't start
```bash
# Check if AppImage has execute permissions
chmod +x /opt/lmstudio/LMStudio.AppImage

# Try running from terminal to see errors
/opt/lmstudio/LMStudio.AppImage
```

### Models not syncing
```bash
# Manually run sync
sudo /opt/heckos/ai-models/sync-models.sh

# Check permissions
ls -la /opt/heckos/ai-models/
```

## Updating

### Update Ollama
```bash
curl -fsSL https://ollama.com/install.sh | sh
sudo systemctl restart ollama
```

### Update LM Studio
Download the latest AppImage from https://lmstudio.ai/ and replace:
```bash
sudo wget -O /opt/lmstudio/LMStudio.AppImage <new-url>
sudo chmod +x /opt/lmstudio/LMStudio.AppImage
```

## Uninstalling

### Remove Ollama
```bash
sudo systemctl stop ollama
sudo systemctl disable ollama
sudo rm /usr/local/bin/ollama
sudo rm /etc/systemd/system/ollama.service
```

### Remove LM Studio
```bash
sudo rm -rf /opt/lmstudio
sudo rm /usr/share/applications/lmstudio.desktop
```

### Keep or remove models
```bash
# Keep models (can reuse later)
# Models stay in /opt/heckos/ai-models/

# Or remove everything
sudo rm -rf /opt/heckos/ai-models/
```

---

For more information:
- Ollama: https://ollama.com/
- LM Studio: https://lmstudio.ai/

## Port Management

If you need to change ports after installation:

### Change Ollama Port

Edit \`/etc/systemd/system/ollama.service.d/environment.conf\`:
\`\`\`ini
[Service]
Environment="OLLAMA_HOST=127.0.0.1:<new-port>"
\`\`\`

Then restart:
\`\`\`bash
sudo systemctl daemon-reload
sudo systemctl restart ollama
\`\`\`

### Change LM Studio Port

Edit \`~/.cache/lm-studio/settings.json\`:
\`\`\`json
{
  "serverPort": <new-port>
}
\`\`\`

Then restart LM Studio.

### Kill Process on Port

If a port is in use:
\`\`\`bash
# Find process using port
sudo lsof -ti:<port>

# Kill process
sudo kill -9 \$(sudo lsof -ti:<port>)
\`\`\`
EOF

echo "[✓] Quick start guide created: $MODELS_DIR/README.md"

# ============================================
# Final Summary
# ============================================
echo ""
echo "========================================"
echo "  ✓ AI Integration Setup Complete!"
echo "========================================"
echo ""
echo "Installed Components:"
echo "  • Ollama - http://localhost:$OLLAMA_PORT"
echo "  • LM Studio - http://localhost:$LMSTUDIO_PORT"
echo ""
echo "Port Lifecycle Management:"
echo "  • Ollama Port: $OLLAMA_PORT (auto-releases on service stop)"
echo "  • LM Studio Port: $LMSTUDIO_PORT (auto-releases on app exit)"
echo "  • Port Range: $PORT_RANGE_START-$PORT_RANGE_END"
echo "  • Port Registry: /var/run/heckos-ports.registry"
echo "  • Cleanup Script: $PORT_CLEANUP_SCRIPT"
echo ""
echo "Port Management:"
echo "  • View active ports: cat /var/run/heckos-ports.registry"
echo "  • GUI Port Manager: Applications > System > AI Port Manager"
echo "  • Cleanup stale ports: sudo $PORT_CLEANUP_SCRIPT check"
echo ""
echo "Shared Models Directory:"
echo "  • $MODELS_DIR"
echo ""
echo "Quick Start:"
echo "  • Ollama: ollama run llama2"
echo "  • LM Studio: $MODELS_DIR/lmstudio-wrapper.sh (or use desktop shortcut)"
echo "  • LM Studio: /opt/lmstudio/LMStudio.AppImage"
echo "  • Sync Models: $MODELS_DIR/sync-models.sh"
echo ""
echo "Documentation:"
echo "  • $MODELS_DIR/README.md"
echo ""
echo "Desktop Shortcuts:"
echo "  • Applications > Development > Ollama"
echo "  • Applications > Development > LM Studio"
echo "  • Applications > System > AI Models Manager"
echo ""

# Test Ollama connection
echo "Testing Ollama connection..."
if curl -s http://localhost:$OLLAMA_PORT/api/tags > /dev/null 2>&1; then
    echo "[✓] Ollama is responding on port $OLLAMA_PORT"
else
    echo "[⚠️] Ollama might still be starting up"
    echo "   Run: systemctl status ollama"
    echo "   Test: curl http://localhost:$OLLAMA_PORT/api/tags"
fi

echo ""
echo "Installation complete! 🎉"
echo ""

# Show correction log summary if there were any issues
if [ -s "$CORRECTION_LOG" ]; then
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "  📋 AI Corrections Applied During Setup"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "Correction log saved to: $CORRECTION_LOG"
    echo ""
    echo "Summary of issues encountered:"
    grep -c "Error:" "$CORRECTION_LOG" && echo " errors detected and handled" || echo " No errors"
    echo ""
    read -p "View detailed correction log? (y/n): " view_log
    if [ "$view_log" = "y" ]; then
        less "$CORRECTION_LOG"
    fi
    echo ""
fi

# Create AI monitoring service for ongoing corrections
echo "[*] Setting up AI monitoring for ongoing corrections..."

cat > /tmp/ai-monitor.service << 'MONITOR_EOF'
[Unit]
Description=HeckOS AI Monitoring Service
After=ollama.service

[Service]
Type=simple
ExecStart=/opt/heckos/ai-models/ai-monitor.sh
Restart=on-failure
RestartSec=60

[Install]
WantedBy=multi-user.target
MONITOR_EOF

# Create monitoring script
cat > "$MODELS_DIR/ai-monitor.sh" << 'MONITOR_SCRIPT_EOF'
#!/bin/bash
# AI Monitoring Service - Watches for system issues and provides corrections

MONITOR_LOG="/var/log/heckos-ai-monitor.log"
CHECK_INTERVAL=300  # 5 minutes

log_message() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$MONITOR_LOG"
}

check_ollama() {
    if ! systemctl is-active --quiet ollama; then
        log_message "⚠️  Ollama service is down, attempting restart..."
        
        # Ask AI for diagnosis if available
        if command -v ollama &> /dev/null; then
            systemctl start ollama
            sleep 3
            if systemctl is-active --quiet ollama; then
                log_message "✓ Ollama restarted successfully"
            else
                log_message "❌ Ollama restart failed, check: journalctl -u ollama"
            fi
        fi
    fi
}

check_models() {
    local model_count=$(ls -1 /opt/heckos/ai-models/shared/ 2>/dev/null | wc -l)
    if [ "$model_count" -eq 0 ]; then
        log_message "⚠️  No models found in shared directory"
        log_message "   Run: /opt/heckos/ai-models/sync-models.sh"
    fi
}

check_disk_space() {
    local usage=$(df /opt/heckos/ai-models/ | tail -1 | awk '{print $5}' | sed 's/%//')
    if [ "$usage" -gt 90 ]; then
        log_message "⚠️  Disk space critical: ${usage}% used"
        log_message "   Consider cleaning old models"
    fi
}

log_message "AI Monitoring Service Started"

while true; do
    check_ollama
    check_models
    check_disk_space
    sleep $CHECK_INTERVAL
done
MONITOR_SCRIPT_EOF

chmod +x "$MODELS_DIR/ai-monitor.sh"

# Install monitoring service (optional)
read -p "Enable AI monitoring service for ongoing corrections? (y/n): " enable_monitor
if [ "$enable_monitor" = "y" ]; then
    $SUDO cp /tmp/ai-monitor.service /etc/systemd/system/
    $SUDO systemctl daemon-reload
    $SUDO systemctl enable ai-monitor.service
    $SUDO systemctl start ai-monitor.service
    echo "[✓] AI monitoring service enabled"
    echo "    Check status: systemctl status ai-monitor"
    echo "    View logs: tail -f /var/log/heckos-ai-monitor.log"
else
    echo "[⚠️] AI monitoring service not enabled"
    echo "    You can enable it later with: systemctl enable ai-monitor.service"
fi
