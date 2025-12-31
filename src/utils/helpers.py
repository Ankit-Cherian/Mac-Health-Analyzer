"""
Helper utilities for the Mac Health Analyzer.
"""

import logging
import psutil
from typing import Dict, List, Tuple, Optional

logger = logging.getLogger(__name__)


def bytes_to_human_readable(bytes_value: int) -> str:
    """
    Convert bytes to human-readable format.
    
    Args:
        bytes_value: Number of bytes
        
    Returns:
        Human-readable string (e.g., "1.5 GB")
    """
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_value < 1024.0:
            return f"{bytes_value:.1f} {unit}"
        bytes_value /= 1024.0
    return f"{bytes_value:.1f} PB"


def get_system_memory_info() -> Dict[str, any]:
    """
    Get system memory information.
    
    Returns:
        Dict with total, available, used, and percent keys
    """
    mem = psutil.virtual_memory()
    return {
        'total': mem.total,
        'available': mem.available,
        'used': mem.used,
        'percent': mem.percent,
        'total_human': bytes_to_human_readable(mem.total),
        'available_human': bytes_to_human_readable(mem.available),
        'used_human': bytes_to_human_readable(mem.used),
    }


def get_cpu_info() -> Dict[str, any]:
    """
    Get CPU information.

    Returns:
        Dict with CPU usage and count information
    """
    # Use interval=None to get cached CPU value instead of blocking
    # This prevents blocking the UI thread during updates
    cpu_percent = psutil.cpu_percent(interval=None)
    cpu_count = psutil.cpu_count()
    cpu_count_logical = psutil.cpu_count(logical=True)

    return {
        'percent': cpu_percent,
        'count': cpu_count,
        'count_logical': cpu_count_logical,
    }


def kill_process(
    pid: int,
    force: bool = False,
    expected_name: Optional[str] = None,
    expected_create_time: Optional[float] = None
) -> bool:
    """
    Kill a process by PID with optional identity verification.

    To prevent PID reuse attacks (where a process exits and another process
    takes its PID before we send the kill signal), this function supports
    verifying the process identity before killing.

    Args:
        pid: Process ID
        force: If True, use SIGKILL instead of SIGTERM
        expected_name: Optional expected process name for verification
        expected_create_time: Optional expected creation time for verification

    Returns:
        True if successful, False otherwise
    """
    try:
        proc = psutil.Process(pid)

        # Verify process identity to prevent PID reuse attacks
        if expected_name is not None:
            actual_name = proc.name()
            if actual_name != expected_name:
                logger.warning(
                    "PID %d name mismatch: expected '%s', got '%s'. "
                    "Process may have changed - refusing to kill.",
                    pid, expected_name, actual_name
                )
                return False

        if expected_create_time is not None:
            actual_create_time = proc.create_time()
            # Allow 1 second tolerance for timing differences
            if abs(actual_create_time - expected_create_time) > 1.0:
                logger.warning(
                    "PID %d create_time mismatch: expected %.2f, got %.2f. "
                    "Process may have changed - refusing to kill.",
                    pid, expected_create_time, actual_create_time
                )
                return False

        if force:
            proc.kill()  # SIGKILL
        else:
            proc.terminate()  # SIGTERM

        logger.info("Successfully terminated process %d", pid)
        return True

    except psutil.NoSuchProcess:
        logger.info("Process %d no longer exists", pid)
        return False
    except psutil.AccessDenied:
        logger.error("Access denied when trying to kill process %d", pid)
        return False
    except psutil.ZombieProcess:
        logger.warning("Process %d is a zombie process", pid)
        return False
    except Exception as e:
        logger.error("Error killing process %d: %s", pid, e)
        return False


def get_resource_usage_color(percent: float) -> str:
    """
    Get color indicator for resource usage percentage.
    
    Args:
        percent: Usage percentage (0-100)
        
    Returns:
        Color code: 'low', 'medium', or 'high'
    """
    if percent < 50:
        return 'low'
    elif percent < 80:
        return 'medium'
    else:
        return 'high'


def format_percentage(value: float, decimals: int = 1) -> str:
    """
    Format a percentage value.
    
    Args:
        value: Percentage value
        decimals: Number of decimal places
        
    Returns:
        Formatted string (e.g., "75.5%")
    """
    return f"{value:.{decimals}f}%"
