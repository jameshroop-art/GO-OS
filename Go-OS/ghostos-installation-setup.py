#!/usr/bin/env python3
"""
Heck-CheckOS Installation Setup - Device Type Selection GUI
First step in installation process - choose what type of device to install on
Then launches appropriate installer for the selected device type

LICENSE: MIT (see LICENSE file in repository root)

LEGAL NOTICE:
This is part of Heck-CheckOS, a derivative work based on Debian 12 (Bookworm).
NOT an official Debian release. NOT endorsed by the Debian Project.
See LEGAL_COMPLIANCE.md for full legal information.
"""

import sys
import os
import subprocess
from pathlib import Path

try:
    import tkinter as tk
    from tkinter import ttk, messagebox, scrolledtext
except ImportError:
    print("Error: tkinter not found. Install with: sudo apt-get install python3-tk")
    sys.exit(1)


class InstallationSetupGUI:
    """Main installation setup GUI for device type selection"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Heck-CheckOS - Installation Setup")
        self.root.geometry("850x750")
        self.root.resizable(False, False)
        
        # Variables
        self.device_type = tk.StringVar(value="")
        self.android_install_type = tk.StringVar(value="usb")
        
        # Setup UI
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the main GUI interface"""
        # Header
        header = tk.Frame(self.root, bg="#2c3e50", height=100)
        header.pack(fill=tk.X, side=tk.TOP)
        
        title = tk.Label(header, text="👻 Heck-CheckOS Installation Setup", 
                        font=("Arial", 26, "bold"), fg="white", bg="#2c3e50")
        title.pack(pady=15)
        
        subtitle = tk.Label(header, text="Choose Your Installation Target Device", 
                           font=("Arial", 14), fg="#ecf0f1", bg="#2c3e50")
        subtitle.pack()
        
        # Main container
        main = ttk.Frame(self.root, padding="30")
        main.pack(fill=tk.BOTH, expand=True)
        
        # Introduction
        intro_frame = ttk.LabelFrame(main, text="Welcome to Heck-CheckOS Installation", padding="15")
        intro_frame.pack(fill=tk.X, pady=(0, 20))
        
        intro_text = tk.Label(intro_frame, 
            text="Please select the type of device you want to install Heck-CheckOS on.\n"
                 "This will determine the installation process and options available to you.",
            font=("Arial", 10), justify=tk.LEFT, wraplength=750)
        intro_text.pack()
        
        # Device Type Selection
        device_frame = ttk.LabelFrame(main, text="Step 1: Select Device Type", padding="15")
        device_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        # PC Options
        pc_section = ttk.Frame(device_frame)
        pc_section.pack(fill=tk.X, pady=5)
        
        ttk.Radiobutton(pc_section, 
                       text="🖥️  Standard PC (BIOS/UEFI)", 
                       variable=self.device_type, 
                       value="pc_standard",
                       command=self.on_device_selected).pack(anchor=tk.W, pady=3)
        
        pc_desc = tk.Label(pc_section, 
            text="    Standard desktop or workstation installation with automatic hardware detection.",
            font=("Arial", 9), fg="#555", justify=tk.LEFT)
        pc_desc.pack(anchor=tk.W, padx=20)
        
        ttk.Radiobutton(pc_section, 
                       text="🖥️  PC with Grub2 (Multi-boot)", 
                       variable=self.device_type, 
                       value="pc_grub2",
                       command=self.on_device_selected).pack(anchor=tk.W, pady=3)
        
        grub_desc = tk.Label(pc_section, 
            text="    Install alongside other operating systems using Grub2 bootloader.",
            font=("Arial", 9), fg="#555", justify=tk.LEFT)
        grub_desc.pack(anchor=tk.W, padx=20)
        
        ttk.Radiobutton(pc_section, 
                       text="💻 Laptop", 
                       variable=self.device_type, 
                       value="laptop",
                       command=self.on_device_selected).pack(anchor=tk.W, pady=3)
        
        laptop_desc = tk.Label(pc_section, 
            text="    Optimized for laptops with power management, touchpad, and WiFi support.",
            font=("Arial", 9), fg="#555", justify=tk.LEFT)
        laptop_desc.pack(anchor=tk.W, padx=20)
        
        # Portable Options
        portable_section = ttk.Frame(device_frame)
        portable_section.pack(fill=tk.X, pady=10)
        
        ttk.Separator(portable_section, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10)
        
        ttk.Radiobutton(portable_section, 
                       text="💾 Bootable USB (with SD Card option)", 
                       variable=self.device_type, 
                       value="usb_combo",
                       command=self.on_device_selected).pack(anchor=tk.W, pady=3)
        
        usb_desc = tk.Label(portable_section, 
            text="    Create portable bootable USB drive with optional SD card persistence.",
            font=("Arial", 9), fg="#555", justify=tk.LEFT)
        usb_desc.pack(anchor=tk.W, padx=20)
        
        # Android Options
        android_section = ttk.Frame(device_frame)
        android_section.pack(fill=tk.X, pady=10)
        
        ttk.Separator(android_section, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10)
        
        ttk.Radiobutton(android_section, 
                       text="📱 Android Device (Termux - Android 9+)", 
                       variable=self.device_type, 
                       value="android",
                       command=self.on_device_selected).pack(anchor=tk.W, pady=3)
        
        android_desc = tk.Label(android_section, 
            text="    Install Debian environment via Termux on Android 9+ devices (no root required).",
            font=("Arial", 9), fg="#555", justify=tk.LEFT)
        android_desc.pack(anchor=tk.W, padx=20)
        
        # Android-specific options (initially hidden)
        self.android_options_frame = ttk.LabelFrame(device_frame, text="Android Installation Options", padding="10")
        
        android_opt_label = tk.Label(self.android_options_frame,
            text="Select installation source for Android device:",
            font=("Arial", 9, "bold"))
        android_opt_label.pack(anchor=tk.W, pady=(0, 5))
        
        ttk.Radiobutton(self.android_options_frame, 
                       text="USB Storage - Install from USB drive connected via OTG",
                       variable=self.android_install_type, 
                       value="usb").pack(anchor=tk.W, pady=2)
        
        ttk.Radiobutton(self.android_options_frame, 
                       text="SD Card - Install from SD card",
                       variable=self.android_install_type, 
                       value="sdcard").pack(anchor=tk.W, pady=2)
        
        ttk.Radiobutton(self.android_options_frame, 
                       text="Network Download - Download directly via internet",
                       variable=self.android_install_type, 
                       value="network").pack(anchor=tk.W, pady=2)
        
        android_note = tk.Label(self.android_options_frame,
            text="Note: Android installation requires Termux and Termux:API from F-Droid.\n"
                 "Device-specific drivers and bridging will be configured during installation.",
            font=("Arial", 8), fg="#d35400", justify=tk.LEFT, wraplength=700)
        android_note.pack(anchor=tk.W, pady=(10, 0))
        
        # Device information display
        self.info_frame = ttk.LabelFrame(main, text="Selected Device Information", padding="15")
        self.info_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        self.info_text = scrolledtext.ScrolledText(self.info_frame, height=8, wrap=tk.WORD,
                                                   font=("Consolas", 9))
        self.info_text.pack(fill=tk.BOTH, expand=True)
        self.info_text.insert(tk.END, "Please select a device type above to see details and requirements.\n")
        self.info_text.config(state=tk.DISABLED)
        
        # Action Buttons
        button_frame = ttk.Frame(main)
        button_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.continue_btn = ttk.Button(button_frame, 
                                       text="➡️  Continue to Installation", 
                                       command=self.continue_installation,
                                       state=tk.DISABLED)
        self.continue_btn.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(button_frame, text="❌ Cancel", 
                  command=self.root.quit).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(button_frame, text="❓ Help", 
                  command=self.show_help).pack(side=tk.RIGHT, padx=5)
    
    def on_device_selected(self):
        """Handle device type selection"""
        device = self.device_type.get()
        
        # Hide Android options first
        self.android_options_frame.pack_forget()
        
        # Show Android-specific options if Android is selected
        if device == "android":
            # Insert after device_frame (which should be the second child)
            main_frame = self.info_frame.master
            device_frame = None
            for child in main_frame.winfo_children():
                if isinstance(child, ttk.LabelFrame) and "Device Type" in str(child.cget('text')):
                    device_frame = child
                    break
            if device_frame:
                self.android_options_frame.pack(fill=tk.X, pady=10, after=device_frame)
            else:
                # Fallback: just pack it
                self.android_options_frame.pack(fill=tk.X, pady=10)
        
        # Update info display
        self.info_text.config(state=tk.NORMAL)
        self.info_text.delete(1.0, tk.END)
        
        device_info = self.get_device_info(device)
        self.info_text.insert(tk.END, device_info)
        
        self.info_text.config(state=tk.DISABLED)
        
        # Enable continue button
        self.continue_btn.config(state=tk.NORMAL)
    
    def get_device_info(self, device_type):
        """Get detailed information about selected device type"""
        info = {
            "pc_standard": """
🖥️  STANDARD PC INSTALLATION

Requirements:
• 64-bit x86_64 processor (Intel or AMD)
• 8GB RAM minimum (16GB recommended)
• 32GB available storage
• BIOS or UEFI firmware
• Network connection (recommended)

Features:
• Full Debian 12 (Bookworm) installation
• Automatic hardware detection
• Support for AMD AM5, Intel, and NVIDIA hardware
• Gaming and development tools
• Privacy and security features

Installation Process:
1. Automatic hardware detection
2. Disk partitioning and formatting
3. Base system installation
4. Bootloader configuration (GRUB)
5. Driver installation
6. Desktop environment setup
""",
            "pc_grub2": """
🖥️  PC WITH GRUB2 (MULTI-BOOT)

Requirements:
• 64-bit x86_64 processor
• 8GB RAM minimum (16GB recommended)  
• 32GB available storage (separate partition or free space)
• UEFI firmware (recommended) or BIOS
• Existing operating system(s)

Features:
• Install alongside Windows, Linux, or other OS
• Grub2 bootloader for multi-boot menu
• Automatic detection of existing OS installations
• Chain-loading support
• Safe installation without affecting other systems

Installation Process:
1. Detect existing operating systems
2. Resize partitions or use free space
3. Install Heck-CheckOS
4. Configure Grub2 with all OS options
5. Set boot order and timeout
6. Verify multi-boot functionality

⚠️  Recommended: Backup important data before installation
""",
            "laptop": """
💻 LAPTOP INSTALLATION

Requirements:
• 64-bit x86_64 laptop processor
• 8GB RAM minimum (16GB recommended)
• 32GB available storage
• UEFI firmware (most modern laptops)
• WiFi adapter

Features:
• Optimized power management (TLP, laptop-mode-tools)
• Touchpad gesture support
• WiFi and Bluetooth drivers
• Battery monitoring and optimization
• Screen brightness controls
• Suspend/hibernate support
• Laptop-specific thermal management

Installation Process:
1. Laptop hardware detection
2. Install laptop-optimized kernel
3. Configure power management
4. Setup WiFi and touchpad
5. Battery optimization
6. Desktop environment with laptop profiles

Common Laptop Brands Supported:
• Dell, HP, Lenovo, ASUS, Acer
• Apple MacBook (Intel-based)
• System76, Framework
• Most other x86_64 laptops
""",
            "usb_combo": """
💾 BOOTABLE USB WITH SD CARD OPTION

Requirements:
• USB drive (16GB minimum, 32GB+ recommended)
• Optional: SD card for additional storage/persistence
• USB 3.0+ for best performance
• Target system: Any PC with USB boot support

Features:
• Portable Heck-CheckOS installation
• Boot from any compatible PC
• Optional persistence (save changes)
• SD card support for extended storage
• Live environment or persistent mode
• No installation required on host PC

Installation Process:
1. Select USB drive (will be formatted)
2. Choose boot mode (live or persistent)
3. Optional: Configure SD card for storage
4. Write Heck-CheckOS to USB
5. Configure bootloader for portability
6. Verify bootable USB creation

Usage Modes:
• Live Mode: No changes saved (reset on reboot)
• Persistent Mode: Changes saved to USB/SD card
• Full Installation: USB as primary drive

⚠️  All data on USB and SD card will be erased!
""",
            "android": """
📱 ANDROID DEVICE (TERMUX - ANDROID 9+)

Requirements:
• Android 9.0+ (API 28 or higher)
• 2GB RAM minimum (4GB recommended)
• 5GB available storage
• Termux app (from F-Droid, NOT Google Play)
• Termux:API app (from F-Droid)
• Storage and Location permissions
• Network connection

Features:
• Full Debian 12 environment via proot
• No root access required
• WiFi management (non-root)
• Bluetooth management (non-root)
• Linux package ecosystem (apt)
• Development tools (Python, Node.js, etc.)
• Driver optimization utilities

Installation Process:
1. Install Termux and Termux:API from F-Droid
2. Grant required permissions
3. Download Heck-CheckOS Android installer
4. Select installation source (USB/SD card/Network)
5. Configure device-specific settings
6. Install Debian proot environment
7. Setup driver bridging for device

Android-Specific Notes:
• Device make/model detection for driver bridging
• Controller/root access configuration (for advanced features)
• Termux integration for hardware access
• Some features limited without root (by design)

⚠️  Important: Install Termux from F-Droid, NOT Google Play!
The Google Play version is outdated and incompatible.

Note: Device-specific driver bridging will be configured during
installation based on your phone's make, model, and Android version.
"""
        }
        
        return info.get(device_type, "No information available for this device type.")
    
    def continue_installation(self):
        """Continue to appropriate installation method"""
        device = self.device_type.get()
        
        if not device:
            messagebox.showerror("Error", "Please select a device type first")
            return
        
        # For Android, show additional confirmation with selected install type
        if device == "android":
            install_type = self.android_install_type.get()
            response = messagebox.askyesno(
                "Android Installation",
                f"You selected Android installation via {install_type.upper()}.\n\n"
                "This will:\n"
                "• Install Debian environment via Termux\n"
                "• Configure device-specific drivers\n"
                "• Setup hardware bridging\n\n"
                "Make sure you have:\n"
                "• Termux from F-Droid (NOT Google Play)\n"
                "• Termux:API from F-Droid\n"
                "• Granted Storage and Location permissions\n\n"
                "Continue with Android installation?"
            )
            if response:
                self.launch_android_installer(install_type)
            return
        
        # For other devices, launch appropriate installer
        if device == "pc_standard":
            self.launch_pc_installer(grub_mode=False, laptop_mode=False)
        elif device == "pc_grub2":
            self.launch_pc_installer(grub_mode=True, laptop_mode=False)
        elif device == "laptop":
            self.launch_pc_installer(grub_mode=False, laptop_mode=True)
        elif device == "usb_combo":
            self.launch_usb_creator()
    
    def launch_pc_installer(self, grub_mode=False, laptop_mode=False):
        """Launch PC installer with appropriate options"""
        script_dir = Path(__file__).parent
        installer_script = script_dir / "ghostos-installer-gui.py"
        
        if not installer_script.exists():
            messagebox.showerror("Error", 
                f"Installer script not found: {installer_script}\n\n"
                "Please ensure ghostos-installer-gui.py is in the same directory.")
            return
        
        try:
            # Prepare environment variables for the installer
            env = os.environ.copy()
            if grub_mode:
                env['GHOSTOS_GRUB_MODE'] = '1'
            if laptop_mode:
                env['GHOSTOS_LAPTOP_MODE'] = '1'
            
            messagebox.showinfo("Launching Installer",
                f"Launching {'Grub2 multi-boot ' if grub_mode else ''}"
                f"{'laptop-optimized ' if laptop_mode else ''}installer...\n\n"
                "The main installation GUI will open in a new window.")
            
            # Launch the installer
            subprocess.Popen([sys.executable, str(installer_script)], env=env)
            
            # Close this setup window
            self.root.quit()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to launch installer: {str(e)}")
    
    def launch_usb_creator(self):
        """Launch USB creator tool"""
        script_dir = Path(__file__).parent
        usb_creator = script_dir / "ghostos-installer-gui.py"
        
        if not usb_creator.exists():
            messagebox.showerror("Error",
                f"USB creator not found: {usb_creator}\n\n"
                "Please ensure ghostos-installer-gui.py is in the same directory.")
            return
        
        try:
            env = os.environ.copy()
            env['GHOSTOS_USB_MODE'] = '1'
            
            messagebox.showinfo("Launching USB Creator",
                "Launching bootable USB creator...\n\n"
                "You can configure SD card options in the USB creator.")
            
            subprocess.Popen([sys.executable, str(usb_creator)], env=env)
            self.root.quit()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to launch USB creator: {str(e)}")
    
    def launch_android_installer(self, install_type):
        """Launch Android-specific installer"""
        script_dir = Path(__file__).parent
        android_script = script_dir / "ghostos-android.sh"
        
        if not android_script.exists():
            messagebox.showwarning("Android Installation",
                "Android installation script location:\n\n"
                f"Expected: {android_script}\n\n"
                "For Android installation:\n"
                "1. Install Termux from F-Droid\n"
                "2. Install Termux:API from F-Droid\n"
                "3. In Termux, run:\n\n"
                "   pkg update && pkg upgrade\n"
                "   pkg install wget\n"
                "   wget https://raw.githubusercontent.com/jameshroop-art/GO-OS/main/Go-OS/ghostos-android.sh\n"
                "   # TODO: Add checksum verification for security:\n"
                "   # wget https://raw.githubusercontent.com/jameshroop-art/GO-OS/main/Go-OS/ghostos-android.sh.sha256\n"
                "   # sha256sum -c ghostos-android.sh.sha256\n"
                "   chmod +x ghostos-android.sh\n"
                f"   bash ghostos-android.sh --source={install_type}\n\n"
                "Or visit the repository for installation instructions.")
            return
        
        # Show instructions for Android installation
        instructions = f"""
ANDROID INSTALLATION INSTRUCTIONS

Installation Type: {install_type.upper()}

Since you're running this from a desktop/laptop, you need to:

Option 1 - Transfer script to Android device:
1. Connect your Android device via USB
2. Enable USB file transfer mode
3. Copy ghostos-android.sh to your device
4. Open Termux on your Android device
5. Navigate to the script location
6. Run: bash ghostos-android.sh --source={install_type}

Option 2 - Direct download on Android device:
1. Open Termux on your Android device
2. Run these commands:

   pkg update && pkg upgrade -y
   pkg install wget -y
   wget https://raw.githubusercontent.com/jameshroop-art/GO-OS/main/Go-OS/ghostos-android.sh
   # Recommended: Verify checksum (TODO: add .sha256 file to repo)
   chmod +x ghostos-android.sh
   bash ghostos-android.sh --source={install_type}

Note: Make sure you have:
• Termux from F-Droid (NOT Google Play)
• Termux:API from F-Droid
• Storage permission granted to Termux
• Location permission granted (for WiFi scanning)

The installer will:
• Detect your device make/model
• Download appropriate drivers
• Configure hardware bridging
• Setup Debian environment
• Install driver optimization tools
"""
        
        # Show instructions in a new window
        inst_window = tk.Toplevel(self.root)
        inst_window.title("Android Installation Instructions")
        inst_window.geometry("700x600")
        
        text_widget = scrolledtext.ScrolledText(inst_window, wrap=tk.WORD, 
                                                font=("Consolas", 10), padx=10, pady=10)
        text_widget.pack(fill=tk.BOTH, expand=True)
        text_widget.insert(tk.END, instructions)
        text_widget.config(state=tk.DISABLED)
        
        btn_frame = ttk.Frame(inst_window)
        btn_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(btn_frame, text="Copy Script Location", 
                  command=lambda: self.copy_to_clipboard(str(android_script))).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Close", 
                  command=inst_window.destroy).pack(side=tk.RIGHT, padx=5)
    
    def copy_to_clipboard(self, text):
        """Copy text to clipboard"""
        self.root.clipboard_clear()
        self.root.clipboard_append(text)
        messagebox.showinfo("Copied", "Script location copied to clipboard!")
    
    def show_help(self):
        """Show help information"""
        help_text = """
HECK-CHECKOS INSTALLATION SETUP HELP

This is the first step in installing Heck-CheckOS. Select the type of device
you want to install on, and you'll be guided through the appropriate installation
process.

DEVICE TYPES:

1. Standard PC - Full installation on desktop or workstation computer
2. PC with Grub2 - Install alongside other operating systems
3. Laptop - Optimized installation for laptop computers
4. Bootable USB - Create portable USB drive with optional SD card storage
5. Android - Install Debian environment on Android 9+ devices via Termux

SYSTEM REQUIREMENTS:

PC/Laptop:
• 64-bit processor (x86_64)
• 8GB RAM minimum (16GB recommended)
• 32GB storage minimum
• BIOS or UEFI firmware

USB Drive:
• 16GB minimum (32GB+ recommended)
• USB 3.0 for best performance

Android:
• Android 9.0 or higher
• 2GB RAM minimum (4GB recommended)
• 5GB storage minimum
• Termux from F-Droid

IMPORTANT NOTES:

• PC installations require root/administrator privileges
• USB creation will erase all data on the selected drive
• Android installation does NOT require root access
• Always backup important data before installation

For detailed installation guides, visit:
https://github.com/jameshroop-art/GO-OS

For support and issues:
https://github.com/jameshroop-art/GO-OS/issues
"""
        
        help_window = tk.Toplevel(self.root)
        help_window.title("Installation Setup Help")
        help_window.geometry("700x600")
        
        text_widget = scrolledtext.ScrolledText(help_window, wrap=tk.WORD,
                                                font=("Arial", 10), padx=15, pady=15)
        text_widget.pack(fill=tk.BOTH, expand=True)
        text_widget.insert(tk.END, help_text)
        text_widget.config(state=tk.DISABLED)
        
        ttk.Button(help_window, text="Close", 
                  command=help_window.destroy).pack(pady=10)


def main():
    """Main entry point"""
    try:
        root = tk.Tk()
    except Exception as e:
        print(f"Error: Cannot create GUI: {e}")
        print("Make sure you're running in a graphical environment")
        sys.exit(1)
    
    # Set theme
    try:
        style = ttk.Style()
        style.theme_use('clam')
    except tk.TclError:
        # Theme not available, use default
        pass
    except Exception as e:
        # Other theme-related errors, use default
        print(f"Warning: Could not set theme: {e}")
    
    # Create app
    app = InstallationSetupGUI(root)
    
    # Run
    root.mainloop()


if __name__ == "__main__":
    main()
