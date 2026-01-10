#!/usr/bin/env python3
"""
Heck-CheckOS Advanced ISO Builder GUI
Comprehensive ISO modification and theme customization tool

LICENSE: MIT (see LICENSE file in repository root)

LEGAL NOTICE:
This is part of Heck-CheckOS, a derivative work based on Debian 12 (Bookworm).
NOT an official Debian release. NOT endorsed by the Debian Project.
See LEGAL_COMPLIANCE.md for full legal information.
"""

import sys
import os
import json
from pathlib import Path

try:
    from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                                  QHBoxLayout, QTabWidget, QLabel, QPushButton,
                                  QFileDialog, QMessageBox, QSplitter)
    from PyQt6.QtCore import Qt, QThread, pyqtSignal
    from PyQt6.QtGui import QIcon, QFont
except ImportError:
    print("Error: PyQt6 not found. Install with: pip install -r requirements.txt")
    sys.exit(1)

# Import custom UI components
from ui.iso_loader import ISOLoaderWidget
from ui.theme_editor import ThemeEditorWidget
from ui.preview_pane import PreviewPaneWidget
from ui.repo_browser import RepoBrowserWidget
from ui.credentials_dialog import CredentialsDialog
from ui.touchscreen_keyboard import TouchscreenKeyboard
from ui.keyboard_designer import KeyboardLayoutDesigner
from ui.driver_manager import DriverManagerWidget

# Import ISO builder backend
from iso_builder_backend import ISOBuilder


class BuildThread(QThread):
    """Background thread for ISO building"""
    progress_update = pyqtSignal(int, str)
    build_complete = pyqtSignal(str)
    build_error = pyqtSignal(str)
    
    def __init__(self, config):
        super().__init__()
        self.config = config
    
    def run(self):
        """Run the build process"""
        try:
            builder = ISOBuilder(self.config)
            
            def progress_callback(percent, message):
                self.progress_update.emit(percent, message)
            
            output_path = builder.build(progress_callback=progress_callback)
            self.build_complete.emit(str(output_path))
            
        except Exception as e:
            self.build_error.emit(str(e))


class HeckCheckOSBuilderGUI(QMainWindow):
    """Main application window for Heck-CheckOS ISO Builder"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Heck-CheckOS Advanced ISO Builder")
        self.setGeometry(100, 100, 1400, 900)
        
        # Initialize variables
        self.current_iso_path = None
        self.current_theme = "default"
        self.gaming_mode_enabled = False
        self.production_mode_enabled = False
        
        # Initialize touchscreen keyboard
        self.touchscreen_keyboard = None
        
        # Setup UI
        self.setup_ui()
        self.setup_menu_bar()
        self.apply_default_style()
        
    def setup_ui(self):
        """Setup the main user interface"""
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        
        # Header
        header = self.create_header()
        main_layout.addWidget(header)
        
        # Main content area with splitter
        content_splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Left panel - ISO Loader and Theme Editor
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(0, 0, 0, 0)
        
        # Tab widget for main controls
        self.main_tabs = QTabWidget()
        
        # ISO Loader tab
        self.iso_loader = ISOLoaderWidget()
        self.iso_loader.iso_loaded.connect(self.on_iso_loaded)
        self.main_tabs.addTab(self.iso_loader, "📀 ISO Loader")
        
        # Theme Editor tab
        self.theme_editor = ThemeEditorWidget()
        self.theme_editor.theme_changed.connect(self.on_theme_changed)
        self.main_tabs.addTab(self.theme_editor, "🎨 Theme Editor")
        
        # Repository Browser tab
        self.repo_browser = RepoBrowserWidget()
        self.repo_browser.integration_selected.connect(self.on_integration_selected)
        self.main_tabs.addTab(self.repo_browser, "📦 Repository Browser")
        
        # Windows Driver Manager tab
        self.driver_manager = DriverManagerWidget()
        self.driver_manager.driver_loaded.connect(self.on_driver_loaded)
        self.main_tabs.addTab(self.driver_manager, "🔧 Driver Manager")
        
        left_layout.addWidget(self.main_tabs)
        
        # Right panel - Preview Pane
        self.preview_pane = PreviewPaneWidget()
        
        # Add panels to splitter
        content_splitter.addWidget(left_panel)
        content_splitter.addWidget(self.preview_pane)
        content_splitter.setStretchFactor(0, 2)  # Left panel gets 2/3
        content_splitter.setStretchFactor(1, 1)  # Right panel gets 1/3
        
        main_layout.addWidget(content_splitter)
        
        # Build action bar
        build_bar = self.create_build_bar()
        main_layout.addWidget(build_bar)
        
        # Status bar
        self.statusBar().showMessage("Ready - No ISO loaded")
        
    def create_header(self):
        """Create the application header"""
        header_widget = QWidget()
        header_layout = QHBoxLayout(header_widget)
        header_layout.setContentsMargins(0, 0, 0, 10)
        
        # Title
        title_label = QLabel("👻 Heck-CheckOS Advanced ISO Builder")
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title_label.setFont(title_font)
        header_layout.addWidget(title_label)
        
        header_layout.addStretch()
        
        # Quick action buttons
        credentials_btn = QPushButton("🔑 Credentials")
        credentials_btn.clicked.connect(self.show_credentials_dialog)
        header_layout.addWidget(credentials_btn)
        
        settings_btn = QPushButton("⚙️ Settings")
        settings_btn.clicked.connect(self.show_settings)
        header_layout.addWidget(settings_btn)
        
        # Touchscreen keyboard toggle
        keyboard_btn = QPushButton("⌨ Keyboard")
        keyboard_btn.setToolTip("Show/Hide Touchscreen Keyboard")
        keyboard_btn.clicked.connect(self.toggle_touchscreen_keyboard)
        header_layout.addWidget(keyboard_btn)
        
        return header_widget
    
    def create_build_bar(self):
        """Create the build action bar"""
        build_widget = QFrame()
        build_widget.setStyleSheet("""
            QFrame {
                background-color: #252525;
                border-top: 1px solid #3d3d3d;
                padding: 10px;
            }
        """)
        build_layout = QHBoxLayout(build_widget)
        
        # Build info
        info_label = QLabel("Ready to build custom ISO")
        build_layout.addWidget(info_label)
        
        build_layout.addStretch()
        
        # Action buttons
        validate_btn = QPushButton("🔍 Validate Configuration")
        validate_btn.clicked.connect(self.validate_build_config)
        build_layout.addWidget(validate_btn)
        
        export_config_btn = QPushButton("💾 Export Config")
        export_config_btn.clicked.connect(self.save_configuration)
        build_layout.addWidget(export_config_btn)
        
        build_btn = QPushButton("🚀 Build ISO")
        build_btn.setStyleSheet("""
            QPushButton {
                background-color: #0078d4;
                color: white;
                padding: 10px 30px;
                font-size: 12pt;
                font-weight: bold;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #1084d8;
            }
            QPushButton:pressed {
                background-color: #006cbd;
            }
        """)
        build_btn.clicked.connect(self.start_iso_build)
        build_layout.addWidget(build_btn)
        
        return build_widget
        
    def validate_build_config(self):
        """Validate the build configuration"""
        issues = []
        
        # Check if ISO loaded
        if not self.current_iso_path:
            issues.append("• No ISO source loaded")
        
        # Check if components selected
        selected = self.iso_loader.selected_components
        if not selected or all(not comps for comps in selected.values()):
            issues.append("• No components selected")
        
        # Check UI targets
        ui_targets = self.iso_loader.get_selected_ui_targets()
        if not ui_targets:
            issues.append("• No UI compatibility targets selected")
        
        # Display results
        if issues:
            QMessageBox.warning(
                self,
                "Configuration Issues",
                "The following issues were found:\n\n" + "\n".join(issues) + 
                "\n\nPlease fix these before building."
            )
        else:
            QMessageBox.information(
                self,
                "Configuration Valid",
                "✓ Configuration is valid!\n\n"
                "Ready to build ISO with:\n"
                f"• {len(self.iso_loader.loaded_isos)} ISO source(s)\n"
                f"• {sum(len(c) for c in selected.values())} component(s)\n"
                f"• {len(ui_targets)} UI target(s)\n"
                f"• Theme: {self.current_theme.get('name', 'Default')}"
            )
    
    def start_iso_build(self):
        """Start the ISO build process"""
        # Validate first
        if not self.current_iso_path:
            QMessageBox.warning(
                self,
                "Cannot Build",
                "Please load at least one ISO source first."
            )
            return
        
        # Check if running as root (Unix/Linux only - ISO building is Linux-specific)
        try:
            if os.geteuid() != 0:
                reply = QMessageBox.warning(
                    self,
                    "Root Privileges Required",
                    "ISO building requires root privileges for operations like:\n"
                    "• Creating chroot environments\n"
                    "• Mounting ISO files\n"
                    "• Modifying system files\n\n"
                    "To build ISOs, please run with elevated privileges:\n\n"
                    "From terminal:\n"
                    "  sudo python3 main.py\n\n"
                    "Or use the system launcher:\n"
                    "  pkexec /opt/heckcheckos-builder/main.py\n\n"
                    "Note: The GUI itself runs normally as a regular user.\n"
                    "Only ISO building requires elevation.",
                    QMessageBox.StandardButton.Ok
                )
                return
        except AttributeError:
            # os.geteuid() doesn't exist on Windows
            QMessageBox.warning(
                self,
                "Platform Not Supported",
                "ISO building requires a Linux system with root privileges.\n\n"
                "Windows is not supported for ISO building."
            )
            return
        
        # Get all configuration
        build_config = {
            'version': 'custom',
            'iso_sources': [iso['path'] for iso in self.iso_loader.loaded_isos],
            'selected_components': self.iso_loader.selected_components,
            'custom_files': self.iso_loader.get_custom_files(),
            'ui_targets': self.iso_loader.get_selected_ui_targets(),
            'theme': self.current_theme,
            'self_install': self.preview_pane.get_self_install_config(),
            'integrations': [],  # Would be populated from repo browser
            'packages': [],  # Would be populated from selections
        }
        
        # Show build dialog
        from PyQt6.QtWidgets import QDialog, QVBoxLayout, QTextEdit, QProgressBar
        
        build_dialog = QDialog(self)
        build_dialog.setWindowTitle("Building Heck-CheckOS ISO")
        build_dialog.setMinimumWidth(800)
        build_dialog.setMinimumHeight(600)
        build_dialog.setModal(True)
        
        dialog_layout = QVBoxLayout(build_dialog)
        
        # Build log
        build_log = QTextEdit()
        build_log.setReadOnly(True)
        build_log.setFont(QFont("Monospace", 10))
        dialog_layout.addWidget(build_log)
        
        # Progress bar
        progress = QProgressBar()
        progress.setMinimum(0)
        progress.setMaximum(100)
        dialog_layout.addWidget(progress)
        
        # Status label
        status_label = QLabel("Preparing build...")
        dialog_layout.addWidget(status_label)
        
        # Start build info
        build_log.append("╔════════════════════════════════════════════════════════╗")
        build_log.append("║  Heck-CheckOS ISO Builder - Pre-Installation Build    ║")
        build_log.append("╚════════════════════════════════════════════════════════╝\n")
        build_log.append(f"Base: Debian 12 (Bookworm)")
        build_log.append(f"ISO Sources: {len(build_config['iso_sources'])}")
        build_log.append(f"Components: {sum(len(c) for c in build_config['selected_components'].values())}")
        build_log.append(f"Custom Files: {len(build_config['custom_files'])}")
        build_log.append(f"UI Targets: {', '.join(build_config['ui_targets'])}")
        build_log.append(f"Theme Mode: {build_config['theme'].get('mode', 'default')}")
        
        if build_config['self_install']['enabled']:
            build_log.append("\n🔧 Self-Installation: ENABLED")
            build_log.append("   Builder will be included at /opt/heckcheckos-builder")
            if build_config['self_install']['desktop_entry']:
                build_log.append("   + Desktop menu entry")
            if build_config['self_install']['cli_launcher']:
                build_log.append("   + CLI launcher (heckcheckos-builder)")
            build_log.append("   + Touchscreen keyboard (heckcheckos-keyboard)")
            build_log.append("   + Keyboard calibration tools")
            build_log.append("   + Custom layout designer")
        
        build_log.append("\n" + "="*60)
        build_log.append("\n🚀 Starting actual ISO build process...")
        build_log.append("All changes will be pre-applied to the ISO!\n")
        
        # Create build thread
        self.build_thread = BuildThread(build_config)
        
        # Connect signals
        def on_progress(percent, message):
            progress.setValue(percent)
            status_label.setText(message)
            build_log.append(f"[{percent}%] {message}")
            QApplication.processEvents()
        
        def on_complete(output_path):
            progress.setValue(100)
            status_label.setText("Build complete!")
            build_log.append("\n" + "="*60)
            build_log.append("✅ BUILD COMPLETE!")
            build_log.append("="*60)
            build_log.append(f"\nOutput: {output_path}")
            build_log.append("\nThe ISO has been created with all your customizations")
            build_log.append("pre-applied. You can now:")
            build_log.append("  1. Write it to a USB drive")
            build_log.append("  2. Boot from it (all settings already configured)")
            build_log.append("  3. Install to disk (with your custom configuration)")
            
            # Add close button
            close_btn = QPushButton("Close")
            close_btn.clicked.connect(build_dialog.accept)
            dialog_layout.addWidget(close_btn)
        
        def on_error(error_msg):
            progress.setValue(0)
            status_label.setText("Build failed!")
            build_log.append("\n" + "="*60)
            build_log.append("❌ BUILD FAILED!")
            build_log.append("="*60)
            build_log.append(f"\nError: {error_msg}")
            build_log.append("\nPlease check the error message and try again.")
            build_log.append("Make sure you have all required tools installed:")
            build_log.append("  sudo apt-get install squashfs-tools xorriso \\")
            build_log.append("    grub-pc-bin grub-efi-amd64-bin syslinux \\")
            build_log.append("    syslinux-utils debootstrap isolinux")
            
            # Add close button
            close_btn = QPushButton("Close")
            close_btn.clicked.connect(build_dialog.accept)
            dialog_layout.addWidget(close_btn)
        
        self.build_thread.progress_update.connect(on_progress)
        self.build_thread.build_complete.connect(on_complete)
        self.build_thread.build_error.connect(on_error)
        
        # Start building
        self.build_thread.start()
        
        build_dialog.exec()

        

    def setup_menu_bar(self):
        """Setup the menu bar"""
        menu_bar = self.menuBar()
        
        # File menu
        file_menu = menu_bar.addMenu("&File")
        
        load_iso_action = file_menu.addAction("Load ISO...")
        load_iso_action.triggered.connect(self.load_iso_dialog)
        load_iso_action.setShortcut("Ctrl+O")
        
        file_menu.addSeparator()
        
        save_config_action = file_menu.addAction("Save Configuration...")
        save_config_action.triggered.connect(self.save_configuration)
        save_config_action.setShortcut("Ctrl+S")
        
        load_config_action = file_menu.addAction("Load Configuration...")
        load_config_action.triggered.connect(self.load_configuration)
        
        file_menu.addSeparator()
        
        exit_action = file_menu.addAction("Exit")
        exit_action.triggered.connect(self.close)
        exit_action.setShortcut("Ctrl+Q")
        
        # Edit menu
        edit_menu = menu_bar.addMenu("&Edit")
        
        preferences_action = edit_menu.addAction("Preferences...")
        preferences_action.triggered.connect(self.show_settings)
        
        # View menu
        view_menu = menu_bar.addMenu("&View")
        
        gaming_mode_action = view_menu.addAction("🎮 Gaming Mode")
        gaming_mode_action.setCheckable(True)
        gaming_mode_action.triggered.connect(self.toggle_gaming_mode)
        
        production_mode_action = view_menu.addAction("💼 Production Mode")
        production_mode_action.setCheckable(True)
        production_mode_action.triggered.connect(self.toggle_production_mode)
        
        view_menu.addSeparator()
        
        fullscreen_action = view_menu.addAction("Fullscreen")
        fullscreen_action.setCheckable(True)
        fullscreen_action.triggered.connect(self.toggle_fullscreen)
        fullscreen_action.setShortcut("F11")
        
        # Help menu
        help_menu = menu_bar.addMenu("&Help")
        
        about_action = help_menu.addAction("About")
        about_action.triggered.connect(self.show_about)
        
        docs_action = help_menu.addAction("Documentation")
        docs_action.triggered.connect(self.show_documentation)
        
    def toggle_touchscreen_keyboard(self):
        """Toggle touchscreen keyboard visibility"""
        if self.touchscreen_keyboard is None:
            # Create keyboard on first use
            self.touchscreen_keyboard = TouchscreenKeyboard()
            self.touchscreen_keyboard.key_pressed.connect(self.on_keyboard_key_pressed)
            self.touchscreen_keyboard.keyboard_hidden.connect(self.on_keyboard_hidden)
            
        if self.touchscreen_keyboard.isVisible():
            self.touchscreen_keyboard.hide_keyboard()
        else:
            self.touchscreen_keyboard.show_keyboard()
            
    def on_keyboard_key_pressed(self, key: str):
        """Handle keyboard key press"""
        # Send key to focused widget
        focused_widget = QApplication.focusWidget()
        if focused_widget and hasattr(focused_widget, 'insert'):
            # For text input widgets
            if key == '\b':  # Backspace
                focused_widget.backspace()
            elif key == '\n':  # Enter
                focused_widget.insert('\n')
            else:
                focused_widget.insert(key)
        elif focused_widget and hasattr(focused_widget, 'setText'):
            # For line edit widgets
            current_text = focused_widget.text()
            if key == '\b':  # Backspace
                focused_widget.setText(current_text[:-1])
            else:
                focused_widget.setText(current_text + key)
                
    def on_keyboard_hidden(self):
        """Handle keyboard hidden event"""
        self.statusBar().showMessage("Touchscreen keyboard hidden")
        
    def apply_default_style(self):
        """Apply default application styling"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1e1e1e;
            }
            QLabel {
                color: #e0e0e0;
            }
            QPushButton {
                background-color: #2d2d2d;
                color: #e0e0e0;
                border: 1px solid #3d3d3d;
                border-radius: 4px;
                padding: 6px 12px;
                font-size: 11pt;
            }
            QPushButton:hover {
                background-color: #3d3d3d;
                border: 1px solid #4d4d4d;
            }
            QPushButton:pressed {
                background-color: #252525;
            }
            QTabWidget::pane {
                border: 1px solid #3d3d3d;
                background-color: #1e1e1e;
            }
            QTabBar::tab {
                background-color: #2d2d2d;
                color: #e0e0e0;
                border: 1px solid #3d3d3d;
                padding: 8px 16px;
                font-size: 11pt;
            }
            QTabBar::tab:selected {
                background-color: #1e1e1e;
                border-bottom: 2px solid #0078d4;
            }
            QTabBar::tab:hover {
                background-color: #3d3d3d;
            }
            QStatusBar {
                background-color: #252525;
                color: #e0e0e0;
            }
            QMenuBar {
                background-color: #2d2d2d;
                color: #e0e0e0;
            }
            QMenuBar::item:selected {
                background-color: #3d3d3d;
            }
            QMenu {
                background-color: #2d2d2d;
                color: #e0e0e0;
                border: 1px solid #3d3d3d;
            }
            QMenu::item:selected {
                background-color: #0078d4;
            }
        """)
        
    def load_iso_dialog(self):
        """Open file dialog to load an ISO"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Debian 12 ISO",
            str(Path.home()),
            "ISO Files (*.iso);;All Files (*)"
        )
        
        if file_path:
            self.iso_loader.load_iso(file_path)
            
    def on_iso_loaded(self, iso_path):
        """Handle ISO loaded event"""
        self.current_iso_path = iso_path
        self.statusBar().showMessage(f"ISO Loaded: {Path(iso_path).name}")
        self.preview_pane.set_iso_info(iso_path)
        
    def on_theme_changed(self, theme_data):
        """Handle theme changed event"""
        self.current_theme = theme_data.get('name', 'custom')
        self.statusBar().showMessage(f"Theme changed: {self.current_theme}")
        self.preview_pane.apply_theme(theme_data)
        
    def on_integration_selected(self, integration_data):
        """Handle integration selected event"""
        repo_name = integration_data.get('name', 'Unknown')
        self.statusBar().showMessage(f"Integration selected: {repo_name}")
    
    def on_driver_loaded(self, driver_info):
        """Handle driver loaded event"""
        self.statusBar().showMessage(f"Driver loaded: {driver_info}")
        
    def show_credentials_dialog(self):
        """Show credentials management dialog"""
        dialog = CredentialsDialog(self)
        dialog.exec()
        
    def show_settings(self):
        """Show settings dialog"""
        QMessageBox.information(
            self,
            "Settings",
            "Settings dialog - Coming soon!\n\nThis will allow you to configure:\n"
            "- Default theme\n- Text scaling\n- Preview quality\n- Build options"
        )
        
    def toggle_gaming_mode(self, checked):
        """Toggle gaming mode"""
        self.gaming_mode_enabled = checked
        if checked:
            self.production_mode_enabled = False
            self.theme_editor.enable_gaming_mode()
            self.statusBar().showMessage("Gaming Mode: ENABLED")
        else:
            self.theme_editor.disable_gaming_mode()
            self.statusBar().showMessage("Gaming Mode: DISABLED")
            
    def toggle_production_mode(self, checked):
        """Toggle production mode"""
        self.production_mode_enabled = checked
        if checked:
            self.gaming_mode_enabled = False
            self.theme_editor.enable_production_mode()
            self.statusBar().showMessage("Production Mode: ENABLED")
        else:
            self.theme_editor.disable_production_mode()
            self.statusBar().showMessage("Production Mode: DISABLED")
            
    def toggle_fullscreen(self, checked):
        """Toggle fullscreen mode"""
        if checked:
            self.showFullScreen()
        else:
            self.showNormal()
            
    def save_configuration(self):
        """Save current configuration"""
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Configuration",
            str(Path.home() / "heckcheckos-config.json"),
            "JSON Files (*.json);;All Files (*)"
        )
        
        if file_path:
            try:
                # Gather configuration from all widgets
                config = {
                    'version': '1.0.0',
                    'theme': self.theme_editor.get_current_theme() if hasattr(self.theme_editor, 'get_current_theme') else {},
                    'iso_path': self.iso_loader.get_iso_path() if hasattr(self.iso_loader, 'get_iso_path') else None,
                    'self_install': self.preview_pane.get_self_install_config() if hasattr(self.preview_pane, 'get_self_install_config') else {},
                    'current_theme_name': self.current_theme if isinstance(self.current_theme, str) else 'default'
                }
                
                # Write configuration to file
                with open(file_path, 'w') as f:
                    json.dump(config, f, indent=2)
                
                QMessageBox.information(self, "Saved", f"Configuration saved to:\n{file_path}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save configuration:\n{str(e)}")
            
    def load_configuration(self):
        """Load configuration from file"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Load Configuration",
            str(Path.home()),
            "JSON Files (*.json);;All Files (*)"
        )
        
        if file_path:
            try:
                # Read configuration from file
                with open(file_path, 'r') as f:
                    config = json.load(f)
                
                # Apply configuration to widgets
                if 'theme' in config and hasattr(self.theme_editor, 'load_theme'):
                    self.theme_editor.load_theme(config['theme'])
                
                if 'current_theme_name' in config:
                    self.current_theme = config['current_theme_name']
                
                if 'self_install' in config and hasattr(self.preview_pane, 'load_self_install_config'):
                    self.preview_pane.load_self_install_config(config['self_install'])
                
                QMessageBox.information(self, "Loaded", f"Configuration loaded from:\n{file_path}")
                self.statusBar().showMessage(f"Configuration loaded: {Path(file_path).name}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to load configuration:\n{str(e)}")
            
    def show_about(self):
        """Show about dialog"""
        about_text = """
        <h2>Heck-CheckOS Advanced ISO Builder</h2>
        <p><b>Version:</b> 1.0.0</p>
        <p><b>Based on:</b> Debian 12 (Bookworm)</p>
        <br>
        <p>A comprehensive ISO modification and theme customization tool for Heck-CheckOS.</p>
        <br>
        <p><b>Features:</b></p>
        <ul>
            <li>Interactive ISO loading and modification</li>
            <li>Gaming and Production theme modes</li>
            <li>Repository integration browser</li>
            <li>Live preview with animations</li>
            <li>Text scaling and customization</li>
        </ul>
        <br>
        <p><b>Project:</b> <a href="https://github.com/jameshroop-art/GO-OS">github.com/jameshroop-art/GO-OS</a></p>
        """
        
        QMessageBox.about(self, "About Heck-CheckOS Builder", about_text)
        
    def show_documentation(self):
        """Show documentation"""
        QMessageBox.information(
            self,
            "Documentation",
            "Documentation is available in the Go-OS directory:\n\n"
            "- ISO_DOWNLOAD_GUIDE.md\n"
            "- GHOSTOS_QUICK_REFERENCE.md\n"
            "- FAQ.md\n"
            "- ARCHITECTURE.md"
        )


def main():
    """Main application entry point"""
    app = QApplication(sys.argv)
    app.setApplicationName("Heck-CheckOS ISO Builder")
    app.setOrganizationName("Heck-CheckOS")
    
    # Create and show main window
    window = HeckCheckOSBuilderGUI()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
