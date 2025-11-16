#!/usr/bin/env python3
"""
Mac Health Analyzer - Main Entry Point
A beautiful, powerful macOS system monitoring and startup management tool.
"""

import sys
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
            (screen.width() - size.width()) // 2,
            (screen.height() - size.height()) // 2
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
        
        # Show welcome message
        QMessageBox.information(
            window,
            "Welcome to Mac Health Analyzer",
            "This tool helps you monitor and manage your Mac's startup items and running processes.\n\n"
            "⚡ Startup Items: View and disable startup applications\n"
            "📊 Running Processes: Monitor and manage active processes\n"
            "🖥️ System Overview: See overall system health\n\n"
            "Note: Some operations may require administrator privileges."
        )
        
        sys.exit(app.exec())
    except Exception as e:
        print(f"Error starting application: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

