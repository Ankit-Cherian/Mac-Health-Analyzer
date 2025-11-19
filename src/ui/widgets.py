"""
Custom styled widgets for the Mac Health Analyzer.
Professional components with sophisticated micro-interactions and polish.
Designed to feel hand-crafted by a seasoned UI/UX professional.
"""

from PyQt6.QtCore import Qt, pyqtSignal, QRect, QPropertyAnimation, QEasingCurve, pyqtProperty, QVariantAnimation
from PyQt6.QtWidgets import (
    QWidget,
    QPushButton,
    QFrame,
    QLabel,
    QHBoxLayout,
    QVBoxLayout,
    QSizePolicy,
    QLineEdit,
    QGraphicsOpacityEffect
)
from PyQt6.QtGui import QPainter, QColor, QPen, QBrush, QLinearGradient
from ui.styles import COLORS


class ToggleSwitch(QWidget):
    """
    Professional toggle switch with smooth, elegant animation.
    Features sophisticated micro-interactions and polished visual feedback.
    """

    toggled = pyqtSignal(bool)

    def __init__(self, parent=None, initial_state=False):
        """
        Initialize toggle switch.

        Args:
            parent: Parent widget
            initial_state: Initial checked state
        """
        super().__init__(parent)
        self._checked = initial_state
        self._circle_position = 24 if initial_state else 2
        self._hovered = False
        self._bg_opacity = 1.0 if initial_state else 0.0
        self._hover_opacity = 0.0

        self.setFixedSize(52, 28)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setMouseTracking(True)

        # Smooth, elegant animation for circle movement
        self.animation = QPropertyAnimation(self, b"circle_position")
        self.animation.setDuration(300)
        self.animation.setEasingCurve(QEasingCurve.Type.InOutQuart)  # Smooth, elegant curve

        # Background color transition animation
        self.bg_animation = QPropertyAnimation(self, b"bg_opacity")
        self.bg_animation.setDuration(300)
        self.bg_animation.setEasingCurve(QEasingCurve.Type.InOutQuart)

        # Hover glow animation for subtle brightness change
        self.hover_animation = QVariantAnimation(self)
        self.hover_animation.setDuration(140)
        self.hover_animation.setEasingCurve(QEasingCurve.Type.InOutQuad)
        self.hover_animation.valueChanged.connect(self._update_hover_opacity)

    def _update_hover_opacity(self, value: float):
        """Update hover intensity and repaint."""
        self._hover_opacity = value
        self.update()

    @pyqtProperty(int)
    def circle_position(self):
        """Get circle position for animation."""
        return self._circle_position

    @circle_position.setter
    def circle_position(self, pos):
        """Set circle position for animation."""
        self._circle_position = pos
        self.update()

    @pyqtProperty(float)
    def bg_opacity(self):
        """Get background opacity for color transition."""
        return self._bg_opacity

    @bg_opacity.setter
    def bg_opacity(self, opacity):
        """Set background opacity for color transition."""
        self._bg_opacity = opacity
        self.update()

    def enterEvent(self, event):
        """Handle mouse enter for hover effect."""
        self._hovered = True
        self.hover_animation.stop()
        self.hover_animation.setStartValue(self._hover_opacity)
        self.hover_animation.setEndValue(1.0)
        self.hover_animation.start()
        super().enterEvent(event)

    def leaveEvent(self, event):
        """Handle mouse leave for hover effect."""
        self._hovered = False
        self.hover_animation.stop()
        self.hover_animation.setStartValue(self._hover_opacity)
        self.hover_animation.setEndValue(0.0)
        self.hover_animation.start()
        super().leaveEvent(event)

    def paintEvent(self, event):
        """Paint the toggle switch with professional depth and smooth gradients."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Interpolate colors for smooth transition
        inactive_bg = QColor(COLORS['border'])
        active_bg = QColor(COLORS['terracotta'])
        inactive_border = QColor(COLORS['border_dark'])
        active_border = QColor(COLORS['terracotta_dark'])

        # Blend colors based on animation progress
        bg_color = QColor(
            int(inactive_bg.red() + (active_bg.red() - inactive_bg.red()) * self._bg_opacity),
            int(inactive_bg.green() + (active_bg.green() - inactive_bg.green()) * self._bg_opacity),
            int(inactive_bg.blue() + (active_bg.blue() - inactive_bg.blue()) * self._bg_opacity)
        )
        border_color = QColor(
            int(inactive_border.red() + (active_border.red() - inactive_border.red()) * self._bg_opacity),
            int(inactive_border.green() + (active_border.green() - inactive_border.green()) * self._bg_opacity),
            int(inactive_border.blue() + (active_border.blue() - inactive_border.blue()) * self._bg_opacity)
        )

        # Apply hover effect - slightly brighter with animation
        if self._hover_opacity > 0:
            brighten = 100 + int(10 * self._hover_opacity)
            bg_color = bg_color.lighter(brighten)

        # Draw outer shadow for depth (only when not hovered)
        if not self._hovered:
            outer_shadow = QColor(0, 0, 0, 8)
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(QBrush(outer_shadow))
            painter.drawRoundedRect(2, 2, 50, 26, 13, 13)

        # Background track with rounded corners and border for depth
        painter.setPen(QPen(border_color, 2))
        painter.setBrush(QBrush(bg_color))
        painter.drawRoundedRect(1, 1, 50, 26, 13, 13)  # Rounded corners matching circle

        # Inner highlight for depth (subtle gradient effect)
        if self._checked:
            highlight_gradient = QLinearGradient(1, 1, 1, 14)
            highlight_gradient.setColorAt(0.0, QColor(255, 255, 255, 30))
            highlight_gradient.setColorAt(1.0, QColor(255, 255, 255, 0))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(QBrush(highlight_gradient))
            painter.drawRoundedRect(3, 3, 48, 12, 6, 6)

        # Interpolate circle color
        inactive_circle = QColor(COLORS['text_secondary'])
        active_circle = QColor(COLORS['bg_elevated'])
        circle_color = QColor(
            int(inactive_circle.red() + (active_circle.red() - inactive_circle.red()) * self._bg_opacity),
            int(inactive_circle.green() + (active_circle.green() - inactive_circle.green()) * self._bg_opacity),
            int(inactive_circle.blue() + (active_circle.blue() - inactive_circle.blue()) * self._bg_opacity)
        )

        if self._hover_opacity > 0:
            brighten = 100 + int(8 * self._hover_opacity)
            circle_color = circle_color.lighter(brighten)

        # Multi-layer shadow for circle depth
        painter.setPen(Qt.PenStyle.NoPen)

        # Outer shadow (subtle)
        shadow_outer = QColor(0, 0, 0, 25)
        painter.setBrush(QBrush(shadow_outer))
        painter.drawEllipse(self._circle_position + 1, 3, 24, 24)

        # Inner shadow (more prominent)
        shadow_inner = QColor(0, 0, 0, 15)
        painter.setBrush(QBrush(shadow_inner))
        painter.drawEllipse(self._circle_position + 0.5, 2.5, 24, 24)

        # Circle with subtle border for definition
        circle_border = QColor(COLORS['border_dark']) if not self._checked else QColor(COLORS['terracotta_dark'])
        circle_border.setAlpha(40)
        painter.setPen(QPen(circle_border, 1))
        painter.setBrush(QBrush(circle_color))
        painter.drawEllipse(self._circle_position, 2, 24, 24)

        # Highlight on circle for 3D effect
        highlight = QColor(255, 255, 255, 80 if self._checked else 40)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(highlight))
        painter.drawEllipse(self._circle_position + 4, 4, 10, 10)

    def mouseReleaseEvent(self, event):
        """Handle mouse click with smooth animation."""
        if event.button() == Qt.MouseButton.LeftButton:
            self._checked = not self._checked

            # Animate circle position
            self.animation.setStartValue(self._circle_position)
            self.animation.setEndValue(24 if self._checked else 2)
            self.animation.start()

            # Animate background color transition
            self.bg_animation.setStartValue(self._bg_opacity)
            self.bg_animation.setEndValue(1.0 if self._checked else 0.0)
            self.bg_animation.start()

            self.toggled.emit(self._checked)

    def setChecked(self, checked: bool):
        """Set checked state programmatically."""
        if self._checked != checked:
            self._checked = checked
            self._circle_position = 24 if checked else 2
            self._bg_opacity = 1.0 if checked else 0.0
            self.update()

    def isChecked(self) -> bool:
        """Get checked state."""
        return self._checked


class StyledButton(QPushButton):
    """
    Enhanced QPushButton with additional styling options.
    """
    
    def __init__(self, text: str, button_type: str = "primary", parent=None):
        """
        Initialize styled button.
        
        Args:
            text: Button text
            button_type: Type of button ("primary", "danger", "secondary")
            parent: Parent widget
        """
        super().__init__(text, parent)
        self.button_type = button_type
        
        if button_type == "danger":
            self.setProperty("danger", "true")
        
        self.setCursor(Qt.CursorShape.PointingHandCursor)


class GlassmorphicPanel(QFrame):
    """Panel with glassmorphic effect and optional style variants."""

    def __init__(self, parent=None, variant: str = "primary"):
        """
        Initialize glassmorphic panel.

        Args:
            parent: Parent widget
            variant: Visual style variant ("primary", "minimal", etc.)
        """
        super().__init__(parent)
        self.setProperty("panel", "true")
        self.setProperty("panelVariant", variant)
        self.setFrameShape(QFrame.Shape.StyledPanel)


class MetricCard(QWidget):
    """
    Professional metric card with sophisticated visual hierarchy and depth.
    Features refined typography, status indicators, and polished animations.
    """

    def __init__(self, title: str, value: str = "", status: str = "low", parent=None):
        """
        Initialize metric card.

        Args:
            title: Card title
            value: Metric value
            status: Status level ("low", "medium", "high")
            parent: Parent widget
        """
        super().__init__(parent)

        # Create panel with depth
        self.panel = GlassmorphicPanel(self)
        self.panel.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        layout = QVBoxLayout(self.panel)
        layout.setSpacing(16)
        layout.setContentsMargins(28, 28, 28, 28)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Title with refined status indicator
        title_layout = QHBoxLayout()
        title_layout.setSpacing(10)
        title_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        # Sophisticated status indicator
        self.status_indicator = QLabel("●")
        self.status_indicator.setProperty("status", status)
        self.status_indicator.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.status_indicator.setStyleSheet(f"font-size: 16px;")
        title_layout.addWidget(self.status_indicator)

        self.title_label = QLabel(title.upper())
        self.title_label.setProperty("heading", "h3")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        title_layout.addWidget(self.title_label)

        layout.addLayout(title_layout)

        # Add subtle spacing
        layout.addSpacing(8)

        # Value with professional typography
        self.value_label = QLabel(value)
        self.value_label.setProperty("metricValue", "true")
        self.value_label.setProperty("status", status)
        self.value_label.setProperty("mono", "true")
        self.value_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.value_label.setWordWrap(True)
        self.value_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        self.value_label.setMinimumHeight(52)
        layout.addWidget(self.value_label)

        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(self.panel)

        self.setMinimumHeight(160)

    def update_value(self, value: str, status: str = None):
        """
        Update the metric value.

        Args:
            value: New value
            status: New status level (optional)
        """
        self.value_label.setText(value)
        if status:
            self.value_label.setProperty("status", status)
            self.status_indicator.setProperty("status", status)
            # Force style refresh
            self.value_label.style().unpolish(self.value_label)
            self.value_label.style().polish(self.value_label)
            self.status_indicator.style().unpolish(self.status_indicator)
            self.status_indicator.style().polish(self.status_indicator)


class StatRow(QWidget):
    """
    Row widget for displaying a statistic with label and value.
    """
    
    def __init__(self, label: str, value: str = "", parent=None):
        """
        Initialize stat row.
        
        Args:
            label: Label text
            value: Value text
            parent: Parent widget
        """
        super().__init__(parent)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 8, 0, 8)
        
        # Label
        self.label = QLabel(label)
        self.label.setProperty("mono", "true")
        layout.addWidget(self.label)
        
        # Spacer
        layout.addStretch()
        
        # Value
        self.value_label = QLabel(value)
        self.value_label.setProperty("mono", "true")
        layout.addWidget(self.value_label)
    
    def update_value(self, value: str):
        """
        Update the value.
        
        Args:
            value: New value
        """
        self.value_label.setText(value)


class SearchBar(QWidget):
    """
    Custom search bar with distinctive styling.
    """
    
    search_changed = pyqtSignal(str)
    
    def __init__(self, placeholder: str = "Search...", parent=None):
        """
        Initialize search bar.
        
        Args:
            placeholder: Placeholder text
            parent: Parent widget
        """
        super().__init__(parent)
        self.setMinimumHeight(44)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.line_edit = QLineEdit()
        self.line_edit.setPlaceholderText(f"🔍 {placeholder}")
        self.line_edit.setObjectName("searchField")
        self.line_edit.setClearButtonEnabled(True)
        self.line_edit.textChanged.connect(self.search_changed.emit)
        layout.addWidget(self.line_edit)
    
    def text(self) -> str:
        """Get search text."""
        return self.line_edit.text()
    
    def clear(self):
        """Clear search text."""
        self.line_edit.clear()
