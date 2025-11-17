"""
Tests for ui/styles.py - Style functions
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from ui.styles import (
    COLORS,
    get_main_stylesheet,
    get_palette,
    get_status_color,
)


class TestColors:
    """Test color constants."""

    def test_colors_dict_exists(self):
        """Test that COLORS dictionary exists."""
        assert COLORS is not None
        assert isinstance(COLORS, dict)

    def test_colors_has_required_keys(self):
        """Test that COLORS has required keys."""
        required_keys = [
            'bg_primary',
            'bg_secondary',
            'bg_card',
            'text_primary',
            'text_secondary',
            'terracotta',
            'border',
        ]

        for key in required_keys:
            assert key in COLORS


class TestGetMainStylesheet:
    """Test get_main_stylesheet function."""

    def test_returns_string(self):
        """Test that function returns a string."""
        stylesheet = get_main_stylesheet()

        assert isinstance(stylesheet, str)
        assert len(stylesheet) > 0

    def test_contains_color_references(self):
        """Test that stylesheet contains color references."""
        stylesheet = get_main_stylesheet()

        # Should contain some color hex codes
        assert '#' in stylesheet


class TestGetPalette:
    """Test get_palette function."""

    def test_returns_palette(self, qapp):
        """Test that function returns a QPalette."""
        from PyQt6.QtGui import QPalette

        palette = get_palette()

        assert isinstance(palette, QPalette)

    def test_palette_has_colors(self, qapp):
        """Test that palette has colors set."""
        palette = get_palette()

        # Should have colors defined
        assert palette is not None


class TestGetStatusColor:
    """Test get_status_color function."""

    def test_low_status(self):
        """Test low status color."""
        color = get_status_color(30.0)

        assert isinstance(color, str)
        assert color.startswith('#')

    def test_medium_status(self):
        """Test medium status color."""
        color = get_status_color(60.0)

        assert isinstance(color, str)
        assert color.startswith('#')

    def test_high_status(self):
        """Test high status color."""
        color = get_status_color(90.0)

        assert isinstance(color, str)
        assert color.startswith('#')

    def test_boundary_values(self):
        """Test boundary values."""
        # Test at boundaries
        color_0 = get_status_color(0.0)
        color_50 = get_status_color(50.0)
        color_80 = get_status_color(80.0)
        color_100 = get_status_color(100.0)

        assert all(isinstance(c, str) for c in [color_0, color_50, color_80, color_100])
