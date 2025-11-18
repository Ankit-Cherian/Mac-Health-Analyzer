"""
Integration Tests for Manager Classes

Tests the integration between managers and their dependencies.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
import time

from process_monitor import ProcessMonitor
from startup_manager import StartupManager


class TestStartupManagerIntegration:
    """Integration tests for StartupManager with real dependencies."""

    @pytest.mark.integration
    @patch('startup_manager.fetch_launchctl_status')
    @patch('startup_manager.get_launch_daemons')
    @patch('startup_manager.get_launch_agents')
    @patch('startup_manager.get_login_items')
    def test_full_refresh_cycle(self, mock_login, mock_agents, mock_daemons, mock_fetch):
        """Test complete refresh cycle with all dependencies."""
        # Mock all dependencies
        mock_fetch.return_value = {'com.agent1', 'com.daemon1'}
        mock_login.return_value = [
            {'name': 'Dropbox', 'type': 'Login Item', 'enabled': True},
            {'name': 'Slack', 'type': 'Login Item', 'enabled': True},
        ]
        mock_agents.return_value = [
            {'name': 'Agent1', 'label': 'com.agent1', 'type': 'Launch Agent', 'enabled': True},
            {'name': 'Agent2', 'label': 'com.agent2', 'type': 'Launch Agent', 'enabled': False},
        ]
        mock_daemons.return_value = [
            {'name': 'Daemon1', 'label': 'com.daemon1', 'type': 'Launch Daemon', 'enabled': True},
        ]

        # Create manager and refresh
        manager = StartupManager()
        result = manager.refresh()

        # Verify all items were loaded
        assert len(result) == 5
        assert len(manager.get_login_items_only()) == 2
        assert len(manager.get_launch_agents_only()) == 2
        assert len(manager.get_launch_daemons_only()) == 1

        # Test filtering
        enabled = manager.get_enabled_items()
        disabled = manager.get_disabled_items()
        assert len(enabled) == 4
        assert len(disabled) == 1

        # Test searching
        dropbox_items = manager.search_items('dropbox')
        assert len(dropbox_items) == 1
        assert dropbox_items[0]['name'] == 'Dropbox'

        # Test type filtering
        agents = manager.filter_by_type('Launch Agent')
        assert len(agents) == 2

        # Test summary
        summary = manager.get_summary()
        assert summary['total'] == 5
        assert summary['enabled'] == 4
        assert summary['disabled'] == 1
        assert summary['login_items'] == 2
        assert summary['launch_agents'] == 2
        assert summary['launch_daemons'] == 1

    @pytest.mark.integration
    @patch('startup_manager.time.time')
    @patch('startup_manager.fetch_launchctl_status')
    @patch('startup_manager.get_launch_daemons')
    @patch('startup_manager.get_launch_agents')
    @patch('startup_manager.get_login_items')
    def test_launchctl_caching_behavior(self, mock_login, mock_agents, mock_daemons,
                                       mock_fetch, mock_time):
        """Test that launchctl caching works correctly across multiple refreshes."""
        mock_login.return_value = []
        mock_agents.return_value = []
        mock_daemons.return_value = []
        mock_fetch.return_value = {'com.test'}

        manager = StartupManager()

        # First refresh at time 0
        mock_time.return_value = 0.0
        manager.refresh()
        assert mock_fetch.call_count == 1

        # Refresh at time 2 (should use cache)
        mock_time.return_value = 2.0
        manager.refresh()
        assert mock_fetch.call_count == 1

        # Refresh at time 6 (should refresh cache)
        mock_time.return_value = 6.0
        manager.refresh()
        assert mock_fetch.call_count == 2

        # Verify cache is passed to get functions
        mock_agents.assert_called_with(loaded_labels={'com.test'})
        mock_daemons.assert_called_with(loaded_labels={'com.test'})

    @pytest.mark.integration
    @patch('startup_manager.enable_launch_agent')
    @patch('startup_manager.disable_launch_agent')
    @patch('startup_manager.disable_login_item')
    def test_enable_disable_workflow(self, mock_disable_login, mock_disable_agent, mock_enable_agent):
        """Test complete enable/disable workflow."""
        mock_disable_login.return_value = True
        mock_disable_agent.return_value = True
        mock_enable_agent.return_value = True

        manager = StartupManager()

        # Test disabling login item
        login_item = {'name': 'TestApp', 'type': 'Login Item'}
        assert manager.disable_item(login_item) is True
        mock_disable_login.assert_called_once_with('TestApp')

        # Test disabling agent
        agent_item = {'label': 'com.test.agent', 'type': 'Launch Agent'}
        assert manager.disable_item(agent_item) is True
        mock_disable_agent.assert_called_once_with('com.test.agent')

        # Test enabling agent
        agent_item['path'] = '/path/to/agent.plist'
        assert manager.enable_item(agent_item) is True
        mock_enable_agent.assert_called_once_with('com.test.agent', '/path/to/agent.plist')

        # Test that login items can't be re-enabled
        assert manager.enable_item(login_item) is False
