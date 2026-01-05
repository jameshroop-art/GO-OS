#!/usr/bin/env python3
"""
Security Whitelist Manager - Dynamic security policy management with temporary whitelisting
"""

import json
from datetime import datetime, timedelta
from pathlib import Path
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                              QPushButton, QListWidget, QListWidgetItem,
                              QGroupBox, QComboBox, QCheckBox, QSpinBox,
                              QMessageBox, QTabWidget, QTextEdit, QLineEdit,
                              QTimeEdit, QRadioButton, QButtonGroup)
from PyQt6.QtCore import Qt, pyqtSignal, QTimer, QTime
from PyQt6.QtGui import QFont


class SecurityWhitelistWidget(QWidget):
    """Widget for managing security whitelists with gaming and productivity modes"""
    
    whitelist_changed = pyqtSignal(dict)
    security_mode_changed = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.whitelist_rules = []
        self.active_mode = "strict"  # strict, gaming, productivity
        self.temporary_rules = {}
        self.timer = QTimer()
        self.timer.timeout.connect(self.check_temporary_rules)
        self.timer.start(60000)  # Check every minute
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the security whitelist interface"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Header
        header_label = QLabel("🔒 Security Whitelist Manager")
        header_font = QFont()
        header_font.setPointSize(14)
        header_font.setBold(True)
        header_label.setFont(header_font)
        layout.addWidget(header_label)
        
        info_label = QLabel("Manage security policies with temporary whitelist capabilities")
        info_label.setStyleSheet("color: #888888; font-size: 10pt;")
        layout.addWidget(info_label)
        
        layout.addSpacing(10)
        
        # Security mode selector
        mode_group = QGroupBox("🎯 Security Mode")
        mode_layout = QVBoxLayout(mode_group)
        
        mode_info = QLabel(
            "Choose security mode based on your current activity.\n"
            "System will maintain integrity while allowing necessary access."
        )
        mode_info.setWordWrap(True)
        mode_layout.addWidget(mode_info)
        
        mode_buttons = QHBoxLayout()
        
        self.mode_button_group = QButtonGroup()
        
        strict_radio = QRadioButton("🔒 Strict Mode")
        strict_radio.setToolTip("Maximum security - All restrictions active")
        strict_radio.setChecked(True)
        strict_radio.toggled.connect(lambda: self.set_security_mode("strict"))
        self.mode_button_group.addButton(strict_radio)
        mode_buttons.addWidget(strict_radio)
        
        gaming_radio = QRadioButton("🎮 Gaming Mode")
        gaming_radio.setToolTip("Relaxed restrictions for multiplayer gaming")
        gaming_radio.toggled.connect(lambda: self.set_security_mode("gaming"))
        self.mode_button_group.addButton(gaming_radio)
        mode_buttons.addWidget(gaming_radio)
        
        productivity_radio = QRadioButton("💼 Productivity Mode")
        productivity_radio.setToolTip("Balanced security for work applications")
        productivity_radio.toggled.connect(lambda: self.set_security_mode("productivity"))
        self.mode_button_group.addButton(productivity_radio)
        mode_buttons.addWidget(productivity_radio)
        
        mode_layout.addLayout(mode_buttons)
        
        # Current mode status
        self.mode_status = QLabel("Current Mode: Strict (All security layers active)")
        self.mode_status.setStyleSheet("background-color: #2d2d2d; padding: 8px; border-radius: 4px; font-weight: bold;")
        mode_layout.addWidget(self.mode_status)
        
        layout.addWidget(mode_group)
        
        # Tab widget for different whitelist categories
        tabs = QTabWidget()
        
        # Temporary whitelist tab
        temp_tab = self.create_temporary_whitelist_tab()
        tabs.addTab(temp_tab, "Temporary Whitelist")
        
        # Security layers tab
        layers_tab = self.create_security_layers_tab()
        tabs.addTab(layers_tab, "Security Layers")
        
        # Application whitelist tab
        apps_tab = self.create_application_whitelist_tab()
        tabs.addTab(apps_tab, "Application Whitelist")
        
        # Network whitelist tab
        network_tab = self.create_network_whitelist_tab()
        tabs.addTab(network_tab, "Network Whitelist")
        
        layout.addWidget(tabs)
        
        # Quick actions
        actions_layout = QHBoxLayout()
        actions_layout.addStretch()
        
        revert_btn = QPushButton("↺ Revert to Secure Defaults")
        revert_btn.setStyleSheet("""
            QPushButton {
                background-color: #d83020;
                color: white;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #e84030;
            }
        """)
        revert_btn.clicked.connect(self.revert_to_secure_defaults)
        actions_layout.addWidget(revert_btn)
        
        layout.addLayout(actions_layout)
        
    def create_temporary_whitelist_tab(self):
        """Create temporary whitelist tab"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Info
        info = QLabel(
            "⏱️ Temporary whitelists allow exceptions for a limited time.\n"
            "All temporary rules automatically revert to secure defaults after expiration."
        )
        info.setWordWrap(True)
        info.setStyleSheet("background-color: #2d2d2d; padding: 10px; border-radius: 4px;")
        layout.addWidget(info)
        
        layout.addSpacing(10)
        
        # Add temporary rule
        add_group = QGroupBox("Add Temporary Whitelist Rule")
        add_layout = QVBoxLayout(add_group)
        
        # Rule type
        type_layout = QHBoxLayout()
        type_layout.addWidget(QLabel("Rule Type:"))
        self.temp_rule_type = QComboBox()
        self.temp_rule_type.addItems([
            "Application", 
            "Network Port", 
            "Firewall Rule", 
            "File Access",
            "System Service"
        ])
        type_layout.addWidget(self.temp_rule_type)
        add_layout.addLayout(type_layout)
        
        # Rule target
        target_layout = QHBoxLayout()
        target_layout.addWidget(QLabel("Target:"))
        self.temp_rule_target = QLineEdit()
        self.temp_rule_target.setPlaceholderText("e.g., Steam, Port 25565, /etc/hosts")
        target_layout.addWidget(self.temp_rule_target)
        add_layout.addLayout(target_layout)
        
        # Duration
        duration_layout = QHBoxLayout()
        duration_layout.addWidget(QLabel("Duration:"))
        self.temp_duration_value = QSpinBox()
        self.temp_duration_value.setRange(1, 720)
        self.temp_duration_value.setValue(60)
        duration_layout.addWidget(self.temp_duration_value)
        self.temp_duration_unit = QComboBox()
        self.temp_duration_unit.addItems(["Minutes", "Hours", "Until Session End"])
        duration_layout.addWidget(self.temp_duration_unit)
        duration_layout.addStretch()
        add_layout.addLayout(duration_layout)
        
        add_temp_btn = QPushButton("➕ Add Temporary Rule")
        add_temp_btn.clicked.connect(self.add_temporary_rule)
        add_layout.addWidget(add_temp_btn)
        
        layout.addWidget(add_group)
        
        # Active temporary rules
        active_group = QGroupBox("Active Temporary Rules")
        active_layout = QVBoxLayout(active_group)
        
        self.temp_rules_list = QListWidget()
        self.temp_rules_list.setMaximumHeight(200)
        active_layout.addWidget(self.temp_rules_list)
        
        temp_buttons = QHBoxLayout()
        
        extend_btn = QPushButton("⏰ Extend")
        extend_btn.clicked.connect(self.extend_temporary_rule)
        temp_buttons.addWidget(extend_btn)
        
        revoke_btn = QPushButton("❌ Revoke Now")
        revoke_btn.clicked.connect(self.revoke_temporary_rule)
        temp_buttons.addWidget(revoke_btn)
        
        active_layout.addLayout(temp_buttons)
        layout.addWidget(active_group)
        
        layout.addStretch()
        
        return tab
        
    def create_security_layers_tab(self):
        """Create security layers control tab"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Warning
        warning = QLabel(
            "⚠️ Warning: Disabling security layers reduces system protection.\n"
            "Only toggle these settings if you understand the security implications."
        )
        warning.setWordWrap(True)
        warning.setStyleSheet("background-color: #3d2d2d; padding: 10px; border-radius: 4px; color: #ff8800;")
        layout.addWidget(warning)
        
        layout.addSpacing(10)
        
        # Firewall
        firewall_group = QGroupBox("🔥 Firewall")
        firewall_layout = QVBoxLayout(firewall_group)
        
        self.firewall_enabled = QCheckBox("Enable Firewall (Recommended)")
        self.firewall_enabled.setChecked(True)
        self.firewall_enabled.stateChanged.connect(self.on_security_layer_changed)
        firewall_layout.addWidget(self.firewall_enabled)
        
        self.firewall_gaming_mode = QCheckBox("Gaming Mode - Allow multiplayer ports (UDP 27000-28000)")
        self.firewall_gaming_mode.stateChanged.connect(self.on_security_layer_changed)
        firewall_layout.addWidget(self.firewall_gaming_mode)
        
        self.firewall_productivity_mode = QCheckBox("Productivity Mode - Allow work ports (HTTP/HTTPS, SSH, VPN)")
        self.firewall_productivity_mode.stateChanged.connect(self.on_security_layer_changed)
        firewall_layout.addWidget(self.firewall_productivity_mode)
        
        layout.addWidget(firewall_group)
        
        # AppArmor
        apparmor_group = QGroupBox("🛡️ AppArmor (Mandatory Access Control)")
        apparmor_layout = QVBoxLayout(apparmor_group)
        
        self.apparmor_enabled = QCheckBox("Enable AppArmor (Recommended)")
        self.apparmor_enabled.setChecked(True)
        self.apparmor_enabled.stateChanged.connect(self.on_security_layer_changed)
        apparmor_layout.addWidget(self.apparmor_enabled)
        
        self.apparmor_mode = QComboBox()
        self.apparmor_mode.addItems(["Enforce Mode", "Complain Mode (Logging only)"])
        self.apparmor_mode.currentTextChanged.connect(self.on_security_layer_changed)
        apparmor_layout.addWidget(self.apparmor_mode)
        
        layout.addWidget(apparmor_group)
        
        # SELinux
        selinux_group = QGroupBox("🔐 SELinux (Additional Security Layer)")
        selinux_layout = QVBoxLayout(selinux_group)
        
        self.selinux_enabled = QCheckBox("Enable SELinux")
        self.selinux_enabled.stateChanged.connect(self.on_security_layer_changed)
        selinux_layout.addWidget(self.selinux_enabled)
        
        self.selinux_mode = QComboBox()
        self.selinux_mode.addItems(["Enforcing", "Permissive", "Disabled"])
        self.selinux_mode.setCurrentIndex(2)
        self.selinux_mode.currentTextChanged.connect(self.on_security_layer_changed)
        selinux_layout.addWidget(self.selinux_mode)
        
        layout.addWidget(selinux_group)
        
        # Integrity checking
        integrity_group = QGroupBox("✓ System Integrity")
        integrity_layout = QVBoxLayout(integrity_group)
        
        self.file_integrity_check = QCheckBox("Enable file integrity monitoring (Recommended)")
        self.file_integrity_check.setChecked(True)
        integrity_layout.addWidget(self.file_integrity_check)
        
        self.process_monitor = QCheckBox("Enable process monitoring")
        self.process_monitor.setChecked(True)
        integrity_layout.addWidget(self.process_monitor)
        
        layout.addWidget(integrity_group)
        
        layout.addStretch()
        
        return tab
        
    def create_application_whitelist_tab(self):
        """Create application whitelist tab"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        info = QLabel("Configure which applications can bypass certain security restrictions:")
        layout.addWidget(info)
        
        # Add application
        add_group = QGroupBox("Add Application to Whitelist")
        add_layout = QHBoxLayout(add_group)
        
        add_layout.addWidget(QLabel("Application:"))
        self.app_name_input = QLineEdit()
        self.app_name_input.setPlaceholderText("e.g., Steam, Discord, Browser")
        add_layout.addWidget(self.app_name_input)
        
        add_app_btn = QPushButton("➕ Add")
        add_app_btn.clicked.connect(self.add_app_to_whitelist)
        add_layout.addWidget(add_app_btn)
        
        layout.addWidget(add_group)
        
        # Whitelisted applications
        list_group = QGroupBox("Whitelisted Applications")
        list_layout = QVBoxLayout(list_group)
        
        self.app_whitelist = QListWidget()
        list_layout.addWidget(self.app_whitelist)
        
        app_buttons = QHBoxLayout()
        
        remove_app_btn = QPushButton("➖ Remove")
        remove_app_btn.clicked.connect(self.remove_app_from_whitelist)
        app_buttons.addWidget(remove_app_btn)
        
        configure_app_btn = QPushButton("⚙️ Configure Permissions")
        configure_app_btn.clicked.connect(self.configure_app_permissions)
        app_buttons.addWidget(configure_app_btn)
        
        list_layout.addLayout(app_buttons)
        layout.addWidget(list_group)
        
        layout.addStretch()
        
        return tab
        
    def create_network_whitelist_tab(self):
        """Create network whitelist tab"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        info = QLabel("Manage network access rules and port whitelisting:")
        layout.addWidget(info)
        
        # Add network rule
        add_group = QGroupBox("Add Network Rule")
        add_layout = QVBoxLayout(add_group)
        
        rule_layout = QHBoxLayout()
        rule_layout.addWidget(QLabel("Protocol:"))
        self.net_protocol = QComboBox()
        self.net_protocol.addItems(["TCP", "UDP", "Both"])
        rule_layout.addWidget(self.net_protocol)
        
        rule_layout.addWidget(QLabel("Port:"))
        self.net_port = QLineEdit()
        self.net_port.setPlaceholderText("e.g., 25565 or 27000-28000")
        rule_layout.addWidget(self.net_port)
        
        add_net_btn = QPushButton("➕ Add Rule")
        add_net_btn.clicked.connect(self.add_network_rule)
        rule_layout.addWidget(add_net_btn)
        
        add_layout.addLayout(rule_layout)
        layout.addWidget(add_group)
        
        # Network rules list
        list_group = QGroupBox("Active Network Rules")
        list_layout = QVBoxLayout(list_group)
        
        self.network_rules_list = QListWidget()
        list_layout.addWidget(self.network_rules_list)
        
        net_buttons = QHBoxLayout()
        
        remove_net_btn = QPushButton("➖ Remove Rule")
        remove_net_btn.clicked.connect(self.remove_network_rule)
        net_buttons.addWidget(remove_net_btn)
        
        list_layout.addLayout(net_buttons)
        layout.addWidget(list_group)
        
        # Gaming presets
        gaming_group = QGroupBox("🎮 Gaming Presets")
        gaming_layout = QVBoxLayout(gaming_group)
        
        gaming_info = QLabel("Quick presets for popular games:")
        gaming_layout.addWidget(gaming_info)
        
        preset_buttons = QHBoxLayout()
        
        minecraft_btn = QPushButton("Minecraft")
        minecraft_btn.clicked.connect(lambda: self.apply_gaming_preset("minecraft"))
        preset_buttons.addWidget(minecraft_btn)
        
        steam_btn = QPushButton("Steam")
        steam_btn.clicked.connect(lambda: self.apply_gaming_preset("steam"))
        preset_buttons.addWidget(steam_btn)
        
        valorant_btn = QPushButton("Valorant")
        valorant_btn.clicked.connect(lambda: self.apply_gaming_preset("valorant"))
        preset_buttons.addWidget(valorant_btn)
        
        gaming_layout.addLayout(preset_buttons)
        layout.addWidget(gaming_group)
        
        layout.addStretch()
        
        return tab
        
    def set_security_mode(self, mode):
        """Set security mode"""
        self.active_mode = mode
        
        mode_configs = {
            'strict': {
                'label': 'Strict (All security layers active)',
                'firewall': True,
                'apparmor': True,
                'selinux': False,
                'gaming_ports': False,
                'productivity_ports': False
            },
            'gaming': {
                'label': 'Gaming (Relaxed firewall for multiplayer)',
                'firewall': True,
                'apparmor': False,
                'selinux': False,
                'gaming_ports': True,
                'productivity_ports': False
            },
            'productivity': {
                'label': 'Productivity (Balanced security)',
                'firewall': True,
                'apparmor': True,
                'selinux': False,
                'gaming_ports': False,
                'productivity_ports': True
            }
        }
        
        if mode in mode_configs:
            config = mode_configs[mode]
            self.mode_status.setText(f"Current Mode: {config['label']}")
            
            # Apply mode configuration
            if hasattr(self, 'firewall_enabled'):
                self.firewall_enabled.setChecked(config['firewall'])
                self.firewall_gaming_mode.setChecked(config['gaming_ports'])
                self.firewall_productivity_mode.setChecked(config['productivity_ports'])
                self.apparmor_enabled.setChecked(config['apparmor'])
                self.selinux_enabled.setChecked(config['selinux'])
            
            self.security_mode_changed.emit(mode)
            
            QMessageBox.information(
                self,
                "Security Mode Changed",
                f"Switched to {config['label']}\n\n"
                "Security settings have been adjusted accordingly."
            )
            
    def add_temporary_rule(self):
        """Add temporary whitelist rule"""
        rule_type = self.temp_rule_type.currentText()
        target = self.temp_rule_target.text()
        duration_value = self.temp_duration_value.value()
        duration_unit = self.temp_duration_unit.currentText()
        
        if not target:
            QMessageBox.warning(self, "Missing Target", "Please specify a target for the rule.")
            return
        
        # Calculate expiration
        if duration_unit == "Until Session End":
            expiration = "Session End"
        else:
            multiplier = 60 if duration_unit == "Hours" else 1
            expiration_time = datetime.now() + timedelta(minutes=duration_value * multiplier)
            expiration = expiration_time.strftime("%Y-%m-%d %H:%M")
        
        # Add to temporary rules
        rule_id = len(self.temporary_rules) + 1
        rule = {
            'id': rule_id,
            'type': rule_type,
            'target': target,
            'expiration': expiration,
            'created': datetime.now().strftime("%Y-%m-%d %H:%M")
        }
        self.temporary_rules[rule_id] = rule
        
        # Add to UI
        item_text = f"⏱️ {rule_type}: {target} (Expires: {expiration})"
        item = QListWidgetItem(item_text)
        item.setData(Qt.ItemDataRole.UserRole, rule)
        self.temp_rules_list.addItem(item)
        
        # Clear inputs
        self.temp_rule_target.clear()
        
        QMessageBox.information(
            self,
            "Temporary Rule Added",
            f"Added temporary whitelist:\n\n"
            f"Type: {rule_type}\n"
            f"Target: {target}\n"
            f"Expires: {expiration}\n\n"
            "This rule will automatically revert when expired."
        )
        
    def extend_temporary_rule(self):
        """Extend expiration of temporary rule"""
        current_item = self.temp_rules_list.currentItem()
        if current_item:
            QMessageBox.information(
                self,
                "Extend Temporary Rule",
                "Would extend the expiration time of this rule by the specified duration."
            )
            
    def revoke_temporary_rule(self):
        """Revoke temporary rule immediately"""
        current_item = self.temp_rules_list.currentItem()
        if current_item:
            rule = current_item.data(Qt.ItemDataRole.UserRole)
            reply = QMessageBox.question(
                self,
                "Revoke Temporary Rule",
                f"Revoke this rule immediately?\n\n"
                f"Type: {rule['type']}\n"
                f"Target: {rule['target']}",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                del self.temporary_rules[rule['id']]
                self.temp_rules_list.takeItem(self.temp_rules_list.row(current_item))
                
    def check_temporary_rules(self):
        """Check and expire temporary rules"""
        current_time = datetime.now()
        expired_rules = []
        
        for rule_id, rule in self.temporary_rules.items():
            if rule['expiration'] != "Session End":
                expiration_time = datetime.strptime(rule['expiration'], "%Y-%m-%d %H:%M")
                if current_time >= expiration_time:
                    expired_rules.append(rule_id)
        
        # Remove expired rules
        for rule_id in expired_rules:
            del self.temporary_rules[rule_id]
            # Remove from UI
            for i in range(self.temp_rules_list.count()):
                item = self.temp_rules_list.item(i)
                if item.data(Qt.ItemDataRole.UserRole)['id'] == rule_id:
                    self.temp_rules_list.takeItem(i)
                    break
                    
    def on_security_layer_changed(self):
        """Handle security layer toggle"""
        self.whitelist_changed.emit(self.get_security_config())
        
    def add_app_to_whitelist(self):
        """Add application to whitelist"""
        app_name = self.app_name_input.text()
        if app_name:
            item = QListWidgetItem(f"✓ {app_name}")
            self.app_whitelist.addItem(item)
            self.app_name_input.clear()
            
    def remove_app_from_whitelist(self):
        """Remove application from whitelist"""
        current_item = self.app_whitelist.currentItem()
        if current_item:
            self.app_whitelist.takeItem(self.app_whitelist.row(current_item))
            
    def configure_app_permissions(self):
        """Configure application permissions"""
        current_item = self.app_whitelist.currentItem()
        if current_item:
            QMessageBox.information(
                self,
                "Configure Permissions",
                f"Would configure detailed permissions for:\n{current_item.text()}"
            )
            
    def add_network_rule(self):
        """Add network whitelist rule"""
        protocol = self.net_protocol.currentText()
        port = self.net_port.text()
        
        if port:
            item = QListWidgetItem(f"🌐 {protocol}: {port}")
            self.network_rules_list.addItem(item)
            self.net_port.clear()
            
    def remove_network_rule(self):
        """Remove network rule"""
        current_item = self.network_rules_list.currentItem()
        if current_item:
            self.network_rules_list.takeItem(self.network_rules_list.row(current_item))
            
    def apply_gaming_preset(self, game):
        """Apply gaming network preset"""
        presets = {
            'minecraft': {'protocol': 'TCP', 'port': '25565'},
            'steam': {'protocol': 'Both', 'port': '27000-28000'},
            'valorant': {'protocol': 'Both', 'port': '5000-5100'}
        }
        
        if game in presets:
            preset = presets[game]
            QMessageBox.information(
                self,
                f"{game.capitalize()} Preset",
                f"Would add network rule:\n\n"
                f"Protocol: {preset['protocol']}\n"
                f"Port: {preset['port']}"
            )
            
    def revert_to_secure_defaults(self):
        """Revert all settings to secure defaults"""
        reply = QMessageBox.warning(
            self,
            "Revert to Secure Defaults",
            "This will:\n"
            "• Remove all temporary whitelist rules\n"
            "• Clear application whitelist\n"
            "• Clear network rules\n"
            "• Enable all security layers\n"
            "• Switch to Strict mode\n\n"
            "Are you sure?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            # Clear all rules
            self.temporary_rules.clear()
            self.temp_rules_list.clear()
            self.app_whitelist.clear()
            self.network_rules_list.clear()
            
            # Enable all security
            self.firewall_enabled.setChecked(True)
            self.apparmor_enabled.setChecked(True)
            self.selinux_enabled.setChecked(False)
            self.firewall_gaming_mode.setChecked(False)
            self.firewall_productivity_mode.setChecked(False)
            
            # Set strict mode
            self.set_security_mode("strict")
            
            QMessageBox.information(
                self,
                "Defaults Restored",
                "All security settings have been restored to secure defaults."
            )
            
    def get_security_config(self):
        """Get current security configuration"""
        return {
            'mode': self.active_mode,
            'firewall': self.firewall_enabled.isChecked() if hasattr(self, 'firewall_enabled') else True,
            'apparmor': self.apparmor_enabled.isChecked() if hasattr(self, 'apparmor_enabled') else True,
            'selinux': self.selinux_enabled.isChecked() if hasattr(self, 'selinux_enabled') else False,
            'gaming_ports': self.firewall_gaming_mode.isChecked() if hasattr(self, 'firewall_gaming_mode') else False,
            'productivity_ports': self.firewall_productivity_mode.isChecked() if hasattr(self, 'firewall_productivity_mode') else False,
            'temporary_rules': list(self.temporary_rules.values())
        }
