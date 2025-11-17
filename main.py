#!/usr/bin/env python3
"""
Mac Health Analyzer - Main Entry Point
A beautiful, powerful macOS system monitoring and startup management tool.
"""

import sys
import os
import json
from pathlib import Path
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon

# Import managers
from startup_manager import StartupManager
from process_monitor import ProcessMonitor

# Import UI components
from ui.dashboard import Dashboard
from ui.styles import get_main_stylesheet, get_palette
from ui.fonts import get_font_manager
from ui.startup_guide import StartupGuide


class MainWindow(QMainWindow):
    """
    Main application window.
    """

    def __init__(self):
        """Initialize main window."""
        super().__init__()

        # Initialize managers
        self.startup_manager = StartupManager()
        self.process_monitor = ProcessMonitor()

        # Set up window
        self.setup_window()

        # Load fonts
        self.load_fonts()

        # Apply styles
        self.apply_styles()

        # Create dashboard
        self.dashboard = Dashboard(self.startup_manager, self.process_monitor)
        self.setCentralWidget(self.dashboard)

    def setup_window(self):
        """Configure main window properties."""
        self.setWindowTitle("Mac Health Analyzer")
        self.setMinimumSize(1200, 800)
        self.resize(1400, 900)

        # Center window on screen
        self.center_on_screen()

    def center_on_screen(self):
        """Center the window on the screen."""
        screen = QApplication.primaryScreen().geometry()
        size = self.geometry()
        self.move(
            (screen.width() - size.width()) // 2, (screen.height() - size.height()) // 2
        )

    def load_fonts(self):
        """Load custom fonts."""
        try:
            font_manager = get_font_manager()
            font_manager.load_fonts()
        except Exception as e:
            print(f"Warning: Could not load custom fonts: {e}")
            print("Falling back to system fonts.")

    def apply_styles(self):
        """Apply application stylesheet and palette."""
        # Set palette
        self.setPalette(get_palette())

        # Set stylesheet
        self.setStyleSheet(get_main_stylesheet())

    def closeEvent(self, event):
        """Handle window close event."""
        # Clean up dashboard timers
        self.dashboard.cleanup()
        event.accept()

    def show_startup_guide_if_needed(self):
        """Show startup guide if it hasn't been shown before."""
        if not self._has_seen_guide():
            guide = StartupGuide(self)
            guide.exec()

            # Save preference if user checked "don't show again"
            if not guide.should_show_again():
                self._save_guide_preference()

    def _has_seen_guide(self) -> bool:
        """Check if user has already seen the startup guide."""
        config_path = self._get_config_path()
        if not config_path.exists():
            return False

        try:
            with open(config_path, "r") as f:
                config = json.load(f)
                return config.get("startup_guide_shown", False)
        except Exception:
            return False

    def _save_guide_preference(self):
        """Save that user has seen the guide."""
        config_path = self._get_config_path()

        # Create config directory if it doesn't exist
        config_path.parent.mkdir(parents=True, exist_ok=True)

        try:
            # Load existing config or create new one
            config = {}
            if config_path.exists():
                with open(config_path, "r") as f:
                    config = json.load(f)

            # Update config
            config["startup_guide_shown"] = True

            # Save config
            with open(config_path, "w") as f:
                json.dump(config, f, indent=2)
        except Exception as e:
            print(f"Warning: Could not save guide preference: {e}")

    def _get_config_path(self) -> Path:
        """Get path to config file."""
        # Use user's home directory
        home = Path.home()
        config_dir = home / ".mac-health-analyzer"
        return config_dir / "config.json"


def main():
    """Main application entry point."""
    # Enable high DPI scaling
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )

    # Create application
    app = QApplication(sys.argv)
    app.setApplicationName("Mac Health Analyzer")
    app.setOrganizationName("Mac Health Analyzer")

    # Set application-wide font
    try:
        from ui.fonts import get_font_manager

        font_manager = get_font_manager()
        default_font = font_manager.get_display_font(size=13, weight=300)
        app.setFont(default_font)
    except Exception as e:
        print(f"Could not set application font: {e}")

    # Create and show main window
    try:
        window = MainWindow()
        window.show()

        # Show startup guide for first-time users
        window.show_startup_guide_if_needed()

        sys.exit(app.exec())
    except Exception as e:
        print(f"Error starting application: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
