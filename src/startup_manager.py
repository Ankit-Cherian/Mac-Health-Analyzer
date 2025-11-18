"""
Startup Manager for macOS.
Handles detection and management of login items, Launch Agents, and Launch Daemons.
"""

from typing import List, Dict
import time
from PyQt6.QtCore import QObject, QRunnable, QThreadPool, pyqtSignal, pyqtSlot
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
    
    def __init__(self, signals, launchctl_cache):
        """
        Initialize worker.
        
        Args:
            signals: StartupManagerSignals instance
            launchctl_cache: Set of loaded launchctl labels
        """
        super().__init__()
        self.signals = signals
        self.launchctl_cache = launchctl_cache
    
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
            
            self.signals.scan_finished.emit(all_items, current_cache)
        except Exception as e:
            self.signals.scan_error.emit(str(e))


class StartupManagerSignals(QObject):
    """Signals for StartupManager."""
    scan_finished = pyqtSignal(list, set)  # items, launchctl_cache
    scan_error = pyqtSignal(str)
    data_updated = pyqtSignal()  # Emitted when data is ready for UI


class StartupManager(QObject):
    """
    Manages startup items on macOS.
    """
    
    def __init__(self):
        """Initialize the startup manager."""
        super().__init__()
        self.login_items = []
        self.launch_agents = []
        self.launch_daemons = []
        self.all_items = []
        self._launchctl_cache = set()
        self._launchctl_cache_ts = 0.0
        
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
        Triggers a background scan.
        """
        now = time.time()
        
        # Reset cache if stale (> 5 seconds)
        if now - self._launchctl_cache_ts > 5:
            self._launchctl_cache = set()
            self._launchctl_cache_ts = now
            
        worker = StartupScanWorker(self._signals, self._launchctl_cache)
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
        print(f"Startup scan error: {error_msg}")

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
