"""
UI Styling for Mac Health Analyzer.
Defines QStyleSheet with distinctive design: gradients, glassmorphism, custom typography.
"""

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QPalette


# Color Palette
COLORS = {
    # Backgrounds
    'bg_primary': '#0a0e1a',      # Deep slate
    'bg_secondary': '#1a1a2e',    # Dark purple-blue
    'bg_tertiary': '#16213e',     # Navy
    
    # Accents
    'accent_blue': '#00d9ff',     # Electric blue
    'accent_orange': '#ff6b35',   # Warm orange
    'accent_red': '#ff1744',      # Vibrant red
    
    # Text
    'text_primary': '#ffffff',    # White
    'text_secondary': '#b0b8c4',  # Light gray
    
    # Status colors
    'status_low': '#00d9ff',      # Blue - low resource usage
    'status_medium': '#ff6b35',   # Orange - medium resource usage
    'status_high': '#ff1744',     # Red - high resource usage
    
    # UI elements
    'border': '#2d3748',
    'hover': '#1e293b',
}


def get_main_stylesheet() -> str:
    """
    Get the main application stylesheet with distinctive design.
    
    Returns:
        QStyleSheet string
    """
    return f"""
    /* Main Application Window */
    QMainWindow {{
        background: qlineargradient(
            x1: 0, y1: 0, x2: 1, y2: 1,
            stop: 0 {COLORS['bg_primary']},
            stop: 0.5 {COLORS['bg_secondary']},
            stop: 1 {COLORS['bg_tertiary']}
        );
    }}
    
    /* Central Widget */
    QWidget {{
        background: transparent;
        color: {COLORS['text_primary']};
        font-family: "Bricolage Grotesque", "Helvetica Neue", sans-serif;
        font-size: 13px;
        font-weight: 300;
    }}
    
    /* Tab Widget */
    QTabWidget::pane {{
        border: none;
        background: transparent;
    }}
    
    QTabBar::tab {{
        background: rgba(26, 26, 46, 0.5);
        color: {COLORS['text_secondary']};
        padding: 16px 32px;
        margin-right: 4px;
        border: none;
        border-top-left-radius: 12px;
        border-top-right-radius: 12px;
        font-size: 15px;
        font-weight: 300;
    }}
    
    QTabBar::tab:selected {{
        background: rgba(0, 217, 255, 0.15);
        color: {COLORS['accent_blue']};
        font-weight: 700;
    }}
    
    QTabBar::tab:hover:!selected {{
        background: rgba(26, 26, 46, 0.8);
        color: {COLORS['text_primary']};
    }}
    
    /* Table Widget */
    QTableWidget {{
        background: rgba(22, 33, 62, 0.3);
        border: 1px solid {COLORS['border']};
        border-radius: 16px;
        gridline-color: {COLORS['border']};
        selection-background-color: {COLORS['accent_blue']};
        selection-color: {COLORS['bg_primary']};
        font-family: "JetBrains Mono", "Menlo", monospace;
        font-size: 12px;
        font-weight: 300;
    }}
    
    QTableWidget::item {{
        padding: 8px;
        border: none;
    }}
    
    QTableWidget::item:selected {{
        background: {COLORS['accent_blue']};
        color: {COLORS['bg_primary']};
    }}
    
    QTableWidget::item:hover {{
        background: rgba(0, 217, 255, 0.1);
    }}
    
    QHeaderView::section {{
        background: rgba(10, 14, 26, 0.8);
        color: {COLORS['text_primary']};
        padding: 12px 8px;
        border: none;
        border-bottom: 2px solid {COLORS['accent_blue']};
        font-size: 11px;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 1px;
    }}
    
    QHeaderView::section:hover {{
        background: rgba(0, 217, 255, 0.15);
    }}
    
    /* Scroll Bars */
    QScrollBar:vertical {{
        background: transparent;
        width: 12px;
        margin: 0px;
    }}
    
    QScrollBar::handle:vertical {{
        background: rgba(0, 217, 255, 0.3);
        border-radius: 6px;
        min-height: 30px;
    }}
    
    QScrollBar::handle:vertical:hover {{
        background: rgba(0, 217, 255, 0.5);
    }}
    
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
        height: 0px;
    }}
    
    QScrollBar:horizontal {{
        background: transparent;
        height: 12px;
        margin: 0px;
    }}
    
    QScrollBar::handle:horizontal {{
        background: rgba(0, 217, 255, 0.3);
        border-radius: 6px;
        min-width: 30px;
    }}
    
    QScrollBar::handle:horizontal:hover {{
        background: rgba(0, 217, 255, 0.5);
    }}
    
    QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
        width: 0px;
    }}
    
    /* Push Buttons */
    QPushButton {{
        background: qlineargradient(
            x1: 0, y1: 0, x2: 1, y2: 0,
            stop: 0 {COLORS['accent_blue']},
            stop: 1 rgba(0, 217, 255, 0.8)
        );
        color: {COLORS['bg_primary']};
        border: none;
        border-radius: 8px;
        padding: 12px 24px;
        font-size: 14px;
        font-weight: 700;
    }}
    
    QPushButton:hover {{
        background: qlineargradient(
            x1: 0, y1: 0, x2: 1, y2: 0,
            stop: 0 rgba(0, 217, 255, 1),
            stop: 1 rgba(0, 217, 255, 0.9)
        );
    }}
    
    QPushButton:pressed {{
        background: rgba(0, 217, 255, 0.6);
    }}
    
    QPushButton:disabled {{
        background: rgba(176, 184, 196, 0.2);
        color: {COLORS['text_secondary']};
    }}
    
    /* Danger Button */
    QPushButton[danger="true"] {{
        background: qlineargradient(
            x1: 0, y1: 0, x2: 1, y2: 0,
            stop: 0 {COLORS['accent_red']},
            stop: 1 rgba(255, 23, 68, 0.8)
        );
        color: {COLORS['text_primary']};
    }}
    
    QPushButton[danger="true"]:hover {{
        background: qlineargradient(
            x1: 0, y1: 0, x2: 1, y2: 0,
            stop: 0 rgba(255, 23, 68, 1),
            stop: 1 rgba(255, 23, 68, 0.9)
        );
    }}
    
    /* Line Edit (Search/Input) */
    QLineEdit {{
        background: rgba(22, 33, 62, 0.5);
        border: 1px solid {COLORS['border']};
        border-radius: 8px;
        padding: 10px 14px;
        color: {COLORS['text_primary']};
        font-size: 13px;
        font-weight: 300;
    }}
    
    QLineEdit:focus {{
        border: 1px solid {COLORS['accent_blue']};
        background: rgba(22, 33, 62, 0.8);
    }}
    
    /* Labels */
    QLabel {{
        color: {COLORS['text_primary']};
        background: transparent;
        font-weight: 300;
    }}
    
    QLabel[heading="h1"] {{
        font-size: 48px;
        font-weight: 800;
        color: {COLORS['text_primary']};
    }}
    
    QLabel[heading="h2"] {{
        font-size: 32px;
        font-weight: 700;
        color: {COLORS['text_primary']};
    }}
    
    QLabel[heading="h3"] {{
        font-size: 20px;
        font-weight: 700;
        color: {COLORS['accent_blue']};
    }}
    
    QLabel[mono="true"] {{
        font-family: "JetBrains Mono", "Menlo", monospace;
        font-weight: 300;
    }}
    
    /* Glassmorphic Panel */
    QFrame[panel="true"] {{
        background: rgba(22, 33, 62, 0.4);
        border: 1px solid rgba(0, 217, 255, 0.2);
        border-radius: 16px;
        padding: 20px;
    }}
    
    /* Status Indicators */
    QLabel[status="low"] {{
        color: {COLORS['status_low']};
        font-weight: 700;
    }}
    
    QLabel[status="medium"] {{
        color: {COLORS['status_medium']};
        font-weight: 700;
    }}
    
    QLabel[status="high"] {{
        color: {COLORS['status_high']};
        font-weight: 700;
    }}
    
    /* Checkboxes */
    QCheckBox {{
        color: {COLORS['text_primary']};
        spacing: 8px;
        font-size: 13px;
    }}
    
    QCheckBox::indicator {{
        width: 20px;
        height: 20px;
        border: 2px solid {COLORS['border']};
        border-radius: 6px;
        background: rgba(22, 33, 62, 0.5);
    }}
    
    QCheckBox::indicator:checked {{
        background: {COLORS['accent_blue']};
        border: 2px solid {COLORS['accent_blue']};
    }}
    
    QCheckBox::indicator:hover {{
        border: 2px solid {COLORS['accent_blue']};
    }}
    
    /* Combo Box */
    QComboBox {{
        background: rgba(22, 33, 62, 0.5);
        border: 1px solid {COLORS['border']};
        border-radius: 8px;
        padding: 10px 14px;
        color: {COLORS['text_primary']};
        font-size: 13px;
    }}
    
    QComboBox:hover {{
        border: 1px solid {COLORS['accent_blue']};
    }}
    
    QComboBox::drop-down {{
        border: none;
        width: 30px;
    }}
    
    QComboBox::down-arrow {{
        image: none;
        border-left: 5px solid transparent;
        border-right: 5px solid transparent;
        border-top: 5px solid {COLORS['text_primary']};
    }}
    
    QComboBox QAbstractItemView {{
        background: {COLORS['bg_secondary']};
        border: 1px solid {COLORS['accent_blue']};
        selection-background-color: {COLORS['accent_blue']};
        selection-color: {COLORS['bg_primary']};
    }}
    
    /* Message Box */
    QMessageBox {{
        background: {COLORS['bg_secondary']};
    }}
    
    QMessageBox QPushButton {{
        min-width: 80px;
    }}
    
    /* Progress Bar */
    QProgressBar {{
        background: rgba(22, 33, 62, 0.5);
        border: 1px solid {COLORS['border']};
        border-radius: 8px;
        text-align: center;
        color: {COLORS['text_primary']};
        font-weight: 700;
    }}
    
    QProgressBar::chunk {{
        background: qlineargradient(
            x1: 0, y1: 0, x2: 1, y2: 0,
            stop: 0 {COLORS['accent_blue']},
            stop: 1 {COLORS['accent_orange']}
        );
        border-radius: 7px;
    }}
    """


def get_status_color(percent: float) -> str:
    """
    Get status color based on percentage.
    
    Args:
        percent: Resource usage percentage
        
    Returns:
        Color hex code
    """
    if percent < 50:
        return COLORS['status_low']
    elif percent < 80:
        return COLORS['status_medium']
    else:
        return COLORS['status_high']


def get_palette() -> QPalette:
    """
    Get application color palette.
    
    Returns:
        QPalette object
    """
    palette = QPalette()
    
    # Window
    palette.setColor(QPalette.ColorRole.Window, QColor(COLORS['bg_primary']))
    palette.setColor(QPalette.ColorRole.WindowText, QColor(COLORS['text_primary']))
    
    # Base
    palette.setColor(QPalette.ColorRole.Base, QColor(COLORS['bg_secondary']))
    palette.setColor(QPalette.ColorRole.AlternateBase, QColor(COLORS['bg_tertiary']))
    
    # Text
    palette.setColor(QPalette.ColorRole.Text, QColor(COLORS['text_primary']))
    palette.setColor(QPalette.ColorRole.BrightText, QColor(COLORS['accent_blue']))
    
    # Button
    palette.setColor(QPalette.ColorRole.Button, QColor(COLORS['bg_secondary']))
    palette.setColor(QPalette.ColorRole.ButtonText, QColor(COLORS['text_primary']))
    
    # Highlight
    palette.setColor(QPalette.ColorRole.Highlight, QColor(COLORS['accent_blue']))
    palette.setColor(QPalette.ColorRole.HighlightedText, QColor(COLORS['bg_primary']))
    
    return palette

