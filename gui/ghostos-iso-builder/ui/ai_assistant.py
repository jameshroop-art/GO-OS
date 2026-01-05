#!/usr/bin/env python3
"""
AI Assistant Widget - Smart suggestions and predictive features
"""

import json
from datetime import datetime
from pathlib import Path
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                              QPushButton, QListWidget, QListWidgetItem,
                              QGroupBox, QTextEdit, QLineEdit, QComboBox,
                              QMessageBox, QCheckBox)
from PyQt6.QtCore import Qt, pyqtSignal, QTimer
from PyQt6.QtGui import QFont


class AIAssistantWidget(QWidget):
    """Widget providing AI-powered suggestions and workflow assistance"""
    
    suggestion_applied = pyqtSignal(dict)
    
    def __init__(self):
        super().__init__()
        self.usage_history = []
        self.common_workflows = []
        self.recent_actions = []
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the AI assistant interface"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Header
        header_label = QLabel("🤖 AI-Powered Assistant")
        header_font = QFont()
        header_font.setPointSize(14)
        header_font.setBold(True)
        header_label.setFont(header_font)
        layout.addWidget(header_label)
        
        info_label = QLabel("Smart suggestions based on your usage patterns")
        info_label.setStyleSheet("color: #888888; font-size: 10pt;")
        layout.addWidget(info_label)
        
        layout.addSpacing(10)
        
        # Smart suggestions
        suggestions_group = QGroupBox("💡 Smart Suggestions")
        suggestions_layout = QVBoxLayout(suggestions_group)
        
        self.suggestions_list = QListWidget()
        self.suggestions_list.setMaximumHeight(150)
        self.suggestions_list.itemDoubleClicked.connect(self.apply_suggestion)
        suggestions_layout.addWidget(self.suggestions_list)
        
        # Populate initial suggestions
        self.populate_suggestions()
        
        suggestion_buttons = QHBoxLayout()
        
        apply_btn = QPushButton("✓ Apply Suggestion")
        apply_btn.clicked.connect(self.apply_selected_suggestion)
        suggestion_buttons.addWidget(apply_btn)
        
        dismiss_btn = QPushButton("✗ Dismiss")
        dismiss_btn.clicked.connect(self.dismiss_suggestion)
        suggestion_buttons.addWidget(dismiss_btn)
        
        suggestions_layout.addLayout(suggestion_buttons)
        layout.addWidget(suggestions_group)
        
        # Quick actions
        quick_group = QGroupBox("⚡ Quick Actions")
        quick_layout = QVBoxLayout(quick_group)
        
        quick_info = QLabel("Frequently used operations:")
        quick_layout.addWidget(quick_info)
        
        self.quick_actions_list = QListWidget()
        self.quick_actions_list.setMaximumHeight(120)
        self.quick_actions_list.itemDoubleClicked.connect(self.execute_quick_action)
        quick_layout.addWidget(self.quick_actions_list)
        
        # Add default quick actions
        default_actions = [
            "Load Gaming Theme + Steam Integration",
            "Production Mode + Development Tools",
            "Minimal Build (Base System Only)",
            "Full Install (All Components)",
            "Apply Last Configuration"
        ]
        for action in default_actions:
            self.quick_actions_list.addItem(f"⚡ {action}")
        
        layout.addWidget(quick_group)
        
        # Context-aware help
        help_group = QGroupBox("❓ Context-Aware Help")
        help_layout = QVBoxLayout(help_group)
        
        self.context_help = QTextEdit()
        self.context_help.setReadOnly(True)
        self.context_help.setMaximumHeight(100)
        self.context_help.setPlainText(
            "Based on your current activity:\n\n"
            "• To add Windows app support, go to Wine Manager tab\n"
            "• To customize themes, use Theme Editor\n"
            "• To manage security, check Security Whitelist"
        )
        help_layout.addWidget(self.context_help)
        
        layout.addWidget(help_group)
        
        # Workflow memory
        workflow_group = QGroupBox("🧠 Workflow Memory")
        workflow_layout = QVBoxLayout(workflow_group)
        
        workflow_info = QLabel("Saved common operations:")
        workflow_layout.addWidget(workflow_info)
        
        self.workflows_list = QListWidget()
        self.workflows_list.setMaximumHeight(100)
        workflow_layout.addWidget(self.workflows_list)
        
        workflow_buttons = QHBoxLayout()
        
        save_workflow_btn = QPushButton("💾 Save Current Workflow")
        save_workflow_btn.clicked.connect(self.save_current_workflow)
        workflow_buttons.addWidget(save_workflow_btn)
        
        load_workflow_btn = QPushButton("📂 Load Workflow")
        load_workflow_btn.clicked.connect(self.load_workflow)
        workflow_buttons.addWidget(load_workflow_btn)
        
        workflow_layout.addLayout(workflow_buttons)
        layout.addWidget(workflow_group)
        
        # Auto-completion
        autocomplete_group = QGroupBox("✏️ Smart Auto-Complete")
        autocomplete_layout = QVBoxLayout(autocomplete_group)
        
        self.enable_autocomplete = QCheckBox("Enable smart path and command completion")
        self.enable_autocomplete.setChecked(True)
        autocomplete_layout.addWidget(self.enable_autocomplete)
        
        self.enable_predictions = QCheckBox("Enable predictive component selection")
        self.enable_predictions.setChecked(True)
        autocomplete_layout.addWidget(self.enable_predictions)
        
        self.enable_recommendations = QCheckBox("Show recommended integrations based on components")
        self.enable_recommendations.setChecked(True)
        autocomplete_layout.addWidget(self.enable_recommendations)
        
        layout.addWidget(autocomplete_group)
        
        layout.addStretch()
        
    def populate_suggestions(self):
        """Populate smart suggestions based on context"""
        suggestions = [
            {
                'title': 'Gaming Setup Detected',
                'description': 'Add Steam and gaming tools? Includes Wine, Lutris, GPU drivers',
                'action': 'gaming_setup'
            },
            {
                'title': 'Development Environment',
                'description': 'Add common dev tools? Includes Git, VS Code, Docker, Python',
                'action': 'dev_setup'
            },
            {
                'title': 'Security Enhancement',
                'description': 'Enable additional security tools? AppArmor profiles + Firewall rules',
                'action': 'security_enhance'
            },
            {
                'title': 'Optimize for Size',
                'description': 'Reduce ISO size by excluding optional components',
                'action': 'optimize_size'
            },
            {
                'title': 'Add Recovery Tools',
                'description': 'Include disk recovery and system repair utilities',
                'action': 'recovery_tools'
            }
        ]
        
        for suggestion in suggestions:
            item_text = f"💡 {suggestion['title']}\n   {suggestion['description']}"
            item = QListWidgetItem(item_text)
            item.setData(Qt.ItemDataRole.UserRole, suggestion)
            self.suggestions_list.addItem(item)
            
    def apply_selected_suggestion(self):
        """Apply currently selected suggestion"""
        current_item = self.suggestions_list.currentItem()
        if current_item:
            self.apply_suggestion(current_item)
            
    def apply_suggestion(self, item):
        """Apply a suggestion"""
        suggestion = item.data(Qt.ItemDataRole.UserRole)
        
        QMessageBox.information(
            self,
            "Suggestion Applied",
            f"Applied: {suggestion['title']}\n\n"
            f"{suggestion['description']}\n\n"
            "Components will be added to your build configuration."
        )
        
        self.suggestion_applied.emit(suggestion)
        
        # Remove applied suggestion
        self.suggestions_list.takeItem(self.suggestions_list.row(item))
        
        # Add to recent actions
        self.recent_actions.append({
            'timestamp': datetime.now().isoformat(),
            'action': suggestion['action'],
            'title': suggestion['title']
        })
        
    def dismiss_suggestion(self):
        """Dismiss current suggestion"""
        current_item = self.suggestions_list.currentItem()
        if current_item:
            self.suggestions_list.takeItem(self.suggestions_list.row(current_item))
            
    def execute_quick_action(self, item):
        """Execute quick action"""
        action_text = item.text()
        
        QMessageBox.information(
            self,
            "Quick Action",
            f"Executing: {action_text}\n\n"
            "This would apply the pre-configured settings for this action."
        )
        
    def save_current_workflow(self):
        """Save current workflow"""
        workflow_name = f"Workflow_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        workflow = {
            'name': workflow_name,
            'timestamp': datetime.now().isoformat(),
            'actions': self.recent_actions.copy()
        }
        
        self.common_workflows.append(workflow)
        
        item = QListWidgetItem(f"📋 {workflow_name}")
        item.setData(Qt.ItemDataRole.UserRole, workflow)
        self.workflows_list.addItem(item)
        
        QMessageBox.information(
            self,
            "Workflow Saved",
            f"Saved workflow: {workflow_name}\n\n"
            f"Captured {len(self.recent_actions)} actions."
        )
        
    def load_workflow(self):
        """Load saved workflow"""
        current_item = self.workflows_list.currentItem()
        if current_item:
            workflow = current_item.data(Qt.ItemDataRole.UserRole)
            
            QMessageBox.information(
                self,
                "Load Workflow",
                f"Would load workflow: {workflow['name']}\n\n"
                f"Actions: {len(workflow['actions'])}\n"
                f"Created: {workflow['timestamp']}"
            )
            
    def update_context_help(self, context):
        """Update context-aware help based on current activity"""
        help_texts = {
            'iso_loader': (
                "ISO Loading Tips:\n\n"
                "• Use 'Load from USB' for drives\n"
                "• Add multiple ISOs to combine components\n"
                "• Select 'Minimal' for smaller builds"
            ),
            'theme_editor': (
                "Theme Customization Tips:\n\n"
                "• Gaming mode adapts to running games\n"
                "• Production mode reduces eye strain\n"
                "• Text scaling affects all UI elements"
            ),
            'wine_manager': (
                "Wine Integration Tips:\n\n"
                "• Each app gets isolated prefix\n"
                "• Use 'Balanced' security for most apps\n"
                "• Gaming profile relaxes network restrictions"
            ),
            'security': (
                "Security Management Tips:\n\n"
                "• Temporary rules auto-expire\n"
                "• Gaming mode opens multiplayer ports\n"
                "• Always test in VM before deploying"
            )
        }
        
        if context in help_texts:
            self.context_help.setPlainText(help_texts[context])
            
    def add_recent_action(self, action_type, description):
        """Add action to recent history"""
        self.recent_actions.append({
            'timestamp': datetime.now().isoformat(),
            'type': action_type,
            'description': description
        })
        
        # Keep only last 50 actions
        if len(self.recent_actions) > 50:
            self.recent_actions = self.recent_actions[-50:]
            
    def get_component_recommendations(self, selected_components):
        """Get recommendations based on selected components"""
        recommendations = []
        
        # Check for gaming components
        gaming_keywords = ['steam', 'lutris', 'wine', 'gpu', 'driver']
        if any(keyword in str(selected_components).lower() for keyword in gaming_keywords):
            recommendations.append({
                'title': 'Gaming Tools Bundle',
                'components': ['Discord', 'OBS Studio', 'GameMode', 'MangoHud']
            })
            
        # Check for development tools
        dev_keywords = ['python', 'nodejs', 'git', 'gcc', 'compiler']
        if any(keyword in str(selected_components).lower() for keyword in dev_keywords):
            recommendations.append({
                'title': 'Development Essentials',
                'components': ['Docker', 'Postman', 'Database Tools', 'REST Client']
            })
            
        # Check for productivity
        office_keywords = ['libreoffice', 'gimp', 'inkscape']
        if any(keyword in str(selected_components).lower() for keyword in office_keywords):
            recommendations.append({
                'title': 'Productivity Suite',
                'components': ['Thunderbird', 'Calendar', 'PDF Tools', 'Scanner Support']
            })
            
        return recommendations
        
    def get_path_completion_suggestions(self, partial_path):
        """Get smart path completion suggestions"""
        common_paths = [
            '/opt/custom',
            '/usr/local/bin',
            '/home/username/Documents',
            '/home/username/Downloads',
            '/etc/apt/sources.list.d',
            '/var/log',
            '~/.config',
            '~/.local/share'
        ]
        
        if partial_path:
            suggestions = [p for p in common_paths if p.startswith(partial_path)]
        else:
            suggestions = common_paths[:5]
            
        return suggestions
        
    def predict_next_action(self, current_state):
        """Predict user's next likely action"""
        predictions = []
        
        # Based on usage patterns
        if current_state.get('iso_loaded') and not current_state.get('components_selected'):
            predictions.append("Select components from loaded ISO")
            
        if current_state.get('components_selected') and not current_state.get('theme_configured'):
            predictions.append("Configure theme settings")
            
        if current_state.get('theme_configured') and not current_state.get('security_reviewed'):
            predictions.append("Review security settings")
            
        if current_state.get('everything_configured'):
            predictions.append("Build ISO")
            
        return predictions
