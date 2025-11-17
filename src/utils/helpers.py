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


def get_process_list(include_system: bool = False) -> List[Dict[str, any]]:
    """
    Get list of running processes with their resource usage.
    
    Args:
        include_system: If True, include system processes
        
    Returns:
        List of dicts with process information
    """
    mem = psutil.virtual_memory()
    total_ram = mem.total

    # Prime CPU percent sampling to avoid initial zeros without blocking UI
    psutil.cpu_percent(interval=None, percpu=False)

    processes = []

    for proc in psutil.process_iter(['pid', 'name', 'username', 'memory_info', 'cpu_percent']):
        try:
            pinfo = proc.info
            
            memory_info = pinfo.get('memory_info')

            # Skip if memory info is not available
            if not memory_info:
                continue

            username = pinfo.get('username') or ''

            # Skip system processes if requested
            if not include_system and username in ['root', '_windowserver', 'nobody']:
                continue

            memory_mb = memory_info.rss / (1024 * 1024)  # Convert to MB
            memory_percent = (memory_info.rss / total_ram) * 100

            # Capture both last reported CPU and a fresh sample
            last_cpu_percent = pinfo.get('cpu_percent') or 0.0
            sampled_cpu_percent = proc.cpu_percent(interval=None) or 0.0

            processes.append({
                'pid': pinfo['pid'],
                'name': pinfo['name'],
                'username': username,
                'memory_mb': memory_mb,
                'memory_percent': memory_percent,
                'memory_human': bytes_to_human_readable(memory_info.rss),
                'cpu_percent': sampled_cpu_percent,
                'cpu_percent_last': last_cpu_percent,
            })
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    
    return processes


def get_top_memory_processes(n: int = 5, include_system: bool = False) -> List[Dict[str, any]]:
    """
    Get top N processes by memory usage.
    
    Args:
        n: Number of processes to return
        include_system: If True, include system processes
        
    Returns:
        List of top N processes sorted by memory usage
    """
    processes = get_process_list(include_system=include_system)
    processes.sort(key=lambda x: x['memory_mb'], reverse=True)
    return processes[:n]


def get_top_cpu_processes(n: int = 5, include_system: bool = False) -> List[Dict[str, any]]:
    """
    Get top N processes by CPU usage.
    
    Args:
        n: Number of processes to return
        include_system: If True, include system processes
        
    Returns:
        List of top N processes sorted by CPU usage
    """
    processes = get_process_list(include_system=include_system)
    processes.sort(key=lambda x: x['cpu_percent'], reverse=True)
    return processes[:n]


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

