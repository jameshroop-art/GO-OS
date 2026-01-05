#!/usr/bin/env python3
"""
Preview Pane Widget - Live preview with animations
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QGroupBox,
                              QTextEdit, QFrame)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QPixmap
from pathlib import Path


class PreviewPaneWidget(QWidget):
    """Widget for live preview of theme and ISO modifications"""
    
    def __init__(self):
        super().__init__()
        self.current_iso = None
        self.current_theme = {}
        self.animation_timer = QTimer()
        self.animation_timer.timeout.connect(self.update_animation)
        self.animation_frame = 0
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the preview pane interface"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Header
        header_label = QLabel("👁️ Live Preview")
        header_font = QFont()
        header_font.setPointSize(14)
        header_font.setBold(True)
        header_label.setFont(header_font)
        layout.addWidget(header_label)
        
        info_label = QLabel("Real-time preview of your customizations")
        info_label.setStyleSheet("color: #888888; font-size: 10pt;")
        layout.addWidget(info_label)
        
        layout.addSpacing(10)
        
        # ISO Info
        iso_group = QGroupBox("ISO Information")
        iso_layout = QVBoxLayout(iso_group)
        
        self.iso_info_label = QLabel("No ISO loaded")
        self.iso_info_label.setWordWrap(True)
        iso_layout.addWidget(self.iso_info_label)
        
        layout.addWidget(iso_group)
        
        # Theme Preview
        theme_group = QGroupBox("Theme Preview")
        theme_layout = QVBoxLayout(theme_group)
        
        # Preview frame
        self.preview_frame = QFrame()
        self.preview_frame.setMinimumHeight(200)
        self.preview_frame.setStyleSheet("""
            QFrame {
                background-color: #2d2d2d;
                border: 2px solid #3d3d3d;
                border-radius: 8px;
            }
        """)
        
        preview_content = QVBoxLayout(self.preview_frame)
        
        self.preview_title = QLabel("Desktop Preview")
        self.preview_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        preview_title_font = QFont()
        preview_title_font.setPointSize(12)
        preview_title_font.setBold(True)
        self.preview_title.setFont(preview_title_font)
        preview_content.addWidget(self.preview_title)
        
        self.preview_description = QLabel("Theme changes will appear here in real-time")
        self.preview_description.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.preview_description.setStyleSheet("color: #888888;")
        preview_content.addWidget(self.preview_description)
        
        preview_content.addStretch()
        
        # Animation indicator
        self.animation_label = QLabel("●")
        self.animation_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.animation_label.setStyleSheet("color: #0078d4; font-size: 24pt;")
        preview_content.addWidget(self.animation_label)
        
        theme_layout.addWidget(self.preview_frame)
        
        layout.addWidget(theme_group)
        
        # Component Summary
        summary_group = QGroupBox("Build Summary")
        summary_layout = QVBoxLayout(summary_group)
        
        self.summary_text = QTextEdit()
        self.summary_text.setReadOnly(True)
        self.summary_text.setMaximumHeight(150)
        self.summary_text.setPlainText("No components selected yet")
        summary_layout.addWidget(self.summary_text)
        
        layout.addWidget(summary_group)
        
        # Self-installation option
        self_install_group = QGroupBox("🔧 Builder Self-Installation")
        self_install_layout = QVBoxLayout(self_install_group)
        
        self_install_info = QLabel(
            "Include this ISO Builder in the custom OS for future use"
        )
        self_install_info.setStyleSheet("font-size: 10pt;")
        self_install_layout.addWidget(self_install_info)
        
        self.include_builder_check = QCheckBox(
            "Install GhostOS ISO Builder in the target OS"
        )
        self.include_builder_check.setChecked(False)
        self.include_builder_check.setToolTip(
            "The ISO Builder will be available in the built OS at /opt/ghostos-builder"
        )
        self_install_layout.addWidget(self.include_builder_check)
        
        install_options = QHBoxLayout()
        
        self.builder_desktop_entry = QCheckBox("Add to Application Menu")
        self.builder_desktop_entry.setChecked(True)
        install_options.addWidget(self.builder_desktop_entry)
        
        self.builder_cli_launcher = QCheckBox("Add CLI Launcher")
        self.builder_cli_launcher.setChecked(True)
        install_options.addWidget(self.builder_cli_launcher)
        
        self_install_layout.addLayout(install_options)
        
        layout.addWidget(self_install_group)
        
        layout.addStretch()
        
        # Start animation
        self.animation_timer.start(50)  # 20 FPS
        
    def set_iso_info(self, iso_path):
        """Update ISO information"""
        self.current_iso = iso_path
        iso_name = Path(iso_path).name
        iso_size = Path(iso_path).stat().st_size / (1024**3)  # GB
        
        info_text = f"""
        <b>Name:</b> {iso_name}<br>
        <b>Size:</b> {iso_size:.2f} GB<br>
        <b>Path:</b> {iso_path}
        """
        
        self.iso_info_label.setText(info_text)
        
    def apply_theme(self, theme_data):
        """Apply theme to preview"""
        self.current_theme = theme_data
        
        mode = theme_data.get('mode', 'default')
        theme_name = theme_data.get('name', 'Unknown')
        
        # Update preview title
        self.preview_title.setText(f"{theme_name} Theme")
        
        # Update description
        if mode == 'gaming':
            self.preview_description.setText("🎮 Gaming Mode Active - Performance Optimized")
            self.preview_frame.setStyleSheet("""
                QFrame {
                    background: qlineargradient(
                        x1:0, y1:0, x2:1, y2:1,
                        stop:0 #1a0033, stop:1 #330066
                    );
                    border: 2px solid #6600cc;
                    border-radius: 8px;
                }
            """)
        elif mode == 'production':
            self.preview_description.setText("💼 Production Mode Active - Professional Theme")
            self.preview_frame.setStyleSheet("""
                QFrame {
                    background: qlineargradient(
                        x1:0, y1:0, x2:1, y2:1,
                        stop:0 #001a33, stop:1 #003366
                    );
                    border: 2px solid #0066cc;
                    border-radius: 8px;
                }
            """)
        else:
            self.preview_description.setText("Theme preview - Default mode")
            self.preview_frame.setStyleSheet("""
                QFrame {
                    background-color: #2d2d2d;
                    border: 2px solid #3d3d3d;
                    border-radius: 8px;
                }
            """)
            
        # Update scaling info
        global_scale = theme_data.get('global_scale', 100)
        terminal_scale = theme_data.get('terminal_scale', 100)
        
        scale_info = f"\n\nGlobal Scale: {global_scale}% | Terminal Scale: {terminal_scale}%"
        self.preview_description.setText(self.preview_description.text() + scale_info)
        
    def update_animation(self):
        """Update preview animation (20 FPS)"""
        self.animation_frame = (self.animation_frame + 1) % 20
        
        # Pulse animation
        opacity = 0.3 + (0.7 * abs(10 - self.animation_frame) / 10)
        
        if self.current_theme.get('mode') == 'gaming':
            color = f"rgba(102, 0, 204, {opacity})"
        elif self.current_theme.get('mode') == 'production':
            color = f"rgba(0, 102, 204, {opacity})"
        else:
            color = f"rgba(0, 120, 212, {opacity})"
            
        self.animation_label.setStyleSheet(f"color: {color}; font-size: 24pt;")
        
    def update_component_summary(self, selected_components):
        """Update the build summary"""
        if not selected_components:
            self.summary_text.setPlainText("No components selected yet")
            return
            
        summary = "Selected Components:\n\n"
        
        for category, components in selected_components.items():
            if components:
                summary += f"{category}:\n"
                for comp in components:
                    summary += f"  • {comp['name']} ({comp['size']}) from {comp['source']}\n"
                summary += "\n"
                
        # Add self-installation info if enabled
        if hasattr(self, 'include_builder_check') and self.include_builder_check.isChecked():
            summary += "\n🔧 GhostOS ISO Builder:\n"
            summary += "  • Included in target OS\n"
            if self.builder_desktop_entry.isChecked():
                summary += "  • Desktop menu entry\n"
            if self.builder_cli_launcher.isChecked():
                summary += "  • CLI launcher (ghostos-builder)\n"
            summary += "  • Installation path: /opt/ghostos-builder\n"
                
        self.summary_text.setPlainText(summary)
    
    def get_self_install_config(self):
        """Get self-installation configuration"""
        return {
            'enabled': self.include_builder_check.isChecked(),
            'desktop_entry': self.builder_desktop_entry.isChecked(),
            'cli_launcher': self.builder_cli_launcher.isChecked(),
        }
