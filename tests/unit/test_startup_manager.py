"""
Unit Tests for startup_manager.py

Tests StartupManager class with comprehensive coverage.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
import time

from startup_manager import StartupManager


class TestStartupManagerInit:
    """Test StartupManager initialization."""

    @pytest.mark.unit
    def test_initialization(self):
        """Test that StartupManager initializes with correct defaults."""
        manager = StartupManager()

        assert manager.login_items == []
        assert manager.launch_agents == []
        assert manager.launch_daemons == []
        assert manager.all_items == []
        assert manager._launchctl_cache == set()
        assert manager._launchctl_cache_ts == 0.0


class TestRefresh:
    """Test refresh method."""

    @pytest.mark.unit
    @patch('startup_manager.fetch_launchctl_status')
    @patch('startup_manager.get_launch_daemons')
    @patch('startup_manager.get_launch_agents')
    @patch('startup_manager.get_login_items')
    def test_refresh_updates_all_items(self, mock_login, mock_agents, mock_daemons, mock_fetch):
        """Test that refresh updates all item lists."""
        mock_fetch.return_value = {'com.test.service'}
        mock_login.return_value = [{'name': 'Login1', 'type': 'Login Item'}]
        mock_agents.return_value = [{'name': 'Agent1', 'type': 'Launch Agent'}]
        mock_daemons.return_value = [{'name': 'Daemon1', 'type': 'Launch Daemon'}]

        manager = StartupManager()
        result = manager.refresh()

        assert len(manager.login_items) == 1
        assert len(manager.launch_agents) == 1
        assert len(manager.launch_daemons) == 1
        assert len(manager.all_items) == 3
        assert result == manager.all_items

    @pytest.mark.unit
    @patch('startup_manager.time.time')
    @patch('startup_manager.fetch_launchctl_status')
    @patch('startup_manager.get_launch_daemons')
    @patch('startup_manager.get_launch_agents')
    @patch('startup_manager.get_login_items')
    def test_launchctl_cache_refresh(self, mock_login, mock_agents, mock_daemons, mock_fetch, mock_time):
        """Test that launchctl cache is refreshed after 5 seconds."""
        mock_fetch.return_value = {'com.test.service'}
        mock_login.return_value = []
        mock_agents.return_value = []
        mock_daemons.return_value = []

        # First call at time 0
        mock_time.return_value = 0.0
        manager = StartupManager()
        manager.refresh()
        assert mock_fetch.call_count == 1

        # Second call at time 3 (within cache window)
        mock_time.return_value = 3.0
        manager.refresh()
        assert mock_fetch.call_count == 1  # Should use cache

        # Third call at time 6 (beyond cache window)
        mock_time.return_value = 6.0
        manager.refresh()
        assert mock_fetch.call_count == 2  # Should refresh cache

    @pytest.mark.unit
    @patch('startup_manager.fetch_launchctl_status')
    @patch('startup_manager.get_launch_daemons')
    @patch('startup_manager.get_launch_agents')
    @patch('startup_manager.get_login_items')
    def test_passes_cache_to_functions(self, mock_login, mock_agents, mock_daemons, mock_fetch):
        """Test that launchctl cache is passed to get functions."""
        test_cache = {'com.test.service', 'com.another.service'}
        mock_fetch.return_value = test_cache
        mock_login.return_value = []
        mock_agents.return_value = []
        mock_daemons.return_value = []

        manager = StartupManager()
        manager.refresh()

        mock_agents.assert_called_once_with(loaded_labels=test_cache)
        mock_daemons.assert_called_once_with(loaded_labels=test_cache)


class TestGetAllItems:
    """Test get_all_items method."""

    @pytest.mark.unit
    def test_returns_all_items(self):
        """Test that get_all_items returns all startup items."""
        manager = StartupManager()
        manager.all_items = [
            {'name': 'Item1', 'type': 'Login Item'},
            {'name': 'Item2', 'type': 'Launch Agent'},
        ]

        result = manager.get_all_items()

        assert result == manager.all_items
        assert len(result) == 2


class TestGetLoginItemsOnly:
    """Test get_login_items_only method."""

    @pytest.mark.unit
    def test_returns_login_items(self):
        """Test that get_login_items_only returns only login items."""
        manager = StartupManager()
        manager.login_items = [{'name': 'Login1', 'type': 'Login Item'}]

        result = manager.get_login_items_only()

        assert result == manager.login_items


class TestGetLaunchAgentsOnly:
    """Test get_launch_agents_only method."""

    @pytest.mark.unit
    def test_returns_launch_agents(self):
        """Test that get_launch_agents_only returns only launch agents."""
        manager = StartupManager()
        manager.launch_agents = [{'name': 'Agent1', 'type': 'Launch Agent'}]

        result = manager.get_launch_agents_only()

        assert result == manager.launch_agents


class TestGetLaunchDaemonsOnly:
    """Test get_launch_daemons_only method."""

    @pytest.mark.unit
    def test_returns_launch_daemons(self):
        """Test that get_launch_daemons_only returns only launch daemons."""
        manager = StartupManager()
        manager.launch_daemons = [{'name': 'Daemon1', 'type': 'Launch Daemon'}]

        result = manager.get_launch_daemons_only()

        assert result == manager.launch_daemons


class TestGetEnabledItems:
    """Test get_enabled_items method."""

    @pytest.mark.unit
    def test_filters_enabled_items(self):
        """Test that get_enabled_items returns only enabled items."""
        manager = StartupManager()
        manager.all_items = [
            {'name': 'Enabled1', 'enabled': True},
            {'name': 'Disabled1', 'enabled': False},
            {'name': 'Enabled2', 'enabled': True},
        ]

        result = manager.get_enabled_items()

        assert len(result) == 2
        assert all(item['enabled'] for item in result)

    @pytest.mark.unit
    def test_treats_missing_enabled_as_true(self):
        """Test that items without 'enabled' key are treated as enabled."""
        manager = StartupManager()
        manager.all_items = [
            {'name': 'Item1'},
            {'name': 'Item2', 'enabled': False},
        ]

        result = manager.get_enabled_items()

        assert len(result) == 1
        assert result[0]['name'] == 'Item1'


class TestGetDisabledItems:
    """Test get_disabled_items method."""

    @pytest.mark.unit
    def test_filters_disabled_items(self):
        """Test that get_disabled_items returns only disabled items."""
        manager = StartupManager()
        manager.all_items = [
            {'name': 'Enabled1', 'enabled': True},
            {'name': 'Disabled1', 'enabled': False},
            {'name': 'Disabled2', 'enabled': False},
        ]

        result = manager.get_disabled_items()

        assert len(result) == 2
        assert all(not item['enabled'] for item in result)


class TestDisableItem:
    """Test disable_item method."""

    @pytest.mark.unit
    @patch('startup_manager.disable_login_item')
    def test_disable_login_item(self, mock_disable_login):
        """Test disabling a login item."""
        mock_disable_login.return_value = True
        manager = StartupManager()

        item = {'name': 'TestApp', 'type': 'Login Item'}
        result = manager.disable_item(item)

        assert result is True
        mock_disable_login.assert_called_once_with('TestApp')

    @pytest.mark.unit
    @patch('startup_manager.disable_launch_agent')
    def test_disable_launch_agent(self, mock_disable_agent):
        """Test disabling a launch agent."""
        mock_disable_agent.return_value = True
        manager = StartupManager()

        item = {'label': 'com.test.agent', 'type': 'Launch Agent'}
        result = manager.disable_item(item)

        assert result is True
        mock_disable_agent.assert_called_once_with('com.test.agent')

    @pytest.mark.unit
    @patch('startup_manager.disable_launch_agent')
    def test_disable_launch_daemon(self, mock_disable_agent):
        """Test disabling a launch daemon."""
        mock_disable_agent.return_value = True
        manager = StartupManager()

        item = {'label': 'com.test.daemon', 'type': 'Launch Daemon'}
        result = manager.disable_item(item)

        assert result is True
        mock_disable_agent.assert_called_once_with('com.test.daemon')

    @pytest.mark.unit
    def test_unknown_type_returns_false(self):
        """Test that unknown type returns False."""
        manager = StartupManager()

        item = {'name': 'Unknown', 'type': 'Unknown Type'}
        result = manager.disable_item(item)

        assert result is False


class TestEnableItem:
    """Test enable_item method."""

    @pytest.mark.unit
    @patch('startup_manager.enable_launch_agent')
    def test_enable_launch_agent(self, mock_enable_agent):
        """Test enabling a launch agent."""
        mock_enable_agent.return_value = True
        manager = StartupManager()

        item = {
            'label': 'com.test.agent',
            'path': '/path/to/agent.plist',
            'type': 'Launch Agent'
        }
        result = manager.enable_item(item)

        assert result is True
        mock_enable_agent.assert_called_once_with('com.test.agent', '/path/to/agent.plist')

    @pytest.mark.unit
    @patch('startup_manager.enable_launch_agent')
    def test_enable_launch_daemon(self, mock_enable_agent):
        """Test enabling a launch daemon."""
        mock_enable_agent.return_value = True
        manager = StartupManager()

        item = {
            'label': 'com.test.daemon',
            'path': '/path/to/daemon.plist',
            'type': 'Launch Daemon'
        }
        result = manager.enable_item(item)

        assert result is True

    @pytest.mark.unit
    def test_enable_login_item_returns_false(self):
        """Test that enabling login item returns False (not supported)."""
        manager = StartupManager()

        item = {'name': 'TestApp', 'type': 'Login Item'}
        result = manager.enable_item(item)

        assert result is False


class TestGetItemCount:
    """Test get_item_count method."""

    @pytest.mark.unit
    def test_returns_correct_count(self):
        """Test that get_item_count returns correct count."""
        manager = StartupManager()
        manager.all_items = [
            {'name': 'Item1'},
            {'name': 'Item2'},
            {'name': 'Item3'},
        ]

        result = manager.get_item_count()

        assert result == 3

    @pytest.mark.unit
    def test_empty_list(self):
        """Test count with empty list."""
        manager = StartupManager()
        manager.all_items = []

        assert manager.get_item_count() == 0


class TestGetEnabledCount:
    """Test get_enabled_count method."""

    @pytest.mark.unit
    def test_returns_correct_count(self):
        """Test that get_enabled_count returns correct count."""
        manager = StartupManager()
        manager.all_items = [
            {'name': 'Enabled1', 'enabled': True},
            {'name': 'Disabled1', 'enabled': False},
            {'name': 'Enabled2', 'enabled': True},
        ]

        result = manager.get_enabled_count()

        assert result == 2


class TestGetDisabledCount:
    """Test get_disabled_count method."""

    @pytest.mark.unit
    def test_returns_correct_count(self):
        """Test that get_disabled_count returns correct count."""
        manager = StartupManager()
        manager.all_items = [
            {'name': 'Enabled1', 'enabled': True},
            {'name': 'Disabled1', 'enabled': False},
            {'name': 'Disabled2', 'enabled': False},
        ]

        result = manager.get_disabled_count()

        assert result == 2


class TestSearchItems:
    """Test search_items method."""

    @pytest.mark.unit
    def test_search_by_name(self):
        """Test searching by name."""
        manager = StartupManager()
        manager.all_items = [
            {'name': 'Dropbox', 'label': 'com.dropbox.app'},
            {'name': 'Slack', 'label': 'com.slack.app'},
            {'name': 'Google Drive', 'label': 'com.google.drive'},
        ]

        result = manager.search_items('drop')

        assert len(result) == 1
        assert result[0]['name'] == 'Dropbox'

    @pytest.mark.unit
    def test_search_by_label(self):
        """Test searching by label."""
        manager = StartupManager()
        manager.all_items = [
            {'name': 'Test1', 'label': 'com.apple.service'},
            {'name': 'Test2', 'label': 'com.google.service'},
        ]

        result = manager.search_items('apple')

        assert len(result) == 1
        assert result[0]['label'] == 'com.apple.service'

    @pytest.mark.unit
    def test_case_insensitive_search(self):
        """Test that search is case-insensitive."""
        manager = StartupManager()
        manager.all_items = [
            {'name': 'Google Chrome', 'label': 'com.google.chrome'},
        ]

        result = manager.search_items('CHROME')

        assert len(result) == 1

    @pytest.mark.unit
    def test_no_matches(self):
        """Test when search returns no matches."""
        manager = StartupManager()
        manager.all_items = [
            {'name': 'Test', 'label': 'com.test'},
        ]

        result = manager.search_items('nonexistent')

        assert result == []

    @pytest.mark.unit
    def test_handles_missing_fields(self):
        """Test that search handles missing name or label fields."""
        manager = StartupManager()
        manager.all_items = [
            {'name': 'HasName'},
            {'label': 'com.has.label'},
        ]

        result = manager.search_items('hasname')

        assert len(result) == 1


class TestFilterByType:
    """Test filter_by_type method."""

    @pytest.mark.unit
    def test_filter_login_items(self):
        """Test filtering login items."""
        manager = StartupManager()
        manager.all_items = [
            {'name': 'Item1', 'type': 'Login Item'},
            {'name': 'Item2', 'type': 'Launch Agent'},
            {'name': 'Item3', 'type': 'Login Item'},
        ]

        result = manager.filter_by_type('Login Item')

        assert len(result) == 2
        assert all(item['type'] == 'Login Item' for item in result)

    @pytest.mark.unit
    def test_filter_launch_agents(self):
        """Test filtering launch agents."""
        manager = StartupManager()
        manager.all_items = [
            {'name': 'Item1', 'type': 'Login Item'},
            {'name': 'Item2', 'type': 'Launch Agent'},
            {'name': 'Item3', 'type': 'Launch Daemon'},
        ]

        result = manager.filter_by_type('Launch Agent')

        assert len(result) == 1
        assert result[0]['type'] == 'Launch Agent'

    @pytest.mark.unit
    def test_no_matches(self):
        """Test when no items match the type."""
        manager = StartupManager()
        manager.all_items = [
            {'name': 'Item1', 'type': 'Login Item'},
        ]

        result = manager.filter_by_type('Launch Agent')

        assert result == []


class TestGetSummary:
    """Test get_summary method."""

    @pytest.mark.unit
    def test_returns_complete_summary(self):
        """Test that summary contains all expected statistics."""
        manager = StartupManager()
        manager.login_items = [{'name': 'Login1', 'enabled': True}]
        manager.launch_agents = [
            {'name': 'Agent1', 'enabled': True},
            {'name': 'Agent2', 'enabled': False}
        ]
        manager.launch_daemons = [{'name': 'Daemon1', 'enabled': True}]
        manager.all_items = manager.login_items + manager.launch_agents + manager.launch_daemons

        result = manager.get_summary()

        assert result['total'] == 4
        assert result['enabled'] == 3
        assert result['disabled'] == 1
        assert result['login_items'] == 1
        assert result['launch_agents'] == 2
        assert result['launch_daemons'] == 1

    @pytest.mark.unit
    def test_empty_manager(self):
        """Test summary with no items."""
        manager = StartupManager()

        result = manager.get_summary()

        assert result['total'] == 0
        assert result['enabled'] == 0
        assert result['disabled'] == 0
        assert result['login_items'] == 0
        assert result['launch_agents'] == 0
        assert result['launch_daemons'] == 0
