# HeckOS AI Integration with Error Correction

## Overview

The HeckOS AI Integration installer includes intelligent error correction powered by both Ollama and LM Studio. During setup, if any step fails, the AI systems can analyze the error and provide actionable solutions.

## Key Features

### 1. Port Lifecycle Management (NEW!)
- **Automatic port allocation** from range 51511-51611
- **Temporary port assignments** - only active during service runtime
- **Auto-release on stop** - ports freed when services/apps exit
- **Port registry tracking** - all allocations logged and managed
- Sequential port selection for conflict-free setup
- Option to kill processes on target ports
- Interactive port conflict resolution
- Dynamic configuration follows port assignments

### 2. AI-Assisted Error Detection
- Automatically detects errors during installation
- Captures error context and stack traces
- Logs all issues for later review

### 3. Intelligent Correction Suggestions
- Uses local Ollama models for analysis (when available)
- Provides fallback rule-based suggestions
- Offers multiple resolution options
- Interactive correction flow

### 4. Shared Model Access
- Both Ollama and LM Studio can access each other's models
- Automatic model syncing between systems
- Unified model directory structure
- Cross-compatibility for corrections

### 5. Continuous Monitoring
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
3. **Allocate unused ports (51511-51611 range)**
4. **Register ports with lifecycle management**
5. Configure shared model access
6. Enable AI error correction
7. Set up monitoring (optional)

### What Happens During Installation

```
🤖 Installing Ollama...
  ✓ Downloaded and installed
  ✓ Port allocated and registered
  ✓ Service started with auto-release hook
  ✓ Configured for shared models

🤖 Installing LM Studio...
  ✓ AppImage downloaded
  ✓ Port allocated and registered
  ✓ Wrapper created with auto-release trap
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

🔒 Port lifecycle management...
  ✓ Port registry initialized
  ✓ Cleanup script installed
  ✓ Auto-release hooks configured
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

## Port Management

### Automatic Port Allocation

The installer automatically manages ports to avoid conflicts:

**Default Ports:**
- Ollama: 11434 (preferred)
- LM Studio: 1234 (preferred)

**Fallback Range:**
- Ports 51511-51611 (sequential allocation)

**Port Lifecycle:**
- Ports are **temporary** - only active during service runtime
- **Auto-release** when service stops or app exits
- Registry tracks all allocations
- Configuration follows port assignments

### Port Allocation Process

When a preferred port is in use:

```
[*] Allocating port for Ollama...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[*] Checking preferred port 11434...
[!] Preferred port 11434 is in use

Options:
  1) Kill process on port 11434 and use it
  2) Find unused port in range 51511-51611
  3) Enter custom port number

Choose option [1-3]:
```

### Option 1: Kill Process on Port

```bash
[*] Checking for processes on port 11434...
[!] Found process(es) using port 11434: 12345

Kill these processes? (y/n): y
[✓] Killed process 12345
[✓] Using port: 11434
[✓] Port registered with auto-release hook
```

### Option 2: Sequential Port Search

```bash
[*] Searching for unused port in range 51511-51611...
[✓] Found unused port: 51511
[✓] Ollama will use port: 51511
[✓] Port registered with auto-release hook
```

The script searches sequentially (51511, 51512, 51513...) until finding an available port.

### Option 3: Custom Port

```bash
Enter port number: 8080
[*] Checking for processes on port 8080...
[✓] Port 8080 is available
[✓] Using custom port: 8080
```

### After Installation

Check allocated ports:
```bash
# Ollama port
grep OLLAMA_HOST /etc/systemd/system/ollama.service.d/environment.conf

# LM Studio port
grep serverPort ~/.cache/lm-studio/settings.json

# Test connections
curl http://localhost:<ollama-port>/api/tags
curl http://localhost:<lmstudio-port>/v1/models
```

## Port Lifecycle Management

### How It Works

**Registration:**
When a service starts, its port is registered:
```bash
# Format in /var/run/heckos-ports.registry:
service|port|pid|timestamp|config_path

# Example:
ollama|51511|12345|1705310400|/etc/systemd/system/ollama.service.d/environment.conf
lmstudio|51512|12346|1705310401|/home/user/.cache/lm-studio/settings.json
```

**Auto-Release Mechanisms:**

1. **Ollama (systemd-managed):**
   ```bash
   # ExecStopPost in service config
   ExecStopPost=/opt/heckos/ai-models/port-cleanup.sh cleanup ollama <port>
   ```
   - Port released automatically when service stops
   - Registry entry removed
   - Port becomes available immediately

2. **LM Studio (wrapper-managed):**
   ```bash
   # Wrapper script with trap
   trap cleanup EXIT INT TERM
   cleanup() {
       /opt/heckos/ai-models/port-cleanup.sh cleanup lmstudio $PORT
   }
   ```
   - Port released when app exits (normal or forced)
   - Works with Ctrl+C, kill signals, or clean exit
   - Registry updated immediately

### View Active Ports

**Command line:**
```bash
# View registry
cat /var/run/heckos-ports.registry

# Example output:
ollama|51511|12345|1705310400|/etc/systemd/system/ollama.service.d/environment.conf
lmstudio|51512|0|1705310401|/home/user/.cache/lm-studio/settings.json

# Check if specific port is registered
grep "|51511|" /var/run/heckos-ports.registry
```

**GUI:**
```bash
# Launch Port Manager
# Applications > System > AI Port Manager

# Or manually:
x-terminal-emulator -e "bash -c 'cat /var/run/heckos-ports.registry; read'"
```

### Cleanup Operations

**Automatic cleanup on service stop:**
```bash
# Ollama stops
sudo systemctl stop ollama
# → Port automatically released
# → Registry entry removed
# → Port 51511 now available

# LM Studio exits
# User closes app or Ctrl+C
# → Wrapper trap catches exit
# → Port automatically released
# → Registry entry removed
```

**Manual cleanup (if needed):**
```bash
# Cleanup specific service
sudo /opt/heckos/ai-models/port-cleanup.sh cleanup ollama 51511

# Cleanup all stale ports (where process no longer exists)
sudo /opt/heckos/ai-models/port-cleanup.sh check

# View cleanup script
cat /opt/heckos/ai-models/port-cleanup.sh
```

### Port Reuse

Ports are immediately available after release:

```bash
# Service A using port 51511
ollama|51511|12345|...

# Service A stops
# Port 51511 released from registry

# Service B can now use port 51511
# No conflicts, no manual intervention
```

### Configuration Follows Port

When a port is allocated, configuration is automatically updated:

**Ollama:**
```bash
# Port allocated: 51511
# Configuration updated:
Environment="OLLAMA_HOST=127.0.0.1:51511"

# Service can start immediately
# API available at http://localhost:51511
```

**LM Studio:**
```json
// Port allocated: 51512
// Configuration updated:
{
  "serverPort": 51512,
  ...
}

// App uses correct port on startup
// API available at http://localhost:51512
```

### Benefits

- ✅ **Temporary allocation** - Ports only used when needed
- ✅ **Automatic cleanup** - No manual intervention required
- ✅ **No resource leaks** - Ports always released properly
- ✅ **Immediate reuse** - Stopped service frees port instantly
- ✅ **Crash-safe** - Cleanup works even with forced termination
- ✅ **Configuration sync** - Settings always match allocated port

### Changing Ports Post-Installation

**Change Ollama Port:**
```bash
# Edit configuration
sudo nano /etc/systemd/system/ollama.service.d/environment.conf

# Change line to:
Environment="OLLAMA_HOST=127.0.0.1:<new-port>"

# Restart service
sudo systemctl daemon-reload
sudo systemctl restart ollama
```

**Change LM Studio Port:**
```bash
# Edit configuration
nano ~/.cache/lm-studio/settings.json

# Change:
"serverPort": <new-port>

# Restart LM Studio
```

### Manual Port Management

**Find process using a port:**
```bash
sudo lsof -ti:<port>
# or
sudo fuser <port>/tcp
# or
sudo netstat -tulpn | grep :<port>
```

**Kill process on port:**
```bash
sudo kill -9 $(sudo lsof -ti:<port>)
```

**Check if port is available:**
```bash
# Should return nothing if port is free
netstat -tuln | grep :<port>
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
