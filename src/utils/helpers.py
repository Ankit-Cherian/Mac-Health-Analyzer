"""
Helper utilities for the Mac Health Analyzer.
"""

import psutil
from typing import Dict, List, Tuple


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


def kill_process(pid: int, force: bool = False) -> bool:
    """
    Kill a process by PID.
    
    Args:
        pid: Process ID
        force: If True, use SIGKILL instead of SIGTERM
        
    Returns:
        True if successful, False otherwise
    """
    try:
        proc = psutil.Process(pid)
        if force:
            proc.kill()  # SIGKILL
        else:
            proc.terminate()  # SIGTERM
        return True
    except Exception as e:
        print(f"Error killing process {pid}: {e}")
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
