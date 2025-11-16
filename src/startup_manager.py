"""
Startup Manager for macOS.
Handles detection and management of login items, Launch Agents, and Launch Daemons.
"""

import logging
from typing import List, Dict
import time
from PyQt6.QtCore import QObject, QRunnable, QThreadPool, pyqtSignal, pyqtSlot

logger = logging.getLogger(__name__)
from utils.system_info import (
    get_login_items,
    get_launch_agents,
    get_launch_daemons,
    disable_login_item,
    disable_launch_agent,
    enable_launch_agent,
    fetch_launchctl_status,
)


class StartupScanWorker(QRunnable):
    """
    Worker runnable for scanning startup items in the background.
    """

    def __init__(self, signals, launchctl_cache, process_monitor=None):
        """
        Initialize worker.

        Args:
            signals: StartupManagerSignals instance
            launchctl_cache: Set of loaded launchctl labels
            process_monitor: Optional ProcessMonitor instance for matching items to processes
        """
        super().__init__()
        self.signals = signals
        self.launchctl_cache = launchctl_cache
        self.process_monitor = process_monitor

    def run(self):
        """Execute the startup scan."""
        try:
            # If cache is empty, fetch it (blocking but in thread)
            current_cache = self.launchctl_cache
            if not current_cache:
                current_cache = fetch_launchctl_status()

            login_items = get_login_items()
            launch_agents = get_launch_agents(loaded_labels=current_cache)
            launch_daemons = get_launch_daemons(loaded_labels=current_cache)

            all_items = login_items + launch_agents + launch_daemons

            # Match items to processes in the background thread if process_monitor is provided
            if self.process_monitor:
                matched_items = self._match_items_to_processes(all_items)
                self.signals.scan_finished.emit(matched_items, current_cache)
            else:
                self.signals.scan_finished.emit(all_items, current_cache)
        except Exception as e:
            self.signals.scan_error.emit(str(e))

    def _match_items_to_processes(self, items: list) -> list:
        """
        Match startup items to running processes and add resource usage data.
        This runs in the background thread to avoid blocking the UI.

        Args:
            items: List of startup items

        Returns:
            List of items with added process data (cpu_percent, memory_percent, pid)
        """
        processes = self.process_monitor.get_processes()

        # Build efficient lookup indices upfront
        # 1. Exact name match dict
        process_by_name = {proc['name'].lower(): proc for proc in processes}

        # 2. Build a token-based index for faster partial matching
        # Extract name tokens (words) from each process
        token_to_processes = {}
        for proc in processes:
            proc_name_lower = proc['name'].lower()
            # Split on common delimiters and extract meaningful tokens
            tokens = proc_name_lower.replace('-', ' ').replace('_', ' ').split()
            for token in tokens:
                if len(token) >= 3:  # Only index meaningful tokens
                    if token not in token_to_processes:
                        token_to_processes[token] = []
                    token_to_processes[token].append(proc)

        matched_items = []

        # Process items (no need for QApplication.processEvents in background thread)
        for item in items:
            # Create a copy to avoid modifying original
            item_copy = item.copy()

            # Try to match by name
            item_name = item.get('name', '').lower()
            label = item.get('label', '').lower()
            matched_proc = None

            # Strategy 1: Direct exact match
            if item_name in process_by_name:
                matched_proc = process_by_name[item_name]

            # Strategy 2: Token-based matching (much faster than nested loops)
            if not matched_proc and item_name:
                # Extract tokens from item name
                item_tokens = item_name.replace('-', ' ').replace('_', ' ').split()
                for token in item_tokens:
                    if len(token) >= 3 and token in token_to_processes:
                        # Found a matching token, use first matching process
                        matched_proc = token_to_processes[token][0]
                        break

            # Strategy 3: Try label tokens
            if not matched_proc and label:
                label_tokens = label.replace('-', ' ').replace('_', ' ').replace('.', ' ').split()
                for token in label_tokens:
                    if len(token) >= 3 and token in token_to_processes:
                        matched_proc = token_to_processes[token][0]
                        break

            # Strategy 4: Substring matching (only as last resort, still optimized)
            if not matched_proc and item_name:
                # Check if item name is a substring of any process name
                for proc_name_lower, proc in process_by_name.items():
                    if item_name in proc_name_lower or proc_name_lower in item_name:
                        matched_proc = proc
                        break

            # Add process data if matched
            if matched_proc:
                item_copy['cpu_percent'] = matched_proc.get('cpu_percent', 0.0)
                item_copy['memory_percent'] = matched_proc.get('memory_percent', 0.0)
                item_copy['pid'] = matched_proc.get('pid', None)
                item_copy['has_process'] = True
            else:
                item_copy['cpu_percent'] = 0.0
                item_copy['memory_percent'] = 0.0
                item_copy['pid'] = None
                item_copy['has_process'] = False

            matched_items.append(item_copy)

        return matched_items


class StartupManagerSignals(QObject):
    """Signals for StartupManager."""
    scan_finished = pyqtSignal(list, set)  # items, launchctl_cache
    scan_error = pyqtSignal(str)
    data_updated = pyqtSignal()  # Emitted when data is ready for UI


class StartupManager(QObject):
    """
    Manages startup items on macOS.
    """

    def __init__(self, process_monitor=None):
        """
        Initialize the startup manager.

        Args:
            process_monitor: Optional ProcessMonitor instance for matching items to processes
        """
        super().__init__()
        self.login_items = []
        self.launch_agents = []
        self.launch_daemons = []
        self.all_items = []
        self._launchctl_cache = set()
        self._launchctl_cache_ts = 0.0
        self._process_monitor = process_monitor

        # Thread pool for async scans
        self._thread_pool = QThreadPool()
        self._signals = StartupManagerSignals()
        self._signals.scan_finished.connect(self._on_scan_finished)
        self._signals.scan_error.connect(self._on_scan_error)

        # Expose data_updated signal through this object
        self.data_updated = self._signals.data_updated
        self.scan_error = self._signals.scan_error

    def refresh(self):
        """
        Refresh all startup items asynchronously.
        No longer performs process matching since CPU/Memory data is not displayed in startup tab.
        """
        now = time.time()

        # Reset cache if stale (> 5 seconds)
        if now - self._launchctl_cache_ts > 5:
            self._launchctl_cache = set()
            self._launchctl_cache_ts = now

        # Pass None for process_monitor to skip expensive process matching
        worker = StartupScanWorker(self._signals, self._launchctl_cache, None)
        self._thread_pool.start(worker)
        
    @pyqtSlot(list, set)
    def _on_scan_finished(self, items, launchctl_cache):
        """Handle completion of background scan."""
        self.all_items = items
        self._launchctl_cache = launchctl_cache
        
        # Split back into categories for convenience
        self.login_items = [i for i in items if i.get('type') == 'Login Item']
        self.launch_agents = [i for i in items if i.get('type') == 'Launch Agent']
        self.launch_daemons = [i for i in items if i.get('type') == 'Launch Daemon']
        
        self.data_updated.emit()
        
    @pyqtSlot(str)
    def _on_scan_error(self, error_msg):
        """Handle scan error."""
        logger.error("Startup scan error: %s", error_msg)

    def get_all_items(self) -> List[Dict[str, any]]:
        """
        Get all startup items.
        
        Returns:
            List of all startup items
        """
        return self.all_items
    
    def get_login_items_only(self) -> List[Dict[str, any]]:
        """
        Get only login items.
        
        Returns:
            List of login items
        """
        return self.login_items
    
    def get_launch_agents_only(self) -> List[Dict[str, any]]:
        """
        Get only launch agents.
        
        Returns:
            List of launch agents
        """
        return self.launch_agents
    
    def get_launch_daemons_only(self) -> List[Dict[str, any]]:
        """
        Get only launch daemons.
        
        Returns:
            List of launch daemons
        """
        return self.launch_daemons
    
    def get_enabled_items(self) -> List[Dict[str, any]]:
        """
        Get all enabled startup items.
        
        Returns:
            List of enabled items
        """
        return [item for item in self.all_items if item.get('enabled', True)]
    
    def get_disabled_items(self) -> List[Dict[str, any]]:
        """
        Get all disabled startup items.
        
        Returns:
            List of disabled items
        """
        return [item for item in self.all_items if not item.get('enabled', True)]
    
    def disable_item(self, item: Dict[str, any]) -> bool:
        """
        Disable a startup item.
        
        Args:
            item: The startup item to disable
            
        Returns:
            True if successful, False otherwise
        """
        item_type = item.get('type', '')
        
        if item_type == 'Login Item':
            return disable_login_item(item['name'])
        elif item_type in ['Launch Agent', 'Launch Daemon']:
            return disable_launch_agent(item['label'])
        
        return False
    
    def enable_item(self, item: Dict[str, any]) -> bool:
        """
        Enable a startup item.
        
        Args:
            item: The startup item to enable
            
        Returns:
            True if successful, False otherwise
        """
        item_type = item.get('type', '')
        
        if item_type in ['Launch Agent', 'Launch Daemon']:
            return enable_launch_agent(item['label'], item['path'])
        
        # Login items can't be re-enabled programmatically easily
        return False
    
    def get_item_count(self) -> int:
        """
        Get total count of startup items.
        
        Returns:
            Total number of startup items
        """
        return len(self.all_items)
    
    def get_enabled_count(self) -> int:
        """
        Get count of enabled startup items.
        
        Returns:
            Number of enabled startup items
        """
        return len(self.get_enabled_items())
    
    def get_disabled_count(self) -> int:
        """
        Get count of disabled startup items.
        
        Returns:
            Number of disabled startup items
        """
        return len(self.get_disabled_items())
    
    def search_items(self, query: str) -> List[Dict[str, any]]:
        """
        Search startup items by name or label.
        
        Args:
            query: Search query
            
        Returns:
            List of matching items
        """
        query_lower = query.lower()
        return [
            item for item in self.all_items
            if query_lower in item.get('name', '').lower()
            or query_lower in item.get('label', '').lower()
        ]
    
    def filter_by_type(self, item_type: str) -> List[Dict[str, any]]:
        """
        Filter items by type.
        
        Args:
            item_type: Type to filter by ('Login Item', 'Launch Agent', 'Launch Daemon')
            
        Returns:
            List of matching items
        """
        return [item for item in self.all_items if item.get('type') == item_type]
    
    def get_summary(self) -> Dict[str, any]:
        """
        Get summary statistics of startup items.
        
        Returns:
            Dict with summary information
        """
        return {
            'total': self.get_item_count(),
            'enabled': self.get_enabled_count(),
            'disabled': self.get_disabled_count(),
            'login_items': len(self.login_items),
            'launch_agents': len(self.launch_agents),
            'launch_daemons': len(self.launch_daemons),
        }
