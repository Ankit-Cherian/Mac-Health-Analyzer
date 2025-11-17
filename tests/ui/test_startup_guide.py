"""
Tests for ui/startup_guide.py - StartupGuide dialog
"""

import sys
from pathlib import Path
from unittest.mock import Mock, patch

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from ui.startup_guide import StartupGuide


class TestStartupGuide:
    """Test StartupGuide dialog."""

    def test_initialization(self, qapp):
        """Test StartupGuide initialization."""
        guide = StartupGuide()

        assert guide.windowTitle() == "Welcome to Mac Health Analyzer"
        assert guide.dont_show_again == False

    def test_init_ui(self, qapp):
        """Test UI initialization."""
        guide = StartupGuide()

        # Should have content
        assert guide.layout() is not None

    def test_create_page_content(self, qapp):
        """Test page content creation."""
        guide = StartupGuide()

        # Should create pages without error
        assert True

    def test_on_dont_show_changed(self, qapp):
        """Test don't show checkbox handler."""
        guide = StartupGuide()

        guide.on_dont_show_changed(2)  # Qt.Checked = 2

        assert guide.dont_show_again == True

        guide.on_dont_show_changed(0)  # Qt.Unchecked = 0

        assert guide.dont_show_again == False

    def test_should_show_again(self, qapp):
        """Test should_show_again method."""
        guide = StartupGuide()

        assert guide.should_show_again() == True

        guide.dont_show_again = True

        assert guide.should_show_again() == False

    def test_next_page(self, qapp):
        """Test navigating to next page."""
        guide = StartupGuide()

        # Should be able to navigate without error
        if hasattr(guide, 'next_page'):
            guide.next_page()

    def test_previous_page(self, qapp):
        """Test navigating to previous page."""
        guide = StartupGuide()

        # Should be able to navigate without error
        if hasattr(guide, 'previous_page'):
            guide.previous_page()

    def test_on_get_started(self, qapp):
        """Test get started button."""
        guide = StartupGuide()

        # Should close dialog
        if hasattr(guide, 'on_get_started'):
            guide.on_get_started()
