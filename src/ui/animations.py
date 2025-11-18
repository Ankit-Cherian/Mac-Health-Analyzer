"""
Animation utilities for the Mac Health Analyzer.
Professional animations with sophisticated easing and micro-interactions.
Designed for smooth, polished UI transitions that feel hand-crafted.
"""

from PyQt6.QtCore import QPropertyAnimation, QEasingCurve, QAbstractAnimation, QParallelAnimationGroup, QSequentialAnimationGroup
from PyQt6.QtWidgets import QWidget, QGraphicsOpacityEffect


# Professional easing curves for different animation types
EASING_CURVES = {
    'smooth': QEasingCurve.Type.InOutCubic,      # General smooth transitions
    'spring': QEasingCurve.Type.OutBack,          # Subtle spring effect
    'ease_out': QEasingCurve.Type.OutCubic,       # Fast start, slow end
    'ease_in': QEasingCurve.Type.InCubic,         # Slow start, fast end
    'bounce': QEasingCurve.Type.OutBounce,        # Playful bounce
    'elastic': QEasingCurve.Type.OutElastic,      # Elastic overshoot
    'soft': QEasingCurve.Type.InOutSine,          # Very gentle transition
}


class AnimationHelper:
    """
    Helper class for creating animations.
    """
    
    @staticmethod
    def fade_in(widget: QWidget, duration: int = 400, delay: int = 0, easing: str = 'ease_out') -> QPropertyAnimation:
        """
        Create a professional fade-in animation with smooth easing.

        Args:
            widget: Widget to animate
            duration: Animation duration in ms (default: 400 for smooth feel)
            delay: Delay before starting in ms
            easing: Easing curve type ('smooth', 'spring', 'ease_out', etc.)

        Returns:
            QPropertyAnimation object
        """
        # Ensure widget has opacity effect
        if not widget.graphicsEffect():
            effect = QGraphicsOpacityEffect(widget)
            widget.setGraphicsEffect(effect)

        effect = widget.graphicsEffect()
        effect.setOpacity(0)

        animation = QPropertyAnimation(effect, b"opacity")
        animation.setDuration(duration)
        animation.setStartValue(0.0)
        animation.setEndValue(1.0)
        animation.setEasingCurve(EASING_CURVES.get(easing, QEasingCurve.Type.OutCubic))

        if delay > 0:
            animation.setStartDelay(delay)

        return animation
    
    @staticmethod
    def fade_out(widget: QWidget, duration: int = 300) -> QPropertyAnimation:
        """
        Create a fade-out animation.
        
        Args:
            widget: Widget to animate
            duration: Animation duration in ms
            
        Returns:
            QPropertyAnimation object
        """
        # Ensure widget has opacity effect
        if not widget.graphicsEffect():
            effect = QGraphicsOpacityEffect(widget)
            widget.setGraphicsEffect(effect)
        
        effect = widget.graphicsEffect()
        
        animation = QPropertyAnimation(effect, b"opacity")
        animation.setDuration(duration)
        animation.setStartValue(effect.opacity())
        animation.setEndValue(0.0)
        animation.setEasingCurve(QEasingCurve.Type.InCubic)
        
        return animation
    
    @staticmethod
    def staggered_fade_in(widgets: list, duration: int = 400, delay_increment: int = 80, easing: str = 'smooth') -> QParallelAnimationGroup:
        """
        Create sophisticated staggered fade-in animations for multiple widgets.
        Perfect for revealing content with professional polish.

        Args:
            widgets: List of widgets to animate
            duration: Animation duration in ms (default: 400 for smooth feel)
            delay_increment: Delay between each widget's animation start (default: 80ms)
            easing: Easing curve type

        Returns:
            QParallelAnimationGroup containing all animations
        """
        group = QParallelAnimationGroup()

        for i, widget in enumerate(widgets):
            animation = AnimationHelper.fade_in(widget, duration, delay=i * delay_increment, easing=easing)
            group.addAnimation(animation)

        return group
    
    @staticmethod
    def scale_on_hover(widget: QWidget, scale_factor: float = 1.05, duration: int = 150) -> tuple:
        """
        Create scale animations for hover effect.
        
        Args:
            widget: Widget to animate
            scale_factor: Scale factor (1.0 = original size)
            duration: Animation duration in ms
            
        Returns:
            Tuple of (scale_up_animation, scale_down_animation)
        """
        # Note: PyQt6 doesn't support scale transform animations directly
        # This would need to be implemented with custom painting or geometry changes
        # For now, we'll return None to indicate manual implementation needed
        return (None, None)
    
    @staticmethod
    def smooth_scroll(widget: QWidget, target_value: int, duration: int = 400) -> QPropertyAnimation:
        """
        Create a smooth scroll animation.
        
        Args:
            widget: Scroll area or widget to animate
            target_value: Target scroll position
            duration: Animation duration in ms
            
        Returns:
            QPropertyAnimation object
        """
        # This would need to be implemented based on the specific scroll widget
        # For now, return None to indicate manual implementation needed
        return None
    
    @staticmethod
    def pulse_animation(widget: QWidget, duration: int = 1000) -> QPropertyAnimation:
        """
        Create a pulsing opacity animation.
        
        Args:
            widget: Widget to animate
            duration: Animation duration in ms
            
        Returns:
            QPropertyAnimation object that loops
        """
        # Ensure widget has opacity effect
        if not widget.graphicsEffect():
            effect = QGraphicsOpacityEffect(widget)
            widget.setGraphicsEffect(effect)
        
        effect = widget.graphicsEffect()
        
        animation = QPropertyAnimation(effect, b"opacity")
        animation.setDuration(duration)
        animation.setStartValue(1.0)
        animation.setEndValue(0.3)
        animation.setEasingCurve(QEasingCurve.Type.InOutSine)
        animation.setLoopCount(-1)  # Loop forever
        
        return animation
    
    @staticmethod
    def fade_transition(old_widget: QWidget, new_widget: QWidget, duration: int = 300) -> QSequentialAnimationGroup:
        """
        Create a fade transition between two widgets.
        
        Args:
            old_widget: Widget to fade out
            new_widget: Widget to fade in
            duration: Animation duration in ms
            
        Returns:
            QSequentialAnimationGroup containing both animations
        """
        group = QSequentialAnimationGroup()
        
        fade_out_anim = AnimationHelper.fade_out(old_widget, duration // 2)
        fade_in_anim = AnimationHelper.fade_in(new_widget, duration // 2)
        
        group.addAnimation(fade_out_anim)
        group.addAnimation(fade_in_anim)
        
        return group


def apply_table_row_stagger(table_widget, duration: int = 300, delay_increment: int = 30):
    """
    Apply staggered fade-in animation to table rows.
    
    Args:
        table_widget: QTableWidget to animate
        duration: Animation duration in ms
        delay_increment: Delay between each row
    """
    # Note: This is tricky with QTableWidget as rows aren't individual widgets
    # Would need custom implementation with item delegates or overlay widgets
    pass


def animate_value_change(widget: QWidget, property_name: bytes, start_value, end_value, duration: int = 500) -> QPropertyAnimation:
    """
    Animate a property value change smoothly.
    
    Args:
        widget: Widget to animate
        property_name: Property name as bytes (e.g., b"value")
        start_value: Starting value
        end_value: Ending value
        duration: Animation duration in ms
        
    Returns:
        QPropertyAnimation object
    """
    animation = QPropertyAnimation(widget, property_name)
    animation.setDuration(duration)
    animation.setStartValue(start_value)
    animation.setEndValue(end_value)
    animation.setEasingCurve(QEasingCurve.Type.OutCubic)
    
    return animation

