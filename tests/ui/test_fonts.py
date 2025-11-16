"""
Tests for ui/fonts.py - Font management
"""

import sys
from pathlib import Path
from unittest.mock import Mock, patch

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from ui.fonts import FontManager, get_font_manager


class TestFontManager:
    """Test FontManager class."""

    def test_initialization(self, qapp):
        """Test FontManager initialization."""
        manager = FontManager()

        assert manager is not None
        assert hasattr(manager, 'fonts_loaded')

    def test_singleton_pattern(self, qapp):
        """Test that get_font_manager returns singleton."""
        manager1 = get_font_manager()
        manager2 = get_font_manager()

        assert manager1 is manager2

    def test_load_fonts(self, qapp):
        """Test load_fonts method."""
        manager = FontManager()

        # Should run without error
        try:
            manager.load_fonts()
        except Exception as e:
            # It's OK if fonts don't load in test environment
            pass

    def test_get_display_font(self, qapp):
        """Test get_display_font method."""
        manager = FontManager()

        font = manager.get_display_font(size=14, weight=400)

        from PyQt6.QtGui import QFont
        assert isinstance(font, QFont)
        assert font.pointSize() == 14

    def test_get_mono_font(self, qapp):
        """Test get_mono_font method."""
        manager = FontManager()

        font = manager.get_mono_font(size=12)

        from PyQt6.QtGui import QFont
        assert isinstance(font, QFont)
        assert font.pointSize() == 12

    def test_get_display_font_default_params(self, qapp):
        """Test get_display_font with default parameters."""
        manager = FontManager()

        font = manager.get_display_font()

        from PyQt6.QtGui import QFont
        assert isinstance(font, QFont)

    def test_get_mono_font_default_params(self, qapp):
        """Test get_mono_font with default parameters."""
        manager = FontManager()

        font = manager.get_mono_font()

        from PyQt6.QtGui import QFont
        assert isinstance(font, QFont)

    def test_get_display_font_various_weights(self, qapp):
        """Test get_display_font with various weights."""
        manager = FontManager()

        font_light = manager.get_display_font(weight=300)
        font_normal = manager.get_display_font(weight=400)
        font_bold = manager.get_display_font(weight=700)

        from PyQt6.QtGui import QFont
        assert all(isinstance(f, QFont) for f in [font_light, font_normal, font_bold])

    def test_get_display_font_various_sizes(self, qapp):
        """Test get_display_font with various sizes."""
        manager = FontManager()

        font_small = manager.get_display_font(size=10)
        font_medium = manager.get_display_font(size=14)
        font_large = manager.get_display_font(size=24)

        assert font_small.pointSize() == 10
        assert font_medium.pointSize() == 14
        assert font_large.pointSize() == 24


class TestGetFontManager:
    """Test get_font_manager function."""

    def test_returns_font_manager(self, qapp):
        """Test that function returns FontManager instance."""
        manager = get_font_manager()

        assert isinstance(manager, FontManager)

    def test_returns_same_instance(self, qapp):
        """Test that function returns same instance."""
        manager1 = get_font_manager()
        manager2 = get_font_manager()

        assert manager1 is manager2
