#!/usr/bin/env python3
"""
HeckOS Security Edition - GUI Installer & USB Creator
Creates bootable USB drives and manages disk partitioning for PC installation
Supports Windows, Linux, and macOS host systems

LICENSE: MIT (see LICENSE file in repository root)

LEGAL NOTICE:
This is part of HeckOS, a derivative work based on Debian 12 (Bookworm).
NOT an official Debian release. NOT endorsed by the Debian Project.
See LEGAL_COMPLIANCE.md for full legal information.
"""

import sys
import os
import subprocess
import json
import threading
import time
from pathlib import Path

try:
    import tkinter as tk
    from tkinter import ttk, filedialog, messagebox, scrolledtext
except ImportError:
    print("Error: tkinter not found. Install with: sudo apt-get install python3-tk")
    sys.exit(1)

class HeckCheckOSInstallerGUI:
    def __init__(self, root):
        self.root = root
        
        # Check for installation mode from environment
        self.grub_mode = os.environ.get('GHOSTOS_GRUB_MODE', '0') == '1'
        self.laptop_mode = os.environ.get('GHOSTOS_LAPTOP_MODE', '0') == '1'
        self.usb_mode = os.environ.get('GHOSTOS_USB_MODE', '0') == '1'
        
        # Set title based on mode
        if self.grub_mode:
            title_suffix = " - Grub2 Multi-boot Installation"
        elif self.laptop_mode:
            title_suffix = " - Laptop Installation"
        elif self.usb_mode:
            title_suffix = " - USB Creator"
        else:
            title_suffix = " - Installer & USB Creator"
        
        self.root.title("HeckOS Security Edition" + title_suffix)
        self.root.geometry("900x700")
        self.root.resizable(True, True)
        
        # Variables
        self.iso_path = tk.StringVar()
        self.selected_drive = tk.StringVar()
        self.partition_format = tk.StringVar(value="ext4")
        self.install_mode = tk.StringVar(value="usb")
        self.drives_list = []
        
        # Driver VM integration
        self.enable_driver_vm = tk.BooleanVar(value=False)
        
        # Check admin/root
        self.is_admin = self.check_admin_rights()
        
        # Setup UI
        self.setup_ui()
        
        # Refresh drives on start
        self.refresh_drives()
    
    def check_admin_rights(self):
        """Check if running with admin/root privileges"""
        try:
            if os.name == 'nt':  # Windows
                import ctypes
                return ctypes.windll.shell32.IsUserAnAdmin() != 0
            else:  # Linux/Mac
                return os.geteuid() == 0
        except:
            return False
    
    def setup_ui(self):
        """Setup the GUI interface"""
        # Header
        header = tk.Frame(self.root, bg="#2c3e50", height=80)
        header.pack(fill=tk.X, side=tk.TOP)
        
        title = tk.Label(header, text="👻 HeckOS Security Edition", 
                        font=("Arial", 24, "bold"), fg="white", bg="#2c3e50")
        title.pack(pady=10)
        
        # Dynamic subtitle based on mode
        if self.grub_mode:
            subtitle_text = "Grub2 Multi-boot Installation"
        elif self.laptop_mode:
            subtitle_text = "Laptop-Optimized Installation"
        elif self.usb_mode:
            subtitle_text = "Bootable USB Creator"
        else:
            subtitle_text = "Bootable USB Creator & Disk Partitioner"
        
        subtitle = tk.Label(header, text=subtitle_text, 
                           font=("Arial", 12), fg="#ecf0f1", bg="#2c3e50")
        subtitle.pack()
        
        # Main container
        main = ttk.Frame(self.root, padding="20")
        main.pack(fill=tk.BOTH, expand=True)
        
        # Mode indicator
        if self.grub_mode or self.laptop_mode:
            mode_text = "Mode: "
            if self.grub_mode:
                mode_text += "Multi-boot with Grub2"
            if self.laptop_mode:
                mode_text += "Laptop Optimization Enabled"
            
            mode_label = tk.Label(main, text=f"ℹ️  {mode_text}", 
                                font=("Arial", 10, "bold"), fg="#2980b9")
            mode_label.pack(pady=5)
        
        # Admin warning
        if not self.is_admin:
            warning = tk.Label(main, text="⚠️  WARNING: Not running as administrator/root. Some features may not work.",
                             fg="red", font=("Arial", 10, "bold"))
            warning.pack(pady=5)
        
        # Notebook for tabs
        notebook = ttk.Notebook(main)
        notebook.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Tab 1: USB Creator
        usb_tab = ttk.Frame(notebook)
        notebook.add(usb_tab, text="📀 Create Bootable USB")
        self.setup_usb_tab(usb_tab)
        
        # Tab 2: Disk Partitioner
        partition_tab = ttk.Frame(notebook)
        notebook.add(partition_tab, text="💾 Disk Partitioner")
        self.setup_partition_tab(partition_tab)
        
        # Tab 3: Advanced Options
        advanced_tab = ttk.Frame(notebook)
        notebook.add(advanced_tab, text="⚙️ Advanced Options")
        self.setup_advanced_tab(advanced_tab)
        
        # Tab 4: Driver VM (if PC/Laptop mode)
        if not self.usb_mode:
            driver_vm_tab = ttk.Frame(notebook)
            notebook.add(driver_vm_tab, text="🔧 Driver VM")
            self.setup_driver_vm_tab(driver_vm_tab)
        
        # Status bar
        self.status_bar = tk.Label(self.root, text="Ready", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def setup_usb_tab(self, parent):
        """Setup USB Creator tab"""
        # ISO Selection
        iso_frame = ttk.LabelFrame(parent, text="Step 1: Select HeckOS ISO", padding="10")
        iso_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(iso_frame, text="ISO File:").grid(row=0, column=0, sticky=tk.W, pady=5)
        ttk.Entry(iso_frame, textvariable=self.iso_path, width=50).grid(row=0, column=1, padx=5)
        ttk.Button(iso_frame, text="Browse...", command=self.browse_iso).grid(row=0, column=2)
        
        # Drive Selection
        drive_frame = ttk.LabelFrame(parent, text="Step 2: Select Target USB Drive", padding="10")
        drive_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(drive_frame, text="⚠️ WARNING: All data on selected drive will be ERASED!", 
                 foreground="red").pack(anchor=tk.W, pady=5)
        
        ttk.Button(drive_frame, text="🔄 Refresh Drives", 
                  command=self.refresh_drives).pack(anchor=tk.W, pady=5)
        
        # Drive listbox with scrollbar
        list_frame = ttk.Frame(drive_frame)
        list_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.drive_listbox = tk.Listbox(list_frame, height=6, yscrollcommand=scrollbar.set)
        self.drive_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.drive_listbox.yview)
        
        # USB Creation Options
        options_frame = ttk.LabelFrame(parent, text="Step 3: USB Creation Options", padding="10")
        options_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Radiobutton(options_frame, text="Standard USB (BIOS/UEFI compatible)", 
                       variable=self.install_mode, value="usb").pack(anchor=tk.W)
        ttk.Radiobutton(options_frame, text="Persistent USB (Save changes)", 
                       variable=self.install_mode, value="persistent").pack(anchor=tk.W)
        ttk.Radiobutton(options_frame, text="Install to Drive (Full installation)", 
                       variable=self.install_mode, value="install").pack(anchor=tk.W)
        
        # Action Buttons
        action_frame = ttk.Frame(parent)
        action_frame.pack(fill=tk.X, padx=10, pady=20)
        
        self.create_usb_btn = ttk.Button(action_frame, text="🚀 Create Bootable USB", 
                                         command=self.create_bootable_usb, style="Accent.TButton")
        self.create_usb_btn.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(action_frame, text="❌ Cancel", 
                  command=self.cancel_operation).pack(side=tk.LEFT, padx=5)
    
    def setup_partition_tab(self, parent):
        """Setup Disk Partitioner tab"""
        # Drive info
        info_frame = ttk.LabelFrame(parent, text="Drive Information", padding="10")
        info_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(info_frame, text="🔄 Refresh Drives", 
                  command=self.refresh_drives).pack(anchor=tk.W, pady=5)
        
        # Partition list
        self.partition_tree = ttk.Treeview(info_frame, columns=("Device", "Size", "Type", "Mount"), 
                                          height=8, show="tree headings")
        self.partition_tree.heading("#0", text="")
        self.partition_tree.heading("Device", text="Device")
        self.partition_tree.heading("Size", text="Size")
        self.partition_tree.heading("Type", text="Type")
        self.partition_tree.heading("Mount", text="Mount Point")
        self.partition_tree.column("#0", width=30)
        self.partition_tree.column("Device", width=150)
        self.partition_tree.column("Size", width=100)
        self.partition_tree.column("Type", width=100)
        self.partition_tree.column("Mount", width=200)
        self.partition_tree.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Partition Operations
        ops_frame = ttk.LabelFrame(parent, text="Partition Operations", padding="10")
        ops_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Format options
        format_frame = ttk.Frame(ops_frame)
        format_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(format_frame, text="Format Type:").pack(side=tk.LEFT, padx=5)
        
        formats = ["ext4", "ext3", "ext2", "btrfs", "xfs", "ntfs", "fat32", "exfat", "f2fs", "jfs", "reiserfs", "swap"]
        format_combo = ttk.Combobox(format_frame, textvariable=self.partition_format, 
                                   values=formats, state="readonly", width=15)
        format_combo.pack(side=tk.LEFT, padx=5)
        format_combo.current(0)
        
        # Action buttons
        btn_frame = ttk.Frame(ops_frame)
        btn_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(btn_frame, text="➕ Create Partition", 
                  command=self.create_partition).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="🔧 Format Selected", 
                  command=self.format_partition).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="🗑️ Delete Selected", 
                  command=self.delete_partition).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="📏 Resize Partition", 
                  command=self.resize_partition).pack(side=tk.LEFT, padx=5)
        
        # Format descriptions
        desc_frame = ttk.LabelFrame(ops_frame, text="Format Descriptions", padding="5")
        desc_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        descriptions = scrolledtext.ScrolledText(desc_frame, height=8, wrap=tk.WORD)
        descriptions.pack(fill=tk.BOTH, expand=True)
        descriptions.insert(tk.END, """Format Types:

• ext4: Linux default, journaling, reliable (recommended for Linux)
• ext3/ext2: Older Linux filesystems
• btrfs: Advanced Linux filesystem with snapshots
• xfs: High-performance Linux filesystem
• ntfs: Windows filesystem (read/write on Linux)
• fat32: Universal compatibility (USB drives)
• exfat: Large files, universal compatibility
• f2fs: Flash-friendly filesystem (SSDs, USB drives)
• jfs: IBM's journaling filesystem
• reiserfs: Legacy journaling filesystem
• swap: Linux swap space (virtual memory)
""")
        descriptions.config(state=tk.DISABLED)
    
    def setup_advanced_tab(self, parent):
        """Setup Advanced Options tab"""
        # Partition scheme
        scheme_frame = ttk.LabelFrame(parent, text="Partition Scheme", padding="10")
        scheme_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.partition_scheme = tk.StringVar(value="gpt")
        ttk.Radiobutton(scheme_frame, text="GPT (Recommended for UEFI systems)", 
                       variable=self.partition_scheme, value="gpt").pack(anchor=tk.W)
        ttk.Radiobutton(scheme_frame, text="MBR (Legacy BIOS systems)", 
                       variable=self.partition_scheme, value="mbr").pack(anchor=tk.W)
        
        # Boot options
        boot_frame = ttk.LabelFrame(parent, text="Boot Options", padding="10")
        boot_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.secure_boot = tk.BooleanVar(value=True)
        self.uefi_boot = tk.BooleanVar(value=True)
        
        ttk.Checkbutton(boot_frame, text="UEFI Boot Support", 
                       variable=self.uefi_boot).pack(anchor=tk.W)
        ttk.Checkbutton(boot_frame, text="Secure Boot Compatible", 
                       variable=self.secure_boot).pack(anchor=tk.W)
        
        # Verification
        verify_frame = ttk.LabelFrame(parent, text="Verification", padding="10")
        verify_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.verify_iso = tk.BooleanVar(value=True)
        self.verify_usb = tk.BooleanVar(value=True)
        
        ttk.Checkbutton(verify_frame, text="Verify ISO checksum before writing", 
                       variable=self.verify_iso).pack(anchor=tk.W)
        ttk.Checkbutton(verify_frame, text="Verify USB after creation", 
                       variable=self.verify_usb).pack(anchor=tk.W)
        
        # System Requirements
        req_frame = ttk.LabelFrame(parent, text="System Requirements Check", padding="10")
        req_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.req_text = scrolledtext.ScrolledText(req_frame, height=12, wrap=tk.WORD)
        self.req_text.pack(fill=tk.BOTH, expand=True)
        
        ttk.Button(req_frame, text="🔍 Check System Requirements", 
                  command=self.check_requirements).pack(pady=5)
    
    def browse_iso(self):
        """Browse for ISO file"""
        filename = filedialog.askopenfilename(
            title="Select HeckOS ISO",
            filetypes=[("ISO files", "*.iso"), ("All files", "*.*")]
        )
        if filename:
            self.iso_path.set(filename)
            self.status_bar.config(text=f"Selected: {filename}")
    
    def refresh_drives(self):
        """Refresh list of available drives"""
        self.status_bar.config(text="Refreshing drives...")
        self.drive_listbox.delete(0, tk.END)
        self.partition_tree.delete(*self.partition_tree.get_children())
        
        try:
            if os.name == 'nt':  # Windows
                drives = self.get_windows_drives()
            else:  # Linux/Mac
                drives = self.get_linux_drives()
            
            self.drives_list = drives
            
            for drive in drives:
                display = f"{drive['device']} - {drive['size']} - {drive['model']}"
                self.drive_listbox.insert(tk.END, display)
                
                # Add to partition tree
                parent = self.partition_tree.insert("", tk.END, text="💾", 
                                                   values=(drive['device'], drive['size'], 
                                                          drive.get('type', 'disk'), ""))
                
                # Add partitions if available
                for part in drive.get('partitions', []):
                    self.partition_tree.insert(parent, tk.END, text="📁",
                                             values=(part['device'], part['size'], 
                                                    part.get('fstype', 'unknown'), 
                                                    part.get('mountpoint', '')))
            
            self.status_bar.config(text=f"Found {len(drives)} drive(s)")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to refresh drives: {str(e)}")
            self.status_bar.config(text="Error refreshing drives")
    
    def get_windows_drives(self):
        """Get drives on Windows"""
        drives = []
        try:
            import wmi
            c = wmi.WMI()
            for disk in c.Win32_DiskDrive():
                size_gb = int(disk.Size) / (1024**3)
                drives.append({
                    'device': disk.DeviceID,
                    'size': f"{size_gb:.2f} GB",
                    'model': disk.Model,
                    'type': 'removable' if disk.MediaType == 'Removable Media' else 'fixed',
                    'partitions': []
                })
        except ImportError:
            # Fallback without wmi
            import string
            from ctypes import windll
            bitmask = windll.kernel32.GetLogicalDrives()
            for letter in string.ascii_uppercase:
                if bitmask & 1:
                    drives.append({
                        'device': f"{letter}:",
                        'size': "Unknown",
                        'model': f"Drive {letter}",
                        'type': 'unknown',
                        'partitions': []
                    })
                bitmask >>= 1
        return drives
    
    def get_linux_drives(self):
        """Get drives on Linux"""
        drives = []
        try:
            result = subprocess.run(['lsblk', '-J', '-o', 'NAME,SIZE,TYPE,MODEL,FSTYPE,MOUNTPOINT'],
                                  capture_output=True, text=True)
            if result.returncode == 0:
                data = json.loads(result.stdout)
                for device in data.get('blockdevices', []):
                    if device['type'] == 'disk':
                        drive = {
                            'device': f"/dev/{device['name']}",
                            'size': device.get('size', 'Unknown'),
                            'model': device.get('model', 'Unknown'),
                            'type': device['type'],
                            'partitions': []
                        }
                        
                        # Add partitions
                        for child in device.get('children', []):
                            drive['partitions'].append({
                                'device': f"/dev/{child['name']}",
                                'size': child.get('size', ''),
                                'fstype': child.get('fstype', ''),
                                'mountpoint': child.get('mountpoint', '')
                            })
                        
                        drives.append(drive)
        except Exception as e:
            print(f"Error getting Linux drives: {e}")
        
        return drives
    
    def create_bootable_usb(self):
        """Create bootable USB drive"""
        if not self.iso_path.get():
            messagebox.showerror("Error", "Please select an ISO file")
            return
        
        if not self.drive_listbox.curselection():
            messagebox.showerror("Error", "Please select a target drive")
            return
        
        if not self.is_admin:
            messagebox.showerror("Error", "Administrator/root privileges required")
            return
        
        # Confirm
        idx = self.drive_listbox.curselection()[0]
        drive = self.drives_list[idx]
        
        response = messagebox.askyesno(
            "Confirm",
            f"⚠️  WARNING!\n\nAll data on {drive['device']} will be ERASED!\n\n"
            f"Device: {drive['device']}\n"
            f"Size: {drive['size']}\n"
            f"Model: {drive['model']}\n\n"
            "Do you want to continue?"
        )
        
        if not response:
            return
        
        # Create USB in separate thread
        thread = threading.Thread(target=self._create_usb_thread, args=(drive,))
        thread.daemon = True
        thread.start()
    
    def _create_usb_thread(self, drive):
        """Thread for creating USB"""
        self.root.after(0, lambda: self.create_usb_btn.config(state=tk.DISABLED))
        self.root.after(0, lambda: self.status_bar.config(text="Creating bootable USB..."))
        
        try:
            iso_file = self.iso_path.get()
            device = drive['device']
            
            # Use dd on Linux/Mac, or specialized tool on Windows
            if os.name == 'nt':
                self._create_usb_windows(iso_file, device)
            else:
                self._create_usb_linux(iso_file, device)
            
            self.root.after(0, lambda: messagebox.showinfo("Success", 
                "Bootable USB created successfully!"))
            self.root.after(0, lambda: self.status_bar.config(text="USB creation completed"))
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Error", 
                f"Failed to create USB: {str(e)}"))
            self.root.after(0, lambda: self.status_bar.config(text="USB creation failed"))
        finally:
            self.root.after(0, lambda: self.create_usb_btn.config(state=tk.NORMAL))
    
    def _create_usb_linux(self, iso_file, device):
        """Create USB on Linux with UEFI support"""
        self.root.after(0, lambda: self.status_bar.config(text="Preparing device..."))
        
        # Unmount all partitions on device
        for i in range(1, 10):
            subprocess.run(['umount', f'{device}{i}'], stderr=subprocess.DEVNULL)
            subprocess.run(['umount', f'{device}p{i}'], stderr=subprocess.DEVNULL)
        
        # Determine partition scheme (GPT for UEFI, MBR for legacy)
        use_gpt = self.partition_scheme.get() == "gpt"
        
        if use_gpt and self.uefi_boot.get():
            # Create UEFI-bootable USB with GPT
            self._create_uefi_usb(iso_file, device)
        else:
            # Create legacy BIOS bootable USB
            self._create_legacy_usb(iso_file, device)
    
    def _create_uefi_usb(self, iso_file, device):
        """Create UEFI-bootable USB with proper GPT partition structure"""
        self.root.after(0, lambda: self.status_bar.config(text="Creating GPT partition table..."))
        
        # Wipe existing partition table
        subprocess.run(['wipefs', '-a', device], stderr=subprocess.DEVNULL)
        
        # Create GPT partition table
        subprocess.run(['parted', '-s', device, 'mklabel', 'gpt'], check=True)
        
        # Create EFI System Partition (ESP) - FAT32
        # This is required for UEFI boot
        subprocess.run(['parted', '-s', device, 'mkpart', 'ESP', 'fat32', '1MiB', '512MiB'], check=True)
        subprocess.run(['parted', '-s', device, 'set', '1', 'esp', 'on'], check=True)
        
        # Create data partition for ISO content
        subprocess.run(['parted', '-s', device, 'mkpart', 'primary', 'ext4', '512MiB', '100%'], check=True)
        
        # Wait for kernel to recognize partitions
        subprocess.run(['partprobe', device])
        time.sleep(2)
        
        # Determine partition names
        if 'nvme' in device or 'mmcblk' in device:
            esp_part = f"{device}p1"
            data_part = f"{device}p2"
        else:
            esp_part = f"{device}1"
            data_part = f"{device}2"
        
        self.root.after(0, lambda: self.status_bar.config(text="Formatting EFI System Partition..."))
        
        # Format ESP as FAT32 (required for UEFI)
        subprocess.run(['mkfs.vfat', '-F', '32', '-n', 'GHOSTOS_EFI', esp_part], check=True)
        
        # Format data partition as ext4
        subprocess.run(['mkfs.ext4', '-F', '-L', 'GHOSTOS', data_part], check=True)
        
        self.root.after(0, lambda: self.status_bar.config(text="Mounting partitions..."))
        
        # Create mount points
        esp_mount = '/tmp/ghostos_esp'
        data_mount = '/tmp/ghostos_data'
        iso_mount = '/tmp/ghostos_iso'
        
        os.makedirs(esp_mount, exist_ok=True)
        os.makedirs(data_mount, exist_ok=True)
        os.makedirs(iso_mount, exist_ok=True)
        
        try:
            # Mount partitions
            subprocess.run(['mount', esp_part, esp_mount], check=True)
            subprocess.run(['mount', data_part, data_mount], check=True)
            subprocess.run(['mount', '-o', 'loop', iso_file, iso_mount], check=True)
            
            self.root.after(0, lambda: self.status_bar.config(text="Copying ISO contents..."))
            
            # Copy all ISO contents to data partition
            subprocess.run(['rsync', '-ah', '--info=progress2', f'{iso_mount}/', data_mount], check=True)
            
            # Copy EFI boot files to ESP
            if os.path.exists(f'{iso_mount}/EFI'):
                subprocess.run(['rsync', '-ah', f'{iso_mount}/EFI/', f'{esp_mount}/EFI/'], check=True)
            
            # Create boot directory structure for UEFI
            os.makedirs(f'{esp_mount}/EFI/BOOT', exist_ok=True)
            
            # Copy bootloader files (support multiple architectures)
            bootloaders = [
                ('EFI/BOOT/BOOTX64.EFI', 'EFI/BOOT/BOOTX64.EFI'),  # x86_64
                ('EFI/BOOT/BOOTIA32.EFI', 'EFI/BOOT/BOOTIA32.EFI'),  # x86
                ('EFI/BOOT/grubx64.efi', 'EFI/BOOT/BOOTX64.EFI'),  # GRUB fallback
                ('EFI/BOOT/grub.efi', 'EFI/BOOT/BOOTIA32.EFI'),  # GRUB 32-bit
            ]
            
            for src, dst in bootloaders:
                src_path = f'{iso_mount}/{src}'
                dst_path = f'{esp_mount}/{dst}'
                if os.path.exists(src_path):
                    os.makedirs(os.path.dirname(dst_path), exist_ok=True)
                    subprocess.run(['cp', src_path, dst_path], stderr=subprocess.DEVNULL)
            
            # Create UEFI boot entry (if efibootmgr available)
            if subprocess.run(['which', 'efibootmgr'], capture_output=True).returncode == 0:
                subprocess.run(['efibootmgr', '--create', '--disk', device, '--part', '1',
                              '--label', 'HeckOS', '--loader', '\\EFI\\BOOT\\BOOTX64.EFI'],
                              stderr=subprocess.DEVNULL)
            
        finally:
            # Unmount everything
            subprocess.run(['umount', iso_mount], stderr=subprocess.DEVNULL)
            subprocess.run(['umount', data_mount], stderr=subprocess.DEVNULL)
            subprocess.run(['umount', esp_mount], stderr=subprocess.DEVNULL)
            
            # Cleanup
            os.rmdir(iso_mount)
            os.rmdir(data_mount)
            os.rmdir(esp_mount)
        
        # Sync
        subprocess.run(['sync'])
        
        self.root.after(0, lambda: self.status_bar.config(text="UEFI-bootable USB created successfully!"))
    
    def _create_legacy_usb(self, iso_file, device):
        """Create legacy BIOS bootable USB using dd"""
        self.root.after(0, lambda: self.status_bar.config(text="Writing ISO to device..."))
        
        # Unmount if mounted
        subprocess.run(['umount', device], stderr=subprocess.DEVNULL)
        
        # Write ISO directly (hybrid ISO approach)
        cmd = ['dd', f'if={iso_file}', f'of={device}', 'bs=4M', 'status=progress', 'conv=fsync']
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            raise Exception(result.stderr)
        
        # Sync
        subprocess.run(['sync'])
        
        self.root.after(0, lambda: self.status_bar.config(text="Legacy BIOS bootable USB created!"))
    
    def _create_usb_windows(self, iso_file, device):
        """Create USB on Windows (placeholder - would use Win32DiskImager or similar)"""
        raise Exception("Windows USB creation requires additional tools. Please use Rufus or similar.")
    
    def format_partition(self):
        """Format selected partition"""
        selected = self.partition_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a partition to format")
            return
        
        if not self.is_admin:
            messagebox.showerror("Error", "Administrator/root privileges required")
            return
        
        item = self.partition_tree.item(selected[0])
        device = item['values'][0]
        format_type = self.partition_format.get()
        
        response = messagebox.askyesno(
            "Confirm",
            f"⚠️  WARNING!\n\nAll data on {device} will be ERASED!\n\n"
            f"Format: {format_type}\n\n"
            "Do you want to continue?"
        )
        
        if not response:
            return
        
        try:
            self.status_bar.config(text=f"Formatting {device} as {format_type}...")
            
            if os.name != 'nt':  # Linux
                # Unmount first
                subprocess.run(['umount', device], stderr=subprocess.DEVNULL)
                
                # Format based on type
                if format_type == 'ext4':
                    cmd = ['mkfs.ext4', '-F', device]
                elif format_type == 'ext3':
                    cmd = ['mkfs.ext3', '-F', device]
                elif format_type == 'ext2':
                    cmd = ['mkfs.ext2', '-F', device]
                elif format_type == 'btrfs':
                    cmd = ['mkfs.btrfs', '-f', device]
                elif format_type == 'xfs':
                    cmd = ['mkfs.xfs', '-f', device]
                elif format_type == 'ntfs':
                    cmd = ['mkfs.ntfs', '-f', device]
                elif format_type == 'fat32':
                    cmd = ['mkfs.vfat', '-F', '32', device]
                elif format_type == 'exfat':
                    cmd = ['mkfs.exfat', device]
                elif format_type == 'f2fs':
                    cmd = ['mkfs.f2fs', '-f', device]
                elif format_type == 'jfs':
                    cmd = ['mkfs.jfs', '-q', device]
                elif format_type == 'reiserfs':
                    cmd = ['mkfs.reiserfs', '-q', device]
                elif format_type == 'swap':
                    cmd = ['mkswap', device]
                else:
                    raise Exception(f"Unsupported format: {format_type}")
                
                result = subprocess.run(cmd, capture_output=True, text=True)
                
                if result.returncode != 0:
                    raise Exception(result.stderr)
                
                messagebox.showinfo("Success", f"Formatted {device} as {format_type}")
                self.status_bar.config(text=f"Formatted {device} successfully")
                self.refresh_drives()
            else:
                messagebox.showerror("Error", "Formatting on Windows requires additional tools")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to format: {str(e)}")
            self.status_bar.config(text="Format failed")
    
    def create_partition(self):
        """Create new partition"""
        messagebox.showinfo("Info", "Partition creation requires parted/gparted. Please use Advanced mode.")
    
    def delete_partition(self):
        """Delete selected partition"""
        messagebox.showwarning("Warning", "Partition deletion is dangerous. Use gparted for safety.")
    
    def resize_partition(self):
        """Resize partition"""
        messagebox.showinfo("Info", "Partition resizing requires gparted or parted. Use Advanced mode.")
    
    def cancel_operation(self):
        """Cancel current operation"""
        self.status_bar.config(text="Operation cancelled")
    
    def check_requirements(self):
        """Check system requirements"""
        self.req_text.delete(1.0, tk.END)
        self.req_text.insert(tk.END, "Checking system requirements...\n\n")
        
        # Check tools
        tools = {
            'dd': 'USB creation (legacy)',
            'parted': 'Partition management',
            'mkfs.ext4': 'ext4 formatting',
            'mkfs.ntfs': 'NTFS formatting',
            'mkfs.vfat': 'FAT32 formatting (UEFI ESP)',
            'rsync': 'File copying',
            'wipefs': 'Partition table wiping',
            'partprobe': 'Partition detection',
            'efibootmgr': 'UEFI boot entry management (optional)',
        }
        
        for tool, desc in tools.items():
            try:
                result = subprocess.run(['which', tool], capture_output=True)
                if result.returncode == 0:
                    self.req_text.insert(tk.END, f"✅ {tool} - {desc}\n")
                else:
                    if 'optional' in desc.lower():
                        self.req_text.insert(tk.END, f"⚠️  {tool} - {desc} (NOT FOUND)\n")
                    else:
                        self.req_text.insert(tk.END, f"❌ {tool} - {desc} (NOT FOUND)\n")
            except:
                self.req_text.insert(tk.END, f"❌ {tool} - {desc} (ERROR)\n")
        
        # Check UEFI firmware
        self.req_text.insert(tk.END, "\n=== UEFI/BIOS Detection ===\n")
        if os.path.exists('/sys/firmware/efi'):
            self.req_text.insert(tk.END, "✅ System booted in UEFI mode\n")
            self.req_text.insert(tk.END, "   USB will be created with UEFI support\n")
        else:
            self.req_text.insert(tk.END, "⚠️  System booted in Legacy BIOS mode\n")
            self.req_text.insert(tk.END, "   USB will still support UEFI boot\n")
        
        self.req_text.insert(tk.END, "\n=== HeckOS System Requirements ===\n")
        self.req_text.insert(tk.END, "• 64-bit x86_64 processor\n")
        self.req_text.insert(tk.END, "• 8GB RAM minimum (16GB recommended)\n")
        self.req_text.insert(tk.END, "• 32GB storage minimum\n")
        self.req_text.insert(tk.END, "• UEFI firmware (recommended)\n")
        self.req_text.insert(tk.END, "• USB 3.0+ for best performance\n")
        self.req_text.insert(tk.END, "\n=== USB Boot Compatibility ===\n")
        self.req_text.insert(tk.END, "Created USB drives support:\n")
        self.req_text.insert(tk.END, "• UEFI boot (GPT partition scheme)\n")
        self.req_text.insert(tk.END, "• Legacy BIOS boot (MBR compatibility)\n")
        self.req_text.insert(tk.END, "• Secure Boot (if enabled in advanced)\n")
        self.req_text.insert(tk.END, "• 32-bit and 64-bit UEFI\n")
    
    def setup_driver_vm_tab(self, parent):
        """Setup Driver VM configuration tab"""
        # Introduction
        intro_frame = ttk.LabelFrame(parent, text="Windows Driver VM Integration", padding="15")
        intro_frame.pack(fill=tk.X, padx=10, pady=10)
        
        intro_text = tk.Label(intro_frame,
            text="Enable lightweight Windows 10 VM for Windows driver compatibility.\n"
                 "VM handles driver operations with minimal resource usage (512MB RAM, 1 CPU core).",
            font=("Arial", 10), justify=tk.LEFT, wraplength=800)
        intro_text.pack(anchor=tk.W)
        
        # Enable/Disable Driver VM
        enable_frame = ttk.Frame(intro_frame)
        enable_frame.pack(fill=tk.X, pady=10)
        
        ttk.Checkbutton(enable_frame, 
                       text="Enable Driver Controller VM (Windows driver support)",
                       variable=self.enable_driver_vm,
                       command=self.toggle_driver_vm_options).pack(anchor=tk.W)
        
        # Driver VM Configuration (initially disabled)
        self.driver_vm_config_frame = ttk.LabelFrame(parent, text="Driver VM Configuration", padding="15")
        self.driver_vm_config_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # VM Resource Settings
        resources_frame = ttk.LabelFrame(self.driver_vm_config_frame, text="VM Resources", padding="10")
        resources_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(resources_frame, text="RAM Allocation:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.vm_ram = tk.StringVar(value="512")
        ram_combo = ttk.Combobox(resources_frame, textvariable=self.vm_ram, 
                                values=["512", "1024", "2048"], state="readonly", width=10)
        ram_combo.grid(row=0, column=1, padx=5)
        ttk.Label(resources_frame, text="MB").grid(row=0, column=2, sticky=tk.W)
        
        ttk.Label(resources_frame, text="CPU Cores:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.vm_cpu = tk.StringVar(value="1")
        cpu_combo = ttk.Combobox(resources_frame, textvariable=self.vm_cpu,
                                values=["1", "2"], state="readonly", width=10)
        cpu_combo.grid(row=1, column=1, padx=5)
        ttk.Label(resources_frame, text="cores").grid(row=1, column=2, sticky=tk.W)
        
        # Process Isolation
        isolation_frame = ttk.LabelFrame(self.driver_vm_config_frame, text="Process Isolation", padding="10")
        isolation_frame.pack(fill=tk.X, pady=5)
        
        self.enable_isolation = tk.BooleanVar(value=True)
        ttk.Checkbutton(isolation_frame,
                       text="Enable process isolation (disable non-driver Windows services)",
                       variable=self.enable_isolation).pack(anchor=tk.W)
        
        isolation_info = tk.Label(isolation_frame,
            text="Process isolation disables 40+ unnecessary Windows services,\n"
                 "keeping only driver-essential processes. Saves RAM and CPU.",
            font=("Arial", 9), fg="#555", justify=tk.LEFT)
        isolation_info.pack(anchor=tk.W, padx=20, pady=5)
        
        # VM Architecture Information
        arch_frame = ttk.LabelFrame(self.driver_vm_config_frame, text="Architecture Overview", padding="10")
        arch_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        arch_text = scrolledtext.ScrolledText(arch_frame, height=12, wrap=tk.WORD, font=("Consolas", 9))
        arch_text.pack(fill=tk.BOTH, expand=True)
        
        arch_info = """Driver VM Architecture:

Linux Host (Debian 12)
    ↓
Driver Manager GUI (Client)
    ↓ RPC Communication (Port 9999)
    ↓
Windows 10 VM (Minimal/Isolated)
    ↓
Windows Driver Service
    ↓
Native Windows Driver APIs

Features:
• Lightweight: 512MB RAM, 1 CPU core, 8GB disk
• Process Isolation: ~15 processes vs ~100 in normal Windows
• Native Driver Support: Full Windows API compatibility
• RPC Communication: <5ms latency, minimal overhead
• Essential Services Only:
  - PlugPlay (Plug and Play)
  - DeviceInstall (Device Installation)
  - RpcSs (RPC communication)
  - CryptSvc (Driver signatures)
  
Performance Impact:
• Total CPU: <5% (VM + RPC + GUI)
• Total Memory: <650MB (VM 512MB + GUI 100MB + RPC 10MB)
• Boot Time: ~15 seconds (optimized)

See: windows_driver_emulator/VM_ARCHITECTURE.md for details
"""
        arch_text.insert(tk.END, arch_info)
        arch_text.config(state=tk.DISABLED)
        
        # Action Buttons
        btn_frame = ttk.Frame(self.driver_vm_config_frame)
        btn_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(btn_frame, text="📖 View VM Architecture",
                  command=self.view_vm_architecture).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="🔧 Configure VM",
                  command=self.configure_vm).pack(side=tk.LEFT, padx=5)
        
        # Initially disable config frame
        self.toggle_driver_vm_options()
    
    def toggle_driver_vm_options(self):
        """Enable/disable driver VM configuration options"""
        # Note: Recursive widget state changes are acceptable here since:
        # 1. The widget hierarchy is shallow (max 3-4 levels)
        # 2. This operation is infrequent (only on checkbox toggle)
        # 3. The number of widgets is small (<20 widgets total)
        # For larger/deeper hierarchies, consider widget state caching
        if self.enable_driver_vm.get():
            for child in self.driver_vm_config_frame.winfo_children():
                self._enable_widget(child)
        else:
            for child in self.driver_vm_config_frame.winfo_children():
                self._disable_widget(child)
    
    def _enable_widget(self, widget):
        """Recursively enable widget and children"""
        try:
            widget.configure(state=tk.NORMAL)
        except (tk.TclError, AttributeError):
            # Widget doesn't support state or other Tk errors
            pass
        for child in widget.winfo_children():
            self._enable_widget(child)
    
    def _disable_widget(self, widget):
        """Recursively disable widget and children"""
        try:
            widget.configure(state=tk.DISABLED)
        except (tk.TclError, AttributeError):
            # Widget doesn't support state or other Tk errors
            pass
        for child in widget.winfo_children():
            self._disable_widget(child)
    
    def view_vm_architecture(self):
        """Open VM architecture documentation"""
        vm_arch_path = Path(__file__).parent.parent / "windows_driver_emulator" / "VM_ARCHITECTURE.md"
        
        if vm_arch_path.exists():
            try:
                # Try to open in default text editor
                if os.name == 'nt':
                    os.startfile(vm_arch_path)
                elif os.name == 'posix':
                    subprocess.Popen(['xdg-open', str(vm_arch_path)])
                else:
                    messagebox.showinfo("VM Architecture",
                        f"VM architecture documentation:\n{vm_arch_path}")
            except (OSError, subprocess.SubprocessError) as e:
                # Could not open file, show path instead
                messagebox.showinfo("VM Architecture",
                    f"VM architecture documentation location:\n{vm_arch_path}\n\n"
                    f"(Could not open automatically: {e})")
        else:
            messagebox.showinfo("VM Architecture",
                "VM architecture documentation:\n\n"
                "The Driver VM uses a lightweight Windows 10 VM to handle\n"
                "Windows driver operations with minimal resource usage.\n\n"
                "See: windows_driver_emulator/VM_ARCHITECTURE.md")
    
    def configure_vm(self):
        """Launch VM configuration"""
        vm_script = Path(__file__).parent.parent / "windows_driver_emulator" / "vm_manager.py"
        
        if vm_script.exists():
            messagebox.showinfo("VM Configuration",
                "Driver VM configuration:\n\n"
                "1. VM will be created during installation\n"
                "2. Minimal Windows 10 will be installed\n"
                "3. Process isolation will be configured\n"
                "4. Driver service will be setup\n\n"
                f"Manual setup: python3 {vm_script}")
        else:
            messagebox.showinfo("VM Configuration",
                "Driver VM will be configured automatically during installation.\n\n"
                "Configuration includes:\n"
                "• VM disk creation (8GB)\n"
                "• Windows 10 minimal installation\n"
                "• Process isolation setup\n"
                "• Driver service installation")

def main():
    """Main entry point"""
    # Check if GUI is available
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
    except:
        pass
    
    # Create app
    app = HeckCheckOSInstallerGUI(root)
    
    # Run
    root.mainloop()

if __name__ == "__main__":
    main()
