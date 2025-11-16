"""
Tests for ui/widgets.py - Custom widgets
"""

import sys
from pathlib import Path
from unittest.mock import Mock, patch

import pytest
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter, QMouseEvent, QEnterEvent
from PyQt6.QtWidgets import QApplication

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from ui.widgets import ToggleSwitch, StyledButton, GlassmorphicPanel, MetricCard, StatRow, SearchBar


class TestToggleSwitch:
    """Test ToggleSwitch widget."""

    def test_initialization(self, qapp):
        """Test ToggleSwitch initialization."""
        switch = ToggleSwitch()

        assert switch._checked == False
        assert switch._circle_position == 2

    def test_initialization_checked(self, qapp):
        """Test ToggleSwitch initialization with checked state."""
        switch = ToggleSwitch(initial_state=True)

        assert switch._checked == True
        assert switch._circle_position == 24

    def test_circle_position_property(self, qapp):
        """Test circle_position property."""
        switch = ToggleSwitch()

        # Test getter
        assert switch.circle_position == 2

        # Test setter
        switch.circle_position = 24
        assert switch._circle_position == 24

    def test_paint_event(self, qapp):
        """Test paint event."""
        switch = ToggleSwitch()

        # Create a paint event (just verify it doesn't crash)
        switch.show()
        switch.update()

    def test_mouse_release_event(self, qapp):
        """Test mouse release event."""
        switch = ToggleSwitch(initial_state=False)

        # Track toggle signal
        toggled = []
        switch.toggled.connect(lambda state: toggled.append(state))

        # Create a mock mouse event
        event = Mock()
        event.button.return_value = Qt.MouseButton.LeftButton

        switch.mouseReleaseEvent(event)

        # Should toggle state
        assert switch._checked == True
        assert len(toggled) == 1
        assert toggled[0] == True

    def test_set_checked(self, qapp):
        """Test setChecked method."""
        switch = ToggleSwitch()

        switch.setChecked(True)
        assert switch._checked == True
        assert switch._circle_position == 24

        switch.setChecked(False)
        assert switch._checked == False
        assert switch._circle_position == 2

    def test_is_checked(self, qapp):
        """Test isChecked method."""
        switch = ToggleSwitch(initial_state=True)

        assert switch.isChecked() == True

        switch.setChecked(False)
        assert switch.isChecked() == False


class TestStyledButton:
    """Test StyledButton widget."""

    def test_initialization_primary(self, qapp):
        """Test StyledButton initialization with primary type."""
        button = StyledButton("Click Me", "primary")

        assert button.text() == "Click Me"
        assert button.button_type == "primary"

    def test_initialization_danger(self, qapp):
        """Test StyledButton initialization with danger type."""
        button = StyledButton("Delete", "danger")

        assert button.text() == "Delete"
        assert button.button_type == "danger"
        assert button.property("danger") == "true"

    def test_initialization_secondary(self, qapp):
        """Test StyledButton initialization with secondary type."""
        button = StyledButton("Cancel", "secondary")

        assert button.text() == "Cancel"
        assert button.button_type == "secondary"


class TestGlassmorphicPanel:
    """Test GlassmorphicPanel widget."""

    def test_initialization(self, qapp):
        """Test GlassmorphicPanel initialization."""
        panel = GlassmorphicPanel()

        assert panel.property("panel") == "true"
        assert panel.property("panelVariant") == "primary"

    def test_minimal_variant(self, qapp):
        """Ensure alternate variants set the proper style hints."""
        panel = GlassmorphicPanel(variant="minimal")

        assert panel.property("panelVariant") == "minimal"


class TestMetricCard:
    """Test MetricCard widget."""

    def test_initialization(self, qapp):
        """Test MetricCard initialization."""
        card = MetricCard("CPU Usage", "45%", "medium")

        assert card.title_label.text() == "CPU USAGE"
        assert card.value_label.text() == "45%"

    def test_update_value(self, qapp):
        """Test update_value method."""
        card = MetricCard("Memory", "50%", "low")

        card.update_value("75%", "high")

        assert card.value_label.text() == "75%"
        assert card.value_label.property("status") == "high"
        assert card.status_indicator.property("status") == "high"

    def test_update_value_without_status(self, qapp):
        """Test update_value without changing status."""
        card = MetricCard("Memory", "50%", "low")

        card.update_value("60%")

        assert card.value_label.text() == "60%"


class TestStatRow:
    """Test StatRow widget."""

    def test_initialization(self, qapp):
        """Test StatRow initialization."""
        row = StatRow("Total Memory", "16 GB")

        assert row.label.text() == "Total Memory"
        assert row.value_label.text() == "16 GB"

    def test_update_value(self, qapp):
        """Test update_value method."""
        row = StatRow("CPU Cores", "8")

        row.update_value("16")

        assert row.value_label.text() == "16"


class TestSearchBar:
    """Test SearchBar widget."""

    def test_initialization(self, qapp):
        """Test SearchBar initialization."""
        search_bar = SearchBar("Search items...")

        assert "Search items..." in search_bar.line_edit.placeholderText()

    def test_text_method(self, qapp):
        """Test text method."""
        search_bar = SearchBar()

        search_bar.line_edit.setText("test query")
        assert search_bar.text() == "test query"

    def test_clear_method(self, qapp):
        """Test clear method."""
        search_bar = SearchBar()

        search_bar.line_edit.setText("test query")
        search_bar.clear()

        assert search_bar.text() == ""

    def test_search_changed_signal(self, qapp):
        """Test search_changed signal."""
        search_bar = SearchBar()

        # Track signal emissions
        signals = []
        search_bar.search_changed.connect(lambda text: signals.append(text))

        search_bar.line_edit.setText("test")

        assert len(signals) > 0
        assert signals[-1] == "test"
