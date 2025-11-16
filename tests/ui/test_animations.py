"""
Tests for ui/animations.py - Animation helper
"""

import sys
from pathlib import Path
from unittest.mock import Mock, patch

import pytest
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import QPropertyAnimation

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from ui.animations import AnimationHelper


class TestAnimationHelper:
    """Test AnimationHelper class."""

    def test_fade_in(self, qapp):
        """Test fade_in animation."""
        widget = QWidget()

        animation = AnimationHelper.fade_in(widget, duration=100)

        assert isinstance(animation, QPropertyAnimation)
        assert animation.targetObject() == widget

    def test_fade_out(self, qapp):
        """Test fade_out animation."""
        widget = QWidget()

        animation = AnimationHelper.fade_out(widget, duration=100)

        assert isinstance(animation, QPropertyAnimation)
        assert animation.targetObject() == widget

    def test_slide_in(self, qapp):
        """Test slide_in animation."""
        widget = QWidget()

        animation = AnimationHelper.slide_in(widget, direction='right', duration=100)

        assert isinstance(animation, QPropertyAnimation)
        assert animation.targetObject() == widget

    def test_slide_in_different_directions(self, qapp):
        """Test slide_in with different directions."""
        widget = QWidget()

        anim_left = AnimationHelper.slide_in(widget, direction='left', duration=100)
        anim_right = AnimationHelper.slide_in(widget, direction='right', duration=100)
        anim_up = AnimationHelper.slide_in(widget, direction='up', duration=100)
        anim_down = AnimationHelper.slide_in(widget, direction='down', duration=100)

        assert all(isinstance(a, QPropertyAnimation) for a in [anim_left, anim_right, anim_up, anim_down])

    def test_pulse(self, qapp):
        """Test pulse animation."""
        widget = QWidget()

        animation = AnimationHelper.pulse(widget, duration=200)

        # Should return an animation (or similar object)
        # Note: Actual implementation may vary
        assert animation is not None

    def test_glow(self, qapp):
        """Test glow animation."""
        widget = QWidget()

        animation = AnimationHelper.glow(widget, duration=500)

        # Should return an animation (or similar object)
        assert animation is not None

    def test_fade_in_custom_duration(self, qapp):
        """Test fade_in with custom duration."""
        widget = QWidget()

        animation = AnimationHelper.fade_in(widget, duration=500)

        assert animation.duration() == 500

    def test_fade_out_custom_duration(self, qapp):
        """Test fade_out with custom duration."""
        widget = QWidget()

        animation = AnimationHelper.fade_out(widget, duration=750)

        assert animation.duration() == 750

    def test_slide_in_custom_duration(self, qapp):
        """Test slide_in with custom duration."""
        widget = QWidget()

        animation = AnimationHelper.slide_in(widget, direction='right', duration=300)

        assert animation.duration() == 300

    def test_animations_can_start(self, qapp):
        """Test that animations can start without error."""
        widget = QWidget()
        widget.show()

        animation = AnimationHelper.fade_in(widget, duration=10)
        animation.start()

        # Should not crash
        assert True
