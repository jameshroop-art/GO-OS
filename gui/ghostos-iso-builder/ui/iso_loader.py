#!/usr/bin/env python3
"""
ISO Loader Widget - Supports multiple ISO sources with component selection
"""

import os
from pathlib import Path
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                              QPushButton, QListWidget, QListWidgetItem,
                              QFileDialog, QGroupBox, QCheckBox, QTreeWidget,
                              QTreeWidgetItem, QProgressBar, QMessageBox,
                              QScrollArea, QFrame)
from PyQt6.QtCore import Qt, pyqtSignal, QThread
from PyQt6.QtGui import QFont


class ISOAnalyzerThread(QThread):
    """Background thread for analyzing ISO contents"""
    progress_update = pyqtSignal(int, str)
    analysis_complete = pyqtSignal(dict)
    
    def __init__(self, iso_path):
        super().__init__()
        self.iso_path = iso_path
        
    def run(self):
        """Analyze ISO and extract package information"""
        try:
            self.progress_update.emit(10, "Reading ISO metadata...")
            
            # Simulate ISO analysis (in real implementation, would parse ISO)
            import time
            time.sleep(0.5)
            
            self.progress_update.emit(30, "Extracting package list...")
            time.sleep(0.5)
            
            self.progress_update.emit(60, "Categorizing components...")
            time.sleep(0.5)
            
            # Mock data - in real implementation, extract from ISO
            iso_info = {
                'path': self.iso_path,
                'name': Path(self.iso_path).name,
                'size': os.path.getsize(self.iso_path) if os.path.exists(self.iso_path) else 0,
                'components': {
                    'Base System': {
                        'Linux Kernel': {'size': '250MB', 'required': True},
                        'System Libraries': {'size': '180MB', 'required': True},
                        'Init System': {'size': '50MB', 'required': True},
                    },
                    'Desktop Environment': {
                        'MATE Desktop': {'size': '420MB', 'required': False},
                        'XFCE Desktop': {'size': '380MB', 'required': False},
                        'KDE Plasma': {'size': '650MB', 'required': False},
                        'GNOME Desktop': {'size': '720MB', 'required': False},
                    },
                    'Security Tools': {
                        'Parrot Security Suite': {'size': '1.2GB', 'required': False},
                        'Network Analysis': {'size': '450MB', 'required': False},
                        'Forensics Tools': {'size': '380MB', 'required': False},
                        'Password Cracking': {'size': '280MB', 'required': False},
                    },
                    'Development Tools': {
                        'GCC/G++ Compilers': {'size': '320MB', 'required': False},
                        'Python Development': {'size': '180MB', 'required': False},
                        'Node.js & NPM': {'size': '120MB', 'required': False},
                        'Git & Version Control': {'size': '85MB', 'required': False},
                    },
                    'Gaming Support': {
                        'Steam': {'size': '450MB', 'required': False},
                        'Lutris': {'size': '120MB', 'required': False},
                        'Wine/Proton': {'size': '380MB', 'required': False},
                        'GPU Drivers': {'size': '520MB', 'required': False},
                    },
                    'Productivity': {
                        'LibreOffice Suite': {'size': '620MB', 'required': False},
                        'GIMP': {'size': '180MB', 'required': False},
                        'Inkscape': {'size': '120MB', 'required': False},
                        'Blender': {'size': '350MB', 'required': False},
                    },
                }
            }
            
            self.progress_update.emit(100, "Analysis complete!")
            self.analysis_complete.emit(iso_info)
            
        except Exception as e:
            self.progress_update.emit(0, f"Error: {str(e)}")


class ISOLoaderWidget(QWidget):
    """Widget for loading multiple ISOs and selecting components"""
    
    iso_loaded = pyqtSignal(str)
    components_changed = pyqtSignal(dict)
    
    def __init__(self):
        super().__init__()
        self.loaded_isos = []  # List of loaded ISO info dicts
        self.selected_components = {}  # Components selected for installation
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the ISO loader interface"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Header
        header_label = QLabel("📀 Multi-ISO Source Loader")
        header_font = QFont()
        header_font.setPointSize(14)
        header_font.setBold(True)
        header_label.setFont(header_font)
        layout.addWidget(header_label)
        
        info_label = QLabel("Load multiple ISO sources and select components to include in your build")
        info_label.setStyleSheet("color: #888888; font-size: 10pt;")
        layout.addWidget(info_label)
        
        layout.addSpacing(10)
        
        # ISO Source List
        iso_group = QGroupBox("Loaded ISO Sources")
        iso_layout = QVBoxLayout(iso_group)
        
        # List of loaded ISOs
        self.iso_list = QListWidget()
        self.iso_list.setMaximumHeight(150)
        self.iso_list.currentItemChanged.connect(self.on_iso_selected)
        iso_layout.addWidget(self.iso_list)
        
        # Buttons for ISO management
        iso_buttons = QHBoxLayout()
        
        add_iso_btn = QPushButton("➕ Add ISO")
        add_iso_btn.clicked.connect(self.add_iso)
        iso_buttons.addWidget(add_iso_btn)
        
        add_usb_btn = QPushButton("💾 Load from USB")
        add_usb_btn.clicked.connect(self.load_from_usb)
        iso_buttons.addWidget(add_usb_btn)
        
        remove_iso_btn = QPushButton("➖ Remove")
        remove_iso_btn.clicked.connect(self.remove_iso)
        iso_buttons.addWidget(remove_iso_btn)
        
        analyze_btn = QPushButton("🔍 Analyze")
        analyze_btn.clicked.connect(self.analyze_current_iso)
        iso_buttons.addWidget(analyze_btn)
        
        iso_layout.addLayout(iso_buttons)
        layout.addWidget(iso_group)
        
        # Progress bar for ISO analysis
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        
        self.progress_label = QLabel("")
        self.progress_label.setStyleSheet("color: #0078d4; font-size: 9pt;")
        self.progress_label.setVisible(False)
        layout.addWidget(self.progress_label)
        
        # Component Selection Tree
        component_group = QGroupBox("Component Selection")
        component_layout = QVBoxLayout(component_group)
        
        # Instructions
        instruction_label = QLabel("Select components to include in your custom build:")
        instruction_label.setStyleSheet("font-size: 10pt;")
        component_layout.addWidget(instruction_label)
        
        # Quick selection buttons
        quick_select = QHBoxLayout()
        
        select_all_btn = QPushButton("✓ Select All")
        select_all_btn.clicked.connect(self.select_all_components)
        quick_select.addWidget(select_all_btn)
        
        select_none_btn = QPushButton("✗ Select None")
        select_none_btn.clicked.connect(self.select_no_components)
        quick_select.addWidget(select_none_btn)
        
        select_minimal_btn = QPushButton("⚡ Minimal")
        select_minimal_btn.clicked.connect(self.select_minimal_components)
        quick_select.addWidget(select_minimal_btn)
        
        select_full_btn = QPushButton("📦 Full Install")
        select_full_btn.clicked.connect(self.select_full_components)
        quick_select.addWidget(select_full_btn)
        
        component_layout.addLayout(quick_select)
        
        # Component tree
        self.component_tree = QTreeWidget()
        self.component_tree.setHeaderLabels(["Component", "Size", "Source ISO"])
        self.component_tree.setColumnWidth(0, 300)
        self.component_tree.setColumnWidth(1, 100)
        self.component_tree.itemChanged.connect(self.on_component_toggled)
        component_layout.addWidget(self.component_tree)
        
        # Summary
        self.summary_label = QLabel("Total Size: 0 MB | Components: 0 selected")
        self.summary_label.setStyleSheet("font-weight: bold; color: #0078d4; font-size: 10pt;")
        component_layout.addWidget(self.summary_label)
        
        layout.addWidget(component_group)
        
        # UI Compatibility Selection
        ui_group = QGroupBox("🖥️ UI Compatibility")
        ui_layout = QVBoxLayout(ui_group)
        
        ui_info = QLabel("Select target desktop environments for compatibility:")
        ui_layout.addWidget(ui_info)
        
        ui_checkboxes = QHBoxLayout()
        
        self.mate_check = QCheckBox("MATE")
        self.mate_check.setChecked(True)
        ui_checkboxes.addWidget(self.mate_check)
        
        self.xfce_check = QCheckBox("XFCE")
        self.xfce_check.setChecked(True)
        ui_checkboxes.addWidget(self.xfce_check)
        
        self.kde_check = QCheckBox("KDE")
        ui_checkboxes.addWidget(self.kde_check)
        
        self.gnome_check = QCheckBox("GNOME")
        ui_checkboxes.addWidget(self.gnome_check)
        
        self.cinnamon_check = QCheckBox("Cinnamon")
        ui_checkboxes.addWidget(self.cinnamon_check)
        
        ui_layout.addLayout(ui_checkboxes)
        layout.addWidget(ui_group)
        
        # Custom Files for Recovery/Base System
        custom_files_group = QGroupBox("🗂️ Custom Files & Recovery Integration")
        custom_files_layout = QVBoxLayout(custom_files_group)
        
        custom_info = QLabel(
            "Add custom files to include in base OS and Recovery partition.\n"
            "These files will persist through system recovery."
        )
        custom_info.setWordWrap(True)
        custom_files_layout.addWidget(custom_info)
        
        # Custom files list
        self.custom_files_list = QListWidget()
        self.custom_files_list.setMaximumHeight(150)
        custom_files_layout.addWidget(self.custom_files_list)
        
        # Custom files buttons
        custom_buttons = QHBoxLayout()
        
        add_file_btn = QPushButton("📄 Add File")
        add_file_btn.clicked.connect(self.add_custom_file)
        custom_buttons.addWidget(add_file_btn)
        
        add_folder_btn = QPushButton("📁 Add Folder")
        add_folder_btn.clicked.connect(self.add_custom_folder)
        custom_buttons.addWidget(add_folder_btn)
        
        load_usb_files_btn = QPushButton("💾 Load from USB")
        load_usb_files_btn.clicked.connect(self.load_files_from_usb)
        custom_buttons.addWidget(load_usb_files_btn)
        
        remove_custom_btn = QPushButton("➖ Remove")
        remove_custom_btn.clicked.connect(self.remove_custom_file)
        custom_buttons.addWidget(remove_custom_btn)
        
        custom_files_layout.addLayout(custom_buttons)
        
        # Recovery integration options
        recovery_options = QHBoxLayout()
        
        self.include_recovery_check = QCheckBox("Include in Recovery partition")
        self.include_recovery_check.setChecked(True)
        self.include_recovery_check.setToolTip("Files will be available after system recovery")
        recovery_options.addWidget(self.include_recovery_check)
        
        self.include_base_check = QCheckBox("Include in Base system")
        self.include_base_check.setChecked(True)
        self.include_base_check.setToolTip("Files will be installed in the base OS")
        recovery_options.addWidget(self.include_base_check)
        
        custom_files_layout.addLayout(recovery_options)
        
        # Installation path
        path_layout = QHBoxLayout()
        path_layout.addWidget(QLabel("Install to:"))
        self.install_path_input = QLineEdit()
        self.install_path_input.setPlaceholderText("/opt/custom or /home/username/...")
        self.install_path_input.setText("/opt/custom")
        path_layout.addWidget(self.install_path_input)
        custom_files_layout.addLayout(path_layout)
        
        layout.addWidget(custom_files_group)
        
        layout.addStretch()
        
    def add_iso(self):
        """Add a new ISO source"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select ISO File",
            str(Path.home()),
            "ISO Files (*.iso);;All Files (*)"
        )
        
        if file_path:
            self.load_iso(file_path)
            
    def load_iso(self, iso_path):
        """Load an ISO file"""
        if not os.path.exists(iso_path):
            QMessageBox.warning(self, "Error", f"ISO file not found: {iso_path}")
            return
            
        # Check if already loaded
        for iso in self.loaded_isos:
            if iso['path'] == iso_path:
                QMessageBox.information(self, "Already Loaded", "This ISO is already loaded.")
                return
                
        # Add to list
        iso_name = Path(iso_path).name
        item = QListWidgetItem(f"📀 {iso_name}")
        item.setData(Qt.ItemDataRole.UserRole, iso_path)
        self.iso_list.addItem(item)
        
        # Start analysis in background
        self.analyze_iso(iso_path)
        
        self.iso_loaded.emit(iso_path)
        
    def analyze_iso(self, iso_path):
        """Analyze ISO in background thread"""
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.progress_label.setVisible(True)
        self.progress_label.setText("Starting analysis...")
        
        self.analyzer_thread = ISOAnalyzerThread(iso_path)
        self.analyzer_thread.progress_update.connect(self.on_analysis_progress)
        self.analyzer_thread.analysis_complete.connect(self.on_analysis_complete)
        self.analyzer_thread.start()
        
    def on_analysis_progress(self, progress, message):
        """Update progress during ISO analysis"""
        self.progress_bar.setValue(progress)
        self.progress_label.setText(message)
        
    def on_analysis_complete(self, iso_info):
        """Handle completion of ISO analysis"""
        self.loaded_isos.append(iso_info)
        self.populate_component_tree()
        
        self.progress_bar.setVisible(False)
        self.progress_label.setVisible(False)
        
        QMessageBox.information(
            self,
            "Analysis Complete",
            f"Successfully analyzed: {iso_info['name']}\n\n"
            f"Found {sum(len(cats) for cats in iso_info['components'].values())} components"
        )
        
    def remove_iso(self):
        """Remove selected ISO from list"""
        current_item = self.iso_list.currentItem()
        if current_item:
            iso_path = current_item.data(Qt.ItemDataRole.UserRole)
            
            # Remove from loaded list
            self.loaded_isos = [iso for iso in self.loaded_isos if iso['path'] != iso_path]
            
            # Remove from UI
            self.iso_list.takeItem(self.iso_list.row(current_item))
            
            # Refresh component tree
            self.populate_component_tree()
            
    def analyze_current_iso(self):
        """Re-analyze currently selected ISO"""
        current_item = self.iso_list.currentItem()
        if current_item:
            iso_path = current_item.data(Qt.ItemDataRole.UserRole)
            self.analyze_iso(iso_path)
        else:
            QMessageBox.information(self, "No Selection", "Please select an ISO to analyze.")
            
    def on_iso_selected(self, current, previous):
        """Handle ISO selection change"""
        if current:
            iso_path = current.data(Qt.ItemDataRole.UserRole)
            # Could highlight components from this ISO in the tree
            
    def populate_component_tree(self):
        """Populate the component tree with all loaded ISOs"""
        self.component_tree.clear()
        
        for iso_info in self.loaded_isos:
            iso_name = iso_info['name']
            
            for category, components in iso_info['components'].items():
                # Find or create category
                category_item = None
                for i in range(self.component_tree.topLevelItemCount()):
                    item = self.component_tree.topLevelItem(i)
                    if item.text(0) == category:
                        category_item = item
                        break
                        
                if not category_item:
                    category_item = QTreeWidgetItem([category, "", ""])
                    category_item.setFlags(category_item.flags() | Qt.ItemFlag.ItemIsAutoTristate)
                    font = QFont()
                    font.setBold(True)
                    category_item.setFont(0, font)
                    self.component_tree.addTopLevelItem(category_item)
                    category_item.setExpanded(True)
                    
                # Add components
                for comp_name, comp_info in components.items():
                    comp_item = QTreeWidgetItem([
                        comp_name,
                        comp_info['size'],
                        Path(iso_name).stem
                    ])
                    comp_item.setFlags(comp_item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
                    
                    if comp_info.get('required', False):
                        comp_item.setCheckState(0, Qt.CheckState.Checked)
                        comp_item.setDisabled(True)
                        comp_item.setToolTip(0, "Required component")
                    else:
                        comp_item.setCheckState(0, Qt.CheckState.Unchecked)
                        
                    category_item.addChild(comp_item)
                    
        self.update_summary()
        
    def on_component_toggled(self, item, column):
        """Handle component checkbox toggle"""
        if column == 0:
            self.update_summary()
            self.update_selected_components()
            
    def update_selected_components(self):
        """Update the selected components dict"""
        self.selected_components = {}
        
        for i in range(self.component_tree.topLevelItemCount()):
            category = self.component_tree.topLevelItem(i)
            category_name = category.text(0)
            self.selected_components[category_name] = []
            
            for j in range(category.childCount()):
                component = category.child(j)
                if component.checkState(0) == Qt.CheckState.Checked:
                    self.selected_components[category_name].append({
                        'name': component.text(0),
                        'size': component.text(1),
                        'source': component.text(2)
                    })
                    
        self.components_changed.emit(self.selected_components)
        
    def update_summary(self):
        """Update the summary label"""
        total_components = 0
        total_size_mb = 0
        
        for i in range(self.component_tree.topLevelItemCount()):
            category = self.component_tree.topLevelItem(i)
            for j in range(category.childCount()):
                component = category.child(j)
                if component.checkState(0) == Qt.CheckState.Checked:
                    total_components += 1
                    size_str = component.text(1)
                    # Parse size (e.g., "250MB", "1.2GB")
                    try:
                        if 'GB' in size_str:
                            size_val = float(size_str.replace('GB', '').strip()) * 1024
                        else:
                            size_val = float(size_str.replace('MB', '').strip())
                        total_size_mb += size_val
                    except:
                        pass
                        
        # Format size
        if total_size_mb >= 1024:
            size_str = f"{total_size_mb / 1024:.2f} GB"
        else:
            size_str = f"{total_size_mb:.0f} MB"
            
        self.summary_label.setText(
            f"Total Size: {size_str} | Components: {total_components} selected"
        )
        
    def select_all_components(self):
        """Select all non-required components"""
        for i in range(self.component_tree.topLevelItemCount()):
            category = self.component_tree.topLevelItem(i)
            for j in range(category.childCount()):
                component = category.child(j)
                if not component.isDisabled():
                    component.setCheckState(0, Qt.CheckState.Checked)
                    
    def select_no_components(self):
        """Deselect all non-required components"""
        for i in range(self.component_tree.topLevelItemCount()):
            category = self.component_tree.topLevelItem(i)
            for j in range(category.childCount()):
                component = category.child(j)
                if not component.isDisabled():
                    component.setCheckState(0, Qt.CheckState.Unchecked)
                    
    def select_minimal_components(self):
        """Select only minimal required components"""
        self.select_no_components()
        # Required components are already checked and disabled
        
    def select_full_components(self):
        """Select all components for full installation"""
        self.select_all_components()
        
    def get_selected_ui_targets(self):
        """Get list of selected UI targets"""
        targets = []
        if self.mate_check.isChecked():
            targets.append('MATE')
        if self.xfce_check.isChecked():
            targets.append('XFCE')
        if self.kde_check.isChecked():
            targets.append('KDE')
        if self.gnome_check.isChecked():
            targets.append('GNOME')
        if self.cinnamon_check.isChecked():
            targets.append('Cinnamon')
        return targets
    
    def load_from_usb(self):
        """Load ISO or files from USB drive"""
        # Detect USB drives
        import subprocess
        try:
            # List block devices that are removable
            result = subprocess.run(
                ['lsblk', '-o', 'NAME,SIZE,TYPE,TRAN,MOUNTPOINT', '-n'],
                capture_output=True,
                text=True
            )
            
            usb_devices = []
            for line in result.stdout.split('\n'):
                if 'usb' in line.lower():
                    parts = line.split()
                    if len(parts) >= 3:
                        device = parts[0]
                        size = parts[1]
                        mountpoint = parts[4] if len(parts) > 4 else "Not mounted"
                        usb_devices.append((device, size, mountpoint))
            
            if not usb_devices:
                QMessageBox.information(
                    self,
                    "No USB Devices",
                    "No USB devices detected.\n\n"
                    "Please insert a USB drive and try again."
                )
                return
            
            # Show USB device selection dialog
            from PyQt6.QtWidgets import QInputDialog
            device_list = [f"{dev} ({size}) - {mount}" for dev, size, mount in usb_devices]
            device, ok = QInputDialog.getItem(
                self,
                "Select USB Device",
                "Choose USB device to load from:",
                device_list,
                0,
                False
            )
            
            if ok and device:
                # Get the selected device info
                idx = device_list.index(device)
                dev_name, size, mountpoint = usb_devices[idx]
                
                if mountpoint == "Not mounted":
                    QMessageBox.warning(
                        self,
                        "Device Not Mounted",
                        f"USB device {dev_name} is not mounted.\n\n"
                        "Please mount the device first."
                    )
                    return
                
                # Browse for ISO on USB
                file_path, _ = QFileDialog.getOpenFileName(
                    self,
                    "Select ISO from USB",
                    mountpoint,
                    "ISO Files (*.iso);;All Files (*)"
                )
                
                if file_path:
                    self.load_iso(file_path)
                    
        except Exception as e:
            QMessageBox.critical(
                self,
                "Error",
                f"Error detecting USB devices:\n{str(e)}\n\n"
                "Try running with sudo/administrator privileges."
            )
    
    def add_custom_file(self):
        """Add custom file to include in OS"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select File to Include",
            str(Path.home()),
            "All Files (*)"
        )
        
        if file_path:
            file_name = Path(file_path).name
            file_size = Path(file_path).stat().st_size / 1024  # KB
            
            item_text = f"📄 {file_name} ({file_size:.1f} KB) → {file_path}"
            item = QListWidgetItem(item_text)
            item.setData(Qt.ItemDataRole.UserRole, {
                'type': 'file',
                'path': file_path,
                'name': file_name,
                'size': file_size
            })
            self.custom_files_list.addItem(item)
    
    def add_custom_folder(self):
        """Add custom folder to include in OS"""
        folder_path = QFileDialog.getExistingDirectory(
            self,
            "Select Folder to Include",
            str(Path.home())
        )
        
        if folder_path:
            folder_name = Path(folder_path).name
            
            # Calculate folder size
            folder_size = sum(
                f.stat().st_size for f in Path(folder_path).rglob('*') if f.is_file()
            ) / (1024 * 1024)  # MB
            
            item_text = f"📁 {folder_name}/ ({folder_size:.1f} MB) → {folder_path}"
            item = QListWidgetItem(item_text)
            item.setData(Qt.ItemDataRole.UserRole, {
                'type': 'folder',
                'path': folder_path,
                'name': folder_name,
                'size': folder_size
            })
            self.custom_files_list.addItem(item)
    
    def load_files_from_usb(self):
        """Load files directly from USB for inclusion"""
        import subprocess
        try:
            # Detect mounted USB devices
            result = subprocess.run(
                ['lsblk', '-o', 'NAME,MOUNTPOINT', '-n'],
                capture_output=True,
                text=True
            )
            
            mountpoints = []
            for line in result.stdout.split('\n'):
                parts = line.split()
                if len(parts) >= 2 and '/media' in parts[1]:
                    mountpoints.append(parts[1])
            
            if not mountpoints:
                QMessageBox.information(
                    self,
                    "No Mounted USB",
                    "No mounted USB devices found.\n\n"
                    "Please mount your USB drive and try again."
                )
                return
            
            from PyQt6.QtWidgets import QInputDialog
            mountpoint, ok = QInputDialog.getItem(
                self,
                "Select USB Mount",
                "Choose USB mount point:",
                mountpoints,
                0,
                False
            )
            
            if ok and mountpoint:
                # Ask user what to load
                reply = QMessageBox.question(
                    self,
                    "Load Files or Folder?",
                    "What would you like to load from USB?",
                    QMessageBox.StandardButton.Open | 
                    QMessageBox.StandardButton.Save | 
                    QMessageBox.StandardButton.Cancel
                )
                
                if reply == QMessageBox.StandardButton.Open:
                    # Load files
                    files, _ = QFileDialog.getOpenFileNames(
                        self,
                        "Select Files from USB",
                        mountpoint,
                        "All Files (*)"
                    )
                    for file_path in files:
                        self.add_file_to_list(file_path)
                        
                elif reply == QMessageBox.StandardButton.Save:
                    # Load folder
                    folder = QFileDialog.getExistingDirectory(
                        self,
                        "Select Folder from USB",
                        mountpoint
                    )
                    if folder:
                        self.add_folder_to_list(folder)
                        
        except Exception as e:
            QMessageBox.critical(
                self,
                "Error",
                f"Error loading from USB:\n{str(e)}"
            )
    
    def add_file_to_list(self, file_path):
        """Helper to add file to custom files list"""
        file_name = Path(file_path).name
        file_size = Path(file_path).stat().st_size / 1024  # KB
        
        item_text = f"📄 {file_name} ({file_size:.1f} KB) → {file_path}"
        item = QListWidgetItem(item_text)
        item.setData(Qt.ItemDataRole.UserRole, {
            'type': 'file',
            'path': file_path,
            'name': file_name,
            'size': file_size
        })
        self.custom_files_list.addItem(item)
    
    def add_folder_to_list(self, folder_path):
        """Helper to add folder to custom files list"""
        folder_name = Path(folder_path).name
        folder_size = sum(
            f.stat().st_size for f in Path(folder_path).rglob('*') if f.is_file()
        ) / (1024 * 1024)  # MB
        
        item_text = f"📁 {folder_name}/ ({folder_size:.1f} MB) → {folder_path}"
        item = QListWidgetItem(item_text)
        item.setData(Qt.ItemDataRole.UserRole, {
            'type': 'folder',
            'path': folder_path,
            'name': folder_name,
            'size': folder_size
        })
        self.custom_files_list.addItem(item)
    
    def remove_custom_file(self):
        """Remove selected custom file"""
        current_item = self.custom_files_list.currentItem()
        if current_item:
            self.custom_files_list.takeItem(
                self.custom_files_list.row(current_item)
            )
    
    def get_custom_files(self):
        """Get list of custom files to include"""
        custom_files = []
        for i in range(self.custom_files_list.count()):
            item = self.custom_files_list.item(i)
            data = item.data(Qt.ItemDataRole.UserRole)
            data['include_recovery'] = self.include_recovery_check.isChecked()
            data['include_base'] = self.include_base_check.isChecked()
            data['install_path'] = self.install_path_input.text()
            custom_files.append(data)
        return custom_files
