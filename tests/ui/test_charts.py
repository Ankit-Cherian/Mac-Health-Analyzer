"""
Tests for ui/charts.py - Chart widgets
"""

import sys
from pathlib import Path
from unittest.mock import Mock, patch

import pytest
from PyQt6.QtCore import Qt

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from ui.charts import RealtimeLineChart, CircularGauge, BarChart


class TestRealtimeLineChart:
    """Test RealtimeLineChart widget."""

    def test_initialization(self, qapp):
        """Test RealtimeLineChart initialization."""
        chart = RealtimeLineChart("CPU Usage", max_points=30)

        assert chart.title == "CPU Usage"
        assert chart.max_points == 30
        assert len(chart.data_points) == 0

    def test_setup_ui(self, qapp):
        """Test UI setup."""
        chart = RealtimeLineChart("Memory Usage")

        assert chart.title_label is not None
        assert chart.plot_widget is not None
        assert chart.current_value_label is not None

    def test_update_data(self, qapp):
        """Test data update."""
        chart = RealtimeLineChart("CPU Usage", max_points=10)

        chart.update_data(50.0)

        assert len(chart.data_points) == 1
        assert chart.data_points[0] == 50.0
        assert chart.current_value_label.text() == "50.0%"

    def test_update_data_multiple(self, qapp):
        """Test multiple data updates."""
        chart = RealtimeLineChart("CPU Usage", max_points=5)

        for i in range(10):
            chart.update_data(float(i * 10))

        # Should be limited to max_points
        assert len(chart.data_points) == 5
        assert chart.data_points[-1] == 90.0

    def test_clear(self, qapp):
        """Test clear method."""
        chart = RealtimeLineChart("CPU Usage")

        chart.update_data(50.0)
        chart.update_data(60.0)

        chart.clear()

        assert len(chart.data_points) == 0


class TestCircularGauge:
    """Test CircularGauge widget."""

    def test_initialization(self, qapp):
        """Test CircularGauge initialization."""
        gauge = CircularGauge("CPU", "%")

        assert gauge.title == "CPU"
        assert gauge.unit == "%"
        assert gauge.value == 0.0
        assert gauge.max_value == 100.0

    def test_set_value(self, qapp):
        """Test set_value method."""
        gauge = CircularGauge("Memory", "%")

        gauge.set_value(75.0, 100.0)

        assert gauge.value == 75.0
        assert gauge.max_value == 100.0

    def test_set_value_updates_display(self, qapp):
        """Test that set_value triggers display update."""
        gauge = CircularGauge("CPU", "%")

        gauge.set_value(50.0, 100.0)

        # Should update without error
        gauge.update()

    def test_paint_event(self, qapp):
        """Test paint event."""
        gauge = CircularGauge("Processes", "")

        gauge.set_value(150, 500)

        # Should paint without error
        gauge.show()
        gauge.update()


class TestBarChart:
    """Test BarChart widget."""

    def test_initialization(self, qapp):
        """Test BarChart initialization."""
        chart = BarChart("Top Memory")

        assert chart.title == "Top Memory"
        assert len(chart.data) == 0

    def test_set_data(self, qapp):
        """Test set_data method."""
        chart = BarChart("Top CPU")

        data = [
            {'label': 'Chrome', 'value': 45.0, 'max': 100},
            {'label': 'Firefox', 'value': 30.0, 'max': 100},
        ]

        chart.set_data(data)

        assert len(chart.data) == 2
        assert chart.data[0]['label'] == 'Chrome'

    def test_set_data_updates_display(self, qapp):
        """Test that set_data triggers display update."""
        chart = BarChart("Top Memory")

        data = [
            {'label': 'Chrome', 'value': 45.0, 'max': 100},
        ]

        chart.set_data(data)

        # Should update without error
        chart.update()

    def test_mouse_double_click_event(self, qapp):
        """Test mouse double-click event."""
        chart = BarChart("Top CPU")

        data = [
            {'label': 'Chrome', 'value': 45.0, 'max': 100, 'payload': {'pid': 123}},
        ]
        chart.set_data(data)

        # Track signal emissions
        signals = []
        chart.clicked.connect(lambda entry: signals.append(entry))

        # Create a mock mouse event
        event = Mock()
        event.button.return_value = Qt.MouseButton.LeftButton
        event.pos.return_value.x.return_value = 100
        event.pos.return_value.y.return_value = 100

        # Simulate double-click
        chart.mouseDoubleClickEvent(event)

        # Signal should be emitted (if clicked on a valid bar)
        # Note: actual click detection depends on geometry, so we just verify no crash

    def test_paint_event(self, qapp):
        """Test paint event."""
        chart = BarChart("Top Memory")

        data = [
            {'label': 'Chrome', 'value': 45.0, 'max': 100},
            {'label': 'Firefox', 'value': 30.0, 'max': 100},
        ]
        chart.set_data(data)

        # Should paint without error
        chart.show()
        chart.update()

    def test_clear_data(self, qapp):
        """Test clearing data."""
        chart = BarChart("Top CPU")

        data = [
            {'label': 'Chrome', 'value': 45.0, 'max': 100},
        ]
        chart.set_data(data)

        chart.set_data([])

        assert len(chart.data) == 0
