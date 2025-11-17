"""
Startup item detail dialog showing friendly explanations and recommendations.
"""

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QScrollArea, QWidget, QFrame, QSizePolicy
)
from ui.widgets import GlassmorphicPanel, StatRow, ToggleSwitch, StyledButton
from ui.styles import COLORS
from utils.startup_descriptions import StartupDescriber


class StartupDetailDialog(QDialog):
    """
    Dialog showing detailed information about a startup item with user-friendly explanations.
    """

    def __init__(self, startup_data: dict, parent=None):
        """
        Initialize startup detail dialog.

        Args:
            startup_data: Dictionary containing startup item information
            parent: Parent widget
        """
        super().__init__(parent)
        self.startup_data = startup_data
        self.simple_mode = False  # Start with technical explanations

        self.setWindowTitle(f"Startup Item Details - {startup_data.get('name', 'Unknown')}")
        self.setModal(False)  # Allow interaction with main window
        self.setMinimumWidth(600)
        self.setMinimumHeight(500)

        # Apply the same styling as main window
        self.setStyleSheet(f"""
            QDialog {{
                background-color: {COLORS['bg_primary']};
                color: {COLORS['text_primary']};
            }}
        """)

        self.init_ui()

    def init_ui(self):
        """Initialize the user interface."""
        layout = QVBoxLayout(self)
        layout.setSpacing(16)
        layout.setContentsMargins(24, 24, 24, 24)

        # Header with item name
        header = self._create_header()
        layout.addWidget(header)

        # Explanation toggle
        toggle_section = self._create_toggle_section()
        layout.addLayout(toggle_section)

        # Scroll area for content
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setStyleSheet("""
            QScrollArea {
                background: transparent;
                border: none;
            }
        """)

        # Content widget
        content_widget = QWidget()
        self.content_layout = QVBoxLayout(content_widget)
        self.content_layout.setSpacing(16)

        # Add all content sections
        self._add_description_section()
        self._add_recommendation_section()
        self._add_item_info_section()

        scroll.setWidget(content_widget)
        layout.addWidget(scroll, 1)  # Stretch factor 1 to take remaining space

        # Close button
        close_button = StyledButton("Close", "primary")
        close_button.clicked.connect(self.accept)
        close_button.setMaximumWidth(120)
        layout.addWidget(close_button, alignment=Qt.AlignmentFlag.AlignRight)

    def _create_header(self) -> QWidget:
        """Create the header section with item name."""
        header_panel = GlassmorphicPanel()
        header_layout = QVBoxLayout(header_panel)
        header_layout.setContentsMargins(24, 20, 24, 20)

        # Item name
        name_label = QLabel(self.startup_data.get('name', 'Unknown Item'))
        name_label.setProperty("heading", "h1")
        name_label.setStyleSheet(f"color: {COLORS['terracotta']};")
        name_label.setWordWrap(True)
        name_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        header_layout.addWidget(name_label)

        # Type and status
        item_type = self.startup_data.get('type', 'Unknown')
        is_enabled = self.startup_data.get('enabled', False)
        status_text = "Enabled" if is_enabled else "Disabled"

        status_color = COLORS['sage'] if is_enabled else COLORS['text_secondary']
        info_label = QLabel(f"{item_type} • {status_text}")
        info_label.setProperty("mono", "true")
        info_label.setStyleSheet(f"color: {status_color}; font-size: 14px;")
        header_layout.addWidget(info_label)

        return header_panel

    def _create_toggle_section(self) -> QHBoxLayout:
        """Create the explanation mode toggle section."""
        toggle_layout = QHBoxLayout()

        # Label
        label = QLabel("Simple Explanations:")
        label.setProperty("mono", "true")
        toggle_layout.addWidget(label)

        # Toggle switch
        self.explanation_toggle = ToggleSwitch(initial_state=self.simple_mode)
        self.explanation_toggle.toggled.connect(self._on_explanation_mode_changed)
        toggle_layout.addWidget(self.explanation_toggle)

        # Help text
        help_text = QLabel("(Enable for non-technical explanations)")
        help_text.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 12px;")
        toggle_layout.addWidget(help_text)

        toggle_layout.addStretch()

        return toggle_layout

    def _add_description_section(self):
        """Add the item description section."""
        panel = GlassmorphicPanel()
        panel_layout = QVBoxLayout(panel)
        panel_layout.setContentsMargins(24, 20, 24, 20)
        panel_layout.setSpacing(12)

        # Title
        title = QLabel("WHAT IS THIS?")
        title.setProperty("heading", "h3")
        title.setStyleSheet(f"color: {COLORS['text_primary']};")
        panel_layout.addWidget(title)

        # Description label (will be updated based on toggle)
        self.description_label = QLabel()
        self.description_label.setWordWrap(True)
        self.description_label.setStyleSheet(f"""
            color: {COLORS['text_primary']};
            font-size: 14px;
            line-height: 1.6;
            padding: 12px;
            background-color: {COLORS['bg_secondary']};
            border-left: 4px solid {COLORS['terracotta']};
            border-radius: 0px;
        """)
        self._update_description()
        panel_layout.addWidget(self.description_label)

        # Add info badge if item is known
        item_name = self.startup_data.get('name', '')
        label_name = self.startup_data.get('label', '')

        # Check both name and label for recognition
        check_name = label_name if label_name else item_name

        if StartupDescriber.is_recognized(check_name):
            known_badge = QLabel("✓ Recognized Startup Item")
            known_badge.setStyleSheet(f"""
                color: {COLORS['sage']};
                font-size: 12px;
                font-weight: bold;
                padding: 4px 8px;
                background-color: rgba(0, 255, 0, 0.1);
                border-radius: 4px;
            """)
            panel_layout.addWidget(known_badge)
        else:
            unknown_badge = QLabel("? Custom or Third-Party Item")
            unknown_badge.setStyleSheet(f"""
                color: {COLORS['warning']};
                font-size: 12px;
                font-weight: bold;
                padding: 4px 8px;
                background-color: rgba(255, 136, 0, 0.1);
                border-radius: 4px;
            """)
            panel_layout.addWidget(unknown_badge)

        self.content_layout.addWidget(panel)

    def _add_recommendation_section(self):
        """Add the recommendation section."""
        panel = GlassmorphicPanel()
        panel_layout = QVBoxLayout(panel)
        panel_layout.setContentsMargins(24, 20, 24, 20)
        panel_layout.setSpacing(12)

        # Title
        title = QLabel("RECOMMENDATION")
        title.setProperty("heading", "h3")
        title.setStyleSheet(f"color: {COLORS['mustard']};")
        panel_layout.addWidget(title)

        # Get recommendation
        item_name = self.startup_data.get('name', '')
        label_name = self.startup_data.get('label', '')
        item_type = self.startup_data.get('type', 'Unknown')

        # Check both name and label for recognition
        check_name = label_name if label_name else item_name

        recommendation = StartupDescriber.get_recommendation(check_name, item_type)

        # Recommendation icon and text based on should_enable
        if recommendation['should_enable'] is True:
            icon = "✓"
            rec_color = COLORS['sage']
            rec_title = "Keep This Enabled"
        elif recommendation['should_enable'] is False:
            icon = "✗"
            rec_color = COLORS['critical']
            rec_title = "Safe to Disable"
        else:  # None - depends on user
            icon = "⚠"
            rec_color = COLORS['warning']
            rec_title = "Your Choice"

        # Recommendation header
        rec_header = QLabel(f"{icon} {rec_title}")
        rec_header.setStyleSheet(f"""
            color: {rec_color};
            font-size: 16px;
            font-weight: bold;
            padding: 8px;
        """)
        panel_layout.addWidget(rec_header)

        # Recommendation reason
        reason_label = QLabel(recommendation['reason'])
        reason_label.setWordWrap(True)
        reason_label.setStyleSheet(f"""
            color: {COLORS['text_primary']};
            font-size: 14px;
            line-height: 1.6;
            padding: 12px;
            background-color: {COLORS['bg_secondary']};
            border-left: 4px solid {rec_color};
            border-radius: 0px;
        """)
        panel_layout.addWidget(reason_label)

        self.content_layout.addWidget(panel)

    def _add_item_info_section(self):
        """Add basic item information section."""
        panel = GlassmorphicPanel()
        panel_layout = QVBoxLayout(panel)
        panel_layout.setContentsMargins(24, 20, 24, 20)
        panel_layout.setSpacing(8)

        # Title
        title = QLabel("ITEM INFORMATION")
        title.setProperty("heading", "h3")
        title.setStyleSheet(f"color: {COLORS['sage']};")
        panel_layout.addWidget(title)

        # Add separator
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setStyleSheet(f"background-color: {COLORS['border']};")
        panel_layout.addWidget(separator)

        # Type
        item_type = self.startup_data.get('type', 'Unknown')
        type_row = StatRow("Type:", item_type)
        panel_layout.addWidget(type_row)

        # Status
        is_enabled = self.startup_data.get('enabled', False)
        status_text = "Enabled (runs at startup)" if is_enabled else "Disabled (will not run)"
        status_row = StatRow("Status:", status_text)
        panel_layout.addWidget(status_row)

        # Label (for Launch Agents/Daemons)
        label = self.startup_data.get('label', '')
        if label:
            label_row = StatRow("Label:", label)
            panel_layout.addWidget(label_row)

        # Location
        location = self.startup_data.get('location', self.startup_data.get('path', 'N/A'))
        location_label = QLabel(location)
        location_label.setWordWrap(True)
        location_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        location_label.setProperty("mono", "true")
        location_label.setStyleSheet(f"""
            color: {COLORS['text_primary']};
            font-size: 12px;
            padding: 8px;
            background-color: rgba(0, 0, 0, 0.2);
            border-radius: 4px;
        """)

        location_title = QLabel("Location:")
        location_title.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 12px;")
        panel_layout.addWidget(location_title)
        panel_layout.addWidget(location_label)

        self.content_layout.addWidget(panel)

    def _update_description(self):
        """Update the description based on current mode."""
        item_name = self.startup_data.get('name', '')
        label_name = self.startup_data.get('label', '')

        # Check both name and label for recognition
        check_name = label_name if label_name else item_name

        description = StartupDescriber.get_description(check_name, technical=not self.simple_mode)
        self.description_label.setText(description)

    def _on_explanation_mode_changed(self, is_simple: bool):
        """Handle explanation mode toggle."""
        self.simple_mode = is_simple
        self._update_description()
