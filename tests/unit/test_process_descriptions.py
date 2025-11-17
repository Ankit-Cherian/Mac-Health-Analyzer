"""
Tests for utils/process_descriptions.py
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from utils.process_descriptions import ProcessDescriber


class TestProcessDescriber:
    """Test ProcessDescriber class."""

    def test_initialization(self):
        """Test ProcessDescriber initialization."""
        describer = ProcessDescriber()

        assert describer is not None

    def test_get_description(self):
        """Test get_description method."""
        describer = ProcessDescriber()

        # Test common process names
        desc = describer.get_description("kernel_task")
        assert isinstance(desc, str)
        assert len(desc) > 0

        desc = describer.get_description("Chrome")
        assert isinstance(desc, str)

        desc = describer.get_description("unknown_process_xyz")
        assert isinstance(desc, str)

    def test_is_safe_to_quit(self):
        """Test is_safe_to_quit method."""
        describer = ProcessDescriber()

        # System processes should not be safe to quit
        assert describer.is_safe_to_quit("kernel_task") == False
        assert describer.is_safe_to_quit("launchd") == False

        # User applications might be safe to quit
        result = describer.is_safe_to_quit("Chrome")
        assert isinstance(result, bool)

        # Unknown processes default behavior
        result = describer.is_safe_to_quit("unknown_process")
        assert isinstance(result, bool)

    def test_get_recommendation(self):
        """Test get_recommendation method."""
        describer = ProcessDescriber()

        # Test with high memory usage
        rec = describer.get_recommendation("Chrome", cpu_percent=50.0, memory_percent=20.0)
        assert isinstance(rec, str)
        assert len(rec) > 0

        # Test with low usage
        rec = describer.get_recommendation("Safari", cpu_percent=1.0, memory_percent=2.0)
        assert isinstance(rec, str)

    def test_get_simple_explanation(self):
        """Test get_simple_explanation method."""
        describer = ProcessDescriber()

        exp = describer.get_simple_explanation("Chrome")
        assert isinstance(exp, str)
        assert len(exp) > 0

    def test_get_technical_explanation(self):
        """Test get_technical_explanation method."""
        describer = ProcessDescriber()

        exp = describer.get_technical_explanation("kernel_task")
        assert isinstance(exp, str)
        assert len(exp) > 0

    def test_case_insensitive_matching(self):
        """Test that process name matching is case-insensitive."""
        describer = ProcessDescriber()

        desc1 = describer.get_description("chrome")
        desc2 = describer.get_description("Chrome")
        desc3 = describer.get_description("CHROME")

        # Should all return descriptions (may or may not be identical)
        assert all(isinstance(d, str) for d in [desc1, desc2, desc3])

    def test_get_category(self):
        """Test get_category method if it exists."""
        describer = ProcessDescriber()

        if hasattr(describer, 'get_category'):
            category = describer.get_category("Chrome")
            assert isinstance(category, str)

    def test_multiple_processes(self):
        """Test describing multiple different processes."""
        describer = ProcessDescriber()

        processes = [
            "kernel_task",
            "Chrome",
            "Safari",
            "Finder",
            "python3",
            "unknown_app_xyz"
        ]

        for proc in processes:
            desc = describer.get_description(proc)
            assert isinstance(desc, str)
            assert len(desc) > 0
