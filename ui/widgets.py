"""
Custom styled widgets for the Mac Health Analyzer.
Includes toggle switches, styled buttons, and animated panels.
"""

from PyQt6.QtCore import Qt, pyqtSignal, QRect, QPropertyAnimation, QEasingCurve, pyqtProperty
from PyQt6.QtWidgets import QWidget, QPushButton, QFrame, QLabel, QHBoxLayout, QVBoxLayout
from PyQt6.QtGui import QPainter, QColor, QPen, QBrush
from ui.styles import COLORS


class ToggleSwitch(QWidget):
    """
    Custom toggle switch widget with smooth animation and neon glow.
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

        self.setFixedSize(50, 28)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        # Animation for smooth toggle
        self.animation = QPropertyAnimation(self, b"circle_position")
        self.animation.setDuration(200)
        self.animation.setEasingCurve(QEasingCurve.Type.InOutCubic)

    @pyqtProperty(int)
    def circle_position(self):
        """Get circle position for animation."""
        return self._circle_position

    @circle_position.setter
    def circle_position(self, pos):
        """Set circle position for animation."""
        self._circle_position = pos
        self.update()

    def paintEvent(self, event):
        """Paint the toggle switch with neon glow."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Draw background track
        if self._checked:
            bg_color = QColor(COLORS['terracotta'])
        else:
            bg_color = QColor(COLORS['border'])

        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(bg_color))
        painter.drawRoundedRect(0, 0, 50, 28, 0, 0)  # Square corners for brutalist style

        # Draw circle
        circle_color = QColor(COLORS['bg_card']) if self._checked else QColor(COLORS['text_secondary'])
        painter.setBrush(QBrush(circle_color))
        painter.drawEllipse(self._circle_position, 2, 24, 24)
    
    def mouseReleaseEvent(self, event):
        """Handle mouse click."""
        if event.button() == Qt.MouseButton.LeftButton:
            self._checked = not self._checked
            
            # Animate circle position
            if self._checked:
                self.animation.setStartValue(self._circle_position)
                self.animation.setEndValue(24)
            else:
                self.animation.setStartValue(self._circle_position)
                self.animation.setEndValue(2)
            
            self.animation.start()
            self.toggled.emit(self._checked)
    
    def setChecked(self, checked: bool):
        """Set checked state programmatically."""
        if self._checked != checked:
            self._checked = checked
            self._circle_position = 24 if checked else 2
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
    """
    Panel with glassmorphic effect.
    """
    
    def __init__(self, parent=None):
        """
        Initialize glassmorphic panel.
        
        Args:
            parent: Parent widget
        """
        super().__init__(parent)
        self.setProperty("panel", "true")
        self.setFrameShape(QFrame.Shape.StyledPanel)


class MetricCard(QWidget):
    """
    Enhanced card widget for displaying metrics with cyberpunk styling.
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

        # Create panel
        self.panel = GlassmorphicPanel(self)

        layout = QVBoxLayout(self.panel)
        layout.setSpacing(12)
        layout.setContentsMargins(24, 24, 24, 24)

        # Title with icon
        title_layout = QHBoxLayout()

        # Status indicator dot
        self.status_indicator = QLabel("●")
        self.status_indicator.setProperty("status", status)
        title_layout.addWidget(self.status_indicator)

        self.title_label = QLabel(title.upper())
        self.title_label.setProperty("heading", "h3")
        title_layout.addWidget(self.title_label)
        title_layout.addStretch()

        layout.addLayout(title_layout)

        # Value with glow effect
        self.value_label = QLabel(value)
        self.value_label.setProperty("heading", "h1")
        self.value_label.setProperty("status", status)
        self.value_label.setProperty("mono", "true")
        self.value_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(self.value_label)

        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(self.panel)

        self.setMinimumHeight(140)

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
        
        from PyQt6.QtWidgets import QLineEdit
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.line_edit = QLineEdit()
        self.line_edit.setPlaceholderText(placeholder)
        self.line_edit.textChanged.connect(self.search_changed.emit)
        
        layout.addWidget(self.line_edit)
    
    def text(self) -> str:
        """Get search text."""
        return self.line_edit.text()
    
    def clear(self):
        """Clear search text."""
        self.line_edit.clear()

