"""
AI Assembly - Natural language UI generation
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                              QLineEdit, QPushButton, QTextEdit, QScrollArea,
                              QFrame, QListWidget, QListWidgetItem)
from PyQt6.QtCore import Qt, pyqtSignal, QTimer
from PyQt6.QtGui import QFont


class AISuggestionWidget(QFrame):
    """Widget for displaying an AI suggestion"""
    
    apply_clicked = pyqtSignal(dict)
    
    def __init__(self, suggestion_data):
        super().__init__()
        self.suggestion_data = suggestion_data
        self.setup_ui()
        
    def setup_ui(self):
        """Setup suggestion display"""
        self.setFrameStyle(QFrame.Shape.StyledPanel)
        self.setStyleSheet("""
            QFrame {
                background-color: #2d2d2d;
                border: 2px solid #3d3d3d;
                border-radius: 8px;
                padding: 10px;
            }
            QFrame:hover {
                border-color: #0078d4;
            }
        """)
        
        layout = QVBoxLayout(self)
        
        # Title
        title = QLabel(self.suggestion_data['title'])
        title_font = QFont()
        title_font.setPointSize(11)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)
        
        # Description
        desc = QLabel(self.suggestion_data['description'])
        desc.setWordWrap(True)
        desc.setStyleSheet("color: #b0b0b0;")
        layout.addWidget(desc)
        
        # Preview (simplified representation)
        preview = QLabel(f"📐 {self.suggestion_data['elements_count']} elements")
        preview.setStyleSheet("color: #888888; font-size: 9pt;")
        layout.addWidget(preview)
        
        # Apply button
        apply_btn = QPushButton("Apply to Canvas")
        apply_btn.setStyleSheet("""
            QPushButton {
                background-color: #0078d4;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 6px 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1084d8;
            }
        """)
        apply_btn.clicked.connect(lambda: self.apply_clicked.emit(self.suggestion_data))
        layout.addWidget(apply_btn)


class AIAssembly(QWidget):
    """AI-powered UI assembly with natural language"""
    
    layout_generated = pyqtSignal(dict)
    
    def __init__(self):
        super().__init__()
        self.processing = False
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the AI assembly interface"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Header
        header = QLabel("🤖 AI Assembly")
        header_font = QFont()
        header_font.setPointSize(12)
        header_font.setBold(True)
        header.setFont(header_font)
        layout.addWidget(header)
        
        desc = QLabel("Describe your UI in natural language")
        desc.setStyleSheet("color: #888888; font-size: 10pt;")
        layout.addWidget(desc)
        
        layout.addSpacing(10)
        
        # Input area
        input_layout = QHBoxLayout()
        
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText('e.g., "Create a login screen with username and password"')
        self.input_field.returnPressed.connect(self.generate_layout)
        input_layout.addWidget(self.input_field)
        
        self.generate_btn = QPushButton("Generate")
        self.generate_btn.setStyleSheet("""
            QPushButton {
                background-color: #0078d4;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1084d8;
            }
            QPushButton:disabled {
                background-color: #3d3d3d;
                color: #888888;
            }
        """)
        self.generate_btn.clicked.connect(self.generate_layout)
        input_layout.addWidget(self.generate_btn)
        
        layout.addLayout(input_layout)
        
        # Quick templates
        templates_label = QLabel("Quick Templates:")
        templates_label.setStyleSheet("color: #b0b0b0; margin-top: 10px;")
        layout.addWidget(templates_label)
        
        templates_layout = QHBoxLayout()
        
        template_btns = [
            ("Login Screen", "Create a login screen"),
            ("Dashboard", "Create a system dashboard"),
            ("Settings Panel", "Create a settings panel"),
            ("Media Player", "Create a media player interface"),
        ]
        
        for label, command in template_btns:
            btn = QPushButton(label)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #2d2d2d;
                    color: #e0e0e0;
                    border: 1px solid #3d3d3d;
                    border-radius: 3px;
                    padding: 5px 10px;
                    font-size: 9pt;
                }
                QPushButton:hover {
                    background-color: #3d3d3d;
                    border-color: #0078d4;
                }
            """)
            btn.clicked.connect(lambda checked, cmd=command: self.quick_generate(cmd))
            templates_layout.addWidget(btn)
            
        layout.addLayout(templates_layout)
        
        # Suggestions area
        suggestions_label = QLabel("Suggestions:")
        suggestions_label.setStyleSheet("color: #b0b0b0; margin-top: 15px;")
        layout.addWidget(suggestions_label)
        
        # Scroll area for suggestions
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        self.suggestions_container = QWidget()
        self.suggestions_layout = QVBoxLayout(self.suggestions_container)
        self.suggestions_layout.setContentsMargins(0, 0, 0, 0)
        
        # Initial message
        self.empty_label = QLabel("Enter a description and click Generate to see AI suggestions")
        self.empty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.empty_label.setStyleSheet("color: #666666; padding: 30px;")
        self.suggestions_layout.addWidget(self.empty_label)
        
        scroll.setWidget(self.suggestions_container)
        layout.addWidget(scroll)
        
        # Style
        self.setStyleSheet("""
            QLineEdit {
                background-color: #2d2d2d;
                color: #e0e0e0;
                border: 1px solid #3d3d3d;
                border-radius: 4px;
                padding: 8px;
                font-size: 10pt;
            }
            QLineEdit:focus {
                border-color: #0078d4;
            }
            QScrollArea {
                background-color: #252525;
                border: 1px solid #3d3d3d;
                border-radius: 4px;
            }
        """)
        
    def quick_generate(self, command):
        """Generate layout from quick template"""
        self.input_field.setText(command)
        self.generate_layout()
        
    def generate_layout(self):
        """Generate layout from natural language input"""
        text = self.input_field.text().strip()
        if not text or self.processing:
            return
            
        self.processing = True
        self.generate_btn.setEnabled(False)
        self.generate_btn.setText("Generating...")
        
        # Clear previous suggestions
        for i in reversed(range(self.suggestions_layout.count())):
            widget = self.suggestions_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()
                
        # Simulate AI processing
        QTimer.singleShot(500, lambda: self.show_suggestions(text))
        
    def show_suggestions(self, input_text):
        """Display AI-generated suggestions"""
        # Mock AI suggestions based on input
        suggestions = self.generate_mock_suggestions(input_text)
        
        for suggestion in suggestions:
            suggestion_widget = AISuggestionWidget(suggestion)
            suggestion_widget.apply_clicked.connect(self.apply_suggestion)
            self.suggestions_layout.addWidget(suggestion_widget)
            
        self.suggestions_layout.addStretch()
        
        self.processing = False
        self.generate_btn.setEnabled(True)
        self.generate_btn.setText("Generate")
        
    def generate_mock_suggestions(self, input_text):
        """Generate mock suggestions based on input"""
        lower_input = input_text.lower()
        
        if "login" in lower_input:
            return [
                {
                    'title': 'Centered Login Form',
                    'description': 'Clean centered login with username, password, and remember me checkbox',
                    'elements_count': 5,
                    'layout': {
                        'elements': [
                            {'type': 'text_input', 'x': 100, 'y': 100, 'width': 200, 'height': 30, 'text': 'Username'},
                            {'type': 'text_input', 'x': 100, 'y': 150, 'width': 200, 'height': 30, 'text': 'Password'},
                            {'type': 'checkbox', 'x': 100, 'y': 190, 'width': 150, 'height': 20, 'text': 'Remember me'},
                            {'type': 'button', 'x': 100, 'y': 230, 'width': 200, 'height': 35, 'text': 'Login'},
                        ]
                    }
                },
                {
                    'title': 'Modern Login Card',
                    'description': 'Card-style login with social media options',
                    'elements_count': 7,
                    'layout': {
                        'elements': [
                            {'type': 'panel', 'x': 50, 'y': 50, 'width': 300, 'height': 350},
                            {'type': 'label', 'x': 150, 'y': 70, 'width': 100, 'height': 30, 'text': 'Welcome'},
                            {'type': 'text_input', 'x': 100, 'y': 120, 'width': 200, 'height': 30, 'text': 'Email'},
                            {'type': 'text_input', 'x': 100, 'y': 170, 'width': 200, 'height': 30, 'text': 'Password'},
                            {'type': 'button', 'x': 100, 'y': 220, 'width': 200, 'height': 35, 'text': 'Sign In'},
                        ]
                    }
                }
            ]
        elif "dashboard" in lower_input:
            return [
                {
                    'title': 'System Dashboard',
                    'description': 'Grid layout with stats cards and graphs',
                    'elements_count': 8,
                    'layout': {
                        'elements': [
                            {'type': 'panel', 'x': 20, 'y': 20, 'width': 180, 'height': 120, 'text': 'CPU Usage'},
                            {'type': 'panel', 'x': 220, 'y': 20, 'width': 180, 'height': 120, 'text': 'Memory'},
                            {'type': 'panel', 'x': 420, 'y': 20, 'width': 180, 'height': 120, 'text': 'Disk Space'},
                            {'type': 'panel', 'x': 20, 'y': 160, 'width': 580, 'height': 200, 'text': 'Activity Graph'},
                        ]
                    }
                }
            ]
        elif "settings" in lower_input:
            return [
                {
                    'title': 'Settings Panel',
                    'description': 'Tabbed settings with categories',
                    'elements_count': 10,
                    'layout': {
                        'elements': [
                            {'type': 'tab_widget', 'x': 20, 'y': 20, 'width': 500, 'height': 400},
                            {'type': 'checkbox', 'x': 50, 'y': 80, 'width': 200, 'height': 25, 'text': 'Enable notifications'},
                            {'type': 'checkbox', 'x': 50, 'y': 120, 'width': 200, 'height': 25, 'text': 'Auto-update'},
                            {'type': 'slider', 'x': 50, 'y': 160, 'width': 300, 'height': 30, 'text': 'Volume'},
                        ]
                    }
                }
            ]
        elif "media" in lower_input or "player" in lower_input:
            return [
                {
                    'title': 'Media Player',
                    'description': 'Full media player with controls',
                    'elements_count': 9,
                    'layout': {
                        'elements': [
                            {'type': 'panel', 'x': 20, 'y': 20, 'width': 600, 'height': 350, 'text': 'Video Display'},
                            {'type': 'button', 'x': 250, 'y': 390, 'width': 50, 'height': 40, 'text': '▶️'},
                            {'type': 'button', 'x': 310, 'y': 390, 'width': 50, 'height': 40, 'text': '⏸️'},
                            {'type': 'slider', 'x': 50, 'y': 450, 'width': 540, 'height': 20, 'text': 'Progress'},
                            {'type': 'volume_control', 'x': 500, 'y': 390, 'width': 80, 'height': 40},
                        ]
                    }
                }
            ]
        else:
            return [
                {
                    'title': 'Basic Layout',
                    'description': 'Simple layout based on your description',
                    'elements_count': 4,
                    'layout': {
                        'elements': [
                            {'type': 'label', 'x': 100, 'y': 50, 'width': 200, 'height': 30, 'text': 'Custom UI'},
                            {'type': 'button', 'x': 100, 'y': 100, 'width': 100, 'height': 35, 'text': 'Button 1'},
                            {'type': 'button', 'x': 220, 'y': 100, 'width': 100, 'height': 35, 'text': 'Button 2'},
                        ]
                    }
                }
            ]
            
    def apply_suggestion(self, suggestion_data):
        """Apply selected suggestion to canvas"""
        self.layout_generated.emit(suggestion_data['layout'])
