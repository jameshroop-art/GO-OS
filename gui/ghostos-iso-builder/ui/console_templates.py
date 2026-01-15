"""
Console-Style GUI Templates
Gaming console and Steam-inspired prebuilt interfaces
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                              QPushButton, QScrollArea, QFrame, QGridLayout,
                              QListWidget, QListWidgetItem, QTextEdit)
from PyQt6.QtCore import Qt, pyqtSignal, QSize
from PyQt6.QtGui import QFont, QIcon, QPixmap


class TemplatePreview(QFrame):
    """Preview widget for a console template"""
    
    template_selected = pyqtSignal(dict)
    
    def __init__(self, template_data):
        super().__init__()
        self.template_data = template_data
        self.setup_ui()
        
    def setup_ui(self):
        """Setup template preview"""
        self.setFrameStyle(QFrame.Shape.StyledPanel)
        self.setStyleSheet("""
            QFrame {
                background-color: #2a2a2a;
                border: 2px solid #3d3d3d;
                border-radius: 8px;
                padding: 12px;
            }
            QFrame:hover {
                border-color: #0078d4;
                background-color: #323232;
            }
        """)
        self.setFixedSize(280, 200)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        
        layout = QVBoxLayout(self)
        
        # Template name
        name_label = QLabel(self.template_data['name'])
        name_font = QFont()
        name_font.setPointSize(11)
        name_font.setBold(True)
        name_label.setFont(name_font)
        name_label.setStyleSheet("color: #ffffff;")
        layout.addWidget(name_label)
        
        # Template type badge
        type_label = QLabel(f"🎮 {self.template_data['type']}")
        type_label.setStyleSheet("""
            color: #0078d4;
            font-size: 9pt;
            font-weight: bold;
        """)
        layout.addWidget(type_label)
        
        # Description
        desc_label = QLabel(self.template_data['description'])
        desc_label.setWordWrap(True)
        desc_label.setStyleSheet("color: #b0b0b0; font-size: 9pt;")
        layout.addWidget(desc_label)
        
        # Features list
        features_text = "Features:\n• " + "\n• ".join(self.template_data['features'][:3])
        features_label = QLabel(features_text)
        features_label.setStyleSheet("color: #888888; font-size: 8pt;")
        features_label.setWordWrap(True)
        layout.addWidget(features_label)
        
        layout.addStretch()
        
        # Select button
        select_btn = QPushButton("Load Template")
        select_btn.setStyleSheet("""
            QPushButton {
                background-color: #0078d4;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1084d8;
            }
        """)
        select_btn.clicked.connect(lambda: self.template_selected.emit(self.template_data))
        layout.addWidget(select_btn)
    
    def mousePressEvent(self, event):
        """Handle click on preview"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.template_selected.emit(self.template_data)


class ConsoleTemplates(QWidget):
    """Console-style prebuilt GUI templates"""
    
    template_loaded = pyqtSignal(dict)
    
    def __init__(self):
        super().__init__()
        self.templates = self.create_templates()
        self.setup_ui()
        
    def create_templates(self):
        """Create all console-style templates"""
        templates = []
        
        # PlayStation-style template
        templates.append({
            'id': 'playstation_home',
            'name': 'PlayStation Home',
            'type': 'Console UI',
            'description': 'PlayStation-inspired home screen with horizontal game library',
            'features': [
                'Horizontal scrolling game tiles',
                'Top navigation bar with user profile',
                'Side menu for settings and features',
                'Background music visualizer',
                'Trophy notifications'
            ],
            'elements': [
                {'type': 'Panel', 'x': 0, 'y': 0, 'width': 1400, 'height': 80, 'bg_color': '#003087', 'text': 'Header Bar'},
                {'type': 'Label', 'x': 20, 'y': 20, 'width': 200, 'height': 40, 'text': 'HeckOS Gaming', 'font_size': 24, 'color': '#ffffff'},
                {'type': 'Button', 'x': 1200, 'y': 20, 'width': 150, 'height': 40, 'text': 'User Profile', 'bg_color': '#0050a0'},
                
                # Game tiles (horizontal scroll)
                {'type': 'Panel', 'x': 50, 'y': 150, 'width': 250, 'height': 350, 'bg_color': '#1a1a1a', 'text': 'Game 1'},
                {'type': 'Label', 'x': 70, 'y': 420, 'width': 210, 'height': 30, 'text': 'Featured Game', 'font_size': 16, 'color': '#ffffff'},
                
                {'type': 'Panel', 'x': 330, 'y': 150, 'width': 250, 'height': 350, 'bg_color': '#1a1a1a', 'text': 'Game 2'},
                {'type': 'Label', 'x': 350, 'y': 420, 'width': 210, 'height': 30, 'text': 'Action Game', 'font_size': 16, 'color': '#ffffff'},
                
                {'type': 'Panel', 'x': 610, 'y': 150, 'width': 250, 'height': 350, 'bg_color': '#1a1a1a', 'text': 'Game 3'},
                {'type': 'Label', 'x': 630, 'y': 420, 'width': 210, 'height': 30, 'text': 'RPG Game', 'font_size': 16, 'color': '#ffffff'},
                
                {'type': 'Panel', 'x': 890, 'y': 150, 'width': 250, 'height': 350, 'bg_color': '#1a1a1a', 'text': 'Game 4'},
                {'type': 'Label', 'x': 910, 'y': 420, 'width': 210, 'height': 30, 'text': 'Racing Game', 'font_size': 16, 'color': '#ffffff'},
                
                # Bottom bar
                {'type': 'Panel', 'x': 0, 'y': 820, 'width': 1400, 'height': 80, 'bg_color': '#002060', 'text': 'Footer Bar'},
                {'type': 'Button', 'x': 50, 'y': 840, 'width': 120, 'height': 40, 'text': 'Library', 'bg_color': '#0050a0'},
                {'type': 'Button', 'x': 190, 'y': 840, 'width': 120, 'height': 40, 'text': 'Store', 'bg_color': '#0050a0'},
                {'type': 'Button', 'x': 330, 'y': 840, 'width': 120, 'height': 40, 'text': 'Friends', 'bg_color': '#0050a0'},
                {'type': 'Button', 'x': 470, 'y': 840, 'width': 120, 'height': 40, 'text': 'Settings', 'bg_color': '#0050a0'},
            ],
            'color_scheme': {
                'primary': '#003087',
                'secondary': '#0050a0',
                'accent': '#ffffff',
                'background': '#000000'
            }
        })
        
        # Xbox-style template
        templates.append({
            'id': 'xbox_dashboard',
            'name': 'Xbox Dashboard',
            'type': 'Console UI',
            'description': 'Xbox-inspired dashboard with tile-based interface',
            'features': [
                'Live tile grid layout',
                'Guide menu sidebar',
                'Achievement popups',
                'Friend activity feed',
                'Quick access to recent games'
            ],
            'elements': [
                # Top navigation
                {'type': 'Panel', 'x': 0, 'y': 0, 'width': 1400, 'height': 70, 'bg_color': '#107c10', 'text': 'Header'},
                {'type': 'Label', 'x': 20, 'y': 15, 'width': 200, 'height': 40, 'text': '🎮 HeckOS Xbox', 'font_size': 20, 'color': '#ffffff'},
                {'type': 'Button', 'x': 1200, 'y': 15, 'width': 150, 'height': 40, 'text': 'My Account', 'bg_color': '#0e6a0e'},
                
                # Side guide menu
                {'type': 'Panel', 'x': 0, 'y': 70, 'width': 250, 'height': 830, 'bg_color': '#1a1a1a', 'text': 'Guide'},
                {'type': 'Button', 'x': 20, 'y': 90, 'width': 210, 'height': 50, 'text': 'Home', 'bg_color': '#2d2d2d'},
                {'type': 'Button', 'x': 20, 'y': 150, 'width': 210, 'height': 50, 'text': 'Recent', 'bg_color': '#2d2d2d'},
                {'type': 'Button', 'x': 20, 'y': 210, 'width': 210, 'height': 50, 'text': 'Library', 'bg_color': '#2d2d2d'},
                {'type': 'Button', 'x': 20, 'y': 270, 'width': 210, 'height': 50, 'text': 'Store', 'bg_color': '#2d2d2d'},
                {'type': 'Button', 'x': 20, 'y': 330, 'width': 210, 'height': 50, 'text': 'Game Pass', 'bg_color': '#2d2d2d'},
                {'type': 'Button', 'x': 20, 'y': 390, 'width': 210, 'height': 50, 'text': 'Community', 'bg_color': '#2d2d2d'},
                
                # Main content area with tiles
                {'type': 'Panel', 'x': 280, 'y': 100, 'width': 280, 'height': 180, 'bg_color': '#107c10', 'text': 'Featured Tile'},
                {'type': 'Label', 'x': 300, 'y': 200, 'width': 240, 'height': 30, 'text': 'Continue Playing', 'font_size': 14, 'color': '#ffffff'},
                
                {'type': 'Panel', 'x': 590, 'y': 100, 'width': 280, 'height': 180, 'bg_color': '#2d2d2d', 'text': 'Game 1'},
                {'type': 'Label', 'x': 610, 'y': 200, 'width': 240, 'height': 30, 'text': 'Recently Played', 'font_size': 14, 'color': '#ffffff'},
                
                {'type': 'Panel', 'x': 900, 'y': 100, 'width': 280, 'height': 180, 'bg_color': '#2d2d2d', 'text': 'Game 2'},
                {'type': 'Label', 'x': 920, 'y': 200, 'width': 240, 'height': 30, 'text': 'New Release', 'font_size': 14, 'color': '#ffffff'},
                
                # Second row
                {'type': 'Panel', 'x': 280, 'y': 310, 'width': 280, 'height': 180, 'bg_color': '#2d2d2d', 'text': 'Tile 4'},
                {'type': 'Panel', 'x': 590, 'y': 310, 'width': 280, 'height': 180, 'bg_color': '#2d2d2d', 'text': 'Tile 5'},
                {'type': 'Panel', 'x': 900, 'y': 310, 'width': 280, 'height': 180, 'bg_color': '#2d2d2d', 'text': 'Tile 6'},
                
                # Third row
                {'type': 'Panel', 'x': 280, 'y': 520, 'width': 280, 'height': 180, 'bg_color': '#2d2d2d', 'text': 'Tile 7'},
                {'type': 'Panel', 'x': 590, 'y': 520, 'width': 280, 'height': 180, 'bg_color': '#2d2d2d', 'text': 'Tile 8'},
                {'type': 'Panel', 'x': 900, 'y': 520, 'width': 280, 'height': 180, 'bg_color': '#2d2d2d', 'text': 'Tile 9'},
            ],
            'color_scheme': {
                'primary': '#107c10',
                'secondary': '#0e6a0e',
                'accent': '#ffffff',
                'background': '#000000'
            }
        })
        
        # Steam Big Picture Mode template
        templates.append({
            'id': 'steam_big_picture',
            'name': 'Steam Big Picture',
            'type': 'Gaming Platform',
            'description': 'Steam Big Picture Mode interface for couch gaming',
            'features': [
                'Large text and buttons for TV viewing',
                'Controller-friendly navigation',
                'Game library with grid view',
                'Friends list and chat',
                'Achievement showcase'
            ],
            'elements': [
                # Top bar with gradient
                {'type': 'Panel', 'x': 0, 'y': 0, 'width': 1400, 'height': 90, 'bg_color': '#1b2838', 'text': 'Header'},
                {'type': 'Label', 'x': 30, 'y': 20, 'width': 300, 'height': 50, 'text': 'HECKO GAMING', 'font_size': 28, 'color': '#c7d5e0'},
                {'type': 'Button', 'x': 1150, 'y': 25, 'width': 200, 'height': 40, 'text': 'Player Profile', 'bg_color': '#417a9b'},
                
                # Left sidebar navigation
                {'type': 'Panel', 'x': 0, 'y': 90, 'width': 300, 'height': 810, 'bg_color': '#1b2838', 'text': 'Navigation'},
                {'type': 'Button', 'x': 20, 'y': 120, 'width': 260, 'height': 60, 'text': '🏠 HOME', 'bg_color': '#2a475e', 'font_size': 16},
                {'type': 'Button', 'x': 20, 'y': 190, 'width': 260, 'height': 60, 'text': '📚 LIBRARY', 'bg_color': '#2a475e', 'font_size': 16},
                {'type': 'Button', 'x': 20, 'y': 260, 'width': 260, 'height': 60, 'text': '🛒 STORE', 'bg_color': '#2a475e', 'font_size': 16},
                {'type': 'Button', 'x': 20, 'y': 330, 'width': 260, 'height': 60, 'text': '👥 FRIENDS', 'bg_color': '#2a475e', 'font_size': 16},
                {'type': 'Button', 'x': 20, 'y': 400, 'width': 260, 'height': 60, 'text': '⚙️ SETTINGS', 'bg_color': '#2a475e', 'font_size': 16},
                
                # Main content area - Featured game
                {'type': 'Panel', 'x': 320, 'y': 110, 'width': 1050, 'height': 400, 'bg_color': '#171a21', 'text': 'Featured'},
                {'type': 'Label', 'x': 350, 'y': 130, 'width': 400, 'height': 60, 'text': 'FEATURED GAME', 'font_size': 32, 'color': '#ffffff'},
                {'type': 'Label', 'x': 350, 'y': 200, 'width': 600, 'height': 100, 'text': 'Continue your adventure...', 'font_size': 16, 'color': '#c7d5e0'},
                {'type': 'Button', 'x': 350, 'y': 420, 'width': 200, 'height': 60, 'text': 'PLAY NOW', 'bg_color': '#5c7e10', 'font_size': 18},
                {'type': 'Button', 'x': 570, 'y': 420, 'width': 200, 'height': 60, 'text': 'VIEW DETAILS', 'bg_color': '#417a9b', 'font_size': 18},
                
                # Game grid
                {'type': 'Label', 'x': 320, 'y': 530, 'width': 300, 'height': 40, 'text': 'RECENT GAMES', 'font_size': 18, 'color': '#c7d5e0'},
                
                {'type': 'Panel', 'x': 320, 'y': 580, 'width': 240, 'height': 135, 'bg_color': '#2a475e', 'text': 'Game 1'},
                {'type': 'Label', 'x': 330, 'y': 690, 'width': 220, 'height': 25, 'text': 'Action Game', 'font_size': 12, 'color': '#c7d5e0'},
                
                {'type': 'Panel', 'x': 580, 'y': 580, 'width': 240, 'height': 135, 'bg_color': '#2a475e', 'text': 'Game 2'},
                {'type': 'Label', 'x': 590, 'y': 690, 'width': 220, 'height': 25, 'text': 'Strategy Game', 'font_size': 12, 'color': '#c7d5e0'},
                
                {'type': 'Panel', 'x': 840, 'y': 580, 'width': 240, 'height': 135, 'bg_color': '#2a475e', 'text': 'Game 3'},
                {'type': 'Label', 'x': 850, 'y': 690, 'width': 220, 'height': 25, 'text': 'RPG Game', 'font_size': 12, 'color': '#c7d5e0'},
                
                {'type': 'Panel', 'x': 1100, 'y': 580, 'width': 240, 'height': 135, 'bg_color': '#2a475e', 'text': 'Game 4'},
                {'type': 'Label', 'x': 1110, 'y': 690, 'width': 220, 'height': 25, 'text': 'Indie Game', 'font_size': 12, 'color': '#c7d5e0'},
                
                # Bottom status bar
                {'type': 'Panel', 'x': 320, 'y': 750, 'width': 1050, 'height': 60, 'bg_color': '#1b2838', 'text': 'Status'},
                {'type': 'Label', 'x': 340, 'y': 765, 'width': 400, 'height': 30, 'text': '🎮 Controller Connected | 🔊 Audio OK', 'font_size': 12, 'color': '#c7d5e0'},
            ],
            'color_scheme': {
                'primary': '#1b2838',
                'secondary': '#2a475e',
                'accent': '#66c0f4',
                'background': '#171a21'
            }
        })
        
        # Nintendo Switch-style template
        templates.append({
            'id': 'switch_home',
            'name': 'Nintendo Switch Home',
            'type': 'Console UI',
            'description': 'Nintendo Switch-inspired clean and simple interface',
            'features': [
                'Minimalist design',
                'Horizontal game row',
                'Quick settings menu',
                'User profiles',
                'News feed'
            ],
            'elements': [
                # Top info bar
                {'type': 'Panel', 'x': 0, 'y': 0, 'width': 1400, 'height': 60, 'bg_color': '#2d2d2d', 'text': 'Info Bar'},
                {'type': 'Label', 'x': 30, 'y': 15, 'width': 200, 'height': 30, 'text': 'HeckOS Switch', 'font_size': 18, 'color': '#ffffff'},
                {'type': 'Label', 'x': 1150, 'y': 15, 'width': 200, 'height': 30, 'text': '🔋 100% | 🕐 12:00', 'font_size': 12, 'color': '#ffffff'},
                
                # Main game selection area
                {'type': 'Label', 'x': 100, 'y': 100, 'width': 300, 'height': 40, 'text': 'Select a Game', 'font_size': 22, 'color': '#ffffff'},
                
                # Large game tiles (horizontal)
                {'type': 'Panel', 'x': 100, 'y': 160, 'width': 280, 'height': 420, 'bg_color': '#e60012', 'text': 'Featured'},
                {'type': 'Label', 'x': 120, 'y': 500, 'width': 240, 'height': 40, 'text': 'Featured Game', 'font_size': 16, 'color': '#ffffff'},
                {'type': 'Label', 'x': 120, 'y': 540, 'width': 240, 'height': 30, 'text': 'Last played 2 hours ago', 'font_size': 11, 'color': '#aaaaaa'},
                
                {'type': 'Panel', 'x': 410, 'y': 160, 'width': 280, 'height': 420, 'bg_color': '#4d4d4d', 'text': 'Game 2'},
                {'type': 'Label', 'x': 430, 'y': 500, 'width': 240, 'height': 40, 'text': 'Adventure Game', 'font_size': 16, 'color': '#ffffff'},
                
                {'type': 'Panel', 'x': 720, 'y': 160, 'width': 280, 'height': 420, 'bg_color': '#4d4d4d', 'text': 'Game 3'},
                {'type': 'Label', 'x': 740, 'y': 500, 'width': 240, 'height': 40, 'text': 'Puzzle Game', 'font_size': 16, 'color': '#ffffff'},
                
                {'type': 'Panel', 'x': 1030, 'y': 160, 'width': 280, 'height': 420, 'bg_color': '#4d4d4d', 'text': 'All Games'},
                {'type': 'Label', 'x': 1050, 'y': 500, 'width': 240, 'height': 40, 'text': 'View All Games', 'font_size': 16, 'color': '#ffffff'},
                
                # Bottom menu buttons
                {'type': 'Panel', 'x': 0, 'y': 800, 'width': 1400, 'height': 100, 'bg_color': '#1a1a1a', 'text': 'Menu Bar'},
                {'type': 'Button', 'x': 100, 'y': 820, 'width': 150, 'height': 60, 'text': '🎮 Controllers', 'bg_color': '#2d2d2d'},
                {'type': 'Button', 'x': 270, 'y': 820, 'width': 150, 'height': 60, 'text': '⚙️ Settings', 'bg_color': '#2d2d2d'},
                {'type': 'Button', 'x': 440, 'y': 820, 'width': 150, 'height': 60, 'text': '💤 Sleep Mode', 'bg_color': '#2d2d2d'},
                {'type': 'Button', 'x': 610, 'y': 820, 'width': 150, 'height': 60, 'text': '🔌 Power', 'bg_color': '#2d2d2d'},
            ],
            'color_scheme': {
                'primary': '#e60012',
                'secondary': '#2d2d2d',
                'accent': '#ffffff',
                'background': '#000000'
            }
        })
        
        # Retro Arcade template
        templates.append({
            'id': 'retro_arcade',
            'name': 'Retro Arcade',
            'type': 'Gaming Platform',
            'description': 'Nostalgic arcade cabinet-style interface',
            'features': [
                'Pixel art aesthetic',
                'High score displays',
                'Coin-op style buttons',
                'CRT screen effect',
                'Retro sound effects'
            ],
            'elements': [
                # Arcade cabinet header
                {'type': 'Panel', 'x': 0, 'y': 0, 'width': 1400, 'height': 100, 'bg_color': '#ff00ff', 'text': 'Arcade Header'},
                {'type': 'Label', 'x': 450, 'y': 20, 'width': 500, 'height': 60, 'text': '🕹️ HECK ARCADE 🕹️', 'font_size': 36, 'color': '#ffff00'},
                
                # Insert coin section
                {'type': 'Panel', 'x': 500, 'y': 120, 'width': 400, 'height': 80, 'bg_color': '#000000', 'text': 'Insert Coin'},
                {'type': 'Label', 'x': 520, 'y': 135, 'width': 360, 'height': 50, 'text': '>>> INSERT COIN <<<', 'font_size': 24, 'color': '#00ff00'},
                
                # Game selection grid (arcade style)
                {'type': 'Label', 'x': 200, 'y': 230, 'width': 300, 'height': 40, 'text': '=== SELECT GAME ===', 'font_size': 20, 'color': '#00ffff'},
                
                {'type': 'Button', 'x': 200, 'y': 290, 'width': 220, 'height': 120, 'text': 'SPACE\nINVADERS', 'bg_color': '#0000ff', 'font_size': 16},
                {'type': 'Button', 'x': 450, 'y': 290, 'width': 220, 'height': 120, 'text': 'PAC-MAN', 'bg_color': '#ffff00', 'font_size': 16},
                {'type': 'Button', 'x': 700, 'y': 290, 'width': 220, 'height': 120, 'text': 'DONKEY\nKONG', 'bg_color': '#ff0000', 'font_size': 16},
                {'type': 'Button', 'x': 950, 'y': 290, 'width': 220, 'height': 120, 'text': 'GALAGA', 'bg_color': '#00ff00', 'font_size': 16},
                
                {'type': 'Button', 'x': 200, 'y': 440, 'width': 220, 'height': 120, 'text': 'STREET\nFIGHTER', 'bg_color': '#ff00ff', 'font_size': 16},
                {'type': 'Button', 'x': 450, 'y': 440, 'width': 220, 'height': 120, 'text': 'TETRIS', 'bg_color': '#00ffff', 'font_size': 16},
                {'type': 'Button', 'x': 700, 'y': 440, 'width': 220, 'height': 120, 'text': 'MORTAL\nKOMBAT', 'bg_color': '#ff8800', 'font_size': 16},
                {'type': 'Button', 'x': 950, 'y': 440, 'width': 220, 'height': 120, 'text': 'SONIC', 'bg_color': '#0088ff', 'font_size': 16},
                
                # High scores panel
                {'type': 'Panel', 'x': 300, 'y': 590, 'width': 800, 'height': 200, 'bg_color': '#1a0033', 'text': 'High Scores'},
                {'type': 'Label', 'x': 600, 'y': 610, 'width': 200, 'height': 40, 'text': 'HIGH SCORES', 'font_size': 20, 'color': '#ffff00'},
                {'type': 'Label', 'x': 350, 'y': 660, 'width': 700, 'height': 30, 'text': '1. AAA ..... 999,999', 'font_size': 14, 'color': '#00ff00'},
                {'type': 'Label', 'x': 350, 'y': 690, 'width': 700, 'height': 30, 'text': '2. BBB ..... 888,888', 'font_size': 14, 'color': '#00ff00'},
                {'type': 'Label', 'x': 350, 'y': 720, 'width': 700, 'height': 30, 'text': '3. CCC ..... 777,777', 'font_size': 14, 'color': '#00ff00'},
                
                # Control info at bottom
                {'type': 'Panel', 'x': 0, 'y': 820, 'width': 1400, 'height': 80, 'bg_color': '#330000', 'text': 'Controls'},
                {'type': 'Label', 'x': 400, 'y': 840, 'width': 600, 'height': 40, 'text': '🎮 USE GAMEPAD OR KEYBOARD', 'font_size': 16, 'color': '#ffffff'},
            ],
            'color_scheme': {
                'primary': '#ff00ff',
                'secondary': '#00ffff',
                'accent': '#ffff00',
                'background': '#000033'
            }
        })
        
        # Modern Gaming Hub template
        templates.append({
            'id': 'modern_gaming_hub',
            'name': 'Modern Gaming Hub',
            'type': 'Gaming Platform',
            'description': 'Contemporary gaming platform with social features',
            'features': [
                'Material design aesthetic',
                'Social feed integration',
                'Live streaming section',
                'Tournament brackets',
                'Achievement tracking'
            ],
            'elements': [
                # Modern header with gradient
                {'type': 'Panel', 'x': 0, 'y': 0, 'width': 1400, 'height': 80, 'bg_color': '#6441a5', 'text': 'Header'},
                {'type': 'Label', 'x': 30, 'y': 20, 'width': 250, 'height': 40, 'text': 'Gaming Hub', 'font_size': 26, 'color': '#ffffff'},
                {'type': 'TextInput', 'x': 400, 'y': 25, 'width': 400, 'height': 30, 'text': '🔍 Search games, players, streams...'},
                {'type': 'Button', 'x': 1100, 'y': 20, 'width': 120, 'height': 40, 'text': 'Go Live', 'bg_color': '#ff4444'},
                {'type': 'Button', 'x': 1240, 'y': 20, 'width': 120, 'height': 40, 'text': 'Profile', 'bg_color': '#9147ff'},
                
                # Left navigation
                {'type': 'Panel', 'x': 0, 'y': 80, 'width': 200, 'height': 820, 'bg_color': '#18181b', 'text': 'Nav'},
                {'type': 'Button', 'x': 10, 'y': 100, 'width': 180, 'height': 45, 'text': '🏠 Home', 'bg_color': '#6441a5'},
                {'type': 'Button', 'x': 10, 'y': 155, 'width': 180, 'height': 45, 'text': '📚 Library', 'bg_color': '#2d2d35'},
                {'type': 'Button', 'x': 10, 'y': 210, 'width': 180, 'height': 45, 'text': '📺 Live', 'bg_color': '#2d2d35'},
                {'type': 'Button', 'x': 10, 'y': 265, 'width': 180, 'height': 45, 'text': '🏆 Tournaments', 'bg_color': '#2d2d35'},
                {'type': 'Button', 'x': 10, 'y': 320, 'width': 180, 'height': 45, 'text': '👥 Friends', 'bg_color': '#2d2d35'},
                {'type': 'Button', 'x': 10, 'y': 375, 'width': 180, 'height': 45, 'text': '🎯 Achievements', 'bg_color': '#2d2d35'},
                
                # Main content - Featured carousel
                {'type': 'Panel', 'x': 220, 'y': 100, 'width': 900, 'height': 400, 'bg_color': '#0e0e10', 'text': 'Featured'},
                {'type': 'Label', 'x': 250, 'y': 130, 'width': 600, 'height': 50, 'text': 'FEATURED: Epic Battle Royale', 'font_size': 28, 'color': '#ffffff'},
                {'type': 'Label', 'x': 250, 'y': 190, 'width': 600, 'height': 80, 'text': 'Join millions of players in the ultimate\ncombat experience', 'font_size': 16, 'color': '#dedede'},
                {'type': 'Button', 'x': 250, 'y': 400, 'width': 180, 'height': 50, 'text': 'PLAY NOW', 'bg_color': '#ff4444', 'font_size': 18},
                {'type': 'Button', 'x': 450, 'y': 400, 'width': 180, 'height': 50, 'text': 'WATCH LIVE', 'bg_color': '#6441a5', 'font_size': 18},
                
                # Right sidebar - Live streams
                {'type': 'Panel', 'x': 1140, 'y': 100, 'width': 240, 'height': 700, 'bg_color': '#18181b', 'text': 'Live'},
                {'type': 'Label', 'x': 1160, 'y': 120, 'width': 200, 'height': 30, 'text': '🔴 LIVE NOW', 'font_size': 16, 'color': '#ffffff'},
                
                {'type': 'Panel', 'x': 1150, 'y': 160, 'width': 220, 'height': 140, 'bg_color': '#0e0e10', 'text': 'Stream 1'},
                {'type': 'Label', 'x': 1160, 'y': 265, 'width': 200, 'height': 25, 'text': 'Streamer1', 'font_size': 11, 'color': '#dedede'},
                {'type': 'Label', 'x': 1160, 'y': 285, 'width': 200, 'height': 20, 'text': '15.2K viewers', 'font_size': 9, 'color': '#adadb8'},
                
                {'type': 'Panel', 'x': 1150, 'y': 320, 'width': 220, 'height': 140, 'bg_color': '#0e0e10', 'text': 'Stream 2'},
                {'type': 'Label', 'x': 1160, 'y': 425, 'width': 200, 'height': 25, 'text': 'Streamer2', 'font_size': 11, 'color': '#dedede'},
                {'type': 'Label', 'x': 1160, 'y': 445, 'width': 200, 'height': 20, 'text': '8.7K viewers', 'font_size': 9, 'color': '#adadb8'},
                
                # Games grid
                {'type': 'Label', 'x': 220, 'y': 520, 'width': 300, 'height': 35, 'text': 'Popular Games', 'font_size': 20, 'color': '#ffffff'},
                
                {'type': 'Panel', 'x': 220, 'y': 570, 'width': 200, 'height': 200, 'bg_color': '#0e0e10', 'text': 'Game 1'},
                {'type': 'Label', 'x': 230, 'y': 745, 'width': 180, 'height': 25, 'text': 'FPS Shooter', 'font_size': 12, 'color': '#ffffff'},
                
                {'type': 'Panel', 'x': 440, 'y': 570, 'width': 200, 'height': 200, 'bg_color': '#0e0e10', 'text': 'Game 2'},
                {'type': 'Label', 'x': 450, 'y': 745, 'width': 180, 'height': 25, 'text': 'RPG Adventure', 'font_size': 12, 'color': '#ffffff'},
                
                {'type': 'Panel', 'x': 660, 'y': 570, 'width': 200, 'height': 200, 'bg_color': '#0e0e10', 'text': 'Game 3'},
                {'type': 'Label', 'x': 670, 'y': 745, 'width': 180, 'height': 25, 'text': 'Strategy War', 'font_size': 12, 'color': '#ffffff'},
                
                {'type': 'Panel', 'x': 880, 'y': 570, 'width': 200, 'height': 200, 'bg_color': '#0e0e10', 'text': 'Game 4'},
                {'type': 'Label', 'x': 890, 'y': 745, 'width': 180, 'height': 25, 'text': 'Sports Title', 'font_size': 12, 'color': '#ffffff'},
            ],
            'color_scheme': {
                'primary': '#6441a5',
                'secondary': '#9147ff',
                'accent': '#ff4444',
                'background': '#0e0e10'
            }
        })
        
        return templates
    
    def setup_ui(self):
        """Setup the console templates interface"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Header
        header_layout = QHBoxLayout()
        header = QLabel("🎮 Console-Style Templates")
        header_font = QFont()
        header_font.setPointSize(14)
        header_font.setBold(True)
        header.setFont(header_font)
        header.setStyleSheet("color: #ffffff;")
        header_layout.addWidget(header)
        
        header_layout.addStretch()
        
        # Info button
        info_label = QLabel("Click any template to load it into the designer")
        info_label.setStyleSheet("color: #888888; font-size: 10pt;")
        header_layout.addWidget(info_label)
        
        layout.addLayout(header_layout)
        
        # Description
        desc = QLabel("Prebuilt gaming interfaces inspired by PlayStation, Xbox, Steam, and more")
        desc.setWordWrap(True)
        desc.setStyleSheet("color: #b0b0b0; font-size: 10pt; padding: 5px 0;")
        layout.addWidget(desc)
        
        # Scroll area for templates
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: #1e1e1e;
            }
        """)
        
        # Container for template grid
        container = QWidget()
        grid = QGridLayout(container)
        grid.setSpacing(15)
        
        # Create template previews in grid (2 columns)
        row = 0
        col = 0
        for template in self.templates:
            preview = TemplatePreview(template)
            preview.template_selected.connect(self.on_template_selected)
            grid.addWidget(preview, row, col)
            
            col += 1
            if col >= 2:  # 2 columns
                col = 0
                row += 1
        
        scroll.setWidget(container)
        layout.addWidget(scroll)
    
    def on_template_selected(self, template_data):
        """Handle template selection"""
        print(f"Loading template: {template_data['name']}")
        self.template_loaded.emit(template_data)
