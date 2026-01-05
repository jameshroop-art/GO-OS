#!/usr/bin/env python3
"""
Theme Editor Widget - Gaming and Production mode themes with cross-UI compatibility
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                              QPushButton, QGroupBox, QSlider, QSpinBox,
                              QColorDialog, QComboBox, QCheckBox, QTabWidget,
                              QListWidget, QListWidgetItem, QScrollArea,
                              QFrame, QGridLayout)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QColor


class ThemeEditorWidget(QWidget):
    """Widget for editing themes with gaming and production modes"""
    
    theme_changed = pyqtSignal(dict)
    
    def __init__(self):
        super().__init__()
        self.current_mode = "default"  # default, gaming, production
        self.current_theme = {}
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the theme editor interface"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Header
        header_label = QLabel("🎨 Theme Customization")
        header_font = QFont()
        header_font.setPointSize(14)
        header_font.setBold(True)
        header_label.setFont(header_font)
        layout.addWidget(header_label)
        
        info_label = QLabel("Customize themes for different UIs and modes")
        info_label.setStyleSheet("color: #888888; font-size: 10pt;")
        layout.addWidget(info_label)
        
        layout.addSpacing(10)
        
        # Mode selection tabs
        self.mode_tabs = QTabWidget()
        
        # Default theme tab
        default_tab = self.create_default_theme_tab()
        self.mode_tabs.addTab(default_tab, "🎯 Default")
        
        # Gaming mode tab
        gaming_tab = self.create_gaming_mode_tab()
        self.mode_tabs.addTab(gaming_tab, "🎮 Gaming Mode")
        
        # Production mode tab
        production_tab = self.create_production_mode_tab()
        self.mode_tabs.addTab(production_tab, "💼 Production Mode")
        
        layout.addWidget(self.mode_tabs)
        
        # Text scaling (global)
        scaling_group = QGroupBox("📏 Text Scaling (Cross-UI)")
        scaling_layout = QVBoxLayout(scaling_group)
        
        # Global scaling
        global_scale = QHBoxLayout()
        global_scale.addWidget(QLabel("Global UI Scale:"))
        self.global_scale_slider = QSlider(Qt.Orientation.Horizontal)
        self.global_scale_slider.setRange(50, 200)
        self.global_scale_slider.setValue(100)
        self.global_scale_slider.setTickInterval(25)
        self.global_scale_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.global_scale_slider.valueChanged.connect(self.on_scale_changed)
        global_scale.addWidget(self.global_scale_slider)
        self.global_scale_value = QLabel("100%")
        global_scale.addWidget(self.global_scale_value)
        scaling_layout.addLayout(global_scale)
        
        # Terminal scaling
        terminal_scale = QHBoxLayout()
        terminal_scale.addWidget(QLabel("Terminal Scale:"))
        self.terminal_scale_slider = QSlider(Qt.Orientation.Horizontal)
        self.terminal_scale_slider.setRange(50, 200)
        self.terminal_scale_slider.setValue(100)
        self.terminal_scale_slider.setTickInterval(25)
        self.terminal_scale_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.terminal_scale_slider.valueChanged.connect(self.on_scale_changed)
        terminal_scale.addWidget(self.terminal_scale_slider)
        self.terminal_scale_value = QLabel("100%")
        terminal_scale.addWidget(self.terminal_scale_value)
        scaling_layout.addLayout(terminal_scale)
        
        layout.addWidget(scaling_group)
        
        # Apply button
        apply_layout = QHBoxLayout()
        apply_layout.addStretch()
        
        apply_btn = QPushButton("✓ Apply Theme")
        apply_btn.setStyleSheet("""
            QPushButton {
                background-color: #0078d4;
                color: white;
                padding: 10px 20px;
                font-size: 11pt;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1084d8;
            }
        """)
        apply_btn.clicked.connect(self.apply_theme)
        apply_layout.addWidget(apply_btn)
        
        layout.addLayout(apply_layout)
        
    def create_default_theme_tab(self):
        """Create the default theme tab"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Preset themes
        preset_group = QGroupBox("Preset Themes")
        preset_layout = QVBoxLayout(preset_group)
        
        self.preset_list = QListWidget()
        presets = [
            "🌙 Dark (Default)",
            "☀️ Light",
            "🌃 Dracula",
            "❄️ Nord",
            "🌅 Solarized Dark",
            "🌄 Solarized Light",
            "🌲 Gruvbox",
            "🎨 Monokai",
        ]
        for preset in presets:
            self.preset_list.addItem(preset)
        self.preset_list.setCurrentRow(0)
        self.preset_list.currentItemChanged.connect(self.on_preset_changed)
        preset_layout.addWidget(self.preset_list)
        
        layout.addWidget(preset_group)
        
        # Custom colors
        color_group = QGroupBox("Custom Colors")
        color_layout = QGridLayout(color_group)
        
        colors = [
            ("Background:", "background"),
            ("Foreground:", "foreground"),
            ("Accent:", "accent"),
            ("Secondary:", "secondary"),
        ]
        
        self.color_buttons = {}
        for i, (label, key) in enumerate(colors):
            color_layout.addWidget(QLabel(label), i, 0)
            btn = QPushButton("Choose Color")
            btn.clicked.connect(lambda checked, k=key: self.choose_color(k))
            self.color_buttons[key] = btn
            color_layout.addWidget(btn, i, 1)
            
        layout.addWidget(color_group)
        layout.addStretch()
        
        return tab
        
    def create_gaming_mode_tab(self):
        """Create the gaming mode tab"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Gaming mode description
        desc = QLabel(
            "🎮 Gaming Mode automatically adapts themes based on the currently running game.\n"
            "Themes are optimized for performance and visual appeal."
        )
        desc.setWordWrap(True)
        desc.setStyleSheet("background-color: #2d2d2d; padding: 10px; border-radius: 4px;")
        layout.addWidget(desc)
        
        layout.addSpacing(10)
        
        # Adaptive theme detection
        adaptive_group = QGroupBox("Adaptive Theme Detection")
        adaptive_layout = QVBoxLayout(adaptive_group)
        
        self.auto_detect_check = QCheckBox("Automatically detect game and adapt theme")
        self.auto_detect_check.setChecked(True)
        adaptive_layout.addWidget(self.auto_detect_check)
        
        self.performance_mode_check = QCheckBox("Enable performance optimizations")
        self.performance_mode_check.setChecked(True)
        adaptive_layout.addWidget(self.performance_mode_check)
        
        layout.addWidget(adaptive_group)
        
        # Game exclusion list
        exclusion_group = QGroupBox("Game Exclusion List")
        exclusion_layout = QVBoxLayout(exclusion_group)
        
        exclusion_info = QLabel("Select games to exclude from auto-theming:")
        exclusion_layout.addWidget(exclusion_info)
        
        self.game_exclusion_list = QListWidget()
        self.game_exclusion_list.setMaximumHeight(200)
        
        games = [
            "Counter-Strike 2",
            "Dota 2",
            "Team Fortress 2",
            "Apex Legends",
            "Valorant",
            "Overwatch 2",
            "Fortnite",
            "Minecraft",
            "Terraria",
            "Cyberpunk 2077",
        ]
        
        for game in games:
            item = QListWidgetItem(game)
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
            item.setCheckState(Qt.CheckState.Unchecked)
            self.game_exclusion_list.addItem(item)
            
        exclusion_layout.addWidget(self.game_exclusion_list)
        layout.addWidget(exclusion_group)
        
        # Gaming theme presets
        preset_group = QGroupBox("Gaming Theme Presets")
        preset_layout = QVBoxLayout(preset_group)
        
        self.gaming_preset_combo = QComboBox()
        self.gaming_preset_combo.addItems([
            "Neon Cyberpunk",
            "Military Tactical",
            "Fantasy RPG",
            "Sci-Fi Space",
            "Retro Arcade",
            "Minimal FPS",
        ])
        preset_layout.addWidget(self.gaming_preset_combo)
        
        layout.addWidget(preset_group)
        layout.addStretch()
        
        return tab
        
    def create_production_mode_tab(self):
        """Create the production mode tab"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Production mode description
        desc = QLabel(
            "💼 Production Mode provides professionally designed color schemes\n"
            "optimized for long work sessions and reduced eye strain."
        )
        desc.setWordWrap(True)
        desc.setStyleSheet("background-color: #2d2d2d; padding: 10px; border-radius: 4px;")
        layout.addWidget(desc)
        
        layout.addSpacing(10)
        
        # Color scheme selection
        scheme_group = QGroupBox("Production Color Schemes")
        scheme_layout = QVBoxLayout(scheme_group)
        
        self.production_scheme_combo = QComboBox()
        self.production_scheme_combo.addItems([
            "Professional Blue",
            "Corporate Gray",
            "Warm Cream",
            "Cool Mint",
            "Earth Tones",
            "Ocean Deep",
            "Forest Green",
            "Sunset Orange",
        ])
        self.production_scheme_combo.currentTextChanged.connect(self.on_production_scheme_changed)
        scheme_layout.addWidget(self.production_scheme_combo)
        
        layout.addWidget(scheme_group)
        
        # Custom color scheme editor
        custom_group = QGroupBox("Custom Color Scheme")
        custom_layout = QGridLayout(custom_group)
        
        production_colors = [
            ("Primary Color:", "prod_primary"),
            ("Secondary Color:", "prod_secondary"),
            ("Text Color:", "prod_text"),
            ("Background:", "prod_background"),
            ("Panel Color:", "prod_panel"),
            ("Accent Color:", "prod_accent"),
        ]
        
        for i, (label, key) in enumerate(production_colors):
            custom_layout.addWidget(QLabel(label), i, 0)
            btn = QPushButton("Choose")
            btn.clicked.connect(lambda checked, k=key: self.choose_color(k))
            custom_layout.addWidget(btn, i, 1)
            
        layout.addWidget(custom_group)
        
        # Application-specific themes
        app_group = QGroupBox("Application-Specific Themes")
        app_layout = QVBoxLayout(app_group)
        
        app_info = QLabel("Customize themes for specific applications:")
        app_layout.addWidget(app_info)
        
        apps = QHBoxLayout()
        
        code_btn = QPushButton("💻 Code Editors")
        code_btn.clicked.connect(lambda: self.customize_app_theme("code"))
        apps.addWidget(code_btn)
        
        terminal_btn = QPushButton("🖥️ Terminals")
        terminal_btn.clicked.connect(lambda: self.customize_app_theme("terminal"))
        apps.addWidget(terminal_btn)
        
        browser_btn = QPushButton("🌐 Browsers")
        browser_btn.clicked.connect(lambda: self.customize_app_theme("browser"))
        apps.addWidget(browser_btn)
        
        app_layout.addLayout(apps)
        layout.addWidget(app_group)
        
        layout.addStretch()
        
        return tab
        
    def on_preset_changed(self, current, previous):
        """Handle preset theme selection"""
        if current:
            theme_name = current.text()
            # Load preset theme colors
            self.load_preset_theme(theme_name)
            
    def load_preset_theme(self, theme_name):
        """Load a preset theme configuration"""
        # This would load actual theme configs in production
        pass
        
    def on_production_scheme_changed(self, scheme_name):
        """Handle production scheme selection"""
        # Load production color scheme
        pass
        
    def choose_color(self, color_key):
        """Open color picker dialog"""
        color = QColorDialog.getColor()
        if color.isValid():
            if not hasattr(self, 'custom_colors'):
                self.custom_colors = {}
            self.custom_colors[color_key] = color.name()
            
            # Update button color
            if color_key in self.color_buttons:
                self.color_buttons[color_key].setStyleSheet(
                    f"background-color: {color.name()}; color: white;"
                )
                
    def customize_app_theme(self, app_type):
        """Open app-specific theme customization"""
        # Would open a dialog for app-specific theme settings
        pass
        
    def on_scale_changed(self):
        """Handle text scale changes"""
        global_val = self.global_scale_slider.value()
        terminal_val = self.terminal_scale_slider.value()
        
        self.global_scale_value.setText(f"{global_val}%")
        self.terminal_scale_value.setText(f"{terminal_val}%")
        
    def enable_gaming_mode(self):
        """Enable gaming mode"""
        self.current_mode = "gaming"
        self.mode_tabs.setCurrentIndex(1)
        self.apply_theme()
        
    def disable_gaming_mode(self):
        """Disable gaming mode"""
        self.current_mode = "default"
        self.mode_tabs.setCurrentIndex(0)
        self.apply_theme()
        
    def enable_production_mode(self):
        """Enable production mode"""
        self.current_mode = "production"
        self.mode_tabs.setCurrentIndex(2)
        self.apply_theme()
        
    def disable_production_mode(self):
        """Disable production mode"""
        self.current_mode = "default"
        self.mode_tabs.setCurrentIndex(0)
        self.apply_theme()
        
    def apply_theme(self):
        """Apply the current theme"""
        theme_data = {
            'mode': self.current_mode,
            'name': self.get_current_theme_name(),
            'global_scale': self.global_scale_slider.value(),
            'terminal_scale': self.terminal_scale_slider.value(),
            'custom_colors': getattr(self, 'custom_colors', {}),
        }
        
        if self.current_mode == "gaming":
            theme_data['gaming'] = {
                'auto_detect': self.auto_detect_check.isChecked(),
                'performance_mode': self.performance_mode_check.isChecked(),
                'preset': self.gaming_preset_combo.currentText(),
                'excluded_games': self.get_excluded_games(),
            }
        elif self.current_mode == "production":
            theme_data['production'] = {
                'scheme': self.production_scheme_combo.currentText(),
            }
            
        self.current_theme = theme_data
        self.theme_changed.emit(theme_data)
        
    def get_current_theme_name(self):
        """Get the name of the current theme"""
        if self.current_mode == "default":
            if self.preset_list.currentItem():
                return self.preset_list.currentItem().text()
        elif self.current_mode == "gaming":
            return f"Gaming - {self.gaming_preset_combo.currentText()}"
        elif self.current_mode == "production":
            return f"Production - {self.production_scheme_combo.currentText()}"
        return "Custom"
        
    def get_excluded_games(self):
        """Get list of excluded games"""
        excluded = []
        for i in range(self.game_exclusion_list.count()):
            item = self.game_exclusion_list.item(i)
            if item.checkState() == Qt.CheckState.Checked:
                excluded.append(item.text())
        return excluded
