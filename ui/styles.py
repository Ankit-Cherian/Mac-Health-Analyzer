"""
UI Styling for Mac Health Analyzer - Neo-Brutalist Earth Edition.
Bold geometric design with warm earth tones, exceptional readability, and organic sophistication.
"""

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QPalette


# Neo-Brutalist Earth Tone Palette
COLORS = {
    # Backgrounds - Warm, layered earth tones
    "bg_primary": "#f5f1e8",  # Warm cream (main background)
    "bg_secondary": "#e8dcc8",  # Light sand
    "bg_tertiary": "#d4c4a8",  # Warm tan
    "bg_card": "#ffffff",  # Pure white for cards
    "bg_dark": "#2d2520",  # Rich espresso for contrast
    # Earth Accent Colors - Muted, sophisticated tones
    "terracotta": "#c1614a",  # Warm terracotta (primary accent)
    "sage": "#6b8e6f",  # Sage green (success/low status)
    "mustard": "#d4a843",  # Warm mustard (warning)
    "burnt_sienna": "#a0522d",  # Burnt orange/sienna (critical)
    "clay": "#8b7355",  # Clay brown (secondary accent)
    "olive": "#6c6c3d",  # Olive green (tertiary)
    # Gradients - Warm earth transitions
    "gradient_start": "#c1614a",  # Terracotta
    "gradient_mid": "#d4a843",  # Mustard
    "gradient_end": "#6b8e6f",  # Sage
    # Text - High contrast, warm tones
    "text_primary": "#2d2520",  # Rich espresso (primary text)
    "text_secondary": "#6b5d54",  # Warm gray-brown (secondary)
    "text_muted": "#9a8b7f",  # Muted brown (tertiary)
    "text_light": "#f5f1e8",  # Cream (for dark backgrounds)
    # Status colors - Organic, readable
    "status_low": "#6b8e6f",  # Sage green - optimal
    "status_medium": "#d4a843",  # Mustard - warning
    "status_high": "#c1614a",  # Terracotta - critical
    "warning": "#d4a843",  # Alias for warning accents
    "critical": "#a0522d",  # Alias for high severity accents
    # UI elements
    "border": "#d4c4a8",  # Warm tan border
    "border_dark": "#8b7355",  # Clay border for emphasis
    "hover": "#e8dcc8",  # Light sand hover
    "shadow": "#2d252020",  # Subtle espresso shadow
    "accent_line": "#2d2520",  # Bold black lines (brutalist)
}


def get_main_stylesheet() -> str:
    """
    Get the main application stylesheet with neo-brutalist earth design.

    Returns:
        QStyleSheet string
    """
    return f"""
    /* Main Application Window - Warm earth gradient */
    QMainWindow {{
        background: qlineargradient(
            x1: 0, y1: 0, x2: 1, y2: 1,
            stop: 0 {COLORS['bg_primary']},
            stop: 0.6 {COLORS['bg_secondary']},
            stop: 1 {COLORS['bg_tertiary']}
        );
    }}

    /* Central Widget */
    QWidget {{
        background: transparent;
        color: {COLORS['text_primary']};
        font-family: "Sora", "DM Sans", "Helvetica Neue", sans-serif;
        font-size: 14px;
        font-weight: 400;
    }}

    /* Tab Widget - Bold brutalist tabs */
    QTabWidget::pane {{
        border: none;
        background: transparent;
    }}

    QTabBar::tab {{
        background: {COLORS['bg_card']};
        color: {COLORS['text_secondary']};
        padding: 18px 40px;
        margin-right: 4px;
        border: 3px solid {COLORS['border']};
        border-bottom: none;
        border-top: 4px solid transparent;
        font-size: 15px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1.5px;
    }}

    QTabBar::tab:selected {{
        background: {COLORS['bg_card']};
        color: {COLORS['terracotta']};
        font-weight: 700;
        border: 3px solid {COLORS['border_dark']};
        border-bottom: none;
        border-top: 4px solid {COLORS['terracotta']};
    }}

    QTabBar::tab:hover:!selected {{
        background: {COLORS['hover']};
        color: {COLORS['text_primary']};
        border-top: 4px solid {COLORS['clay']};
    }}

    /* Table Widget - Clean, readable data display */
    QTableWidget {{
        background: {COLORS['bg_card']};
        border: 3px solid {COLORS['border']};
        border-radius: 0px;
        gridline-color: {COLORS['border']};
        selection-background-color: {COLORS['terracotta']};
        selection-color: {COLORS['text_light']};
        font-family: "IBM Plex Mono", "Menlo", "Courier New", monospace;
        font-size: 13px;
        font-weight: 400;
    }}

    QTableWidget::item {{
        padding: 12px;
        border: none;
        color: {COLORS['text_primary']};
    }}

    QTableWidget::item:selected {{
        background: {COLORS['terracotta']};
        color: {COLORS['text_light']};
        font-weight: 500;
    }}

    QTableWidget::item:hover {{
        background: {COLORS['hover']};
        color: {COLORS['text_primary']};
    }}

    QHeaderView::section {{
        background: {COLORS['bg_dark']};
        color: {COLORS['text_light']};
        padding: 14px 10px;
        border: none;
        border-right: 1px solid {COLORS['clay']};
        border-bottom: 3px solid {COLORS['terracotta']};
        font-size: 11px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1.5px;
    }}

    QHeaderView::section:hover {{
        background: {COLORS['clay']};
        color: {COLORS['text_light']};
    }}

    /* Scroll Bars - Minimalist geometric style */
    QScrollBar:vertical {{
        background: {COLORS['bg_secondary']};
        width: 12px;
        margin: 0px;
        border-radius: 0px;
        border-left: 2px solid {COLORS['border']};
    }}

    QScrollBar::handle:vertical {{
        background: {COLORS['clay']};
        border-radius: 0px;
        border: 2px solid {COLORS['border_dark']};
        min-height: 30px;
    }}

    QScrollBar::handle:vertical:hover {{
        background: {COLORS['terracotta']};
        border: 2px solid {COLORS['burnt_sienna']};
    }}

    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
        height: 0px;
    }}

    QScrollBar:horizontal {{
        background: {COLORS['bg_secondary']};
        height: 12px;
        margin: 0px;
        border-radius: 0px;
        border-top: 2px solid {COLORS['border']};
    }}

    QScrollBar::handle:horizontal {{
        background: {COLORS['clay']};
        border-radius: 0px;
        border: 2px solid {COLORS['border_dark']};
        min-width: 30px;
    }}

    QScrollBar::handle:horizontal:hover {{
        background: {COLORS['terracotta']};
        border: 2px solid {COLORS['burnt_sienna']};
    }}

    QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
        width: 0px;
    }}

    /* Push Buttons - Bold brutalist style */
    QPushButton {{
        background: {COLORS['terracotta']};
        color: {COLORS['text_light']};
        border: 3px solid {COLORS['accent_line']};
        border-radius: 0px;
        padding: 14px 28px;
        font-size: 14px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1.2px;
    }}

    QPushButton:hover {{
        background: {COLORS['burnt_sienna']};
        border: 3px solid {COLORS['bg_dark']};
        color: {COLORS['text_light']};
    }}

    QPushButton:pressed {{
        background: {COLORS['clay']};
        border: 3px solid {COLORS['accent_line']};
    }}

    QPushButton:disabled {{
        background: {COLORS['border']};
        color: {COLORS['text_muted']};
        border: 3px solid {COLORS['border']};
    }}

    /* Danger Button - Burnt sienna accent */
    QPushButton[danger="true"] {{
        background: {COLORS['burnt_sienna']};
        color: {COLORS['text_light']};
        border: 3px solid {COLORS['accent_line']};
    }}

    QPushButton[danger="true"]:hover {{
        background: {COLORS['terracotta']};
        border: 3px solid {COLORS['bg_dark']};
    }}

    /* Line Edit (Search/Input) - Clean input style */
    QLineEdit {{
        background: {COLORS['bg_card']};
        border: 3px solid {COLORS['border']};
        border-radius: 0px;
        padding: 12px 16px;
        color: {COLORS['text_primary']};
        font-size: 14px;
        font-weight: 400;
    }}

    QLineEdit#searchField {{
        border: 3px solid {COLORS['border_dark']};
        padding-left: 32px;
        background-color: {COLORS['bg_card']};
        background-position: 10px center;
    }}

    QLineEdit:focus {{
        border: 3px solid {COLORS['terracotta']};
        background: {COLORS['bg_card']};
        color: {COLORS['text_primary']};
    }}

    QLineEdit::placeholder {{
        color: {COLORS['text_muted']};
    }}

    /* Labels - Clear, bold typography */
    QLabel {{
        color: {COLORS['text_primary']};
        background: transparent;
        font-weight: 400;
    }}

    QLabel[heading="h1"] {{
        font-size: 52px;
        font-weight: 800;
        color: {COLORS['bg_dark']};
        letter-spacing: -0.5px;
    }}

    QLabel[heading="h2"] {{
        font-size: 34px;
        font-weight: 700;
        color: {COLORS['terracotta']};
        letter-spacing: 0px;
    }}

    QLabel[heading="h3"] {{
        font-size: 20px;
        font-weight: 700;
        color: {COLORS['bg_dark']};
        text-transform: uppercase;
        letter-spacing: 1.5px;
    }}

    QLabel[metricValue="true"] {{
        font-size: 30px;
        font-weight: 700;
        color: {COLORS['text_primary']};
        letter-spacing: 0.5px;
    }}

    QLabel[chartTitle="true"] {{
        font-size: 16px;
        font-weight: 700;
        color: {COLORS['terracotta']};
        letter-spacing: 1px;
    }}

    QLabel[mono="true"] {{
        font-family: "IBM Plex Mono", "Menlo", "Courier New", monospace;
        font-weight: 400;
    }}

    /* Search field - matches brutalist cards */
    QFrame[search="true"] {{
        background: {COLORS['bg_card']};
        border: 3px solid {COLORS['border']};
        border-radius: 0px;
    }}

    QFrame[search="true"]:focus-within {{
        border-color: {COLORS['terracotta']};
        box-shadow: 4px 4px 0 {COLORS['accent_line']};
    }}

    QFrame[search="true"] QLabel {{
        color: {COLORS['text_secondary']};
    }}

    QFrame[search="true"] QLineEdit {{
        border: none;
        background: transparent;
        color: {COLORS['text_primary']};
        font-size: 14px;
    }}

    QFrame[search="true"] QLineEdit::placeholder {{
        color: {COLORS['text_muted']};
    }}

    /* Brutalist Panel - Bold card style */
    QFrame[panel="true"] {{
        background: {COLORS['bg_card']};
        border: 4px solid {COLORS['accent_line']};
        border-radius: 0px;
        padding: 24px;
    }}

    QFrame[panel="true"]:hover {{
        border: 4px solid {COLORS['terracotta']};
    }}

    /* Status Indicators - Earth tone colors */
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

    /* Checkboxes - Bold geometric style */
    QCheckBox {{
        color: {COLORS['text_primary']};
        spacing: 10px;
        font-size: 14px;
    }}

    QCheckBox::indicator {{
        width: 22px;
        height: 22px;
        border: 3px solid {COLORS['border_dark']};
        border-radius: 0px;
        background: {COLORS['bg_card']};
    }}

    QCheckBox::indicator:checked {{
        background: {COLORS['terracotta']};
        border: 3px solid {COLORS['accent_line']};
    }}

    QCheckBox::indicator:hover {{
        border: 3px solid {COLORS['terracotta']};
    }}

    /* Combo Box - Clean dropdown */
    QComboBox {{
        background: {COLORS['bg_card']};
        border: 3px solid {COLORS['border']};
        border-radius: 0px;
        padding: 12px 16px;
        color: {COLORS['text_primary']};
        font-size: 14px;
    }}

    QComboBox:hover {{
        border: 3px solid {COLORS['terracotta']};
    }}

    QComboBox::drop-down {{
        border: none;
        width: 30px;
    }}

    QComboBox::down-arrow {{
        image: none;
        border-left: 6px solid transparent;
        border-right: 6px solid transparent;
        border-top: 6px solid {COLORS['terracotta']};
    }}

    QComboBox QAbstractItemView {{
        background: {COLORS['bg_card']};
        border: 3px solid {COLORS['terracotta']};
        selection-background-color: {COLORS['terracotta']};
        selection-color: {COLORS['text_light']};
    }}

    /* Message Box */
    QMessageBox {{
        background: {COLORS['bg_primary']};
    }}

    QMessageBox QPushButton {{
        min-width: 100px;
    }}

    /* Progress Bar - Bold geometric bar */
    QProgressBar {{
        background: {COLORS['bg_secondary']};
        border: 3px solid {COLORS['border_dark']};
        border-radius: 0px;
        text-align: center;
        color: {COLORS['text_primary']};
        font-weight: 700;
        height: 28px;
    }}

    QProgressBar::chunk {{
        background: {COLORS['terracotta']};
        border-radius: 0px;
    }}

    /* Tooltip - Clean popup */
    QToolTip {{
        background: {COLORS['bg_dark']};
        color: {COLORS['text_light']};
        border: 3px solid {COLORS['terracotta']};
        border-radius: 0px;
        padding: 10px;
        font-family: "IBM Plex Mono", monospace;
        font-size: 12px;
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
        return COLORS["status_low"]
    elif percent < 80:
        return COLORS["status_medium"]
    else:
        return COLORS["status_high"]


def get_palette() -> QPalette:
    """
    Get application color palette.

    Returns:
        QPalette object
    """
    palette = QPalette()

    # Window
    palette.setColor(QPalette.ColorRole.Window, QColor(COLORS["bg_primary"]))
    palette.setColor(QPalette.ColorRole.WindowText, QColor(COLORS["text_primary"]))

    # Base
    palette.setColor(QPalette.ColorRole.Base, QColor(COLORS["bg_card"]))
    palette.setColor(QPalette.ColorRole.AlternateBase, QColor(COLORS["bg_secondary"]))

    # Text
    palette.setColor(QPalette.ColorRole.Text, QColor(COLORS["text_primary"]))
    palette.setColor(QPalette.ColorRole.BrightText, QColor(COLORS["terracotta"]))

    # Button
    palette.setColor(QPalette.ColorRole.Button, QColor(COLORS["terracotta"]))
    palette.setColor(QPalette.ColorRole.ButtonText, QColor(COLORS["text_light"]))

    # Highlight
    palette.setColor(QPalette.ColorRole.Highlight, QColor(COLORS["terracotta"]))
    palette.setColor(QPalette.ColorRole.HighlightedText, QColor(COLORS["text_light"]))

    return palette
