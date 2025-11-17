"""
Startup guide dialog for first-time users.
Provides a friendly introduction to the Mac Health Analyzer app.
"""

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel,
    QWidget, QStackedWidget, QCheckBox
)
from ui.widgets import GlassmorphicPanel, StyledButton
from ui.styles import COLORS


class StartupGuide(QDialog):
    """
    Multi-step startup guide dialog for new users.
    """

    def __init__(self, parent=None):
        """
        Initialize startup guide.

        Args:
            parent: Parent widget
        """
        super().__init__(parent)
        self.current_step = 0
        self.dont_show_again = False

        self.setWindowTitle("Welcome to Mac Health Analyzer")
        self.setModal(True)
        self.setMinimumWidth(800)
        self.setMinimumHeight(700)

        # Apply styling
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
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)

        # Title
        title = QLabel("Welcome to Mac Health Analyzer! 👋")
        title.setProperty("heading", "h1")
        title.setStyleSheet(f"color: {COLORS['terracotta']};")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # Subtitle
        subtitle = QLabel("A friendly guide for non-tech-savvy users")
        subtitle.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 14px;")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(subtitle)

        # Stacked widget for different guide steps
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.addWidget(self._create_step_1())  # Overview
        self.stacked_widget.addWidget(self._create_step_2())  # Startup items
        self.stacked_widget.addWidget(self._create_step_3())  # Processes
        self.stacked_widget.addWidget(self._create_step_4())  # Tips & tricks
        layout.addWidget(self.stacked_widget, 1)

        # Step indicator
        self.step_indicator = QLabel("Step 1 of 4")
        self.step_indicator.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.step_indicator.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 12px;")
        layout.addWidget(self.step_indicator)

        # "Don't show again" checkbox
        self.dont_show_checkbox = QCheckBox("Don't show this guide again")
        self.dont_show_checkbox.setStyleSheet(f"""
            QCheckBox {{
                color: {COLORS['text_secondary']};
                font-size: 13px;
            }}
            QCheckBox::indicator {{
                width: 18px;
                height: 18px;
            }}
        """)
        self.dont_show_checkbox.stateChanged.connect(self._on_checkbox_changed)
        layout.addWidget(self.dont_show_checkbox)

        # Navigation buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()

        self.back_btn = StyledButton("Back", "secondary")
        self.back_btn.clicked.connect(self._on_back)
        self.back_btn.setEnabled(False)
        self.back_btn.setMinimumWidth(100)
        button_layout.addWidget(self.back_btn)

        self.next_btn = StyledButton("Next", "primary")
        self.next_btn.clicked.connect(self._on_next)
        self.next_btn.setMinimumWidth(100)
        button_layout.addWidget(self.next_btn)

        layout.addLayout(button_layout)

    def _create_step_1(self) -> QWidget:
        """Create step 1: Overview."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(16)

        panel = GlassmorphicPanel()
        panel_layout = QVBoxLayout(panel)
        panel_layout.setContentsMargins(30, 30, 30, 30)
        panel_layout.setSpacing(20)

        # Icon and title
        icon = QLabel("🖥️")
        icon.setStyleSheet("font-size: 64px;")
        icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        panel_layout.addWidget(icon)

        title = QLabel("What is Mac Health Analyzer?")
        title.setProperty("heading", "h2")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        panel_layout.addWidget(title)

        # Description
        description = QLabel(
            "Mac Health Analyzer helps you understand what's running on your Mac and "
            "keep it running smoothly. Think of it as a health checkup for your computer!\n\n"
            "This app shows you:\n"
            "• What programs start automatically when you log in\n"
            "• What programs are running right now\n"
            "• How much memory and CPU they're using\n"
            "• Recommendations to improve performance"
        )
        description.setWordWrap(True)
        description.setMinimumHeight(200)
        description.setStyleSheet(f"""
            color: {COLORS['text_primary']};
            font-size: 15px;
            line-height: 1.8;
            padding: 20px;
            background-color: {COLORS['bg_secondary']};
            border-left: 4px solid {COLORS['terracotta']};
        """)
        panel_layout.addWidget(description)

        layout.addWidget(panel)
        return widget

    def _create_step_2(self) -> QWidget:
        """Create step 2: Startup Items tab."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(16)

        panel = GlassmorphicPanel()
        panel_layout = QVBoxLayout(panel)
        panel_layout.setContentsMargins(30, 30, 30, 30)
        panel_layout.setSpacing(20)

        # Icon and title
        icon = QLabel("🚀")
        icon.setStyleSheet("font-size: 64px;")
        icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        panel_layout.addWidget(icon)

        title = QLabel("Startup Items Tab")
        title.setProperty("heading", "h2")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        panel_layout.addWidget(title)

        # Description
        description = QLabel(
            "The Startup Items tab shows programs that start automatically when you log in.\n\n"
            "✨ <b>Double-click any item</b> to see:\n"
            "• What it does (in plain English!)\n"
            "• Whether you should keep it enabled\n"
            "• Personalized recommendations\n\n"
            "<b>Tip:</b> Having too many startup items can slow down your Mac when you log in. "
            "Disable items you don't need to start automatically!"
        )
        description.setWordWrap(True)
        description.setTextFormat(Qt.TextFormat.RichText)
        description.setMinimumHeight(200)
        description.setStyleSheet(f"""
            color: {COLORS['text_primary']};
            font-size: 15px;
            line-height: 1.8;
            padding: 20px;
            background-color: {COLORS['bg_secondary']};
            border-left: 4px solid {COLORS['sage']};
        """)
        panel_layout.addWidget(description)

        layout.addWidget(panel)
        return widget

    def _create_step_3(self) -> QWidget:
        """Create step 3: Processes tab."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(16)

        panel = GlassmorphicPanel()
        panel_layout = QVBoxLayout(panel)
        panel_layout.setContentsMargins(30, 30, 30, 30)
        panel_layout.setSpacing(20)

        # Icon and title
        icon = QLabel("⚙️")
        icon.setStyleSheet("font-size: 64px;")
        icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        panel_layout.addWidget(icon)

        title = QLabel("Processes Tab")
        title.setProperty("heading", "h2")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        panel_layout.addWidget(title)

        # Description
        description = QLabel(
            "The Processes tab shows all programs currently running on your Mac.\n\n"
            "✨ <b>Double-click any process</b> to see:\n"
            "• What the program does\n"
            "• How long it's been running\n"
            "• How much memory and CPU it's using\n"
            "• <b>Smart recommendations</b> (e.g., \"This process has been running for a long time, "
            "consider closing it if you're not using it\")\n\n"
            "<b>Tip:</b> If your Mac feels slow, look for processes using a lot of memory or CPU!"
        )
        description.setWordWrap(True)
        description.setTextFormat(Qt.TextFormat.RichText)
        description.setMinimumHeight(200)
        description.setStyleSheet(f"""
            color: {COLORS['text_primary']};
            font-size: 15px;
            line-height: 1.8;
            padding: 20px;
            background-color: {COLORS['bg_secondary']};
            border-left: 4px solid {COLORS['mustard']};
        """)
        panel_layout.addWidget(description)

        layout.addWidget(panel)
        return widget

    def _create_step_4(self) -> QWidget:
        """Create step 4: Tips and tricks."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(16)

        panel = GlassmorphicPanel()
        panel_layout = QVBoxLayout(panel)
        panel_layout.setContentsMargins(30, 30, 30, 30)
        panel_layout.setSpacing(20)

        # Icon and title
        icon = QLabel("💡")
        icon.setStyleSheet("font-size: 64px;")
        icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        panel_layout.addWidget(icon)

        title = QLabel("Tips for Success")
        title.setProperty("heading", "h2")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        panel_layout.addWidget(title)

        # Tips
        tips = QLabel(
            "<b>🔒 Be Careful:</b> Don't disable system processes (especially Apple ones) "
            "unless you're sure about what they do.\n\n"
            "<b>⚡ Speed Up Your Mac:</b> Disable startup items you don't need and close "
            "apps you're not using.\n\n"
            "<b>🔄 Refresh Data:</b> Click the Refresh button to see the latest information.\n\n"
            "<b>📊 Monitor Resources:</b> Check the System tab to see overall CPU and memory usage.\n\n"
            "<b>❓ Need Help?</b> Use the Simple Explanations toggle in detail dialogs "
            "for easier-to-understand descriptions!"
        )
        tips.setWordWrap(True)
        tips.setTextFormat(Qt.TextFormat.RichText)
        tips.setMinimumHeight(200)
        tips.setStyleSheet(f"""
            color: {COLORS['text_primary']};
            font-size: 15px;
            line-height: 2.0;
            padding: 20px;
            background-color: {COLORS['bg_secondary']};
            border-left: 4px solid {COLORS['terracotta']};
        """)
        panel_layout.addWidget(tips)

        # Ready message
        ready = QLabel("You're all set! Click 'Finish' to start using Mac Health Analyzer.")
        ready.setAlignment(Qt.AlignmentFlag.AlignCenter)
        ready.setStyleSheet(f"color: {COLORS['sage']}; font-size: 13px; font-weight: bold; margin-top: 10px;")
        panel_layout.addWidget(ready)

        layout.addWidget(panel)
        return widget

    def _on_next(self):
        """Handle next button click."""
        if self.current_step < 3:
            self.current_step += 1
            self.stacked_widget.setCurrentIndex(self.current_step)
            self.step_indicator.setText(f"Step {self.current_step + 1} of 4")
            self.back_btn.setEnabled(True)

            # Change button text on last step
            if self.current_step == 3:
                self.next_btn.setText("Finish")
        else:
            # Finish - close the dialog
            self.accept()

    def _on_back(self):
        """Handle back button click."""
        if self.current_step > 0:
            self.current_step -= 1
            self.stacked_widget.setCurrentIndex(self.current_step)
            self.step_indicator.setText(f"Step {self.current_step + 1} of 4")

            # Disable back button on first step
            if self.current_step == 0:
                self.back_btn.setEnabled(False)

            # Reset next button text
            self.next_btn.setText("Next")

    def _on_checkbox_changed(self, state):
        """Handle checkbox state change."""
        self.dont_show_again = (state == Qt.CheckState.Checked.value)

    def should_show_again(self) -> bool:
        """
        Check if guide should be shown again.

        Returns:
            True if guide should be shown again, False otherwise
        """
        return not self.dont_show_again
