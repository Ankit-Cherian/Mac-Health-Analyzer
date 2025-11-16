"""
Process Monitor for macOS.
Handles real-time monitoring of running processes and system resources.
"""

import logging
import psutil
import time
from typing import List, Dict, Optional
from PyQt6.QtCore import QObject, QThread, pyqtSignal, QMutex, QMutexLocker

logger = logging.getLogger(__name__)
from utils.helpers import (
    get_system_memory_info,
    get_cpu_info,
    kill_process,
    bytes_to_human_readable
)


class ProcessWorker(QThread):
    """
    Background worker thread for process monitoring.
    """
    stats_updated = pyqtSignal(dict)  # Emits full stats dictionary

    def __init__(self):
        """Initialize the worker thread."""
        super().__init__()
        self._running = True
        self._paused = False
        self.include_system_processes = False
        self._mutex = QMutex()
        
        # Persistent cache for process objects
        # Key: PID, Value: psutil.Process object
        self._process_cache = {}
        
        # Prime global CPU usage
        psutil.cpu_percent(interval=None)

    def set_include_system_processes(self, include: bool):
        """Set whether to include system processes."""
        with QMutexLocker(self._mutex):
            self.include_system_processes = include

    def stop(self):
        """Stop the worker thread."""
        self._running = False
        self.wait()

    def run(self):
        """Main loop for the worker thread."""
        while self._running:
            if not self._paused:
                try:
                    self._collect_metrics()
                except Exception as e:
                    logger.error("Error in process worker: %s", e)
            
            # Sleep for 2 seconds
            # We use shorter sleeps to check for stop signal more frequently
            for _ in range(20):
                if not self._running:
                    break
                self.msleep(100)

    def _collect_metrics(self):
        """Collect system metrics and process list."""
        # 1. System-wide metrics
        memory_info = get_system_memory_info()
        cpu_info = get_cpu_info()
        
        # 2. Process list
        current_pids = set()
        processes_data = []
        
        total_ram = memory_info['total']
        
        with QMutexLocker(self._mutex):
            include_system = self.include_system_processes
            
        # Iterate through all running processes
        for pid in psutil.pids():
            current_pids.add(pid)
            
            # Get or create process object
            try:
                if pid in self._process_cache:
                    proc = self._process_cache[pid]
                else:
                    proc = psutil.Process(pid)
                    self._process_cache[pid] = proc
                
                # Use oneshot for efficient attribute retrieval
                with proc.oneshot():
                    name = proc.name()
                    username = proc.username()
                    
                    # Filter system processes if needed
                    if not include_system and username in ['root', '_windowserver', 'nobody']:
                        continue
                        
                    memory_full = proc.memory_info()
                    memory_rss = memory_full.rss
                    memory_mb = memory_rss / (1024 * 1024)
                    memory_percent = (memory_rss / total_ram) * 100
                    
                    # CPU percent - this works correctly because we persist the object!
                    # interval=None compares with the last call on this object
                    cpu_percent = proc.cpu_percent(interval=None)
                    
                    processes_data.append({
                        'pid': pid,
                        'name': name,
                        'username': username,
                        'memory_mb': memory_mb,
                        'memory_percent': memory_percent,
                        'memory_human': bytes_to_human_readable(memory_rss),
                        'cpu_percent': cpu_percent,
                    })
                    
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                # Process is gone or inaccessible
                if pid in self._process_cache:
                    del self._process_cache[pid]
                continue
            except Exception:
                continue
                
        # Clean up cache for dead processes
        cached_pids = list(self._process_cache.keys())
        for pid in cached_pids:
            if pid not in current_pids:
                del self._process_cache[pid]
                
        # Emit all data
        self.stats_updated.emit({
            'processes': processes_data,
            'memory_info': memory_info,
            'cpu_info': cpu_info,
            'process_count': len(processes_data)
        })


class ProcessMonitor(QObject):
    """
    Monitors running processes and system resources.
    Acts as a facade for the background worker.
    """
    data_updated = pyqtSignal()  # Signal when new data is available
    
    def __init__(self):
        """Initialize the process monitor."""
        super().__init__()
        self._worker = ProcessWorker()
        self._worker.stats_updated.connect(self._on_stats_updated)
        
        # Cache for UI access
        self._latest_data = {
            'processes': [],
            'memory_info': {},
            'cpu_info': {},
            'process_count': 0
        }
        
        self._worker.start()
        
    def _on_stats_updated(self, data):
        """Handle updates from worker."""
        self._latest_data = data
        self.data_updated.emit()
        
    def cleanup(self):
        """Clean up resources."""
        self._worker.stop()
        
    def set_include_system_processes(self, include: bool):
        """
        Set whether to include system processes.
        
        Args:
            include: True to include system processes, False otherwise
        """
        self._worker.set_include_system_processes(include)
        
    def refresh(self):
        """
        Legacy method for compatibility.
        Now essentially a no-op since the worker runs automatically.
        """
        pass
        
    def get_processes(self) -> List[Dict[str, any]]:
        """
        Get list of all processes (instant return from cache).
        
        Returns:
            List of process information dicts
        """
        return self._latest_data['processes']
    
    def get_process_count(self) -> int:
        """Get count of processes."""
        return self._latest_data['process_count']
    
    def get_memory_info(self) -> Dict[str, any]:
        """Get system memory information."""
        return self._latest_data['memory_info']
    
    def get_cpu_info(self) -> Dict[str, any]:
        """Get CPU information."""
        return self._latest_data['cpu_info']
    
    def get_top_memory_processes(self, n: int = 10) -> List[Dict[str, any]]:
        """Get top N processes by memory usage."""
        sorted_processes = sorted(
            self._latest_data['processes'],
            key=lambda x: x['memory_mb'],
            reverse=True
        )
        return sorted_processes[:n]
    
    def get_top_cpu_processes(self, n: int = 10) -> List[Dict[str, any]]:
        """Get top N processes by CPU usage."""
        sorted_processes = sorted(
            self._latest_data['processes'],
            key=lambda x: x['cpu_percent'],
            reverse=True
        )
        return sorted_processes[:n]

    def get_top_processes(self, n: int = 10) -> Dict[str, List[Dict[str, any]]]:
        """
        Get top N processes by both CPU and memory usage in a single operation.
        """
        processes = self._latest_data['processes']
        
        # Sort by CPU
        cpu_sorted = sorted(
            processes,
            key=lambda x: x['cpu_percent'],
            reverse=True
        )

        # Sort by memory
        memory_sorted = sorted(
            processes,
            key=lambda x: x['memory_mb'],
            reverse=True
        )

        return {
            'cpu': cpu_sorted[:n],
            'memory': memory_sorted[:n]
        }
    
    def search_processes(self, query: str) -> List[Dict[str, any]]:
        """Search processes by name."""
        query_lower = query.lower()
        return [
            proc for proc in self._latest_data['processes']
            if query_lower in proc['name'].lower()
        ]
    
    def get_process_by_pid(self, pid: int) -> Optional[Dict[str, any]]:
        """Get process information by PID."""
        for proc in self._latest_data['processes']:
            if proc['pid'] == pid:
                return proc
        return None
    
    def kill_process(self, pid: int, force: bool = False) -> bool:
        """
        Kill a process by PID.
        This is a write action, so we can just call the helper directly.
        """
        return kill_process(pid, force)
    
    def get_memory_usage_percentage(self) -> float:
        """Get overall memory usage percentage."""
        return self._latest_data['memory_info'].get('percent', 0.0)
    
    def get_cpu_usage_percentage(self) -> float:
        """Get overall CPU usage percentage."""
        return self._latest_data['cpu_info'].get('percent', 0.0)
    
    def get_system_summary(self) -> Dict[str, any]:
        """Get summary of system resources."""
        mem_info = self._latest_data['memory_info']
        cpu_info = self._latest_data['cpu_info']
        
        return {
            'process_count': self.get_process_count(),
            'memory_percent': self.get_memory_usage_percentage(),
            'memory_used_human': mem_info.get('used_human', 'N/A'),
            'memory_total_human': mem_info.get('total_human', 'N/A'),
            'cpu_percent': self.get_cpu_usage_percentage(),
            'cpu_count': cpu_info.get('count', 0),
            'cpu_count_logical': cpu_info.get('count_logical', 0),
        }
    
    def sort_processes(self, key: str, reverse: bool = True) -> List[Dict[str, any]]:
        """Sort processes by a given key."""
        if key not in ['name', 'pid', 'memory_mb', 'cpu_percent', 'username']:
            key = 'memory_mb'
            
        return sorted(self._latest_data['processes'], key=lambda x: x[key], reverse=reverse)
    
    def filter_by_memory_threshold(self, threshold_mb: float) -> List[Dict[str, any]]:
        """Filter processes by memory usage threshold."""
        return [
            proc for proc in self._latest_data['processes']
            if proc['memory_mb'] >= threshold_mb
        ]
    
    def filter_by_cpu_threshold(self, threshold_percent: float) -> List[Dict[str, any]]:
        """Filter processes by CPU usage threshold."""
        return [
            proc for proc in self._latest_data['processes']
            if proc['cpu_percent'] >= threshold_percent
        ]
    
    def get_process_details(self, pid: int) -> Optional[Dict[str, any]]:
        """
        Get detailed information about a process.
        This fetches fresh data on demand since it's a user-initiated action.
        """
        try:
            proc = psutil.Process(pid)
            return {
                'pid': proc.pid,
                'name': proc.name(),
                'username': proc.username(),
                'status': proc.status(),
                'create_time': proc.create_time(),
                'cpu_percent': proc.cpu_percent(interval=None),
                'memory_info': proc.memory_info(),
                'num_threads': proc.num_threads(),
                'cmdline': ' '.join(proc.cmdline()) if proc.cmdline() else '',
            }
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            return None
