#!/usr/bin/env python3
"""
Windows Process Isolator - Strips Windows 10 VM to minimal driver-only processes
Eliminates bloat and isolates only driver management functions

LICENSE: MIT (see LICENSE file in repository root)
"""

import json
from typing import Dict, List, Set

# Essential Windows processes for driver operations ONLY
ESSENTIAL_DRIVER_PROCESSES = {
    # Core system
    'System',
    'smss.exe',           # Session Manager
    'csrss.exe',          # Client/Server Runtime
    'wininit.exe',        # Windows Initialization
    'services.exe',       # Service Control Manager
    'lsass.exe',          # Local Security Authority
    
    # Driver-specific
    'DriverStore',        # Driver installation service
    'PnPUtil.exe',        # Plug and Play utility
    'devcon.exe',         # Device Console (driver management)
    'setupapi.dll',       # Setup API for device installation
    
    # Minimal support
    'svchost.exe',        # Service Host (minimal instances only)
    'dllhost.exe',        # COM surrogate (for driver COM operations)
    'RuntimeBroker.exe',  # Minimal runtime for driver APIs
}

# Windows services to KEEP (driver-related only)
ESSENTIAL_SERVICES = {
    'PlugPlay',           # Plug and Play - CRITICAL for drivers
    'DeviceInstall',      # Device Installation Service
    'DeviceSetupManager', # Device Setup Manager
    'DcomLaunch',         # DCOM Server Process Launcher (for driver COM)
    'RpcSs',              # Remote Procedure Call (for our RPC layer)
    'RpcEptMapper',       # RPC Endpoint Mapper
    'SENS',               # System Event Notification Service
    'EventLog',           # Windows Event Log (for driver diagnostics)
    'WinMgmt',            # Windows Management Instrumentation (driver queries)
    'CryptSvc',           # Cryptographic Services (driver signatures)
}

# Windows services to DISABLE (bloat removal)
DISABLE_SERVICES = {
    # Windows Update (not needed in isolated VM)
    'wuauserv',
    'UsoSvc',
    'WaaSMedicSvc',
    
    # Telemetry (privacy)
    'DiagTrack',
    'dmwappushservice',
    
    # Cortana/Search
    'WSearch',
    
    # Windows Defender (lightweight VM doesn't need it)
    'WinDefend',
    'SecurityHealthService',
    'WdNisSvc',
    
    # Store
    'InstallService',
    'LicenseManager',
    
    # Xbox
    'XblAuthManager',
    'XblGameSave',
    'XboxGipSvc',
    'XboxNetApiSvc',
    
    # OneDrive
    'OneSyncSvc',
    
    # Superfetch/Prefetch (not needed in minimal VM)
    'SysMain',
    
    # Print Spooler (no printing in driver VM)
    'Spooler',
    
    # Themes (headless VM)
    'Themes',
    
    # Windows Time (not critical)
    'W32Time',
    
    # Remote Desktop (using RPC instead)
    'TermService',
    'SessionEnv',
    
    # Bluetooth (if not managing BT drivers)
    'bthserv',
    
    # Windows Media (not needed)
    'WMPNetworkSvc',
    
    # HomeGroup (deprecated)
    'HomeGroupListener',
    'HomeGroupProvider',
    
    # Geolocation (not needed)
    'lfsvc',
}


class WindowsProcessIsolator:
    """
    Isolates Windows 10 to driver-only processes
    Strips unnecessary services and bloat
    """
    
    def __init__(self):
        """Initialize process isolator"""
        self.essential_processes = ESSENTIAL_DRIVER_PROCESSES
        self.essential_services = ESSENTIAL_SERVICES
        self.disable_services = DISABLE_SERVICES
    
    def generate_service_config(self) -> str:
        """
        Generate Windows service configuration script
        PowerShell script to disable bloat and enable only driver services
        
        Returns:
            PowerShell script content
        """
        script = """# Windows 10 Driver VM - Service Isolation Script
# Disables bloat, keeps only driver-related services
# Run as Administrator in the VM

Write-Host "Isolating Windows processes for driver operations..." -ForegroundColor Cyan
Write-Host "This will disable non-essential services to minimize VM footprint." -ForegroundColor Yellow
Write-Host ""

# Disable bloat services
$servicesToDisable = @(
"""
        
        # Add services to disable
        for service in sorted(self.disable_services):
            script += f'    "{service}",\n'
        
        script += """)

foreach ($service in $servicesToDisable) {
    try {
        $svc = Get-Service -Name $service -ErrorAction SilentlyContinue
        if ($svc) {
            Write-Host "Disabling: $service" -ForegroundColor Gray
            Stop-Service -Name $service -Force -ErrorAction SilentlyContinue
            Set-Service -Name $service -StartupType Disabled -ErrorAction SilentlyContinue
        }
    } catch {
        # Service might not exist, ignore
    }
}

# Ensure essential driver services are running
$essentialServices = @(
"""
        
        # Add essential services
        for service in sorted(self.essential_services):
            script += f'    "{service}",\n'
        
        script += """)

foreach ($service in $essentialServices) {
    try {
        $svc = Get-Service -Name $service -ErrorAction SilentlyContinue
        if ($svc) {
            Write-Host "Ensuring essential: $service" -ForegroundColor Green
            Set-Service -Name $service -StartupType Automatic -ErrorAction SilentlyContinue
            Start-Service -Name $service -ErrorAction SilentlyContinue
        }
    } catch {
        Write-Host "Warning: Could not configure $service" -ForegroundColor Yellow
    }
}

Write-Host ""
Write-Host "Process isolation complete!" -ForegroundColor Green
Write-Host "VM is now optimized for driver operations only." -ForegroundColor Cyan
Write-Host ""
Write-Host "Lightweight metrics:" -ForegroundColor White
Write-Host "  - Disabled services: $($servicesToDisable.Count)" -ForegroundColor Gray
Write-Host "  - Essential services: $($essentialServices.Count)" -ForegroundColor Gray
Write-Host "  - Estimated RAM savings: ~200-300 MB" -ForegroundColor Gray
Write-Host "  - Estimated CPU savings: ~50-70%" -ForegroundColor Gray
"""
        
        return script
    
    def generate_process_monitor_script(self) -> str:
        """
        Generate process monitoring script
        Monitors and kills non-essential processes
        
        Returns:
            PowerShell script content
        """
        script = """# Process Monitor - Kills non-essential processes
# Maintains lightweight operation
# Run periodically or on startup

$essentialProcesses = @(
"""
        
        # Add essential processes
        for proc in sorted(self.essential_processes):
            script += f'    "{proc}",\n'
        
        script += """)

# Get all processes
$allProcesses = Get-Process

# Kill non-essential processes
foreach ($proc in $allProcesses) {
    $processName = $proc.ProcessName + ".exe"
    
    # Skip essential processes
    if ($essentialProcesses -contains $processName -or $essentialProcesses -contains $proc.ProcessName) {
        continue
    }
    
    # Kill non-essential process
    try {
        Write-Host "Terminating non-essential: $processName" -ForegroundColor Gray
        Stop-Process -Id $proc.Id -Force -ErrorAction SilentlyContinue
    } catch {
        # Process might be protected, ignore
    }
}

Write-Host "Process cleanup complete." -ForegroundColor Green
"""
        
        return script
    
    def generate_startup_config(self) -> str:
        """
        Generate lightweight startup configuration
        Disables startup programs and unnecessary features
        
        Returns:
            PowerShell script content
        """
        script = """# Startup Configuration - Minimize boot processes
# Removes startup bloat for fastest boot

Write-Host "Configuring minimal startup..." -ForegroundColor Cyan

# Disable Windows features we don't need
$featuresToDisable = @(
    "MediaPlayback",
    "WindowsMediaPlayer",
    "Internet-Explorer-Optional-amd64",
    "Printing-XPSServices-Features",
    "WorkFolders-Client"
)

foreach ($feature in $featuresToDisable) {
    Write-Host "Disabling feature: $feature" -ForegroundColor Gray
    Disable-WindowsOptionalFeature -FeatureName $feature -Online -NoRestart -ErrorAction SilentlyContinue
}

# Disable visual effects for performance
$regPath = "HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\VisualEffects"
Set-ItemProperty -Path $regPath -Name "VisualFXSetting" -Value 2 -ErrorAction SilentlyContinue

# Disable unnecessary scheduled tasks
$tasksToDisable = @(
    "\\Microsoft\\Windows\\Application Experience\\*",
    "\\Microsoft\\Windows\\Customer Experience Improvement Program\\*",
    "\\Microsoft\\Windows\\Windows Error Reporting\\*",
    "\\Microsoft\\Windows\\Maintenance\\WinSAT"
)

foreach ($task in $tasksToDisable) {
    Get-ScheduledTask -TaskPath $task -ErrorAction SilentlyContinue | Disable-ScheduledTask -ErrorAction SilentlyContinue
}

Write-Host "Startup configuration complete!" -ForegroundColor Green
Write-Host "VM will boot faster and use fewer resources." -ForegroundColor Cyan
"""
        
        return script
    
    def get_isolation_summary(self) -> Dict[str, any]:
        """
        Get summary of isolation configuration
        
        Returns:
            Dictionary with isolation metrics
        """
        return {
            'essential_processes': len(self.essential_processes),
            'essential_services': len(self.essential_services),
            'disabled_services': len(self.disable_services),
            'estimated_ram_savings_mb': 250,
            'estimated_cpu_savings_percent': 60,
            'boot_time_reduction_percent': 40,
            'isolated_to_driver_functions': True,
        }
    
    def export_scripts(self, output_dir: str) -> bool:
        """
        Export all isolation scripts to directory
        
        Args:
            output_dir: Directory to save scripts
            
        Returns:
            True if successful, False otherwise
        """
        try:
            import os
            os.makedirs(output_dir, exist_ok=True)
            
            # Export service config
            with open(f"{output_dir}/isolate_services.ps1", 'w') as f:
                f.write(self.generate_service_config())
            
            # Export process monitor
            with open(f"{output_dir}/monitor_processes.ps1", 'w') as f:
                f.write(self.generate_process_monitor_script())
            
            # Export startup config
            with open(f"{output_dir}/configure_startup.ps1", 'w') as f:
                f.write(self.generate_startup_config())
            
            # Export summary
            with open(f"{output_dir}/isolation_summary.json", 'w') as f:
                json.dump(self.get_isolation_summary(), f, indent=2)
            
            print(f"Exported isolation scripts to: {output_dir}")
            return True
        
        except Exception as e:
            print(f"Error exporting scripts: {e}")
            return False


def main():
    """Generate Windows process isolation scripts"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Windows Process Isolator - Strip Windows to driver-only functions'
    )
    parser.add_argument(
        '--output-dir',
        default='/var/lib/heckcheckos/vm-scripts',
        help='Output directory for isolation scripts'
    )
    parser.add_argument(
        '--show-summary',
        action='store_true',
        help='Show isolation summary'
    )
    
    args = parser.parse_args()
    
    isolator = WindowsProcessIsolator()
    
    if args.show_summary:
        summary = isolator.get_isolation_summary()
        print("\nWindows Process Isolation Summary:")
        print("="*50)
        print(f"Essential Processes: {summary['essential_processes']}")
        print(f"Essential Services: {summary['essential_services']}")
        print(f"Disabled Services: {summary['disabled_services']}")
        print(f"\nEstimated Savings:")
        print(f"  RAM: ~{summary['estimated_ram_savings_mb']} MB")
        print(f"  CPU: ~{summary['estimated_cpu_savings_percent']}%")
        print(f"  Boot Time: ~{summary['boot_time_reduction_percent']}% faster")
        print(f"\nIsolated to driver functions only: {summary['isolated_to_driver_functions']}")
        print("="*50)
    
    # Export scripts
    success = isolator.export_scripts(args.output_dir)
    
    if success:
        print(f"\n✓ Scripts exported successfully!")
        print(f"\nUsage in Windows VM:")
        print(f"1. Copy scripts to VM")
        print(f"2. Run as Administrator: .\\isolate_services.ps1")
        print(f"3. Run: .\\configure_startup.ps1")
        print(f"4. Restart VM")
        print(f"\nVM will be stripped to driver-only functions.")
    
    return 0 if success else 1


if __name__ == '__main__':
    import sys
    sys.exit(main())
