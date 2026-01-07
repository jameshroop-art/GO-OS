# Windows 10 Integration Requirements

## Overview

This document outlines requirements for integrating a Windows 10 compatibility layer into Heck-CheckOS while maintaining Debian 12 as the base system.

## Core Requirements

### Base System
- **Backend**: Debian 12 Edition (unchanged)
- **UI/Desktop**: Debian 12 desktop environment
- **Security**: Maintain all Debian security features
- **Isolation**: Windows layer must be completely isolated

### Windows 10 Layer
- **Type**: Isolated compatibility layer (Wine/Proton or VM)
- **Version**: Windows 10 optimized for performance
- **Updates**: Windows Update capability enabled
- **Purpose**: Smooth running of Windows applications and games

### Network Isolation Requirements

**CRITICAL SECURITY REQUIREMENT:**

1. **Default State**: Windows 10 layer has **ZERO internet access**
   - No network connectivity by default
   - All Windows services blocked from internet
   - All Microsoft telemetry blocked
   - Windows Update blocked (unless specifically enabled)

2. **Exception**: Xbox Game Pass
   - **ONLY** Xbox Game Pass gets internet access
   - Dedicated network route for Game Pass only
   - All other Microsoft services remain blocked
   - Game Pass authentication allowed
   - Game downloads allowed

3. **Implementation**:
   - Network isolation via firewall rules
   - Per-application network permissions
   - Game Pass whitelisted at network layer
   - All other Windows traffic blackholed

### Port Management Requirements

**CRITICAL**: Windows must use different ports than Debian 12 to avoid crashes.

1. **Port Detection**:
   - Scan all ports used by Debian 12
   - Identify services: SSH, HTTP, VNC, X11, databases, etc.
   - Document occupied ports

2. **Port Allocation**:
   - Allocate free ports for Windows services
   - Default Windows ports shifted if occupied
   - RDP: 3390 instead of 3389 (if 3389 used by Debian)
   - VNC: 5910+ instead of 5900+ (if occupied)
   - SPICE: 5920+ instead of 5900+ (if occupied)

3. **Port Manager Tool**:
   - Automatic port scanning
   - Intelligent port allocation
   - Configuration file generation
   - Conflict detection and resolution

**Tool**: `port_manager.py` - Scans Debian 12 ports and allocates free ports for Windows

## Technical Approach

### Constraints (CRITICAL)

**User Requirements**:
- ❌ **NO Wine/Proton** - Wine compatibility layer not allowed
- ❌ **NO Virtual Machine** - No QEMU/KVM, VirtualBox, etc.
- ✅ **Extract Windows 10 ISO** - Use latest Windows 10 build source
- ✅ **Complete Network Isolation** - Zero internet except Game Pass
- ✅ **Debian 12 remains backend** - Base system unchanged

### Problem: Windows Without Wine or VM

**Challenge**: Running Windows applications without Wine or virtualization is technically very difficult on Linux.

### Proposed Alternative Solutions

#### Option 1: Dual-Boot with Network Control (RECOMMENDED)

```
Physical System:
├── GRUB Bootloader
├── Debian 12 (Default boot)
│   ├── Full security features
│   ├── Linux applications
│   └── Controls Windows network access
└── Windows 10 (Separate partition)
    ├── Extracted from ISO
    ├── Network controlled by Debian
    ├── Firewall rules from Debian
    └── Boot via GRUB menu
```

**How Network Isolation Works**:
- Debian 12 controls the network hardware/firmware
- Windows boots with network pre-configured
- Network firewall rules set at hardware/BIOS level
- Only Game Pass domains whitelisted at router/firewall level
- Windows sees network but can only reach whitelisted IPs

**Pros**:
- ✅ True Windows 10 (not VM, not Wine)
- ✅ Full performance (native hardware)
- ✅ Can extract and pre-configure Windows ISO
- ✅ Network can be controlled from Debian
- ✅ Complete isolation via dual-boot

**Cons**:
- ⚠️ Requires reboot to switch OS
- ⚠️ More complex to enforce network rules
- ⚠️ Windows could potentially override settings

#### Option 2: Windows 10 on Bare Metal with Custom Bootloader

```
Custom Boot System:
├── Custom bootloader (GRUB + scripts)
├── Debian 12 partition
├── Windows 10 partition (extracted ISO)
└── Network Filtering Service
    ├── Runs before OS boot
    ├── Configures hardware firewall
    ├── Whitelists Game Pass only
    └── Blocks everything else
```

**Pros**:
- ✅ No VM overhead
- ✅ No Wine compatibility issues
- ✅ Can control network at boot level

**Cons**:
- ⚠️ Very complex to implement
- ⚠️ Difficult to maintain isolation
- ⚠️ Windows updates could break it

#### Option 3: Container-Based Windows (Limited)

**Note**: This is technically challenging and has severe limitations.

Using technologies like:
- LXC/LXD containers (doesn't support Windows)
- Docker with Windows Server Core (limited app support)

**Limitations**:
- ❌ Very limited Windows app compatibility
- ❌ No GUI support
- ❌ No gaming support
- ❌ Most Windows apps won't work

**This option is NOT recommended**.

#### Option 4: ReactOS (Open Source Windows Alternative)

```
Debian 12 (Host)
├── ReactOS (open-source Windows reimplementation)
│   ├── Windows API compatibility
│   ├── Can run some Windows apps
│   ├── Network can be isolated
│   └── No Microsoft telemetry (not real Windows)
```

**Pros**:
- ✅ Open source, no licensing issues
- ✅ Can be tightly integrated with Linux
- ✅ Easy network isolation

**Cons**:
- ❌ **NOT real Windows 10**
- ❌ Limited app compatibility
- ❌ Many modern apps won't work
- ❌ Xbox Game Pass likely won't work

### RECOMMENDED SOLUTION: Dual-Boot with Network Firewall

Given the constraints (no Wine, no VM), the most practical approach is:

**Dual-Boot Setup**:
1. Debian 12 on main partition
2. Windows 10 on separate partition (extracted from ISO)
3. Shared data partition (for file transfer)
4. Network firewall configured from Debian 12
5. GRUB boot menu to select OS

**Network Isolation Strategy**:
```bash
# From Debian 12, configure router/firewall rules
# These rules persist even when Windows boots

# Option A: Configure home router
# - Set MAC-address-based firewall rules
# - Windows MAC only allowed to Game Pass IPs

# Option B: Use hardware firewall appliance
# - Configure before Windows boots
# - Whitelist Game Pass domains only

# Option C: BIOS-level network control
# - Some systems support network filtering in UEFI
# - Configure allowed domains in BIOS
```

## Network Isolation Implementation

### VM Network Configuration (QEMU/KVM)

**Virtual Network Setup**:
```xml
<!-- libvirt network definition -->
<network>
  <name>heckcheckos-windows-isolated</name>
  <forward mode='nat'/>
  <bridge name='virbr-win' stp='on' delay='0'/>
  <ip address='192.168.100.1' netmask='255.255.255.0'>
    <dhcp>
      <range start='192.168.100.2' end='192.168.100.254'/>
    </dhcp>
  </ip>
</network>
```

### Host Firewall Rules (iptables/nftables)

```bash
#!/bin/bash
# Network isolation for Windows 10 VM
# Default: Block ALL traffic from Windows VM

VM_NETWORK="192.168.100.0/24"
VM_IP="192.168.100.2"

# Block all traffic by default
iptables -A FORWARD -s $VM_NETWORK -j DROP

# Allow Xbox Game Pass domains
# These IPs/domains need to be resolved and whitelisted
GAME_PASS_DOMAINS=(
    "xboxlive.com"
    "xbox.com"
    "gamepass.com"
    "xboxservices.com"
    "msftncsi.com"  # Network connectivity check
)

# Convert domains to IPs and whitelist
for domain in "${GAME_PASS_DOMAINS[@]}"; do
    # Allow DNS resolution first
    iptables -A FORWARD -s $VM_IP -p udp --dport 53 -d 8.8.8.8 -j ACCEPT
    iptables -A FORWARD -s $VM_IP -p tcp --dport 53 -d 8.8.8.8 -j ACCEPT
    
    # Allow specific domain traffic
    # Note: This requires DNS-based filtering or IP resolution
done

# Block Microsoft telemetry explicitly
TELEMETRY_DOMAINS=(
    "telemetry.microsoft.com"
    "watson.microsoft.com"
    "vortex.data.microsoft.com"
    "settings-win.data.microsoft.com"
)

for domain in "${TELEMETRY_DOMAINS[@]}"; do
    iptables -A FORWARD -s $VM_IP -d $(host $domain | awk '/has address/ {print $4}') -j DROP 2>/dev/null
done

# Log blocked attempts
iptables -A FORWARD -s $VM_NETWORK -j LOG --log-prefix "WIN-BLOCKED: "
```

### DNS Filtering (Critical for VM)

```bash
# Install and configure dnsmasq for VM
cat > /etc/dnsmasq.d/windows-vm.conf << EOF
# Only allow Game Pass domains
address=/xboxlive.com/
address=/xbox.com/
address=/gamepass.com/
address=/xboxservices.com/

# Block everything else by default
address=/#/0.0.0.0

# Block Microsoft telemetry
address=/telemetry.microsoft.com/0.0.0.0
address=/watson.microsoft.com/0.0.0.0
address=/vortex.data.microsoft.com/0.0.0.0
EOF

# Use dnsmasq as DNS server for VM
# Set in VM network config
```

### VM-Level Firewall (Windows Firewall)

Inside the Windows 10 VM, also configure Windows Firewall:

```powershell
# Block all outbound by default
New-NetFirewallRule -DisplayName "Block All Outbound" `
    -Direction Outbound -Action Block

# Allow only Xbox/Game Pass
New-NetFirewallRule -DisplayName "Allow Xbox Game Pass" `
    -Direction Outbound -Action Allow `
    -RemoteAddress xboxlive.com,xbox.com,gamepass.com

# Block Windows Update explicitly
New-NetFirewallRule -DisplayName "Block Windows Update" `
    -Direction Outbound -Action Block `
    -RemoteAddress windowsupdate.microsoft.com,update.microsoft.com
```

## Integration with ISO Builder

### GUI Integration Options

1. **VM Configuration Tab**
   - Configure Windows 10 VM (QEMU/KVM)
   - Set resource limits (CPU, RAM, disk)
   - Configure network isolation rules
   - Add Game Pass whitelist
   - GPU passthrough options
   - USB device passthrough

2. **Windows 10 VM Settings**
   - VM disk image location
   - ISO installation source
   - VirtIO driver installation
   - Network adapter configuration
   - Display settings (Spice/VNC)

3. **Game Pass Setup**
   - Install Xbox app in VM
   - Configure authentication
   - Enable network access for Game Pass only
   - Test connectivity
   - Download game testing

### ISO Build Process

**Windows 10 ISO Extraction and Integration**:

1. **Obtain Windows 10 ISO (Latest Build)**
   ```bash
   # User provides or script downloads Windows 10 ISO
   # Latest build from Microsoft (e.g., 22H2)
   WIN10_ISO="Win10_22H2_English_x64.iso"
   ```

2. **Extract Windows 10 ISO**
   ```bash
   # Mount Windows ISO
   mkdir -p /tmp/win10-mount
   mount -o loop $WIN10_ISO /tmp/win10-mount
   
   # Extract install.wim (main Windows image)
   mkdir -p /tmp/win10-extracted
   cp -r /tmp/win10-mount/* /tmp/win10-extracted/
   
   # Get install.wim
   INSTALL_WIM="/tmp/win10-extracted/sources/install.wim"
   ```

3. **Create Optimized Windows VM Image**
   ```bash
   # Create QEMU disk image
   qemu-img create -f qcow2 windows10.qcow2 80G
   
   # Install Windows from extracted ISO
   virt-install \
     --name heckcheckos-windows10 \
     --memory 8192 \
     --vcpus 4 \
     --disk path=windows10.qcow2,format=qcow2 \
     --cdrom $WIN10_ISO \
     --os-variant win10 \
     --network network=isolated,model=virtio \
     --graphics spice \
     --autostart
   ```

4. **Optimize Windows Installation**
   ```bash
   # Inside Windows VM (automated with scripts):
   # - Disable telemetry
   # - Disable unnecessary services
   # - Install VirtIO drivers
   # - Install Xbox Game Pass
   # - Configure network to be blocked
   # - Install required runtimes (DirectX, .NET, etc.)
   # - Optimize for performance
   # - Create snapshot of clean state
   ```

5. **Include in Heck-CheckOS ISO**
   ```bash
   # Compress Windows VM image
   qemu-img convert -O qcow2 -c windows10.qcow2 windows10-compressed.qcow2
   
   # Include in Heck-CheckOS ISO build
   mkdir -p iso-build/opt/ghostos/windows/
   cp windows10-compressed.qcow2 iso-build/opt/ghostos/windows/
   cp vm-launcher.sh iso-build/usr/local/bin/
   
   # Add to ISO
   mkisofs -o Heck-CheckOS-with-Windows.iso iso-build/
   ```

6. **Pre-configure Network Isolation**
   - Include firewall rules in ISO
   - Configure dnsmasq for DNS filtering
   - Create VM network definition
   - Install monitoring scripts

7. **Pre-install Required Packages**
   ```bash
   # Include in Heck-CheckOS ISO:
   apt-get install qemu-system-x86 libvirt-daemon-system \
                   libvirt-clients bridge-utils virtinst \
                   dnsmasq iptables-persistent
   
   # Install VirtIO drivers ISO
   wget https://fedorapeople.org/groups/virt/virtio-win/direct-downloads/latest-virtio/virtio-win.iso
   ```

8. **Create Launcher Scripts**
   - Desktop shortcut for Windows VM
   - Command-line launcher
   - Network isolation enforcer
   - Xbox Game Pass launcher

9. **Include Documentation**
   - How to start Windows VM
   - Network isolation explanation
   - Game Pass setup guide
   - Troubleshooting tips

10. **Final ISO Composition**
    ```
    Heck-CheckOS ISO:
    ├── Debian 12 base system
    ├── /opt/ghostos/windows/
    │   ├── windows10.qcow2 (pre-installed Windows)
    │   ├── vm-config.xml (libvirt definition)
    │   └── network-rules.sh (firewall config)
    ├── /usr/local/bin/
    │   ├── start-windows-vm
    │   ├── stop-windows-vm
    │   └── gamepass-launcher
    └── Desktop entries for easy access
    ```

## Configuration Files

### Windows VM Config

```json
{
  "vm_name": "Heck-CheckOS-Windows10",
  "os_type": "win10",
  "memory": "8192",
  "cpus": 4,
  "disk_size": "60G",
  "network": {
    "mode": "isolated",
    "whitelist": [
      "xboxlive.com",
      "gamepass.com",
      "xbox.com"
    ],
    "blacklist": [
      "telemetry.microsoft.com",
      "watson.microsoft.com",
      "*.msn.com",
      "bing.com"
    ]
  }
}
```

### Firewall Rules Config

```yaml
network_isolation:
  enabled: true
  default_policy: DROP
  
  whitelisted_services:
    - name: "Xbox Game Pass"
      domains:
        - "*.xboxlive.com"
        - "*.xbox.com"
        - "*.gamepass.com"
      ports: [80, 443]
  
  blacklisted_services:
    - "Windows Update"
    - "Microsoft Telemetry"
    - "Cortana"
    - "Edge Browser"
```

## User Interface Requirements

### Settings Panel: Windows Integration

```
[Windows 10 Virtual Machine]

Status: ○ Not Installed  ● Installed  ○ Running

VM Configuration:
RAM: [8 GB] ━━━━━━●━━━━ (slider: 4-16 GB)
CPU Cores: [4] ━━━●━━━━ (slider: 2-8 cores)
Disk Space: [80 GB] (input)

Display:
○ VNC (Remote access)
● Spice (Better performance)
○ GPU Passthrough (Requires compatible GPU)

Network Isolation:
[✓] Enable network isolation (REQUIRED)
[ ] Allow Windows Update (Not recommended)

Game Pass Network Access:
[✓] Allow Xbox Game Pass internet access
    Whitelisted domains:
    • xboxlive.com
    • xbox.com  
    • gamepass.com
    
[✓] Block all other Microsoft services
[✓] Block Windows telemetry

[Create VM] [Start VM] [Configure Advanced]
```

### Launcher Integration

```
Applications Menu:
├── Debian Applications (Linux native)
├── Windows 10 VM
│   ├── [▶] Start Windows 10 VM
│   ├── [⏸] Pause VM
│   ├── [⏹] Stop VM
│   └── [⚙] VM Settings
├── Windows Applications (in VM)
│   ├── MS Office (via VM)
│   ├── Adobe Apps (via VM)
│   └── Windows Games (offline in VM)
└── Xbox Game Pass (in VM, with internet)
    ├── Launch Game Pass
    └── (Opens VM with network access)
```

## Security Considerations

### Isolation Layers

1. **Network Layer**: VM isolated network with strict firewall
2. **VM Isolation**: Complete hardware virtualization boundary
3. **Filesystem Layer**: Separate VM disk image (qcow2)
4. **Process Layer**: VM runs in isolated process space
5. **Memory Layer**: VM has dedicated memory allocation

### Monitoring

- Log all network attempts from Windows layer
- Alert on unauthorized network access
- Monitor Game Pass traffic (ensure only Game Pass)
- Regular security audits

### Threat Model

**Threats Mitigated**:
- Windows telemetry to Microsoft
- Unwanted Windows Update
- Malware phone-home attempts
- Privacy violations from MS services

**Remaining Risks**:
- Game Pass app itself (trusted)
- GPU drivers (needed for gaming)
- Games downloaded via Game Pass

## Implementation Priority

### Phase 1: QEMU/KVM Setup
- [ ] Add QEMU/KVM to ISO build
- [ ] Include libvirt packages
- [ ] Include VirtIO drivers
- [ ] Create VM definition templates
- [ ] Test VM creation and boot

### Phase 2: Network Isolation
- [ ] Implement firewall rules
- [ ] Configure dnsmasq DNS filtering  
- [ ] Block all Windows network by default
- [ ] Test isolation effectiveness

### Phase 3: Game Pass Integration
- [ ] Create Windows 10 VM
- [ ] Install Windows in VM
- [ ] Install Xbox app in VM
- [ ] Configure Game Pass whitelist
- [ ] Test Game Pass connectivity
- [ ] Verify other services blocked

### Phase 4: GUI Integration
- [ ] Add Windows VM settings panel to ISO Builder
- [ ] VM configuration options
- [ ] Network rules management
- [ ] VM launcher scripts
- [ ] Testing and validation tools

## Testing Requirements

### Network Isolation Tests

1. **Verify Default Block**:
   ```bash
   # Inside Windows 10 VM, should fail:
   ping google.com
   curl microsoft.com
   Test-NetConnection -ComputerName google.com
   ```

2. **Verify Game Pass Access**:
   ```bash
   # From Xbox app in VM, should succeed:
   Test-NetConnection -ComputerName xboxlive.com -Port 443
   nslookup gamepass.com
   ```

3. **Verify Telemetry Block**:
   ```bash
   # Should be blocked:
   Test-NetConnection -ComputerName telemetry.microsoft.com
   ping vortex.data.microsoft.com
   ```

4. **Monitor VM Network**:
   ```bash
   # On Debian host, monitor VM traffic:
   tcpdump -i virbr-win -n
   # Should only see Game Pass traffic
   ```

### Functional Tests

- [ ] VM creates successfully
- [ ] Windows 10 installs properly
- [ ] VM boots and runs
- [ ] Windows apps launch successfully
- [ ] Games run with good performance
- [ ] Game Pass authentication works
- [ ] Game downloads succeed
- [ ] Other network access fails
- [ ] Debian 12 unaffected by VM
- [ ] VM can be paused/resumed
- [ ] VM snapshots work
- [ ] GPU passthrough (if enabled)

## Documentation Needs

- [ ] User guide for Windows layer
- [ ] Network isolation explanation
- [ ] Game Pass setup guide
- [ ] Troubleshooting guide
- [ ] Security implications document

## Related Files

This requirement affects:
- `gui/heckcheckos-iso-builder/` - Need Windows integration tab
- `Go-OS/heckcheckos-build.sh` - Need Wine/VM packages
- Firewall configuration scripts
- Desktop launchers

## Future Enhancements

- [ ] Multiple Wine prefixes (32-bit, 64-bit)
- [ ] DirectX 12 support via VKD3D
- [ ] Proton integration for Steam games
- [ ] Windows 11 option
- [ ] GPU passthrough for VM
- [ ] Per-game network rules

## Notes

- This is separate from the touchscreen keyboard work
- Should be implemented after keyboard PR is merged
- Requires significant testing for security
- May need legal review for license compliance
- User should understand isolation implications

---

**Status**: Requirements documented, implementation pending

**Priority**: High (user requested feature)

**Complexity**: High (security + compatibility)

**Estimated Effort**: 2-3 weeks development + testing
