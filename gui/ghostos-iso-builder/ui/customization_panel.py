#!/usr/bin/env python3
"""
Customization Panel Widget - Extensive GUI customization with drag-and-drop
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                              QPushButton, QGroupBox, QSlider, QSpinBox,
                              QComboBox, QCheckBox, QListWidget, QListWidgetItem,
                              QColorDialog, QFontDialog, QMessageBox, QTabWidget,
                              QTextEdit, QLineEdit, QGridLayout)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QColor, QKeySequence


class CustomizationPanelWidget(QWidget):
    """Widget for extensive GUI customization"""
    
    customization_changed = pyqtSignal(dict)
    
    def __init__(self):
        super().__init__()
        self.custom_colors = {}
        self.custom_shortcuts = {}
        self.layout_config = {}
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the customization interface"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Header
        header_label = QLabel("🎨 Advanced GUI Customization")
        header_font = QFont()
        header_font.setPointSize(14)
        header_font.setBold(True)
        header_label.setFont(header_font)
        layout.addWidget(header_label)
        
        info_label = QLabel("Customize every aspect of the interface")
        info_label.setStyleSheet("color: #888888; font-size: 10pt;")
        layout.addWidget(info_label)
        
        layout.addSpacing(10)
        
        # Tab widget
        tabs = QTabWidget()
        
        # Colors tab
        colors_tab = self.create_colors_tab()
        tabs.addTab(colors_tab, "Colors")
        
        # Layout tab
        layout_tab = self.create_layout_tab()
        tabs.addTab(layout_tab, "Layout")
        
        # Fonts & Icons tab
        fonts_tab = self.create_fonts_icons_tab()
        tabs.addTab(fonts_tab, "Fonts & Icons")
        
        # Keyboard shortcuts tab
        shortcuts_tab = self.create_shortcuts_tab()
        tabs.addTab(shortcuts_tab, "Keyboard Shortcuts")
        
        # Advanced tab
        advanced_tab = self.create_advanced_tab()
        tabs.addTab(advanced_tab, "Advanced")
        
        layout.addWidget(tabs)
        
        # Preview and apply
        actions_layout = QHBoxLayout()
        actions_layout.addStretch()
        
        preview_btn = QPushButton("👁️ Preview Changes")
        preview_btn.clicked.connect(self.preview_customization)
        actions_layout.addWidget(preview_btn)
        
        apply_btn = QPushButton("✓ Apply Customization")
        apply_btn.setStyleSheet("""
            QPushButton {
                background-color: #0078d4;
                color: white;
                padding: 10px 20px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1084d8;
            }
        """)
        apply_btn.clicked.connect(self.apply_customization)
        actions_layout.addWidget(apply_btn)
        
        layout.addLayout(actions_layout)
        
    def create_colors_tab(self):
        """Create colors customization tab"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Color scheme selector
        scheme_group = QGroupBox("Color Scheme")
        scheme_layout = QVBoxLayout(scheme_group)
        
        self.color_scheme = QComboBox()
        self.color_scheme.addItems([
            "Dark (Default)",
            "Light",
            "Dracula",
            "Nord",
            "Solarized Dark",
            "Solarized Light",
            "Gruvbox",
            "Monokai",
            "Custom"
        ])
        self.color_scheme.currentTextChanged.connect(self.on_color_scheme_changed)
        scheme_layout.addWidget(self.color_scheme)
        
        layout.addWidget(scheme_group)
        
        # Custom colors
        custom_group = QGroupBox("Custom Colors")
        custom_layout = QGridLayout(custom_group)
        
        color_elements = [
            ("Primary Background", "bg_primary"),
            ("Secondary Background", "bg_secondary"),
            ("Primary Text", "text_primary"),
            ("Secondary Text", "text_secondary"),
            ("Accent Color", "accent"),
            ("Success Color", "success"),
            ("Warning Color", "warning"),
            ("Error Color", "error"),
            ("Border Color", "border"),
            ("Hover Color", "hover"),
            ("Selection Color", "selection"),
            ("Link Color", "link")
        ]
        
        self.color_buttons = {}
        for i, (label, key) in enumerate(color_elements):
            row = i // 2
            col = (i % 2) * 2
            
            custom_layout.addWidget(QLabel(label + ":"), row, col)
            btn = QPushButton("Choose Color")
            btn.clicked.connect(lambda checked, k=key: self.choose_custom_color(k))
            self.color_buttons[key] = btn
            custom_layout.addWidget(btn, row, col + 1)
            
        layout.addWidget(custom_group)
        
        # RGB color picker for gaming
        rgb_group = QGroupBox("🎮 RGB Gaming Colors")
        rgb_layout = QVBoxLayout(rgb_group)
        
        rgb_info = QLabel("Set RGB colors for gaming mode elements:")
        rgb_layout.addWidget(rgb_info)
        
        self.enable_rgb = QCheckBox("Enable RGB color cycling")
        rgb_layout.addWidget(self.enable_rgb)
        
        rgb_speed = QHBoxLayout()
        rgb_speed.addWidget(QLabel("Cycle Speed:"))
        self.rgb_speed_slider = QSlider(Qt.Orientation.Horizontal)
        self.rgb_speed_slider.setRange(1, 10)
        self.rgb_speed_slider.setValue(5)
        rgb_speed.addWidget(self.rgb_speed_slider)
        rgb_layout.addLayout(rgb_speed)
        
        layout.addWidget(rgb_group)
        
        layout.addStretch()
        
        return tab
        
    def create_layout_tab(self):
        """Create layout customization tab"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Layout presets
        preset_group = QGroupBox("Layout Presets")
        preset_layout = QVBoxLayout(preset_group)
        
        self.layout_preset = QComboBox()
        self.layout_preset.addItems([
            "Standard (Default)",
            "Compact",
            "Wide",
            "Vertical Split",
            "Horizontal Split",
            "Minimalist",
            "HUD Style (Gaming)",
            "Dashboard",
            "Custom"
        ])
        preset_layout.addWidget(self.layout_preset)
        
        layout.addWidget(preset_group)
        
        # Widget positioning
        position_group = QGroupBox("Widget Positioning")
        position_layout = QVBoxLayout(position_group)
        
        position_info = QLabel("Drag and drop to rearrange interface elements:")
        position_layout.addWidget(position_info)
        
        self.widget_list = QListWidget()
        self.widget_list.setDragDropMode(QListWidget.DragDropMode.InternalMove)
        
        widgets = [
            "ISO Loader",
            "Component Selector",
            "Theme Editor",
            "Preview Pane",
            "Security Manager",
            "Wine Manager",
            "Repository Browser",
            "AI Assistant"
        ]
        
        for widget in widgets:
            item = QListWidgetItem(f"📦 {widget}")
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsEditable)
            self.widget_list.addItem(item)
            
        position_layout.addWidget(self.widget_list)
        
        position_buttons = QHBoxLayout()
        
        reset_layout_btn = QPushButton("↺ Reset Layout")
        reset_layout_btn.clicked.connect(self.reset_layout)
        position_buttons.addWidget(reset_layout_btn)
        
        position_layout.addLayout(position_buttons)
        layout.addWidget(position_group)
        
        # Panel configuration
        panel_group = QGroupBox("Panel Configuration")
        panel_layout = QVBoxLayout(panel_group)
        
        self.show_toolbar = QCheckBox("Show toolbar")
        self.show_toolbar.setChecked(True)
        panel_layout.addWidget(self.show_toolbar)
        
        self.show_sidebar = QCheckBox("Show sidebar")
        self.show_sidebar.setChecked(True)
        panel_layout.addWidget(self.show_sidebar)
        
        self.show_statusbar = QCheckBox("Show status bar")
        self.show_statusbar.setChecked(True)
        panel_layout.addWidget(self.show_statusbar)
        
        toolbar_pos = QHBoxLayout()
        toolbar_pos.addWidget(QLabel("Toolbar Position:"))
        self.toolbar_position = QComboBox()
        self.toolbar_position.addItems(["Top", "Bottom", "Left", "Right"])
        toolbar_pos.addWidget(self.toolbar_position)
        panel_layout.addLayout(toolbar_pos)
        
        layout.addWidget(panel_group)
        
        layout.addStretch()
        
        return tab
        
    def create_fonts_icons_tab(self):
        """Create fonts and icons customization tab"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Font settings
        font_group = QGroupBox("Font Settings")
        font_layout = QVBoxLayout(font_group)
        
        # UI Font
        ui_font_layout = QHBoxLayout()
        ui_font_layout.addWidget(QLabel("UI Font:"))
        self.ui_font_btn = QPushButton("Choose Font")
        self.ui_font_btn.clicked.connect(lambda: self.choose_font("ui"))
        ui_font_layout.addWidget(self.ui_font_btn)
        self.ui_font_label = QLabel("Default")
        ui_font_layout.addWidget(self.ui_font_label)
        font_layout.addLayout(ui_font_layout)
        
        # Code Font
        code_font_layout = QHBoxLayout()
        code_font_layout.addWidget(QLabel("Code Font:"))
        self.code_font_btn = QPushButton("Choose Font")
        self.code_font_btn.clicked.connect(lambda: self.choose_font("code"))
        code_font_layout.addWidget(self.code_font_btn)
        self.code_font_label = QLabel("Monospace")
        code_font_layout.addWidget(self.code_font_label)
        font_layout.addLayout(code_font_layout)
        
        # Font size
        size_layout = QHBoxLayout()
        size_layout.addWidget(QLabel("Base Font Size:"))
        self.font_size = QSpinBox()
        self.font_size.setRange(8, 24)
        self.font_size.setValue(11)
        size_layout.addWidget(self.font_size)
        size_layout.addWidget(QLabel("pt"))
        size_layout.addStretch()
        font_layout.addLayout(size_layout)
        
        layout.addWidget(font_group)
        
        # Icon theme
        icon_group = QGroupBox("Icon Theme")
        icon_layout = QVBoxLayout(icon_group)
        
        self.icon_theme = QComboBox()
        self.icon_theme.addItems([
            "Papirus (Default)",
            "Numix Circle",
            "Breeze",
            "Adwaita",
            "Faenza",
            "Moka",
            "Flat Remix"
        ])
        icon_layout.addWidget(self.icon_theme)
        
        icon_size_layout = QHBoxLayout()
        icon_size_layout.addWidget(QLabel("Icon Size:"))
        self.icon_size = QComboBox()
        self.icon_size.addItems(["Small (16px)", "Medium (24px)", "Large (32px)", "Extra Large (48px)"])
        self.icon_size.setCurrentIndex(1)
        icon_size_layout.addWidget(self.icon_size)
        icon_layout.addLayout(icon_size_layout)
        
        layout.addWidget(icon_group)
        
        # Cursor theme
        cursor_group = QGroupBox("Cursor Theme")
        cursor_layout = QVBoxLayout(cursor_group)
        
        self.cursor_theme = QComboBox()
        self.cursor_theme.addItems([
            "Default",
            "Breeze",
            "DMZ",
            "Redglass",
            "Oxygen"
        ])
        cursor_layout.addWidget(self.cursor_theme)
        
        layout.addWidget(cursor_group)
        
        layout.addStretch()
        
        return tab
        
    def create_shortcuts_tab(self):
        """Create keyboard shortcuts customization tab"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        info = QLabel("Customize keyboard shortcuts for quick access:")
        layout.addWidget(info)
        
        # Shortcuts list
        shortcuts_group = QGroupBox("Keyboard Shortcuts")
        shortcuts_layout = QVBoxLayout(shortcuts_group)
        
        self.shortcuts_list = QListWidget()
        self.shortcuts_list.setMaximumHeight(300)
        
        default_shortcuts = [
            ("Load ISO", "Ctrl+O"),
            ("Save Configuration", "Ctrl+S"),
            ("Build ISO", "Ctrl+B"),
            ("Toggle Gaming Mode", "Ctrl+G"),
            ("Toggle Production Mode", "Ctrl+P"),
            ("Open Wine Manager", "Ctrl+W"),
            ("Security Settings", "Ctrl+Shift+S"),
            ("AI Assistant", "Ctrl+A"),
            ("Quick Actions", "Ctrl+Q"),
            ("Toggle Fullscreen", "F11"),
            ("Help", "F1"),
            ("Exit", "Ctrl+Q")
        ]
        
        for action, shortcut in default_shortcuts:
            item = QListWidgetItem(f"{action}: {shortcut}")
            item.setData(Qt.ItemDataRole.UserRole, {'action': action, 'shortcut': shortcut})
            self.shortcuts_list.addItem(item)
            
        shortcuts_layout.addWidget(self.shortcuts_list)
        
        shortcut_buttons = QHBoxLayout()
        
        edit_shortcut_btn = QPushButton("✏️ Edit Shortcut")
        edit_shortcut_btn.clicked.connect(self.edit_shortcut)
        shortcut_buttons.addWidget(edit_shortcut_btn)
        
        reset_shortcuts_btn = QPushButton("↺ Reset to Defaults")
        reset_shortcuts_btn.clicked.connect(self.reset_shortcuts)
        shortcut_buttons.addWidget(reset_shortcuts_btn)
        
        shortcuts_layout.addLayout(shortcut_buttons)
        layout.addWidget(shortcuts_group)
        
        layout.addStretch()
        
        return tab
        
    def create_advanced_tab(self):
        """Create advanced customization tab"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Live CSS editor
        css_group = QGroupBox("🎨 Live CSS Editor")
        css_layout = QVBoxLayout(css_group)
        
        css_info = QLabel("Advanced: Edit raw CSS for complete control:")
        css_layout.addWidget(css_info)
        
        self.css_editor = QTextEdit()
        self.css_editor.setPlaceholderText(
            "/* Enter custom CSS here */\n"
            "QWidget {\n"
            "    background-color: #1e1e1e;\n"
            "    color: #e0e0e0;\n"
            "}"
        )
        css_layout.addWidget(self.css_editor)
        
        css_buttons = QHBoxLayout()
        
        load_css_btn = QPushButton("📂 Load CSS File")
        load_css_btn.clicked.connect(self.load_css_file)
        css_buttons.addWidget(load_css_btn)
        
        save_css_btn = QPushButton("💾 Save CSS File")
        save_css_btn.clicked.connect(self.save_css_file)
        css_buttons.addWidget(save_css_btn)
        
        apply_css_btn = QPushButton("✓ Apply CSS")
        apply_css_btn.clicked.connect(self.apply_custom_css)
        css_buttons.addWidget(apply_css_btn)
        
        css_layout.addLayout(css_buttons)
        layout.addWidget(css_group)
        
        # Animation settings
        animation_group = QGroupBox("Animation Settings")
        animation_layout = QVBoxLayout(animation_group)
        
        self.enable_animations = QCheckBox("Enable UI animations")
        self.enable_animations.setChecked(True)
        animation_layout.addWidget(self.enable_animations)
        
        anim_speed = QHBoxLayout()
        anim_speed.addWidget(QLabel("Animation Speed:"))
        self.anim_speed_slider = QSlider(Qt.Orientation.Horizontal)
        self.anim_speed_slider.setRange(1, 10)
        self.anim_speed_slider.setValue(5)
        anim_speed.addWidget(self.anim_speed_slider)
        self.anim_speed_label = QLabel("Normal")
        anim_speed.addWidget(self.anim_speed_label)
        animation_layout.addLayout(anim_speed)
        
        layout.addWidget(animation_group)
        
        # Performance settings
        performance_group = QGroupBox("Performance")
        performance_layout = QVBoxLayout(performance_group)
        
        self.enable_transparency = QCheckBox("Enable window transparency effects")
        performance_layout.addWidget(self.enable_transparency)
        
        self.enable_shadows = QCheckBox("Enable drop shadows")
        self.enable_shadows.setChecked(True)
        performance_layout.addWidget(self.enable_shadows)
        
        self.enable_blur = QCheckBox("Enable background blur")
        performance_layout.addWidget(self.enable_blur)
        
        layout.addWidget(performance_group)
        
        layout.addStretch()
        
        return tab
        
    def on_color_scheme_changed(self, scheme):
        """Handle color scheme change"""
        if scheme != "Custom":
            QMessageBox.information(
                self,
                "Color Scheme",
                f"Would apply {scheme} color scheme to the interface."
            )
            
    def choose_custom_color(self, color_key):
        """Choose custom color"""
        color = QColorDialog.getColor()
        if color.isValid():
            self.custom_colors[color_key] = color.name()
            self.color_buttons[color_key].setStyleSheet(
                f"background-color: {color.name()}; color: white;"
            )
            
    def choose_font(self, font_type):
        """Choose font"""
        font, ok = QFontDialog.getFont()
        if ok:
            if font_type == "ui":
                self.ui_font_label.setText(f"{font.family()} {font.pointSize()}pt")
            elif font_type == "code":
                self.code_font_label.setText(f"{font.family()} {font.pointSize()}pt")
                
    def edit_shortcut(self):
        """Edit keyboard shortcut"""
        current_item = self.shortcuts_list.currentItem()
        if current_item:
            QMessageBox.information(
                self,
                "Edit Shortcut",
                "Would open dialog to record new keyboard shortcut."
            )
            
    def reset_shortcuts(self):
        """Reset shortcuts to defaults"""
        QMessageBox.information(
            self,
            "Reset Shortcuts",
            "Would reset all keyboard shortcuts to default values."
        )
        
    def reset_layout(self):
        """Reset layout to default"""
        QMessageBox.information(
            self,
            "Reset Layout",
            "Would reset the interface layout to default configuration."
        )
        
    def load_css_file(self):
        """Load CSS from file"""
        QMessageBox.information(
            self,
            "Load CSS",
            "Would open file dialog to load CSS file."
        )
        
    def save_css_file(self):
        """Save CSS to file"""
        QMessageBox.information(
            self,
            "Save CSS",
            "Would save current CSS to file."
        )
        
    def apply_custom_css(self):
        """Apply custom CSS"""
        css_content = self.css_editor.toPlainText()
        if css_content.strip():
            QMessageBox.information(
                self,
                "Apply CSS",
                "Would apply custom CSS to the interface.\n\n"
                "Preview the changes before finalizing."
            )
            
    def preview_customization(self):
        """Preview customization changes"""
        QMessageBox.information(
            self,
            "Preview Customization",
            "Would show live preview of all customization changes."
        )
        
    def apply_customization(self):
        """Apply all customization settings"""
        config = {
            'colors': {
                'scheme': self.color_scheme.currentText(),
                'custom_colors': self.custom_colors,
                'rgb_enabled': self.enable_rgb.isChecked() if hasattr(self, 'enable_rgb') else False
            },
            'layout': {
                'preset': self.layout_preset.currentText(),
                'show_toolbar': self.show_toolbar.isChecked(),
                'show_sidebar': self.show_sidebar.isChecked(),
                'show_statusbar': self.show_statusbar.isChecked(),
                'toolbar_position': self.toolbar_position.currentText()
            },
            'fonts': {
                'base_size': self.font_size.value(),
                'icon_theme': self.icon_theme.currentText(),
                'icon_size': self.icon_size.currentText(),
                'cursor_theme': self.cursor_theme.currentText()
            },
            'animations': {
                'enabled': self.enable_animations.isChecked() if hasattr(self, 'enable_animations') else True,
                'speed': self.anim_speed_slider.value() if hasattr(self, 'anim_speed_slider') else 5
            },
            'performance': {
                'transparency': self.enable_transparency.isChecked() if hasattr(self, 'enable_transparency') else False,
                'shadows': self.enable_shadows.isChecked() if hasattr(self, 'enable_shadows') else True,
                'blur': self.enable_blur.isChecked() if hasattr(self, 'enable_blur') else False
            }
        }
        
        self.customization_changed.emit(config)
        
        QMessageBox.information(
            self,
            "Customization Applied",
            "Interface customization has been applied successfully!\n\n"
            "Changes will be included in the next ISO build."
        )
