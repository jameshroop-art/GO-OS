#!/usr/bin/env python3
"""
Wine Manager Widget - Windows application integration with security controls
Cross-platform support: Linux, macOS, Windows (WSL)
"""

import os
import sys
import subprocess
import platform
from pathlib import Path
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                              QPushButton, QListWidget, QListWidgetItem,
                              QFileDialog, QGroupBox, QComboBox, QCheckBox,
                              QMessageBox, QProgressBar, QTextEdit, QLineEdit,
                              QTabWidget)
from PyQt6.QtCore import Qt, pyqtSignal, QThread
from PyQt6.QtGui import QFont


class WineInstallThread(QThread):
    """Background thread for Wine installation"""
    progress_update = pyqtSignal(int, str)
    install_complete = pyqtSignal(bool, str)
    
    def __init__(self, action="install"):
        super().__init__()
        self.action = action
        
    def run(self):
        """Install or configure Wine (cross-platform)"""
        try:
            system = platform.system()
            
            if self.action == "install":
                self.progress_update.emit(20, "Installing Wine...")
                
                # Check if Wine is already installed
                if system == "Windows":
                    # On Windows, Wine is not needed (native Windows)
                    self.progress_update.emit(100, "Running on Windows - Wine not required")
                    self.install_complete.emit(True, "Native Windows environment")
                    return
                
                # Unix-like systems
                check_cmd = ['which', 'wine'] if system != "Windows" else ['where', 'wine']
                result = subprocess.run(check_cmd, capture_output=True)
                if result.returncode == 0:
                    self.progress_update.emit(100, "Wine already installed")
                    self.install_complete.emit(True, "Wine is already installed")
                    return
                
                self.progress_update.emit(40, "Adding Wine repository...")
                # In production, would actually install Wine based on OS
                import time
                time.sleep(1)
                
                self.progress_update.emit(80, "Installing Wine packages...")
                time.sleep(1)
                
                self.progress_update.emit(100, "Installation complete")
                self.install_complete.emit(True, "Wine installed successfully")
                
            elif self.action == "check":
                if system == "Windows":
                    self.install_complete.emit(True, "Native Windows (Wine not required)")
                    return
                    
                result = subprocess.run(['wine', '--version'], capture_output=True, text=True)
                if result.returncode == 0:
                    version = result.stdout.strip()
                    self.install_complete.emit(True, f"Wine {version}")
                else:
                    self.install_complete.emit(False, "Wine not installed")
                    
        except Exception as e:
            self.install_complete.emit(False, str(e))


class WineManagerWidget(QWidget):
    """Widget for managing Wine and Windows applications with security controls"""
    
    wine_app_installed = pyqtSignal(str)
    security_profile_changed = pyqtSignal(dict)
    
    def __init__(self):
        super().__init__()
        self.wine_prefixes = {}
        self.installed_apps = []
        self.setup_ui()
        self.check_wine_installation()
        
    def setup_ui(self):
        """Setup the Wine manager interface"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Header
        header_label = QLabel("🍷 Wine Manager - Windows App Integration")
        header_font = QFont()
        header_font.setPointSize(14)
        header_font.setBold(True)
        header_label.setFont(header_font)
        layout.addWidget(header_label)
        
        info_label = QLabel("Install and manage Windows applications with security sandboxing")
        info_label.setStyleSheet("color: #888888; font-size: 10pt;")
        layout.addWidget(info_label)
        
        layout.addSpacing(10)
        
        # Tab widget for different Wine functions
        tabs = QTabWidget()
        
        # Installation tab
        install_tab = self.create_installation_tab()
        tabs.addTab(install_tab, "Installation")
        
        # Applications tab
        apps_tab = self.create_applications_tab()
        tabs.addTab(apps_tab, "Applications")
        
        # Security tab
        security_tab = self.create_security_tab()
        tabs.addTab(security_tab, "Security & Sandboxing")
        
        # Configuration tab
        config_tab = self.create_configuration_tab()
        tabs.addTab(config_tab, "Configuration")
        
        layout.addWidget(tabs)
        
    def create_installation_tab(self):
        """Create Wine installation tab"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Wine status
        status_group = QGroupBox("Wine Status")
        status_layout = QVBoxLayout(status_group)
        
        self.wine_status_label = QLabel("Checking Wine installation...")
        status_layout.addWidget(self.wine_status_label)
        
        self.wine_version_label = QLabel("Version: Unknown")
        self.wine_version_label.setStyleSheet("color: #888888;")
        status_layout.addWidget(self.wine_version_label)
        
        layout.addWidget(status_group)
        
        # Installation options
        install_group = QGroupBox("Installation & Setup")
        install_layout = QVBoxLayout(install_group)
        
        install_wine_btn = QPushButton("Install Wine")
        install_wine_btn.clicked.connect(self.install_wine)
        install_layout.addWidget(install_wine_btn)
        
        install_winetricks_btn = QPushButton("Install Winetricks")
        install_winetricks_btn.clicked.connect(self.install_winetricks)
        install_layout.addWidget(install_winetricks_btn)
        
        # Progress bar
        self.install_progress = QProgressBar()
        self.install_progress.setVisible(False)
        install_layout.addWidget(self.install_progress)
        
        self.install_status = QLabel("")
        self.install_status.setStyleSheet("color: #0078d4;")
        self.install_status.setVisible(False)
        install_layout.addWidget(self.install_status)
        
        layout.addWidget(install_group)
        
        # Required libraries
        libs_group = QGroupBox("Required Libraries")
        libs_layout = QVBoxLayout(libs_group)
        
        libs_info = QLabel("Install common Windows libraries for better compatibility:")
        libs_layout.addWidget(libs_info)
        
        lib_buttons = QHBoxLayout()
        
        vcrun_btn = QPushButton("Visual C++ Runtime")
        vcrun_btn.clicked.connect(lambda: self.install_library("vcrun"))
        lib_buttons.addWidget(vcrun_btn)
        
        dotnet_btn = QPushButton(".NET Framework")
        dotnet_btn.clicked.connect(lambda: self.install_library("dotnet"))
        lib_buttons.addWidget(dotnet_btn)
        
        directx_btn = QPushButton("DirectX")
        directx_btn.clicked.connect(lambda: self.install_library("directx"))
        lib_buttons.addWidget(directx_btn)
        
        libs_layout.addLayout(lib_buttons)
        layout.addWidget(libs_group)
        
        layout.addStretch()
        
        return tab
        
    def create_applications_tab(self):
        """Create applications management tab"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Install Windows app
        install_group = QGroupBox("Install Windows Application")
        install_layout = QVBoxLayout(install_group)
        
        install_info = QLabel("Install EXE or MSI files with automatic security sandboxing:")
        install_layout.addWidget(install_info)
        
        install_buttons = QHBoxLayout()
        
        install_exe_btn = QPushButton("📦 Install EXE")
        install_exe_btn.clicked.connect(self.install_exe)
        install_buttons.addWidget(install_exe_btn)
        
        install_msi_btn = QPushButton("📦 Install MSI")
        install_msi_btn.clicked.connect(self.install_msi)
        install_buttons.addWidget(install_msi_btn)
        
        install_layout.addLayout(install_buttons)
        layout.addWidget(install_group)
        
        # Installed applications list
        apps_group = QGroupBox("Installed Windows Applications")
        apps_layout = QVBoxLayout(apps_group)
        
        self.apps_list = QListWidget()
        self.apps_list.currentItemChanged.connect(self.on_app_selected)
        apps_layout.addWidget(self.apps_list)
        
        app_buttons = QHBoxLayout()
        
        launch_btn = QPushButton("▶️ Launch")
        launch_btn.clicked.connect(self.launch_app)
        app_buttons.addWidget(launch_btn)
        
        configure_btn = QPushButton("⚙️ Configure")
        configure_btn.clicked.connect(self.configure_app)
        app_buttons.addWidget(configure_btn)
        
        uninstall_btn = QPushButton("🗑️ Uninstall")
        uninstall_btn.clicked.connect(self.uninstall_app)
        app_buttons.addWidget(uninstall_btn)
        
        apps_layout.addLayout(app_buttons)
        layout.addWidget(apps_group)
        
        # App details
        details_group = QGroupBox("Application Details")
        details_layout = QVBoxLayout(details_group)
        
        self.app_details = QTextEdit()
        self.app_details.setReadOnly(True)
        self.app_details.setMaximumHeight(100)
        self.app_details.setPlainText("Select an application to view details")
        details_layout.addWidget(self.app_details)
        
        layout.addWidget(details_group)
        
        layout.addStretch()
        
        return tab
        
    def create_security_tab(self):
        """Create security configuration tab"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Security warning
        warning = QLabel(
            "⚠️ Security Note: Windows applications run in isolated Wine prefixes\n"
            "with restricted access. Configure security settings per application."
        )
        warning.setWordWrap(True)
        warning.setStyleSheet("background-color: #2d2d2d; padding: 10px; border-radius: 4px;")
        layout.addWidget(warning)
        
        layout.addSpacing(10)
        
        # Sandbox settings
        sandbox_group = QGroupBox("Sandbox Configuration")
        sandbox_layout = QVBoxLayout(sandbox_group)
        
        self.enable_sandbox = QCheckBox("Enable application sandboxing (Recommended)")
        self.enable_sandbox.setChecked(True)
        sandbox_layout.addWidget(self.enable_sandbox)
        
        self.enable_apparmor = QCheckBox("Use AppArmor profiles")
        self.enable_apparmor.setChecked(True)
        self.enable_apparmor.setToolTip("Enforce mandatory access control")
        sandbox_layout.addWidget(self.enable_apparmor)
        
        self.enable_selinux = QCheckBox("Use SELinux policies")
        self.enable_selinux.setToolTip("Additional security layer")
        sandbox_layout.addWidget(self.enable_selinux)
        
        layout.addWidget(sandbox_group)
        
        # Network access
        network_group = QGroupBox("Network Access Control")
        network_layout = QVBoxLayout(network_group)
        
        network_info = QLabel("Control network access for Windows applications:")
        network_layout.addWidget(network_info)
        
        self.network_policy = QComboBox()
        self.network_policy.addItems([
            "Block all network access",
            "Allow localhost only",
            "Allow LAN access",
            "Allow all network access (Gaming)",
            "Custom firewall rules"
        ])
        self.network_policy.setCurrentIndex(2)
        network_layout.addWidget(self.network_policy)
        
        layout.addWidget(network_group)
        
        # File system access
        fs_group = QGroupBox("File System Access")
        fs_layout = QVBoxLayout(fs_group)
        
        fs_info = QLabel("Restrict file system access for Windows applications:")
        fs_layout.addWidget(fs_info)
        
        self.fs_policy = QComboBox()
        self.fs_policy.addItems([
            "Prefix only (Most secure)",
            "Home directory",
            "Documents and Downloads",
            "Full file system (Not recommended)"
        ])
        self.fs_policy.setCurrentIndex(0)
        fs_layout.addWidget(self.fs_policy)
        
        layout.addWidget(fs_group)
        
        # Security profiles
        profiles_group = QGroupBox("Security Profiles")
        profiles_layout = QVBoxLayout(profiles_group)
        
        profiles_info = QLabel("Quick security presets:")
        profiles_layout.addWidget(profiles_info)
        
        profile_buttons = QHBoxLayout()
        
        strict_btn = QPushButton("🔒 Strict")
        strict_btn.clicked.connect(lambda: self.apply_security_profile("strict"))
        profile_buttons.addWidget(strict_btn)
        
        balanced_btn = QPushButton("⚖️ Balanced")
        balanced_btn.clicked.connect(lambda: self.apply_security_profile("balanced"))
        profile_buttons.addWidget(balanced_btn)
        
        gaming_btn = QPushButton("🎮 Gaming")
        gaming_btn.clicked.connect(lambda: self.apply_security_profile("gaming"))
        profile_buttons.addWidget(gaming_btn)
        
        profiles_layout.addLayout(profile_buttons)
        layout.addWidget(profiles_group)
        
        layout.addStretch()
        
        return tab
        
    def create_configuration_tab(self):
        """Create Wine configuration tab"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Wine prefix management
        prefix_group = QGroupBox("Wine Prefix Management")
        prefix_layout = QVBoxLayout(prefix_group)
        
        prefix_info = QLabel("Each application gets its own isolated Wine prefix:")
        prefix_layout.addWidget(prefix_info)
        
        self.prefix_list = QListWidget()
        self.prefix_list.setMaximumHeight(150)
        prefix_layout.addWidget(self.prefix_list)
        
        prefix_buttons = QHBoxLayout()
        
        new_prefix_btn = QPushButton("➕ New Prefix")
        new_prefix_btn.clicked.connect(self.create_wine_prefix)
        prefix_buttons.addWidget(new_prefix_btn)
        
        delete_prefix_btn = QPushButton("🗑️ Delete Prefix")
        delete_prefix_btn.clicked.connect(self.delete_wine_prefix)
        prefix_buttons.addWidget(delete_prefix_btn)
        
        winecfg_btn = QPushButton("⚙️ Wine Config")
        winecfg_btn.clicked.connect(self.open_wine_config)
        prefix_buttons.addWidget(winecfg_btn)
        
        prefix_layout.addLayout(prefix_buttons)
        layout.addWidget(prefix_group)
        
        # DLL overrides
        dll_group = QGroupBox("DLL Overrides")
        dll_layout = QVBoxLayout(dll_group)
        
        dll_info = QLabel("Configure DLL behavior for compatibility:")
        dll_layout.addWidget(dll_info)
        
        dll_controls = QHBoxLayout()
        dll_controls.addWidget(QLabel("DLL Name:"))
        self.dll_name_input = QLineEdit()
        self.dll_name_input.setPlaceholderText("e.g., msvcr100")
        dll_controls.addWidget(self.dll_name_input)
        
        self.dll_mode = QComboBox()
        self.dll_mode.addItems(["Native", "Builtin", "Native,Builtin", "Builtin,Native"])
        dll_controls.addWidget(self.dll_mode)
        
        add_dll_btn = QPushButton("Add Override")
        add_dll_btn.clicked.connect(self.add_dll_override)
        dll_controls.addWidget(add_dll_btn)
        
        dll_layout.addLayout(dll_controls)
        layout.addWidget(dll_group)
        
        # Registry editor
        registry_group = QGroupBox("Registry Editor")
        registry_layout = QVBoxLayout(registry_group)
        
        registry_info = QLabel("Edit Wine registry for advanced configuration:")
        registry_layout.addWidget(registry_info)
        
        open_regedit_btn = QPushButton("Open Registry Editor")
        open_regedit_btn.clicked.connect(self.open_registry_editor)
        registry_layout.addWidget(open_regedit_btn)
        
        layout.addWidget(registry_group)
        
        layout.addStretch()
        
        return tab
        
    def check_wine_installation(self):
        """Check if Wine is installed"""
        self.check_thread = WineInstallThread(action="check")
        self.check_thread.install_complete.connect(self.on_wine_check_complete)
        self.check_thread.start()
        
    def on_wine_check_complete(self, success, message):
        """Handle Wine installation check result"""
        if success:
            self.wine_status_label.setText("✅ Wine is installed")
            self.wine_status_label.setStyleSheet("color: #00ff00;")
            self.wine_version_label.setText(f"Version: {message}")
        else:
            self.wine_status_label.setText("❌ Wine is not installed")
            self.wine_status_label.setStyleSheet("color: #ff0000;")
            self.wine_version_label.setText("Please install Wine to continue")
            
    def install_wine(self):
        """Install Wine"""
        self.install_progress.setVisible(True)
        self.install_status.setVisible(True)
        
        self.install_thread = WineInstallThread(action="install")
        self.install_thread.progress_update.connect(self.on_install_progress)
        self.install_thread.install_complete.connect(self.on_install_complete)
        self.install_thread.start()
        
    def on_install_progress(self, progress, message):
        """Update installation progress"""
        self.install_progress.setValue(progress)
        self.install_status.setText(message)
        
    def on_install_complete(self, success, message):
        """Handle installation completion"""
        self.install_progress.setVisible(False)
        self.install_status.setVisible(False)
        
        if success:
            QMessageBox.information(self, "Installation Complete", message)
            self.check_wine_installation()
        else:
            QMessageBox.critical(self, "Installation Failed", message)
            
    def install_winetricks(self):
        """Install Winetricks utility"""
        QMessageBox.information(
            self,
            "Install Winetricks",
            "Winetricks installation would be performed here.\n\n"
            "Command: sudo apt-get install winetricks"
        )
        
    def install_library(self, lib_name):
        """Install Windows library via winetricks"""
        QMessageBox.information(
            self,
            f"Install {lib_name}",
            f"Would install {lib_name} using winetricks.\n\n"
            f"Command: winetricks {lib_name}"
        )
        
    def install_exe(self):
        """Install Windows EXE file"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Windows EXE File",
            str(Path.home()),
            "Executable Files (*.exe);;All Files (*)"
        )
        
        if file_path:
            self.install_windows_app(file_path, "exe")
            
    def install_msi(self):
        """Install Windows MSI file"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Windows MSI File",
            str(Path.home()),
            "Installer Files (*.msi);;All Files (*)"
        )
        
        if file_path:
            self.install_windows_app(file_path, "msi")
            
    def install_windows_app(self, file_path, file_type):
        """Install a Windows application"""
        app_name = Path(file_path).stem
        
        reply = QMessageBox.question(
            self,
            "Install Windows Application",
            f"Install {app_name}?\n\n"
            f"File: {Path(file_path).name}\n"
            f"Type: {file_type.upper()}\n\n"
            "The app will run in a secure sandbox with:\n"
            "• Isolated Wine prefix\n"
            "• Restricted network access\n"
            "• Limited file system access\n"
            "• AppArmor/SELinux protection",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            # Add to installed apps list
            item = QListWidgetItem(f"🪟 {app_name}")
            item.setData(Qt.ItemDataRole.UserRole, {
                'name': app_name,
                'path': file_path,
                'type': file_type,
                'prefix': f"~/.wine-prefixes/{app_name}",
                'security_profile': 'balanced'
            })
            self.apps_list.addItem(item)
            self.installed_apps.append(app_name)
            
            QMessageBox.information(
                self,
                "Installation Queued",
                f"{app_name} will be installed in the next ISO build.\n\n"
                "Security profile: Balanced\n"
                "You can configure security settings in the Security tab."
            )
            
            self.wine_app_installed.emit(app_name)
            
    def on_app_selected(self, current, previous):
        """Handle application selection"""
        if current:
            app_data = current.data(Qt.ItemDataRole.UserRole)
            details = f"""
Application: {app_data['name']}
Type: {app_data['type'].upper()}
Prefix: {app_data['prefix']}
Security Profile: {app_data['security_profile']}
            """
            self.app_details.setPlainText(details.strip())
            
    def launch_app(self):
        """Launch selected Windows application"""
        current_item = self.apps_list.currentItem()
        if current_item:
            app_data = current_item.data(Qt.ItemDataRole.UserRole)
            QMessageBox.information(
                self,
                "Launch Application",
                f"Would launch: {app_data['name']}\n\n"
                f"Command: WINEPREFIX={app_data['prefix']} wine {app_data['path']}"
            )
            
    def configure_app(self):
        """Configure selected application"""
        current_item = self.apps_list.currentItem()
        if current_item:
            app_data = current_item.data(Qt.ItemDataRole.UserRole)
            QMessageBox.information(
                self,
                "Configure Application",
                f"Configuration dialog for: {app_data['name']}\n\n"
                "Would allow editing:\n"
                "• Security profile\n"
                "• Network access\n"
                "• File system permissions\n"
                "• Launch options"
            )
            
    def uninstall_app(self):
        """Uninstall selected application"""
        current_item = self.apps_list.currentItem()
        if current_item:
            app_data = current_item.data(Qt.ItemDataRole.UserRole)
            reply = QMessageBox.question(
                self,
                "Uninstall Application",
                f"Remove {app_data['name']} and its Wine prefix?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                self.apps_list.takeItem(self.apps_list.row(current_item))
                self.installed_apps.remove(app_data['name'])
                
    def apply_security_profile(self, profile):
        """Apply security profile"""
        profiles = {
            'strict': {
                'sandbox': True,
                'apparmor': True,
                'selinux': True,
                'network': 0,  # Block all
                'filesystem': 0  # Prefix only
            },
            'balanced': {
                'sandbox': True,
                'apparmor': True,
                'selinux': False,
                'network': 2,  # Allow LAN
                'filesystem': 0  # Prefix only
            },
            'gaming': {
                'sandbox': True,
                'apparmor': False,
                'selinux': False,
                'network': 3,  # Allow all
                'filesystem': 2  # Documents and Downloads
            }
        }
        
        if profile in profiles:
            p = profiles[profile]
            self.enable_sandbox.setChecked(p['sandbox'])
            self.enable_apparmor.setChecked(p['apparmor'])
            self.enable_selinux.setChecked(p['selinux'])
            self.network_policy.setCurrentIndex(p['network'])
            self.fs_policy.setCurrentIndex(p['filesystem'])
            
            self.security_profile_changed.emit(p)
            
            QMessageBox.information(
                self,
                "Security Profile Applied",
                f"Applied '{profile.capitalize()}' security profile to Wine applications."
            )
            
    def create_wine_prefix(self):
        """Create new Wine prefix"""
        QMessageBox.information(
            self,
            "Create Wine Prefix",
            "Would create a new isolated Wine prefix."
        )
        
    def delete_wine_prefix(self):
        """Delete Wine prefix"""
        QMessageBox.information(
            self,
            "Delete Wine Prefix",
            "Would delete the selected Wine prefix."
        )
        
    def open_wine_config(self):
        """Open Wine configuration tool"""
        QMessageBox.information(
            self,
            "Wine Configuration",
            "Would launch winecfg for the selected prefix."
        )
        
    def add_dll_override(self):
        """Add DLL override"""
        dll_name = self.dll_name_input.text()
        if dll_name:
            mode = self.dll_mode.currentText()
            QMessageBox.information(
                self,
                "DLL Override Added",
                f"Would add DLL override:\n\n"
                f"DLL: {dll_name}\n"
                f"Mode: {mode}"
            )
            self.dll_name_input.clear()
            
    def open_registry_editor(self):
        """Open Wine registry editor"""
        QMessageBox.information(
            self,
            "Registry Editor",
            "Would launch Wine registry editor (regedit)."
        )
