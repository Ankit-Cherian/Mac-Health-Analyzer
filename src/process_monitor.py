"""
Process Monitor for macOS.
Handles real-time monitoring of running processes and system resources.
"""

import psutil
from typing import List, Dict, Optional
from utils.helpers import (
    get_process_list,
    get_system_memory_info,
    get_cpu_info,
    get_top_memory_processes,
    get_top_cpu_processes,
    kill_process,
)


class ProcessMonitor:
    """
    Monitors running processes and system resources.
    """
    
    def __init__(self):
        """Initialize the process monitor."""
        self.processes = []
        self.memory_info = {}
        self.cpu_info = {}
        self.include_system_processes = False
        
    def set_include_system_processes(self, include: bool):
        """
        Set whether to include system processes.
        
        Args:
            include: True to include system processes, False otherwise
        """
        self.include_system_processes = include
        
    def refresh(self):
        """Refresh all process and system information."""
        self.processes = get_process_list(include_system=self.include_system_processes)
        self.memory_info = get_system_memory_info()
        self.cpu_info = get_cpu_info()
        
    def get_processes(self) -> List[Dict[str, any]]:
        """
        Get list of all processes.
        
        Returns:
            List of process information dicts
        """
        return self.processes
    
    def get_process_count(self) -> int:
        """
        Get count of processes.
        
        Returns:
            Number of processes
        """
        return len(self.processes)
    
    def get_memory_info(self) -> Dict[str, any]:
        """
        Get system memory information.
        
        Returns:
            Dict with memory information
        """
        return self.memory_info
    
    def get_cpu_info(self) -> Dict[str, any]:
        """
        Get CPU information.
        
        Returns:
            Dict with CPU information
        """
        return self.cpu_info
    
    def get_top_memory_processes(self, n: int = 10) -> List[Dict[str, any]]:
        """
        Get top N processes by memory usage.
        
        Args:
            n: Number of processes to return
            
        Returns:
            List of top N processes
        """
        sorted_processes = sorted(
            self.processes,
            key=lambda x: x['memory_mb'],
            reverse=True
        )
        return sorted_processes[:n]
    
    def get_top_cpu_processes(self, n: int = 10) -> List[Dict[str, any]]:
        """
        Get top N processes by CPU usage.
        
        Args:
            n: Number of processes to return
            
        Returns:
            List of top N processes
        """
        sorted_processes = sorted(
            self.processes,
            key=lambda x: x['cpu_percent'],
            reverse=True
        )
        return sorted_processes[:n]
    
    def search_processes(self, query: str) -> List[Dict[str, any]]:
        """
        Search processes by name.
        
        Args:
            query: Search query
            
        Returns:
            List of matching processes
        """
        query_lower = query.lower()
        return [
            proc for proc in self.processes
            if query_lower in proc['name'].lower()
        ]
    
    def get_process_by_pid(self, pid: int) -> Optional[Dict[str, any]]:
        """
        Get process information by PID.
        
        Args:
            pid: Process ID
            
        Returns:
            Process information or None if not found
        """
        for proc in self.processes:
            if proc['pid'] == pid:
                return proc
        return None
    
    def kill_process(self, pid: int, force: bool = False) -> bool:
        """
        Kill a process by PID.
        
        Args:
            pid: Process ID
            force: If True, use SIGKILL instead of SIGTERM
            
        Returns:
            True if successful, False otherwise
        """
        return kill_process(pid, force)
    
    def get_memory_usage_percentage(self) -> float:
        """
        Get overall memory usage percentage.
        
        Returns:
            Memory usage percentage
        """
        return self.memory_info.get('percent', 0.0)
    
    def get_cpu_usage_percentage(self) -> float:
        """
        Get overall CPU usage percentage.
        
        Returns:
            CPU usage percentage
        """
        return self.cpu_info.get('percent', 0.0)
    
    def get_system_summary(self) -> Dict[str, any]:
        """
        Get summary of system resources.
        
        Returns:
            Dict with system summary
        """
        return {
            'process_count': self.get_process_count(),
            'memory_percent': self.get_memory_usage_percentage(),
            'memory_used_human': self.memory_info.get('used_human', 'N/A'),
            'memory_total_human': self.memory_info.get('total_human', 'N/A'),
            'cpu_percent': self.get_cpu_usage_percentage(),
            'cpu_count': self.cpu_info.get('count', 0),
            'cpu_count_logical': self.cpu_info.get('count_logical', 0),
        }
    
    def sort_processes(self, key: str, reverse: bool = True) -> List[Dict[str, any]]:
        """
        Sort processes by a given key.
        
        Args:
            key: Key to sort by ('name', 'pid', 'memory_mb', 'cpu_percent')
            reverse: If True, sort in descending order
            
        Returns:
            Sorted list of processes
        """
        if key not in ['name', 'pid', 'memory_mb', 'cpu_percent', 'username']:
            key = 'memory_mb'
            
        return sorted(self.processes, key=lambda x: x[key], reverse=reverse)
    
    def filter_by_memory_threshold(self, threshold_mb: float) -> List[Dict[str, any]]:
        """
        Filter processes by memory usage threshold.
        
        Args:
            threshold_mb: Minimum memory usage in MB
            
        Returns:
            List of processes using more than threshold
        """
        return [
            proc for proc in self.processes
            if proc['memory_mb'] >= threshold_mb
        ]
    
    def filter_by_cpu_threshold(self, threshold_percent: float) -> List[Dict[str, any]]:
        """
        Filter processes by CPU usage threshold.
        
        Args:
            threshold_percent: Minimum CPU usage percentage
            
        Returns:
            List of processes using more than threshold
        """
        return [
            proc for proc in self.processes
            if proc['cpu_percent'] >= threshold_percent
        ]
    
    def get_process_details(self, pid: int) -> Optional[Dict[str, any]]:
        """
        Get detailed information about a process.
        
        Args:
            pid: Process ID
            
        Returns:
            Detailed process information or None if not found
        """
        try:
            proc = psutil.Process(pid)
            return {
                'pid': proc.pid,
                'name': proc.name(),
                'username': proc.username(),
                'status': proc.status(),
                'create_time': proc.create_time(),
                'cpu_percent': proc.cpu_percent(interval=0.1),
                'memory_info': proc.memory_info(),
                'num_threads': proc.num_threads(),
                'cmdline': ' '.join(proc.cmdline()) if proc.cmdline() else '',
            }
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            return None

