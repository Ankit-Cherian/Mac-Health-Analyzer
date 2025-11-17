"""
Chart widgets for Mac Health Analyzer - Neo-Brutalist Earth Edition.
Clean, readable visualizations with bold geometric design.
"""

from collections import deque
import pyqtgraph as pg
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QSize
from PyQt6.QtGui import QPainter, QColor, QPen, QBrush, QLinearGradient, QConicalGradient
from .styles import COLORS


# Configure PyQtGraph for light theme
pg.setConfigOption('background', COLORS['bg_primary'])
pg.setConfigOption('foreground', COLORS['text_primary'])
pg.setConfigOption('antialias', True)


class RealtimeLineChart(QWidget):
    """
    Real-time line chart with neon glow effect for CPU/Memory monitoring.
    """

    def __init__(self, title: str = "Metric", max_points: int = 60, parent=None):
        super().__init__(parent)
        self.title = title
        self.max_points = max_points
        self.data_points = deque(maxlen=max_points)
        self.current_value_label = None

        self.setup_ui()

    def setup_ui(self):
        """Setup the chart UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.title_label = QLabel(self.title.upper())
        self.title_label.setProperty("chartTitle", "true")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.title_label)

        # Add current value label at the top
        self.current_value_label = QLabel("--")
        self.current_value_label.setStyleSheet(f"""
            color: {COLORS['terracotta']};
            font-size: 24px;
            font-weight: bold;
            padding: 8px;
            background-color: {COLORS['bg_card']};
        """)
        self.current_value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.current_value_label)

        # Create plot widget
        self.plot_widget = pg.PlotWidget()
        self.plot_widget.setBackground(COLORS['bg_card'])
        # Use very light grid lines to avoid overwhelming the nested card layout
        self.plot_widget.showGrid(x=True, y=True, alpha=0.08)
        self.plot_widget.setMouseEnabled(x=False, y=False)
        self.plot_widget.setMenuEnabled(False)
        self.plot_widget.hideButtons()

        # Style the plot with clearer labels
        self.plot_widget.setLabel('left', self.title, color=COLORS['terracotta'],
                                  **{'font-size': '14pt', 'font-weight': 'bold'})
        self.plot_widget.setLabel('bottom', 'Time (seconds ago)', color=COLORS['text_secondary'],
                                  **{'font-size': '12pt', 'font-weight': 'bold'})

        # Set axis color and styling
        axis_pen = pg.mkPen(color=COLORS['border'], width=1)
        left_axis = self.plot_widget.getAxis('left')
        bottom_axis = self.plot_widget.getAxis('bottom')

        left_axis.setPen(axis_pen)
        bottom_axis.setPen(axis_pen)

        # Make axis labels more visible
        left_axis.setStyle(tickTextOffset=10)
        bottom_axis.setStyle(tickTextOffset=10)

        # Set fixed ranges to keep the chart scale stable
        self.plot_widget.setYRange(0, 100)
        self.plot_widget.enableAutoRange(axis='xy', enable=False)
        self.plot_widget.setLimits(xMin=0, xMax=self.max_points, yMin=0, yMax=100)

        # Add percentage symbols to Y-axis if this is a percentage chart
        if '%' in self.title:
            left_axis.setLabel(units='%')

        # Create the line with bold style
        line_pen = pg.mkPen(color=COLORS['terracotta'], width=3)
        self.data_line = self.plot_widget.plot(
            pen=line_pen,
            name=self.title
        )

        # Create fill area under the curve
        terracotta_rgb = QColor(COLORS['terracotta'])
        self.fill_curve = pg.PlotCurveItem(pen=None,
                                           brush=(terracotta_rgb.red(), terracotta_rgb.green(),
                                                 terracotta_rgb.blue(), 40),  # Semi-transparent
                                           fillLevel=0)
        self.plot_widget.addItem(self.fill_curve)

        layout.addWidget(self.plot_widget)

    def update_data(self, value: float):
        """
        Add a new data point and update the chart.

        Args:
            value: New value to add (0-100)
        """
        self.data_points.append(value)

        # Update current value label
        if self.current_value_label:
            self.current_value_label.setText(f"{value:.1f}%")

        # Update the line
        x_data = list(range(len(self.data_points)))
        y_data = list(self.data_points)

        self.data_line.setData(x_data, y_data)
        self.fill_curve.setData(x_data, y_data)
        if self.max_points > 1:
            self.plot_widget.setXRange(0, self.max_points - 1, padding=0)
        self.plot_widget.setYRange(0, 100, padding=0)

    def clear(self):
        """Clear all data points."""
        self.data_points.clear()
        self.data_line.clear()
        self.fill_curve.clear()


class CircularGauge(QWidget):
    """
    Circular gauge widget with neon cyberpunk styling.
    """

    def __init__(self, title: str = "Metric", unit: str = "%", parent=None):
        super().__init__(parent)
        self.title = title
        self.unit = unit
        self.value = 0.0
        self.max_value = 100.0

        self.setMinimumSize(200, 220)

    def set_value(self, value: float, max_value: float = 100.0):
        """
        Set the gauge value.

        Args:
            value: Current value
            max_value: Maximum value
        """
        self.value = value
        self.max_value = max_value
        self.update()

    def get_color_for_value(self) -> str:
        """Get color based on value percentage."""
        percent = (self.value / self.max_value) * 100 if self.max_value > 0 else 0

        if percent < 50:
            return COLORS['sage']
        elif percent < 80:
            return COLORS['mustard']
        else:
            return COLORS['terracotta']

    def paintEvent(self, event):
        """Paint the circular gauge."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        width = self.width()
        height = self.height() - 40  # Leave space for title
        size = min(width, height)

        # Center the gauge
        center_x = width // 2
        center_y = (height // 2) + 20
        radius = (size // 2) - 20

        # Draw background circle
        bg_pen = QPen(QColor(COLORS['border']), 12, Qt.PenStyle.SolidLine)
        bg_pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        painter.setPen(bg_pen)
        painter.drawArc(center_x - radius, center_y - radius,
                       radius * 2, radius * 2,
                       0, 360 * 16)

        # Draw value arc with gradient
        value_percent = (self.value / self.max_value) if self.max_value > 0 else 0
        span_angle = int(value_percent * 360 * 16)

        color = self.get_color_for_value()
        value_pen = QPen(QColor(color), 12, Qt.PenStyle.SolidLine)
        value_pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        painter.setPen(value_pen)

        # Start from top (90 degrees)
        start_angle = 90 * 16
        painter.drawArc(center_x - radius, center_y - radius,
                       radius * 2, radius * 2,
                       start_angle, -span_angle)

        # Draw center circle
        center_radius = radius - 30
        gradient = QConicalGradient(center_x, center_y, 0)
        gradient.setColorAt(0, QColor(COLORS['bg_card']))
        gradient.setColorAt(1, QColor(COLORS['bg_secondary']))

        painter.setBrush(QBrush(gradient))
        painter.setPen(QPen(QColor(color), 2))
        painter.drawEllipse(center_x - center_radius, center_y - center_radius,
                           center_radius * 2, center_radius * 2)

        # Draw value text
        painter.setPen(QColor(color))
        painter.setFont(self.font())

        # Value
        value_font = painter.font()
        value_font.setPointSize(24)
        value_font.setBold(True)
        painter.setFont(value_font)

        value_text = f"{self.value:.1f}" if isinstance(self.value, float) else str(self.value)
        value_rect = painter.fontMetrics().boundingRect(value_text)
        painter.drawText(center_x - value_rect.width() // 2,
                        center_y + value_rect.height() // 4,
                        value_text)

        # Unit
        unit_font = painter.font()
        unit_font.setPointSize(12)
        unit_font.setBold(False)
        painter.setFont(unit_font)
        painter.setPen(QColor(COLORS['text_secondary']))

        unit_rect = painter.fontMetrics().boundingRect(self.unit)
        painter.drawText(center_x - unit_rect.width() // 2,
                        center_y + value_rect.height() + 10,
                        self.unit)

        # Draw title at top
        title_font = painter.font()
        title_font.setPointSize(14)
        title_font.setBold(True)
        painter.setFont(title_font)
        painter.setPen(QColor(COLORS['text_primary']))

        title_rect = painter.fontMetrics().boundingRect(self.title)
        painter.drawText(center_x - title_rect.width() // 2, 18, self.title)


class SparkLine(QWidget):
    """
    Mini sparkline chart for inline metrics.
    """

    def __init__(self, max_points: int = 20, parent=None):
        super().__init__(parent)
        self.max_points = max_points
        self.data_points = deque(maxlen=max_points)
        self.setMinimumSize(100, 40)
        self.setMaximumHeight(50)

    def add_point(self, value: float):
        """Add a data point."""
        self.data_points.append(value)
        self.update()

    def paintEvent(self, event):
        """Paint the sparkline."""
        if len(self.data_points) < 2:
            return

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        width = self.width()
        height = self.height()

        # Calculate points
        max_val = max(self.data_points) if self.data_points else 100
        min_val = min(self.data_points) if self.data_points else 0
        value_range = max_val - min_val if max_val != min_val else 1

        points = []
        step = width / (len(self.data_points) - 1)

        for i, value in enumerate(self.data_points):
            x = i * step
            # Invert y because Qt coordinates go down
            y = height - ((value - min_val) / value_range * (height - 10)) - 5
            points.append((x, y))

        # Draw line
        pen = QPen(QColor(COLORS['clay']), 2)
        painter.setPen(pen)

        for i in range(len(points) - 1):
            painter.drawLine(int(points[i][0]), int(points[i][1]),
                           int(points[i + 1][0]), int(points[i + 1][1]))


class BarChart(QWidget):
    """
    Horizontal bar chart for process resources.
    """

    clicked = pyqtSignal(dict)  # Emit the data entry for the double-clicked bar

    def __init__(self, title: str = "Processes", parent=None):
        super().__init__(parent)
        self.title = title
        self.data = []  # Normalized list of dict entries
        self.bar_rects = []  # Store bar rectangles for click detection

        self.setMinimumSize(300, 200)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

    def set_data(self, data: list):
        """
        Set bar chart data.

        Args:
            data: Iterable of dicts or tuples describing each bar.
                  Supported formats:
                    - {'label': str, 'value': float, 'max': float, 'payload': Any}
                    - (label, value, max[, payload])
        """
        normalized = []
        for item in data[:10]:
            if isinstance(item, dict):
                normalized.append({
                    'label': item.get('label', ''),
                    'value': item.get('value', 0),
                    'max': item.get('max', 100),
                    'payload': item.get('payload')
                })
            elif isinstance(item, (list, tuple)):
                label = item[0] if len(item) > 0 else ''
                value = item[1] if len(item) > 1 else 0
                max_value = item[2] if len(item) > 2 else 100
                payload = item[3] if len(item) > 3 else None
                normalized.append({
                    'label': label,
                    'value': value,
                    'max': max_value,
                    'payload': payload
                })

        self.data = normalized
        self.update()

    def paintEvent(self, event):
        """Paint the bar chart."""
        if not self.data:
            return

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        width = self.width()
        height = self.height()

        # Title
        painter.setPen(QColor(COLORS['text_primary']))
        title_font = painter.font()
        title_font.setPointSize(14)
        title_font.setBold(True)
        painter.setFont(title_font)
        painter.drawText(10, 20, self.title)

        # Hint text
        hint_font = painter.font()
        hint_font.setPointSize(10)
        painter.setFont(hint_font)
        painter.setPen(QColor(COLORS['text_secondary']))
        painter.drawText(width - 280, 20, "Double-click to learn more")

        # Draw bars
        bar_height = 25
        bar_spacing = 8
        start_y = 40
        max_bar_width = width - 120

        painter.setFont(self.font())

        # Clear previous bar rectangles
        self.bar_rects = []

        metrics = painter.fontMetrics()

        for i, entry in enumerate(self.data):
            label = entry.get('label', '')
            value = entry.get('value', 0)
            max_value = entry.get('max', 100)
            y = start_y + i * (bar_height + bar_spacing)

            # Calculate bar width
            percent = (value / max_value) if max_value > 0 else 0
            bar_width = int(percent * max_bar_width)

            # Color based on percentage
            if percent < 0.5:
                color = COLORS['sage']
            elif percent < 0.8:
                color = COLORS['mustard']
            else:
                color = COLORS['terracotta']

            # Draw background bar
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(QColor(COLORS['border']))
            painter.drawRoundedRect(80, y, max_bar_width, bar_height, 4, 4)

            # Draw value bar with gradient
            if bar_width > 0:
                gradient = QLinearGradient(80, y, 80 + bar_width, y)
                gradient.setColorAt(0, QColor(color))
                gradient.setColorAt(1, QColor(color).darker(120))

                painter.setBrush(gradient)
                painter.drawRoundedRect(80, y, bar_width, bar_height, 4, 4)

            # Store bar rectangle for click detection
            from PyQt6.QtCore import QRect
            bar_rect = QRect(10, y, max_bar_width + 80, bar_height)
            self.bar_rects.append((bar_rect, entry))

            # Draw label
            painter.setPen(QColor(COLORS['text_primary']))
            display_label = metrics.elidedText(label, Qt.TextElideMode.ElideRight, 70)
            painter.drawText(10, y + 17, display_label)

            # Draw value with unit
            painter.setPen(QColor(color))
            value_text = f"{value:.1f}%" if isinstance(value, float) else str(value)
            painter.drawText(max_bar_width + 90, y + 17, value_text)

    def mouseDoubleClickEvent(self, event):
        """Handle double-click on bars."""
        from PyQt6.QtCore import QPoint
        click_pos = event.pos()

        # Check if click is on any bar
        for bar_rect, entry in self.bar_rects:
            if bar_rect.contains(click_pos):
                # Emit signal with the entire entry (label, value, payload)
                self.clicked.emit(entry)
                return

        super().mouseDoubleClickEvent(event)

    def sizeHint(self):
        """Suggest size based on data."""
        bar_height = 25
        bar_spacing = 8
        title_height = 40

        height = title_height + len(self.data) * (bar_height + bar_spacing)
        return self.minimumSize().expandedTo(QSize(300, height))
