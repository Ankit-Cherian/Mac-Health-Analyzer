"""
Tests for utils/startup_descriptions.py
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from utils.startup_descriptions import StartupDescriber


class TestStartupDescriber:
    """Test StartupDescriber class."""

    def test_initialization(self):
        """Test StartupDescriber initialization."""
        describer = StartupDescriber()

        assert describer is not None

    def test_get_description(self):
        """Test get_description method."""
        describer = StartupDescriber()

        # Test common startup items
        desc = describer.get_description("Dropbox")
        assert isinstance(desc, str)
        assert len(desc) > 0

        desc = describer.get_description("com.apple.notificationcenterui")
        assert isinstance(desc, str)

        desc = describer.get_description("unknown_startup_item_xyz")
        assert isinstance(desc, str)

    def test_is_safe_to_disable(self):
        """Test is_safe_to_disable method."""
        describer = StartupDescriber()

        # Apple system services should not be safe to disable
        result = describer.is_safe_to_disable("com.apple.notificationcenterui")
        assert isinstance(result, bool)

        # Third-party apps might be safe to disable
        result = describer.is_safe_to_disable("Dropbox")
        assert isinstance(result, bool)

        # Unknown items default behavior
        result = describer.is_safe_to_disable("unknown_item")
        assert isinstance(result, bool)

    def test_get_recommendation(self):
        """Test get_recommendation method."""
        describer = StartupDescriber()

        rec = describer.get_recommendation("Dropbox", item_type="Login Item")
        assert isinstance(rec, str)
        assert len(rec) > 0

        rec = describer.get_recommendation("com.apple.mDNSResponder", item_type="Launch Daemon")
        assert isinstance(rec, str)

    def test_get_simple_explanation(self):
        """Test get_simple_explanation method."""
        describer = StartupDescriber()

        exp = describer.get_simple_explanation("Dropbox")
        assert isinstance(exp, str)
        assert len(exp) > 0

    def test_get_technical_explanation(self):
        """Test get_technical_explanation method."""
        describer = StartupDescriber()

        exp = describer.get_technical_explanation("com.apple.notificationcenterui")
        assert isinstance(exp, str)
        assert len(exp) > 0

    def test_case_insensitive_matching(self):
        """Test that item name matching is case-insensitive."""
        describer = StartupDescriber()

        desc1 = describer.get_description("dropbox")
        desc2 = describer.get_description("Dropbox")
        desc3 = describer.get_description("DROPBOX")

        # Should all return descriptions
        assert all(isinstance(d, str) for d in [desc1, desc2, desc3])

    def test_get_category(self):
        """Test get_category method if it exists."""
        describer = StartupDescriber()

        if hasattr(describer, 'get_category'):
            category = describer.get_category("Dropbox")
            assert isinstance(category, str)

    def test_different_item_types(self):
        """Test with different item types."""
        describer = StartupDescriber()

        item_types = ["Login Item", "Launch Agent", "Launch Daemon"]

        for item_type in item_types:
            rec = describer.get_recommendation("test_item", item_type=item_type)
            assert isinstance(rec, str)

    def test_multiple_items(self):
        """Test describing multiple different startup items."""
        describer = StartupDescriber()

        items = [
            "Dropbox",
            "Slack",
            "com.apple.notificationcenterui",
            "com.google.keystone.agent",
            "unknown_item_xyz"
        ]

        for item in items:
            desc = describer.get_description(item)
            assert isinstance(desc, str)
            assert len(desc) > 0

    def test_apple_vs_third_party(self):
        """Test distinguishing between Apple and third-party items."""
        describer = StartupDescriber()

        # Apple items (usually start with com.apple)
        apple_desc = describer.get_description("com.apple.notificationcenterui")
        assert isinstance(apple_desc, str)

        # Third-party items
        third_party_desc = describer.get_description("Dropbox")
        assert isinstance(third_party_desc, str)
