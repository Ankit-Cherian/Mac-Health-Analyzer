"""
UI Styling for Mac Health Analyzer.
Professional design with warm earth tones and sophisticated visual polish.
"""

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QPalette


# Refined Earth Tone Palette with Professional Depth
COLORS = {
    # Layered Backgrounds - Atmospheric earth tones with depth
    'bg_primary': '#f5f1e8',      # Warm cream (main background)
    'bg_secondary': '#e8dcc8',    # Light sand
    'bg_tertiary': '#d4c4a8',     # Warm tan
    'bg_card': '#fffcf7',         # Off-white with warmth for cards
    'bg_elevated': '#ffffff',     # Pure white for elevated elements
    'bg_dark': '#2d2520',         # Rich espresso for contrast
    'bg_overlay': '#2d252008',    # Subtle overlay for depth

    # Textured accents for atmosphere
    'texture_light': '#f5f1e810',  # Subtle texture overlay
    'texture_pattern': '#2d252005', # Micro-pattern overlay

    # Earth Accent Colors - Professional, sophisticated tones
    'terracotta': '#c1614a',      # Warm terracotta (primary accent)
    'terracotta_dark': '#a04d38',  # Deeper terracotta for depth
    'sage': '#6b8e6f',            # Sage green (success/low status)
    'sage_dark': '#587258',       # Deeper sage
    'mustard': '#d4a843',         # Warm mustard (warning)
    'mustard_dark': '#b38f36',    # Deeper mustard
    'golden': '#f4c430',          # Bright golden yellow (complements teal)
    'burnt_sienna': '#a0522d',    # Burnt orange/sienna (critical)
    'clay': '#8b7355',            # Clay brown (secondary accent)
    'clay_light': '#a38a6f',      # Lighter clay
    'olive': '#6c6c3d',           # Olive green (tertiary)
    'teal': '#4a9b8e',            # Muted teal (creative complement to sage)

    # Sophisticated Gradients - Layered transitions
    'gradient_start': '#c1614a',   # Terracotta
    'gradient_mid': '#d4a843',     # Mustard
    'gradient_end': '#6b8e6f',     # Sage
    'gradient_overlay': '#f5f1e8cc', # Atmospheric overlay

    # Professional Typography Colors
    'text_primary': '#2d2520',    # Rich espresso (primary text)
    'text_secondary': '#6b5d54',  # Warm gray-brown (secondary)
    'text_tertiary': '#8b7d70',   # Medium warm gray
    'text_muted': '#9a8b7f',      # Muted brown (tertiary)
    'text_light': '#f5f1e8',      # Cream (for dark backgrounds)
    'text_accent': '#c1614a',     # Terracotta for emphasis

    # Refined Status Colors
    'status_low': '#6b8e6f',      # Sage green - optimal
    'status_medium': '#d4a843',   # Mustard - warning
    'status_high': '#c1614a',     # Terracotta - critical
    'warning': '#d4a843',         # Alias for warning accents
    'critical': '#a0522d',        # Alias for high severity accents

    # Professional UI Elements with Depth
    'border': '#d4c4a8',          # Warm tan border
    'border_subtle': '#e8dcc8',   # Subtle border
    'border_dark': '#8b7355',     # Clay border for emphasis
    'border_focus': '#c1614a',    # Focus state
    'hover': '#e8dcc8',           # Light sand hover
    'hover_elevated': '#f5f1e8',  # Elevated hover state

    # Sophisticated Shadow System
    'shadow_sm': 'rgba(45, 37, 32, 0.04)',   # Subtle depth
    'shadow_md': 'rgba(45, 37, 32, 0.08)',   # Medium depth
    'shadow_lg': 'rgba(45, 37, 32, 0.12)',   # Strong depth
    'shadow_xl': 'rgba(45, 37, 32, 0.16)',   # Maximum depth
    'shadow_inner': 'rgba(45, 37, 32, 0.06)', # Inner shadow

    # Accent elements
    'accent_line': '#2d2520',     # Bold lines
    'accent_glow': '#c1614a40',   # Subtle glow effect
    'divider': '#d4c4a880',       # Subtle dividers
}


def get_main_stylesheet() -> str:
    """
    Get the main application stylesheet with refined professional earth design.

    Returns:
        QStyleSheet string with expert-level polish and depth
    """
    return f"""
    /* Main Application Window - Sophisticated layered background */
    QMainWindow {{
        background: qlineargradient(
            x1: 0, y1: 0, x2: 1, y2: 1,
            stop: 0 {COLORS['bg_primary']},
            stop: 0.5 {COLORS['bg_secondary']},
            stop: 1 {COLORS['bg_tertiary']}
        );
    }}

    /* Central Widget - Professional base styling */
    QWidget {{
        background: transparent;
        color: {COLORS['text_primary']};
        font-family: "Fraunces", "Sora", "Georgia", serif;
        font-size: 14px;
        font-weight: 400;
        line-height: 1.6;
    }}

    /* Tab Widget - Refined professional tabs with depth */
    QTabWidget::pane {{
        border: none;
        background: transparent;
    }}

    QTabBar::tab {{
        background: {COLORS['bg_card']};
        color: {COLORS['text_secondary']};
        padding: 20px 48px;
        margin-right: 6px;
        border: 2px solid {COLORS['border_subtle']};
        border-bottom: none;
        border-top: 3px solid transparent;
        font-family: "Sora", "Helvetica Neue", Arial;
        font-size: 13px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 2px;
    }}

    QTabBar::tab:selected {{
        background: {COLORS['bg_elevated']};
        color: {COLORS['terracotta']};
        font-weight: 700;
        border: 2px solid {COLORS['terracotta']};
        border-bottom: none;
        border-top: 3px solid {COLORS['terracotta']};
    }}

    QTabBar::tab:hover:!selected {{
        background: {COLORS['hover']};
        color: {COLORS['text_primary']};
        border-top: 3px solid {COLORS['clay_light']};
        border-color: {COLORS['border']};
    }}

    /* Table Widget - Professional data display with depth */
    QTableWidget {{
        background: {COLORS['bg_elevated']};
        border: 2px solid {COLORS['border']};
        border-radius: 0px;
        gridline-color: {COLORS['border_subtle']};
        selection-background-color: {COLORS['terracotta']};
        selection-color: {COLORS['text_light']};
        font-family: "IBM Plex Mono", "SF Mono", "Menlo", monospace;
        font-size: 13px;
        font-weight: 400;
        line-height: 1.5;
    }}

    QTableWidget::item {{
        padding: 14px 16px;
        border: none;
        color: {COLORS['text_primary']};
        border-bottom: 1px solid {COLORS['border_subtle']};
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
        background: qlineargradient(
            x1: 0, y1: 0, x2: 0, y2: 1,
            stop: 0 {COLORS['bg_dark']},
            stop: 1 #1f1a17
        );
        color: {COLORS['text_light']};
        padding: 16px 12px;
        border: none;
        border-right: 1px solid rgba(255, 255, 255, 0.05);
        border-bottom: 2px solid {COLORS['terracotta']};
        font-family: "Sora", "Helvetica Neue", Arial;
        font-size: 11px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 2px;
    }}

    QHeaderView::section:hover {{
        background: qlineargradient(
            x1: 0, y1: 0, x2: 0, y2: 1,
            stop: 0 {COLORS['clay']},
            stop: 1 {COLORS['bg_dark']}
        );
        color: {COLORS['text_light']};
    }}

    /* Scroll Bars - Refined minimal style */
    QScrollBar:vertical {{
        background: {COLORS['bg_secondary']};
        width: 10px;
        margin: 0px;
        border-radius: 0px;
        border-left: 1px solid {COLORS['border_subtle']};
    }}

    QScrollBar::handle:vertical {{
        background: {COLORS['clay_light']};
        border-radius: 0px;
        border: none;
        min-height: 40px;
    }}

    QScrollBar::handle:vertical:hover {{
        background: {COLORS['terracotta']};
    }}

    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
        height: 0px;
    }}

    QScrollBar:horizontal {{
        background: {COLORS['bg_secondary']};
        height: 10px;
        margin: 0px;
        border-radius: 0px;
        border-top: 1px solid {COLORS['border_subtle']};
    }}

    QScrollBar::handle:horizontal {{
        background: {COLORS['clay_light']};
        border-radius: 0px;
        border: none;
        min-width: 40px;
    }}

    QScrollBar::handle:horizontal:hover {{
        background: {COLORS['terracotta']};
    }}

    QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
        width: 0px;
    }}

    /* Push Buttons - Refined professional style */
    QPushButton {{
        background: qlineargradient(
            x1: 0, y1: 0, x2: 0, y2: 1,
            stop: 0 {COLORS['terracotta']},
            stop: 1 {COLORS['terracotta_dark']}
        );
        color: {COLORS['text_light']};
        border: 2px solid {COLORS['terracotta_dark']};
        border-radius: 0px;
        padding: 16px 32px;
        font-family: "Sora", "Helvetica Neue", Arial;
        font-size: 13px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1.5px;
    }}

    QPushButton:hover {{
        background: qlineargradient(
            x1: 0, y1: 0, x2: 0, y2: 1,
            stop: 0 {COLORS['terracotta_dark']},
            stop: 1 {COLORS['burnt_sienna']}
        );
        border: 2px solid {COLORS['burnt_sienna']};
        color: {COLORS['text_light']};
    }}

    QPushButton:pressed {{
        background: {COLORS['burnt_sienna']};
        border: 2px solid {COLORS['burnt_sienna']};
        padding: 17px 32px 15px 32px;
    }}

    QPushButton:disabled {{
        background: {COLORS['border']};
        color: {COLORS['text_muted']};
        border: 2px solid {COLORS['border']};
    }}

    /* Danger Button - Critical action styling */
    QPushButton[danger="true"] {{
        background: qlineargradient(
            x1: 0, y1: 0, x2: 0, y2: 1,
            stop: 0 {COLORS['burnt_sienna']},
            stop: 1 #8a4223
        );
        color: {COLORS['text_light']};
        border: 2px solid #8a4223;
    }}

    QPushButton[danger="true"]:hover {{
        background: qlineargradient(
            x1: 0, y1: 0, x2: 0, y2: 1,
            stop: 0 #8a4223,
            stop: 1 #6d341b
        );
        border: 2px solid #6d341b;
    }}

    /* Line Edit (Search/Input) - Professional input style */
    QLineEdit {{
        background: {COLORS['bg_elevated']};
        border: 2px solid {COLORS['border']};
        border-radius: 0px;
        padding: 14px 18px;
        color: {COLORS['text_primary']};
        font-family: "Sora", "Helvetica Neue", Arial;
        font-size: 14px;
        font-weight: 400;
    }}

    QLineEdit#searchField {{
        border: 2px solid {COLORS['border_dark']};
        padding-left: 40px;
        background-color: {COLORS['bg_elevated']};
        background-position: 12px center;
    }}

    QLineEdit:focus {{
        border: 2px solid {COLORS['terracotta']};
        background: {COLORS['bg_elevated']};
        color: {COLORS['text_primary']};
        outline: none;
    }}

    QLineEdit::placeholder {{
        color: {COLORS['text_muted']};
        font-weight: 400;
    }}

    /* Labels - Professional typography hierarchy */
    QLabel {{
        color: {COLORS['text_primary']};
        background: transparent;
        font-weight: 400;
        line-height: 1.6;
    }}

    QLabel[heading="h1"] {{
        font-family: "Fraunces", "Georgia", serif;
        font-size: 56px;
        font-weight: 700;
        color: {COLORS['bg_dark']};
        letter-spacing: -1px;
        line-height: 1.1;
    }}

    QLabel[heading="h2"] {{
        font-family: "Fraunces", "Georgia", serif;
        font-size: 36px;
        font-weight: 600;
        color: {COLORS['terracotta']};
        letter-spacing: -0.5px;
        line-height: 1.2;
    }}

    QLabel[heading="h3"] {{
        font-family: "Sora", "Helvetica Neue", Arial;
        font-size: 14px;
        font-weight: 700;
        color: {COLORS['text_secondary']};
        text-transform: uppercase;
        letter-spacing: 2.5px;
    }}

    QLabel[metricValue="true"] {{
        font-family: "IBM Plex Mono", "SF Mono", monospace;
        font-size: 32px;
        font-weight: 600;
        color: {COLORS['text_primary']};
        letter-spacing: -0.5px;
        line-height: 1.2;
    }}

    QLabel[chartTitle="true"] {{
        font-family: "Sora", "Helvetica Neue", Arial;
        font-size: 15px;
        font-weight: 600;
        color: {COLORS['terracotta']};
        letter-spacing: 0.5px;
    }}

    QLabel[mono="true"] {{
        font-family: "IBM Plex Mono", "SF Mono", "Menlo", monospace;
        font-weight: 400;
        line-height: 1.5;
    }}

    /* Search field - Professional search styling */
    QFrame[search="true"] {{
        background: {COLORS['bg_elevated']};
        border: 2px solid {COLORS['border']};
        border-radius: 0px;
    }}

    QFrame[search="true"]:focus-within {{
        border-color: {COLORS['terracotta']};
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

    /* Panel - Professional card with depth */
    QFrame[panel="true"][panelVariant="primary"] {{
        background: {COLORS['bg_elevated']};
        border: 2px solid {COLORS['border']};
        border-radius: 0px;
        padding: 28px;
    }}

    QFrame[panel="true"][panelVariant="primary"]:hover {{
        border: 2px solid {COLORS['terracotta']};
    }}

    /* Minimal panel variant for nested content */
    QFrame[panel="true"][panelVariant="minimal"] {{
        background: {COLORS['bg_card']};
        border: none;
        border-radius: 0px;
        padding: 0px;
    }}

    /* Status Indicators - Professional status styling */
    QLabel[status="low"] {{
        color: {COLORS['status_low']};
        font-weight: 600;
    }}

    QLabel[status="medium"] {{
        color: {COLORS['status_medium']};
        font-weight: 600;
    }}

    QLabel[status="high"] {{
        color: {COLORS['status_high']};
        font-weight: 600;
    }}

    /* Checkboxes - Refined checkbox style */
    QCheckBox {{
        color: {COLORS['text_primary']};
        spacing: 12px;
        font-family: "Sora", "Helvetica Neue", Arial;
        font-size: 14px;
        line-height: 1.6;
    }}

    QCheckBox::indicator {{
        width: 20px;
        height: 20px;
        border: 2px solid {COLORS['border_dark']};
        border-radius: 0px;
        background: {COLORS['bg_elevated']};
    }}

    QCheckBox::indicator:checked {{
        background: qlineargradient(
            x1: 0, y1: 0, x2: 1, y2: 1,
            stop: 0 {COLORS['terracotta']},
            stop: 1 {COLORS['terracotta_dark']}
        );
        border: 2px solid {COLORS['terracotta_dark']};
    }}

    QCheckBox::indicator:hover {{
        border: 2px solid {COLORS['terracotta']};
    }}

    /* Combo Box - Professional dropdown */
    QComboBox {{
        background: {COLORS['bg_elevated']};
        border: 2px solid {COLORS['border']};
        border-radius: 0px;
        padding: 14px 18px;
        color: {COLORS['text_primary']};
        font-family: "Sora", "Helvetica Neue", Arial;
        font-size: 14px;
    }}

    QComboBox:hover {{
        border: 2px solid {COLORS['terracotta']};
    }}

    QComboBox::drop-down {{
        border: none;
        width: 32px;
    }}

    QComboBox::down-arrow {{
        image: none;
        border-left: 5px solid transparent;
        border-right: 5px solid transparent;
        border-top: 5px solid {COLORS['terracotta']};
    }}

    QComboBox QAbstractItemView {{
        background: {COLORS['bg_elevated']};
        border: 2px solid {COLORS['terracotta']};
        selection-background-color: {COLORS['terracotta']};
        selection-color: {COLORS['text_light']};
    }}

    /* Message Box */
    QMessageBox {{
        background: {COLORS['bg_primary']};
    }}

    QMessageBox QPushButton {{
        min-width: 120px;
    }}

    /* Progress Bar - Professional progress indicator */
    QProgressBar {{
        background: {COLORS['bg_secondary']};
        border: 2px solid {COLORS['border']};
        border-radius: 0px;
        text-align: center;
        color: {COLORS['text_primary']};
        font-family: "IBM Plex Mono", "SF Mono", monospace;
        font-weight: 600;
        height: 32px;
    }}

    QProgressBar::chunk {{
        background: qlineargradient(
            x1: 0, y1: 0, x2: 1, y2: 0,
            stop: 0 {COLORS['terracotta']},
            stop: 1 {COLORS['terracotta_dark']}
        );
        border-radius: 0px;
    }}

    /* Tooltip - Professional tooltip */
    QToolTip {{
        background: {COLORS['bg_dark']};
        color: {COLORS['text_light']};
        border: 2px solid {COLORS['terracotta']};
        border-radius: 0px;
        padding: 12px 16px;
        font-family: "IBM Plex Mono", "SF Mono", monospace;
        font-size: 12px;
        line-height: 1.5;
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
    palette.setColor(QPalette.ColorRole.Base, QColor(COLORS['bg_card']))
    palette.setColor(QPalette.ColorRole.AlternateBase, QColor(COLORS['bg_secondary']))

    # Text
    palette.setColor(QPalette.ColorRole.Text, QColor(COLORS['text_primary']))
    palette.setColor(QPalette.ColorRole.BrightText, QColor(COLORS['terracotta']))

    # Button
    palette.setColor(QPalette.ColorRole.Button, QColor(COLORS['terracotta']))
    palette.setColor(QPalette.ColorRole.ButtonText, QColor(COLORS['text_light']))

    # Highlight
    palette.setColor(QPalette.ColorRole.Highlight, QColor(COLORS['terracotta']))
    palette.setColor(QPalette.ColorRole.HighlightedText, QColor(COLORS['text_light']))

    return palette
