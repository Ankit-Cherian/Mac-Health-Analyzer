"""
Startup guide dialog for first-time users.
Provides a friendly introduction to the Mac Health Analyzer app.
"""

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QWidget,
    QStackedWidget,
    QCheckBox,
    QSizePolicy,
    QScrollArea,
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
        self.setStyleSheet(
            f"""
            QDialog {{
                background-color: {COLORS['bg_primary']};
                color: {COLORS['text_primary']};
            }}
        """
        )

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
        self.step_indicator.setStyleSheet(
            f"color: {COLORS['text_secondary']}; font-size: 12px;"
        )
        layout.addWidget(self.step_indicator)

        # "Don't show again" checkbox
        self.dont_show_checkbox = QCheckBox("Don't show this guide again")
        self.dont_show_checkbox.setStyleSheet(
            f"""
            QCheckBox {{
                color: {COLORS['text_secondary']};
                font-size: 13px;
            }}
            QCheckBox::indicator {{
                width: 18px;
                height: 18px;
            }}
        """
        )
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

    def _create_step_panel(
        self, icon_text: str, title_text: str, body_html: str, accent_color: str
    ) -> QWidget:
        """Create a reusable info panel used by each step."""
        panel = GlassmorphicPanel()
        panel_layout = QVBoxLayout(panel)
        panel_layout.setContentsMargins(24, 18, 24, 24)
        panel_layout.setSpacing(12)

        icon = QLabel(icon_text)
        icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon.setStyleSheet("font-size: 48px; margin-bottom: 4px;")
        panel_layout.addWidget(icon)

        title = QLabel(title_text)
        title.setProperty("heading", "h2")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setWordWrap(True)
        panel_layout.addWidget(title)

        body = QLabel(body_html)
        body.setWordWrap(True)
        body.setTextFormat(Qt.TextFormat.RichText)
        body.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        body.setStyleSheet(
            f"""
            color: {COLORS['text_primary']};
            font-size: 15px;
            line-height: 1.7;
            padding: 16px;
            background-color: {COLORS['bg_secondary']};
            border-left: 4px solid {accent_color};
        """
        )
        body.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        panel_layout.addWidget(body)
        panel_layout.addStretch()

        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setContentsMargins(0, 0, 0, 0)
        scroll_layout.addWidget(panel)
        scroll_layout.addStretch()

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.Shape.NoFrame)
        scroll.setWidget(scroll_content)

        wrapper = QWidget()
        wrapper_layout = QVBoxLayout(wrapper)
        wrapper_layout.setContentsMargins(0, 0, 0, 0)
        wrapper_layout.addWidget(scroll)
        return wrapper

    def _create_step_1(self) -> QWidget:
        """Create step 1: Overview."""
        description_html = (
            "<p>Mac Health Analyzer helps you understand what's running on your Mac and "
            "keep it running smoothly. Think of it as a health checkup for your computer!</p>"
            "<ul style='margin-left: 18px; padding-left: 6px;'>"
            "<li>See what programs start automatically when you log in.</li>"
            "<li>Watch the apps and processes currently running.</li>"
            "<li>Monitor how much memory and CPU they're using.</li>"
            "<li>Get simple recommendations to improve performance.</li>"
            "</ul>"
        )
        return self._create_step_panel(
            "🖥️", "What is Mac Health Analyzer?", description_html, COLORS["terracotta"]
        )

    def _create_step_2(self) -> QWidget:
        """Create step 2: Startup Items tab."""
        description_html = (
            "<p>The Startup Items tab shows programs that start automatically when you log in.</p>"
            "<p><b>Double-click any item</b> to quickly see:</p>"
            "<ul style='margin-left: 18px; padding-left: 6px;'>"
            "<li>What it does (in plain English).</li>"
            "<li>If you should keep it enabled.</li>"
            "<li>Friendly tips for speeding up your login.</li>"
            "</ul>"
            "<p><b>Tip:</b> Disable startup items you don't need to launch automatically.</p>"
        )
        return self._create_step_panel(
            "🚀", "Startup Items Tab", description_html, COLORS["sage"]
        )

    def _create_step_3(self) -> QWidget:
        """Create step 3: Processes tab."""
        description_html = (
            "<p>The Processes tab shows everything currently running on your Mac.</p>"
            "<p><b>Double-click a process</b> to learn:</p>"
            "<ul style='margin-left: 18px; padding-left: 6px;'>"
            "<li>What the program does and how long it's been active.</li>"
            "<li>How much memory and CPU it uses.</li>"
            "<li>Smart suggestions (like closing unused apps).</li>"
            "</ul>"
            "<p><b>Tip:</b> If your Mac feels slow, look for processes using lots of memory or CPU.</p>"
        )
        return self._create_step_panel(
            "⚙️", "Processes Tab", description_html, COLORS["mustard"]
        )

    def _create_step_4(self) -> QWidget:
        """Create step 4: Tips and tricks."""
        tips_html = (
            "<ul style='margin-left: 18px; padding-left: 6px;'>"
            "<li><b>🔒 Be Careful:</b> Avoid disabling Apple system processes unless you know what they do.</li>"
            "<li><b>⚡ Speed Up:</b> Disable startup items you don't need and close unused apps.</li>"
            "<li><b>🔄 Refresh:</b> Click the Refresh button for the latest data.</li>"
            "<li><b>📊 Monitor:</b> Use the System tab to keep an eye on CPU and memory.</li>"
            "<li><b>❓ Need Help?</b> Toggle Simple Explanations inside detail dialogs.</li>"
            "</ul>"
        )
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)

        panel = self._create_step_panel(
            "💡", "Tips for Success", tips_html, COLORS["terracotta"]
        )
        layout.addWidget(panel, alignment=Qt.AlignmentFlag.AlignTop)

        ready = QLabel(
            'You\'re all set! Click "Finish" to start using Mac Health Analyzer.'
        )
        ready.setAlignment(Qt.AlignmentFlag.AlignCenter)
        ready.setStyleSheet(
            f"color: {COLORS['sage']}; font-size: 13px; font-weight: bold;"
        )
        layout.addWidget(ready)
        layout.addStretch()
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
        self.dont_show_again = state == Qt.CheckState.Checked.value

    def should_show_again(self) -> bool:
        """
        Check if guide should be shown again.

        Returns:
            True if guide should be shown again, False otherwise
        """
        return not self.dont_show_again
