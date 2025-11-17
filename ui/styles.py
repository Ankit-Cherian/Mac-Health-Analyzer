"""
UI Styling for Mac Health Analyzer - Neon Terminal Edition.
Cyberpunk-inspired design with electric accents, terminal aesthetics, and futuristic vibes.
"""

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QPalette


# Neon Terminal Color Palette
COLORS = {
    # Backgrounds - Deep blacks with purple/blue tints
    'bg_primary': '#0a0a0f',      # Almost black
    'bg_secondary': '#12121a',    # Dark purple-black
    'bg_tertiary': '#1a1a2e',     # Deep navy-purple
    'bg_card': '#15151f',         # Card background

    # Neon Accents - Vibrant electric colors
    'neon_green': '#00ff41',      # Matrix green (primary)
    'neon_pink': '#ff006e',       # Hot magenta (secondary)
    'neon_cyan': '#00f5ff',       # Electric cyan
    'neon_amber': '#ffbe0b',      # Warning amber
    'neon_purple': '#bf00ff',     # Electric purple

    # Gradients
    'gradient_start': '#00ff41',   # Green
    'gradient_mid': '#00f5ff',     # Cyan
    'gradient_end': '#bf00ff',     # Purple

    # Text
    'text_primary': '#e0e0e0',    # Off-white (easier on eyes)
    'text_secondary': '#8a8a9e',  # Muted purple-gray
    'text_glow': '#00ff41',       # Glowing green text

    # Status colors
    'status_low': '#00ff41',      # Neon green - optimal
    'status_medium': '#ffbe0b',   # Amber - warning
    'status_high': '#ff006e',     # Hot pink - critical

    # UI elements
    'border': '#2a2a3e',
    'border_glow': '#00ff41',
    'hover': '#1e1e2e',
    'shadow': '#000000',
}


def get_main_stylesheet() -> str:
    """
    Get the main application stylesheet with cyberpunk terminal design.

    Returns:
        QStyleSheet string
    """
    return f"""
    /* Main Application Window - Dark terminal background */
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
        font-family: "Chakra Petch", "Rajdhani", "Helvetica Neue", sans-serif;
        font-size: 14px;
        font-weight: 400;
    }}

    /* Tab Widget - Futuristic tabs with glow effect */
    QTabWidget::pane {{
        border: none;
        background: transparent;
    }}

    QTabBar::tab {{
        background: rgba(18, 18, 26, 0.6);
        color: {COLORS['text_secondary']};
        padding: 18px 40px;
        margin-right: 2px;
        border: none;
        border-top: 2px solid transparent;
        font-size: 16px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 2px;
    }}

    QTabBar::tab:selected {{
        background: qlineargradient(
            x1: 0, y1: 0, x2: 0, y2: 1,
            stop: 0 rgba(0, 255, 65, 0.2),
            stop: 1 rgba(0, 255, 65, 0.05)
        );
        color: {COLORS['neon_green']};
        font-weight: 700;
        border-top: 2px solid {COLORS['neon_green']};
    }}

    QTabBar::tab:hover:!selected {{
        background: rgba(26, 26, 46, 0.8);
        color: {COLORS['neon_cyan']};
        border-top: 2px solid {COLORS['neon_cyan']};
    }}

    /* Table Widget - Terminal-style data display */
    QTableWidget {{
        background: rgba(21, 21, 31, 0.4);
        border: 1px solid {COLORS['border']};
        border-radius: 12px;
        gridline-color: rgba(0, 255, 65, 0.1);
        selection-background-color: {COLORS['neon_green']};
        selection-color: {COLORS['bg_primary']};
        font-family: "JetBrains Mono", "Fira Code", "Menlo", monospace;
        font-size: 13px;
        font-weight: 400;
    }}

    QTableWidget::item {{
        padding: 10px;
        border: none;
        color: {COLORS['text_primary']};
    }}

    QTableWidget::item:selected {{
        background: {COLORS['neon_green']};
        color: {COLORS['bg_primary']};
        font-weight: 600;
    }}

    QTableWidget::item:hover {{
        background: rgba(0, 255, 65, 0.15);
        color: {COLORS['neon_green']};
    }}

    QHeaderView::section {{
        background: qlineargradient(
            x1: 0, y1: 0, x2: 1, y2: 0,
            stop: 0 rgba(0, 255, 65, 0.3),
            stop: 0.5 rgba(0, 245, 255, 0.3),
            stop: 1 rgba(191, 0, 255, 0.3)
        );
        color: {COLORS['text_primary']};
        padding: 14px 10px;
        border: none;
        border-bottom: 2px solid {COLORS['neon_green']};
        font-size: 11px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 2px;
    }}

    QHeaderView::section:hover {{
        background: rgba(0, 255, 65, 0.4);
        color: {COLORS['neon_green']};
    }}

    /* Scroll Bars - Glowing neon style */
    QScrollBar:vertical {{
        background: rgba(18, 18, 26, 0.5);
        width: 10px;
        margin: 0px;
        border-radius: 5px;
    }}

    QScrollBar::handle:vertical {{
        background: qlineargradient(
            x1: 0, y1: 0, x2: 0, y2: 1,
            stop: 0 {COLORS['neon_green']},
            stop: 1 {COLORS['neon_cyan']}
        );
        border-radius: 5px;
        min-height: 30px;
    }}

    QScrollBar::handle:vertical:hover {{
        background: {COLORS['neon_green']};
    }}

    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
        height: 0px;
    }}

    QScrollBar:horizontal {{
        background: rgba(18, 18, 26, 0.5);
        height: 10px;
        margin: 0px;
        border-radius: 5px;
    }}

    QScrollBar::handle:horizontal {{
        background: qlineargradient(
            x1: 0, y1: 0, x2: 1, y2: 0,
            stop: 0 {COLORS['neon_green']},
            stop: 1 {COLORS['neon_cyan']}
        );
        border-radius: 5px;
        min-width: 30px;
    }}

    QScrollBar::handle:horizontal:hover {{
        background: {COLORS['neon_green']};
    }}

    QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
        width: 0px;
    }}

    /* Push Buttons - Neon glow effect */
    QPushButton {{
        background: qlineargradient(
            x1: 0, y1: 0, x2: 1, y2: 0,
            stop: 0 rgba(0, 255, 65, 0.8),
            stop: 1 rgba(0, 245, 255, 0.8)
        );
        color: {COLORS['bg_primary']};
        border: 2px solid {COLORS['neon_green']};
        border-radius: 6px;
        padding: 14px 28px;
        font-size: 14px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1px;
    }}

    QPushButton:hover {{
        background: {COLORS['neon_green']};
        border: 2px solid {COLORS['neon_cyan']};
    }}

    QPushButton:pressed {{
        background: rgba(0, 255, 65, 0.6);
    }}

    QPushButton:disabled {{
        background: rgba(138, 138, 158, 0.2);
        color: {COLORS['text_secondary']};
        border: 2px solid {COLORS['border']};
    }}

    /* Danger Button - Hot pink accent */
    QPushButton[danger="true"] {{
        background: qlineargradient(
            x1: 0, y1: 0, x2: 1, y2: 0,
            stop: 0 rgba(255, 0, 110, 0.8),
            stop: 1 rgba(255, 190, 11, 0.8)
        );
        color: {COLORS['text_primary']};
        border: 2px solid {COLORS['neon_pink']};
    }}

    QPushButton[danger="true"]:hover {{
        background: {COLORS['neon_pink']};
        border: 2px solid {COLORS['neon_amber']};
    }}

    /* Line Edit (Search/Input) - Terminal input style */
    QLineEdit {{
        background: rgba(21, 21, 31, 0.6);
        border: 2px solid {COLORS['border']};
        border-radius: 8px;
        padding: 12px 16px;
        color: {COLORS['text_primary']};
        font-size: 14px;
        font-weight: 400;
    }}

    QLineEdit:focus {{
        border: 2px solid {COLORS['neon_green']};
        background: rgba(21, 21, 31, 0.9);
        color: {COLORS['neon_green']};
    }}

    QLineEdit::placeholder {{
        color: {COLORS['text_secondary']};
    }}

    /* Labels - Glowing text effects */
    QLabel {{
        color: {COLORS['text_primary']};
        background: transparent;
        font-weight: 400;
    }}

    QLabel[heading="h1"] {{
        font-size: 56px;
        font-weight: 700;
        color: {COLORS['neon_green']};
        letter-spacing: 2px;
    }}

    QLabel[heading="h2"] {{
        font-size: 36px;
        font-weight: 700;
        color: {COLORS['neon_cyan']};
        letter-spacing: 1px;
    }}

    QLabel[heading="h3"] {{
        font-size: 22px;
        font-weight: 600;
        color: {COLORS['neon_green']};
        text-transform: uppercase;
        letter-spacing: 2px;
    }}

    QLabel[mono="true"] {{
        font-family: "JetBrains Mono", "Fira Code", "Menlo", monospace;
        font-weight: 400;
    }}

    /* Glassmorphic Panel - Cyberpunk card style */
    QFrame[panel="true"] {{
        background: qlineargradient(
            x1: 0, y1: 0, x2: 0, y2: 1,
            stop: 0 rgba(21, 21, 31, 0.6),
            stop: 1 rgba(18, 18, 26, 0.4)
        );
        border: 2px solid rgba(0, 255, 65, 0.3);
        border-radius: 16px;
        padding: 24px;
    }}

    QFrame[panel="true"]:hover {{
        border: 2px solid rgba(0, 255, 65, 0.5);
    }}

    /* Status Indicators - Neon colors */
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

    /* Checkboxes - Cyberpunk style */
    QCheckBox {{
        color: {COLORS['text_primary']};
        spacing: 10px;
        font-size: 14px;
    }}

    QCheckBox::indicator {{
        width: 22px;
        height: 22px;
        border: 2px solid {COLORS['border']};
        border-radius: 4px;
        background: rgba(21, 21, 31, 0.6);
    }}

    QCheckBox::indicator:checked {{
        background: {COLORS['neon_green']};
        border: 2px solid {COLORS['neon_green']};
    }}

    QCheckBox::indicator:hover {{
        border: 2px solid {COLORS['neon_cyan']};
    }}

    /* Combo Box - Terminal dropdown */
    QComboBox {{
        background: rgba(21, 21, 31, 0.6);
        border: 2px solid {COLORS['border']};
        border-radius: 8px;
        padding: 12px 16px;
        color: {COLORS['text_primary']};
        font-size: 14px;
    }}

    QComboBox:hover {{
        border: 2px solid {COLORS['neon_green']};
    }}

    QComboBox::drop-down {{
        border: none;
        width: 30px;
    }}

    QComboBox::down-arrow {{
        image: none;
        border-left: 6px solid transparent;
        border-right: 6px solid transparent;
        border-top: 6px solid {COLORS['neon_green']};
    }}

    QComboBox QAbstractItemView {{
        background: {COLORS['bg_secondary']};
        border: 2px solid {COLORS['neon_green']};
        selection-background-color: {COLORS['neon_green']};
        selection-color: {COLORS['bg_primary']};
    }}

    /* Message Box */
    QMessageBox {{
        background: {COLORS['bg_secondary']};
    }}

    QMessageBox QPushButton {{
        min-width: 100px;
    }}

    /* Progress Bar - Neon loading bar */
    QProgressBar {{
        background: rgba(21, 21, 31, 0.6);
        border: 2px solid {COLORS['border']};
        border-radius: 10px;
        text-align: center;
        color: {COLORS['text_primary']};
        font-weight: 700;
        height: 24px;
    }}

    QProgressBar::chunk {{
        background: qlineargradient(
            x1: 0, y1: 0, x2: 1, y2: 0,
            stop: 0 {COLORS['neon_green']},
            stop: 0.5 {COLORS['neon_cyan']},
            stop: 1 {COLORS['neon_purple']}
        );
        border-radius: 8px;
    }}

    /* Tooltip - Terminal popup */
    QToolTip {{
        background: {COLORS['bg_card']};
        color: {COLORS['neon_green']};
        border: 2px solid {COLORS['neon_green']};
        border-radius: 6px;
        padding: 8px;
        font-family: "JetBrains Mono", monospace;
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
    palette.setColor(QPalette.ColorRole.BrightText, QColor(COLORS['neon_green']))

    # Button
    palette.setColor(QPalette.ColorRole.Button, QColor(COLORS['bg_secondary']))
    palette.setColor(QPalette.ColorRole.ButtonText, QColor(COLORS['text_primary']))

    # Highlight
    palette.setColor(QPalette.ColorRole.Highlight, QColor(COLORS['neon_green']))
    palette.setColor(QPalette.ColorRole.HighlightedText, QColor(COLORS['bg_primary']))

    return palette
