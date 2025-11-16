"""
Startup Manager for macOS.
Handles detection and management of login items, Launch Agents, and Launch Daemons.
"""

from typing import List, Dict
from utils.system_info import (
    get_login_items,
    get_launch_agents,
    get_launch_daemons,
    disable_login_item,
    disable_launch_agent,
    enable_launch_agent,
)


class StartupManager:
    """
    Manages startup items on macOS.
    """
    
    def __init__(self):
        """Initialize the startup manager."""
        self.login_items = []
        self.launch_agents = []
        self.launch_daemons = []
        self.all_items = []
        
    def refresh(self):
        """Refresh all startup items."""
        self.login_items = get_login_items()
        self.launch_agents = get_launch_agents()
        self.launch_daemons = get_launch_daemons()
        
        # Combine all items
        self.all_items = self.login_items + self.launch_agents + self.launch_daemons
        
        return self.all_items
    
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

