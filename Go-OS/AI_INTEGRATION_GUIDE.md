# HeckOS AI Integration with Error Correction

## Overview

The HeckOS AI Integration installer includes intelligent error correction powered by both Ollama and LM Studio. During setup, if any step fails, the AI systems can analyze the error and provide actionable solutions.

## Key Features

### 1. AI-Assisted Error Detection
- Automatically detects errors during installation
- Captures error context and stack traces
- Logs all issues for later review

### 2. Intelligent Correction Suggestions
- Uses local Ollama models for analysis (when available)
- Provides fallback rule-based suggestions
- Offers multiple resolution options
- Interactive correction flow

### 3. Shared Model Access
- Both Ollama and LM Studio can access each other's models
- Automatic model syncing between systems
- Unified model directory structure
- Cross-compatibility for corrections

### 4. Continuous Monitoring
- Optional AI monitoring service
- Automatic health checks
- Proactive problem detection
- Self-healing capabilities

## Installation

### Quick Install

```bash
cd Go-OS
sudo bash install-ai-integration.sh
```

The script will:
1. Install Ollama
2. Install LM Studio  
3. Configure shared model access
4. Enable AI error correction
5. Set up monitoring (optional)

### What Happens During Installation

```
🤖 Installing Ollama...
  ✓ Downloaded and installed
  ✓ Service started
  ✓ Configured for shared models

🤖 Installing LM Studio...
  ✓ AppImage downloaded
  ✓ Configured for model sharing
  ✓ API endpoints configured

🔗 Setting up model sharing...
  ✓ Created shared directory
  ✓ Symlinks configured
  ✓ Cross-access enabled

🤖 Enabling AI corrections...
  ✓ Error handling active
  ✓ Correction log created
  ✓ Interactive mode enabled
```

## Error Correction in Action

### Example 1: Service Failure

```bash
[1/4] Installing Ollama...
❌ Error: Failed to start Ollama service

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  🤖 AI Error Correction Activated
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[AI] Analyzing error with local AI model...

AI Suggestion:
• Port 11434 is likely already in use
• Check running services: netstat -tulpn | grep 11434
• Solution: Kill conflicting process or change Ollama port
  Run: sudo systemctl stop ollama && sudo systemctl start ollama

Options:
  1) Retry the step
  2) Skip this step and continue
  3) Apply suggested fix and retry
  4) Exit setup

Choose option [1-4]: 3

[*] Please apply the suggested fix, then press Enter to retry
[Manual fix applied]
[*] Retrying step: service_start
✓ Ollama service started successfully
```

### Example 2: Download Failure

```bash
[2/4] Installing LM Studio...
❌ Error: Failed to download LM Studio

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Common Solutions:
  • Check internet connection: ping -c 3 lmstudio.ai
  • Verify wget is installed: apt-get install wget
  • Try manual download from: https://lmstudio.ai/
  • Check disk space: df -h

Options:
  1) Retry the step
  2) Skip this step and continue
  3) Apply suggested fix and retry
  4) Exit setup

Choose option [1-4]: 1

[*] Retrying step: lmstudio_download
✓ LM Studio downloaded successfully
```

### Example 3: Permission Error

```bash
[3/4] Setting up model sharing...
❌ Error: Permission denied creating symlinks

[AI] Analyzing error...

AI Suggestion:
• Directory permissions issue detected
• Current user may not have write access
• Fix: sudo chown -R $USER:$USER /opt/heckos/ai-models/
• Or run entire script with sudo

Options:
  1) Retry the step
  2) Skip this step and continue
  3) Apply suggested fix and retry
  4) Exit setup

Choose option [1-4]: 3

[Manual fix: sudo chown -R $USER:$USER /opt/heckos/ai-models/]
[*] Retrying step: permissions
✓ Model sharing configured successfully
```

## How AI Corrections Work

### 1. Error Detection

When a step fails, the script:
- Captures the exit code
- Records the error message
- Notes the context and step name
- Logs to `/tmp/heckos-ai-corrections.log`

### 2. AI Analysis

If Ollama is available:
```python
Prompt: "You are a Linux system administrator AI assistant.
An error occurred during HeckOS AI integration setup.

Step: ollama_install
Error: curl: (7) Failed to connect to ollama.com port 443
Context: Downloading from ollama.com

Provide a concise fix suggestion (max 3 bullet points)."

Response: 
• Check internet connection (ping 8.8.8.8)
• Verify DNS resolution (nslookup ollama.com)
• Try alternative mirror or manual download
```

If Ollama is not available, uses rule-based fallbacks.

### 3. Interactive Resolution

User chooses:
1. **Retry** - Attempt the step again immediately
2. **Skip** - Continue without this component
3. **Apply Fix** - Manually fix, then retry
4. **Exit** - Cancel installation

### 4. Logging

All errors and corrections are logged:
```bash
[2026-01-14 05:30:15] Step: ollama_install | Error: Connection failed | Context: curl download
[AI Suggestion] Check network, try mirror
[User Action] Applied fix and retried
[Result] Success on retry
```

## Ongoing AI Monitoring

### Enable Monitoring Service

After installation, optionally enable continuous monitoring:

```bash
sudo systemctl enable ai-monitor.service
sudo systemctl start ai-monitor.service
```

### What It Monitors

Every 5 minutes, checks:
- **Ollama Service**: Is it running?
- **Model Availability**: Are models accessible?
- **Disk Space**: Is storage running low?
- **API Health**: Are endpoints responding?

### Automatic Corrections

The monitor can:
- Restart failed services
- Clean up old logs
- Sync models automatically
- Alert on critical issues

### View Monitor Logs

```bash
# Real-time monitoring
tail -f /var/log/heckos-ai-monitor.log

# Check service status
systemctl status ai-monitor

# Recent corrections
grep "Correction:" /var/log/heckos-ai-monitor.log
```

## Model Sharing Between Ollama and LM Studio

### Shared Directory Structure

```
/opt/heckos/ai-models/
├── ollama/           # Ollama-specific models
│   ├── llama2
│   ├── codellama
│   └── mistral
├── lmstudio/         # LM Studio models
│   ├── llama-2-7b.gguf
│   └── codellama-13b.gguf
└── shared/           # Symlinks to all models
    ├── llama2 -> ../ollama/llama2
    ├── codellama -> ../ollama/codellama
    ├── llama-2-7b.gguf -> ../lmstudio/llama-2-7b.gguf
    └── codellama-13b.gguf -> ../lmstudio/codellama-13b.gguf
```

### How Sharing Works

1. **Ollama downloads a model** → Automatically accessible to LM Studio
2. **LM Studio downloads a model** → Automatically accessible to Ollama
3. **Sync script** creates bidirectional symlinks
4. **Both systems** see all models

### Manual Sync

If models aren't syncing automatically:

```bash
sudo /opt/heckos/ai-models/sync-models.sh
```

### Using Shared Models

**In Ollama:**
```bash
ollama list  # Shows all models including LM Studio's
ollama run llama-2-7b  # Can run LM Studio model
```

**In LM Studio:**
- Open LM Studio GUI
- Navigate to Models tab
- Ollama models appear in list
- Can load and use any model

## Advanced Configuration

### Change Model Directory

Edit `/etc/systemd/system/ollama.service.d/environment.conf`:
```ini
[Service]
Environment="OLLAMA_MODELS=/path/to/new/models"
```

Then:
```bash
sudo systemctl daemon-reload
sudo systemctl restart ollama
```

### Disable AI Corrections

Edit `install-ai-integration.sh`:
```bash
AI_CORRECTION_ENABLED=false
```

### Use Different AI Model for Corrections

If you want to use a specific model for error analysis:
```bash
# In the script, change:
ollama run llama2 "$ai_prompt"
# To:
ollama run mistral "$ai_prompt"  # Or any other model
```

### Configure Monitoring Interval

Edit `/opt/heckos/ai-models/ai-monitor.sh`:
```bash
CHECK_INTERVAL=300  # Change to desired seconds
```

## Troubleshooting

### AI Corrections Not Working

```bash
# Check if Ollama is running
systemctl status ollama

# Verify Ollama can respond
ollama list

# Check correction log
cat /tmp/heckos-ai-corrections.log

# Test AI query manually
ollama run llama2 "Test query"
```

### Models Not Sharing

```bash
# Check directory permissions
ls -la /opt/heckos/ai-models/

# Fix permissions
sudo chown -R $USER:$USER /opt/heckos/ai-models/

# Run sync manually
sudo /opt/heckos/ai-models/sync-models.sh

# Verify symlinks
ls -la /opt/heckos/ai-models/shared/
```

### Monitoring Service Issues

```bash
# Check service status
systemctl status ai-monitor

# View service logs
journalctl -u ai-monitor -f

# Restart service
sudo systemctl restart ai-monitor

# Check script permissions
ls -la /opt/heckos/ai-models/ai-monitor.sh
```

## Use Cases

### 1. Development Environment Setup
- Install on developer laptop/desktop
- Use Ollama for quick CLI queries
- Use LM Studio for longer context tasks
- Share models to save disk space

### 2. Server Deployment
- Install on localhost server
- Ollama for API services
- LM Studio for admin tasks
- AI monitoring for 24/7 operation

### 3. Testing and Experimentation
- Try different models easily
- Compare Ollama vs LM Studio performance
- Use AI corrections during setup
- Quick model switching

## Benefits

### AI-Powered Error Handling
- ✅ Faster problem resolution
- ✅ Learn from errors (logged for review)
- ✅ Less manual intervention needed
- ✅ Guided troubleshooting

### Model Sharing
- ✅ Save disk space (no duplicate models)
- ✅ Use best tool for each task
- ✅ Seamless switching
- ✅ Unified model management

### Continuous Monitoring
- ✅ Proactive issue detection
- ✅ Automatic service recovery
- ✅ System health tracking
- ✅ Peace of mind

## Security Considerations

- All AI processing happens **locally on localhost**
- No data sent to external servers
- Models stored in controlled directory
- Service runs with minimal privileges
- Logs contain no sensitive data

## Performance

- **Memory**: ~2-4GB for small models
- **CPU**: Varies by model (GPU recommended)
- **Disk**: ~10-50GB for model storage
- **Network**: Only for initial downloads

## Getting Help

If you encounter issues:

1. Check correction log: `/tmp/heckos-ai-corrections.log`
2. View monitor log: `/var/log/heckos-ai-monitor.log`
3. Review service status: `systemctl status ollama ai-monitor`
4. Consult AI: Ask Ollama for help with specific errors

## Next Steps

After installation:
1. Download your first model: `ollama pull llama2`
2. Test Ollama: `ollama run llama2 "Hello!"`
3. Launch LM Studio: `/opt/lmstudio/LMStudio.AppImage`
4. Verify model sharing: `ls -la /opt/heckos/ai-models/shared/`
5. Enable monitoring: `sudo systemctl enable ai-monitor`

---

**AI-Powered Installation Made Easy!** 🤖✨

The combination of Ollama and LM Studio with AI-assisted error correction provides a robust, self-healing installation process on localhost.
