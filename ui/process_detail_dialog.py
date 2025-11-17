"""
Process detail dialog showing friendly explanations and detailed information.
"""

from datetime import datetime
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QScrollArea, QWidget, QFrame
)
from ui.widgets import GlassmorphicPanel, StatRow, ToggleSwitch, StyledButton
from ui.styles import COLORS
from utils.process_descriptions import ProcessDescriber


class ProcessDetailDialog(QDialog):
    """
    Dialog showing detailed information about a process with user-friendly explanations.
    """

    def __init__(self, process_data: dict, parent=None):
        """
        Initialize process detail dialog.

        Args:
            process_data: Dictionary containing process information
            parent: Parent widget
        """
        super().__init__(parent)
        self.process_data = process_data
        self.simple_mode = False  # Start with technical explanations

        self.setWindowTitle(f"Process Details - {process_data.get('name', 'Unknown')}")
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

        # Header with process name
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
        self._add_process_info_section()
        self._add_resource_usage_section()
        self._add_command_line_section()

        scroll.setWidget(content_widget)
        layout.addWidget(scroll, 1)  # Stretch factor 1 to take remaining space

        # Close button
        close_button = StyledButton("Close", "primary")
        close_button.clicked.connect(self.accept)
        close_button.setMaximumWidth(120)
        layout.addWidget(close_button, alignment=Qt.AlignmentFlag.AlignRight)

    def _create_header(self) -> QWidget:
        """Create the header section with process name and icon."""
        header_panel = GlassmorphicPanel()
        header_layout = QVBoxLayout(header_panel)
        header_layout.setContentsMargins(24, 20, 24, 20)

        # Process name
        name_label = QLabel(self.process_data.get('name', 'Unknown Process'))
        name_label.setProperty("heading", "h1")
        name_label.setStyleSheet(f"color: {COLORS['terracotta']};")
        header_layout.addWidget(name_label)

        # PID
        pid_label = QLabel(f"PID: {self.process_data.get('pid', 'N/A')}")
        pid_label.setProperty("mono", "true")
        pid_label.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 14px;")
        header_layout.addWidget(pid_label)

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
        """Add the process description section."""
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

        # Add info badge if process is known
        process_name = self.process_data.get('name', '')
        if ProcessDescriber.is_known_process(process_name):
            known_badge = QLabel("✓ Recognized Process")
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
            unknown_badge = QLabel("? Custom or System Process")
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

    def _add_process_info_section(self):
        """Add basic process information section."""
        panel = GlassmorphicPanel()
        panel_layout = QVBoxLayout(panel)
        panel_layout.setContentsMargins(24, 20, 24, 20)
        panel_layout.setSpacing(8)

        # Title
        title = QLabel("PROCESS INFORMATION")
        title.setProperty("heading", "h3")
        title.setStyleSheet(f"color: {COLORS['sage']};")
        panel_layout.addWidget(title)

        # Add separator
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setStyleSheet(f"background-color: {COLORS['border']};")
        panel_layout.addWidget(separator)

        # Status
        status = self.process_data.get('status', 'unknown')
        status_row = StatRow("Status:", status.capitalize())
        panel_layout.addWidget(status_row)

        # Username
        username = self.process_data.get('username', 'N/A')
        user_row = StatRow("User:", username)
        panel_layout.addWidget(user_row)

        # Create time
        create_time = self.process_data.get('create_time')
        if create_time:
            create_dt = datetime.fromtimestamp(create_time)
            create_str = create_dt.strftime("%Y-%m-%d %H:%M:%S")
            uptime_seconds = (datetime.now() - create_dt).total_seconds()
            uptime_str = self._format_uptime(uptime_seconds)
            time_row = StatRow("Started:", f"{create_str} ({uptime_str} ago)")
        else:
            time_row = StatRow("Started:", "N/A")
        panel_layout.addWidget(time_row)

        # Number of threads
        num_threads = self.process_data.get('num_threads', 'N/A')
        threads_row = StatRow("Threads:", str(num_threads))
        panel_layout.addWidget(threads_row)

        self.content_layout.addWidget(panel)

    def _add_resource_usage_section(self):
        """Add resource usage section."""
        panel = GlassmorphicPanel()
        panel_layout = QVBoxLayout(panel)
        panel_layout.setContentsMargins(24, 20, 24, 20)
        panel_layout.setSpacing(8)

        # Title
        title = QLabel("RESOURCE USAGE")
        title.setProperty("heading", "h3")
        title.setStyleSheet(f"color: {COLORS['sage']};")
        panel_layout.addWidget(title)

        # Add separator
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setStyleSheet(f"background-color: {COLORS['border']};")
        panel_layout.addWidget(separator)

        # CPU
        cpu = self.process_data.get('cpu_percent', 0)
        cpu_row = StatRow("CPU Usage:", f"{cpu:.1f}%")
        panel_layout.addWidget(cpu_row)

        # Memory
        memory_info = self.process_data.get('memory_info')
        if memory_info:
            mem_mb = memory_info.rss / (1024 * 1024)
            mem_row = StatRow("Memory:", f"{mem_mb:.1f} MB")
        else:
            mem_mb = self.process_data.get('memory_mb', 0)
            mem_row = StatRow("Memory:", f"{mem_mb:.1f} MB")
        panel_layout.addWidget(mem_row)

        # Memory percent
        mem_percent = self.process_data.get('memory_percent', 0)
        mem_pct_row = StatRow("Memory %:", f"{mem_percent:.2f}%")
        panel_layout.addWidget(mem_pct_row)

        self.content_layout.addWidget(panel)

    def _add_command_line_section(self):
        """Add command line section."""
        cmdline = self.process_data.get('cmdline', '').strip()

        if not cmdline:
            return  # Don't show section if no command line

        panel = GlassmorphicPanel()
        panel_layout = QVBoxLayout(panel)
        panel_layout.setContentsMargins(24, 20, 24, 20)
        panel_layout.setSpacing(12)

        # Title
        title = QLabel("COMMAND LINE")
        title.setProperty("heading", "h3")
        title.setStyleSheet(f"color: {COLORS['sage']};")
        panel_layout.addWidget(title)

        # Add separator
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setStyleSheet(f"background-color: {COLORS['border']};")
        panel_layout.addWidget(separator)

        # Command line text
        cmd_label = QLabel(cmdline)
        cmd_label.setWordWrap(True)
        cmd_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        cmd_label.setProperty("mono", "true")
        cmd_label.setStyleSheet(f"""
            color: {COLORS['text_primary']};
            font-size: 12px;
            padding: 12px;
            background-color: rgba(0, 0, 0, 0.3);
            border: 1px solid {COLORS['border']};
            border-radius: 4px;
        """)
        panel_layout.addWidget(cmd_label)

        # Help text
        help_text = QLabel("This is the full command used to start this process.")
        help_text.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 11px; font-style: italic;")
        panel_layout.addWidget(help_text)

        self.content_layout.addWidget(panel)

    def _update_description(self):
        """Update the description based on current mode."""
        process_name = self.process_data.get('name', 'Unknown')
        description = ProcessDescriber.get_description(process_name, simple=self.simple_mode)
        self.description_label.setText(description)

    def _on_explanation_mode_changed(self, is_simple: bool):
        """Handle explanation mode toggle."""
        self.simple_mode = is_simple
        self._update_description()

    def _format_uptime(self, seconds: float) -> str:
        """Format uptime in human-readable format."""
        if seconds < 60:
            return f"{int(seconds)}s"
        elif seconds < 3600:
            minutes = int(seconds / 60)
            return f"{minutes}m"
        elif seconds < 86400:
            hours = int(seconds / 3600)
            return f"{hours}h"
        else:
            days = int(seconds / 86400)
            hours = int((seconds % 86400) / 3600)
            return f"{days}d {hours}h"
