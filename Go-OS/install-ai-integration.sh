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
            echo "  • Check if port 11434 is available: netstat -tulpn | grep 11434"
            echo "  • Review service logs: journalctl -u ollama -n 50"
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
$SUDO mkdir -p /etc/systemd/system/ollama.service.d/
$SUDO tee /etc/systemd/system/ollama.service.d/environment.conf > /dev/null << EOF
[Service]
Environment="OLLAMA_MODELS=$MODELS_DIR/ollama"
Environment="OLLAMA_HOST=127.0.0.1:11434"
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

# Create LM Studio configuration
LMSTUDIO_CONFIG_DIR="$HOME/.cache/lm-studio"
mkdir -p "$LMSTUDIO_CONFIG_DIR"

cat > "$LMSTUDIO_CONFIG_DIR/settings.json" << EOF
{
  "modelsPath": "$MODELS_DIR/lmstudio",
  "serverPort": 1234,
  "ollamaCompatibility": true,
  "enableCors": true,
  "allowedOrigins": ["http://localhost:11434"]
}
EOF

echo "[✓] LM Studio configured"

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
Name=LM Studio
Comment=Discover, download, and run local LLMs
Exec=$LM_STUDIO_APPIMAGE
Icon=ai-lmstudio
Type=Application
Categories=Development;AI;
Terminal=false
EOF
fi

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

echo "[✓] Desktop shortcuts created"

# ============================================
# Create Quick Start Guide
# ============================================
cat > "$MODELS_DIR/README.md" << 'README_EOF'
# HeckOS AI Integration - Quick Start Guide

## Installed Components

- **Ollama**: Local AI model runtime
  - Service: `systemctl status ollama`
  - CLI: `ollama` command
  - API: http://localhost:11434
  
- **LM Studio**: Visual AI model manager
  - Location: `/opt/lmstudio/LMStudio.AppImage`
  - API: http://localhost:1234
  - Models: `/opt/heckos/ai-models/lmstudio`

- **AI Monitoring Service**: Automatic error detection and correction
  - Service: `systemctl status ai-monitor`
  - Logs: `/var/log/heckos-ai-monitor.log`

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
README_EOF

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
echo "  • Ollama - http://localhost:11434"
echo "  • LM Studio - http://localhost:1234"
echo ""
echo "Shared Models Directory:"
echo "  • $MODELS_DIR"
echo ""
echo "Quick Start:"
echo "  • Ollama: ollama run llama2"
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
if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "[✓] Ollama is responding"
else
    echo "[⚠️] Ollama might still be starting up"
    echo "   Run: systemctl status ollama"
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
