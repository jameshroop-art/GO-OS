# HeckOS - OS Design & Customization Workflow

## Overview

This guide explains how to design and customize HeckOS before building it into an ISO for installation. It covers launching the design tools, using the editor, AI integration, and customizing the system.

## Quick Start - Launch the OS Designer

### Method 1: Installation Setup GUI (New!)

The recommended way to start designing your OS:

```bash
cd Go-OS
sudo bash ghostos-installation-setup.sh
```

This launches the device type selection GUI. Once you select your target device type, you can proceed to:
1. Choose installation options
2. Configure the OS design
3. Build the customized ISO

### Method 2: ISO Builder GUI (Advanced Customization)

For advanced OS design and customization:

```bash
cd gui/ghostos-iso-builder

# Interactive launcher menu
./launch-menu.sh

# Or launch directly
./start-gui.sh
```

This opens the comprehensive ISO Builder GUI with:
- Multi-ISO source loading
- Theme customization (Gaming/Production modes)
- Component selection
- Repository integration
- Live preview
- Touchscreen keyboard support

### Method 3: Command Line Build

For automated/scripted builds:

```bash
cd Go-OS
sudo bash ghostos-build.sh
```

Select your version (v1.0, v1.1, v2.0) and the build process starts.

## Robust Editor Integration

### Built-in File Editor

The ISO Builder GUI includes a file editor for customizing:

1. **Configuration Files**
   - System configs: `/etc/`
   - User configs: `/home/`
   - Application configs

2. **Script Files**
   - Startup scripts: `/etc/init.d/`
   - User scripts: `~/.bashrc`, `~/.profile`
   - Custom automation

3. **Desktop Files**
   - Applications: `/usr/share/applications/`
   - Shortcuts: `~/.local/share/applications/`
   - Launchers

### External Editor Integration

You can configure your preferred editor:

```bash
# Set in ISO Builder GUI settings
export EDITOR=nano       # or vim, emacs, code, gedit
export VISUAL=$EDITOR
```

Supported editors:
- **nano** - Simple, beginner-friendly
- **vim/nvim** - Advanced, modal editing
- **emacs** - Extensible, powerful
- **VSCode** - Modern IDE with GUI
- **gedit/kate** - Desktop text editors

## AI Integration for Directory Mapping

### AI-Assisted File Organization (Planned Feature)

**Status:** Framework ready, AI models to be integrated

The ISO Builder will support AI-powered features:

#### 1. Intelligent Directory Mapping

```python
# AI will analyze your files and suggest organization
ai_mapper = AIDirectoryMapper()
suggestions = ai_mapper.analyze_project("/path/to/files")

# Example output:
# {
#   "scripts/": ["*.sh", "*.py"],
#   "configs/": ["*.conf", "*.cfg", "*.json"],
#   "docs/": ["*.md", "*.txt", "README*"],
#   "binaries/": ["*.bin", "*.exe"]
# }
```

#### 2. Smart Path Resolution

```python
# AI suggests optimal paths based on Linux FHS
ai_pather = AIPathResolver()
suggestion = ai_pather.suggest_install_path("my-tool")

# Example output:
# /opt/my-tool/          # For custom software
# /usr/local/bin/        # For user-installed binaries
# /etc/my-tool/          # For configuration
```

#### 3. Automatic Link Creation

```python
# AI detects related files and suggests symlinks
ai_linker = AILinkSuggester()
links = ai_linker.find_link_opportunities("/")

# Example output:
# Create symlink: /usr/bin/python3 -> /usr/bin/python
# Create symlink: /etc/nginx/sites-enabled/ -> /etc/nginx/sites-available/
```

### Current AI Integration

While full AI features are being developed, current integration includes:

1. **Pattern Recognition**
   - File type detection
   - Directory structure analysis
   - Dependency mapping

2. **Recommendations**
   - Package suggestions based on usage
   - Theme recommendations
   - Component optimization

3. **Integration with External AI**
   - Configure API keys in ISO Builder settings
   - Support for OpenAI, Anthropic, Hugging Face
   - Local model support (Ollama, LM Studio)

### Enabling AI Features

```bash
# In ISO Builder GUI:
# 1. Go to Settings > AI Integration
# 2. Choose AI provider:
#    - OpenAI (GPT-4, GPT-3.5)
#    - Anthropic (Claude)
#    - Hugging Face (Open models)
#    - Local (Ollama, LM Studio)
# 3. Enter API credentials
# 4. Enable desired features:
#    ☑ Directory mapping
#    ☑ Path suggestions
#    ☑ Auto-linking
#    ☑ Permission optimization
```

## Adding Links and Shortcuts

### Desktop Shortcuts

#### Method 1: Using ISO Builder GUI

1. Open ISO Builder GUI
2. Go to **Custom Files** tab
3. Click **➕ Add Desktop Shortcut**
4. Fill in details:
   - Name: Application name
   - Command: Executable path
   - Icon: Icon file path
   - Categories: Application category
5. Choose installation location:
   - System-wide: `/usr/share/applications/`
   - User-specific: `~/.local/share/applications/`

#### Method 2: Manual Desktop File Creation

Create a `.desktop` file:

```bash
# Example: /usr/share/applications/my-app.desktop
[Desktop Entry]
Name=My Application
Comment=Description of my app
Exec=/usr/local/bin/my-app
Icon=/usr/share/icons/my-app.png
Type=Application
Categories=Utility;Development;
Terminal=false
StartupNotify=true
```

Add to ISO Builder:
1. Click **📄 Add File**
2. Select the `.desktop` file
3. Set destination: `/usr/share/applications/`
4. ☑ Include in Base system

### Symbolic Links

#### Method 1: Using ISO Builder

1. Go to **Advanced** > **Symlink Manager**
2. Click **➕ Create Symlink**
3. Specify:
   - Target: Original file/directory
   - Link: Symlink path
4. Add to build configuration

#### Method 2: In Build Script

Add to custom post-install script:

```bash
# Create symlinks in /opt/custom-scripts/post-install.sh
ln -sf /opt/my-app/bin/app /usr/local/bin/my-app
ln -sf /etc/my-app/config.conf /home/user/.config/my-app.conf
```

Add script to ISO Builder:
1. **📄 Add File** > select script
2. Destination: `/opt/custom-scripts/`
3. Mark as executable
4. Add to post-install hooks

### Panel Launchers (Desktop Environment Specific)

#### MATE Panel
```bash
mate-panel --add-launcher /usr/share/applications/my-app.desktop
```

#### XFCE Panel
```xml
<!-- Add to ~/.config/xfce4/panel/launcher-X/Y.desktop -->
```

#### KDE Plasma
```bash
kwriteconfig5 --file plasma-org.kde.plasma.desktop-appletsrc \
  --group Containments --group 1 --group Applets --key app my-app
```

## User Permission System Customization

### Permission Presets in ISO Builder

The ISO Builder includes preset permission configurations:

1. **Standard User**
   - Basic permissions
   - No sudo access
   - Home directory only

2. **Power User**
   - Extended permissions
   - Selective sudo access
   - System monitoring

3. **Administrator**
   - Full sudo access
   - All system areas
   - Installation rights

4. **Custom**
   - Define your own permission set
   - Fine-grained control
   - Group membership management

### Configuring Permissions

#### In ISO Builder GUI:

1. Go to **System** > **User Permissions**
2. Select or create user
3. Configure:
   - **Groups**: Add user to groups (wheel, sudo, docker, etc.)
   - **Sudo Access**: Define sudoers rules
   - **File Permissions**: Set default umask
   - **Capabilities**: Linux capabilities (CAP_NET_ADMIN, etc.)

#### Sudoers Configuration

```bash
# Add to /etc/sudoers.d/custom-permissions
# User can run specific commands without password
username ALL=(ALL) NOPASSWD: /usr/bin/apt, /usr/bin/systemctl

# User can run any command with password
username ALL=(ALL:ALL) ALL

# Group-based permissions
%powerusers ALL=(ALL) NOPASSWD: /usr/bin/docker, /usr/bin/systemctl restart
```

#### Group Management

```bash
# Common useful groups:
# - sudo: Full administrative access
# - wheel: Alternative admin group
# - docker: Docker container management
# - vboxusers: VirtualBox access
# - libvirt: KVM/QEMU virtual machines
# - audio: Audio device access
# - video: Video device access
# - plugdev: USB device access

# Add user to groups (in post-install script):
usermod -aG sudo,docker,audio,video username
```

#### File Permission Defaults

```bash
# Set default umask in /etc/profile or ~/.bashrc
umask 0022  # Default: rw-r--r-- for files, rwxr-xr-x for directories
umask 0077  # Strict: rw------- for files, rwx------ for directories
```

### SELinux/AppArmor Configuration

For enhanced security:

#### AppArmor (Debian default)

```bash
# Enable AppArmor in ISO build
aa-enforce /etc/apparmor.d/usr.bin.my-app

# Custom profile: /etc/apparmor.d/usr.bin.my-app
#include <tunables/global>

/usr/bin/my-app {
  #include <abstractions/base>
  
  /usr/bin/my-app r,
  /etc/my-app/** r,
  /var/log/my-app/** w,
}
```

#### Polkit Rules

For GUI application permissions:

```javascript
// /etc/polkit-1/rules.d/50-my-app.rules
polkit.addRule(function(action, subject) {
    if (action.id == "org.freedesktop.my-app.elevated" &&
        subject.isInGroup("powerusers")) {
        return polkit.Result.YES;
    }
});
```

### Access Control Lists (ACL)

For fine-grained file permissions:

```bash
# Give user read access to specific file
setfacl -m u:username:r /path/to/file

# Give group write access
setfacl -m g:groupname:rw /path/to/directory

# Set default ACL for new files in directory
setfacl -d -m g:developers:rw /opt/projects/
```

## Complete Workflow Example

### Designing a Custom OS for Development

```bash
# Step 1: Launch ISO Builder
cd gui/ghostos-iso-builder
./start-gui.sh

# Step 2: Load base ISO
# Click "➕ Add ISO" > Select Debian 12 ISO

# Step 3: Select Components
# - ✓ Base system
# - ✓ Development tools (gcc, make, git)
# - ✓ Python development
# - ✓ Docker
# - ✗ Office suite (not needed)
# - ✗ Games (not needed)

# Step 4: Add Custom Files
# Click "📄 Add File" > Add your dotfiles
# - ~/.bashrc
# - ~/.vimrc
# - ~/.gitconfig
# Destination: /etc/skel/ (copies to all new users)

# Step 5: Create Shortcuts
# Click "➕ Add Desktop Shortcut"
# - Name: VSCode
# - Command: /usr/bin/code
# - Icon: /usr/share/icons/vscode.png

# Step 6: Configure Permissions
# Go to System > User Permissions
# - Add default user to: sudo, docker, developers
# - Configure sudo: NOPASSWD for docker commands

# Step 7: Theme Customization
# Go to Theme Editor
# - Mode: Production
# - Scheme: Professional Blue
# - Text scaling: 125% (for 1440p monitor)

# Step 8: AI Optimization (if enabled)
# Click "🤖 AI Optimize"
# - Analyze project structure
# - Apply suggested organization
# - Review and approve changes

# Step 9: Build ISO
# Click "🚀 Build ISO"
# - Output: ~/custom-dev-os.iso
# - Size: ~8GB
# - Build time: ~20-30 minutes

# Step 10: Test in VM
qemu-system-x86_64 -enable-kvm -m 4096 -cdrom ~/custom-dev-os.iso
```

## Advanced Features

### Custom Package Repository

Add your own packages to the ISO:

```bash
# In ISO Builder:
# 1. Go to Advanced > Package Manager
# 2. Click "➕ Add Custom Repository"
# 3. Enter repository URL or add local .deb files
# 4. Select packages to include
```

### Pre-configured Applications

Set application preferences that survive installation:

```bash
# Add config files to ISO:
# VSCode settings: ~/.config/Code/User/settings.json
# Terminal profile: ~/.config/mate-terminal/profiles/
# Firefox profile: ~/.mozilla/firefox/
```

### Automated Post-Install Scripts

Execute scripts after OS installation:

```bash
# Create: /opt/post-install.sh
#!/bin/bash
# Configure system after installation
echo "Running post-install customization..."

# Install additional software
apt update
apt install -y my-favorite-tools

# Configure services
systemctl enable docker
systemctl start docker

# Setup user environment
sudo -u $SUDO_USER git config --global user.name "My Name"
sudo -u $SUDO_USER git config --global user.email "my@email.com"
```

Add to ISO Builder:
1. **📄 Add File** > `/opt/post-install.sh`
2. Mark as executable
3. Add to **Post-Install Hooks**

## Troubleshooting

### ISO Builder Won't Launch

```bash
# Check dependencies
pip install -r gui/ghostos-iso-builder/requirements.txt

# Check Python version
python3 --version  # Should be 3.8+

# Run with debug output
python3 gui/ghostos-iso-builder/main.py --debug
```

### Permission Errors During Build

```bash
# Ensure running with sudo
sudo bash ghostos-build.sh

# Check file permissions
ls -la /home/runner/work/GO-OS/GO-OS/gui/ghostos-iso-builder/
```

### Build Fails

```bash
# Check logs
cat ~/ghostos-ultimate/build/build.log

# Verify disk space (need 50GB+)
df -h

# Retry with clean build
rm -rf ~/ghostos-ultimate/build
sudo bash ghostos-build.sh
```

## Next Steps

After designing your OS:

1. **Build the ISO**: Use the ISO Builder or build script
2. **Test in VM**: Validate in QEMU or VirtualBox
3. **Create Bootable USB**: Use the Installation Setup GUI
4. **Install on Hardware**: Boot from USB and install

For more information:
- **ISO Builder Details**: `gui/ghostos-iso-builder/README.md`
- **Installation Guide**: `Go-OS/INSTALLATION_SETUP_GUIDE.md`
- **Build System**: `Go-OS/GHOSTOS_BUILD_README.md`

## Future Enhancements

Planned AI features:
- **Smart dependency resolution**: AI suggests missing dependencies
- **Conflict detection**: Identifies package conflicts before build
- **Performance optimization**: AI analyzes and optimizes system configuration
- **Security hardening**: Automated security best practices
- **Custom model training**: Learn from your preferences

---

**Version:** 1.0  
**Last Updated:** January 2026  
**License:** MIT (See LICENSE file)
