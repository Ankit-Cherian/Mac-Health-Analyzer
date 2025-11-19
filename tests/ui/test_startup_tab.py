"""
Tests for ui/startup_tab.py - StartupTab class
"""

import sys
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

import pytest
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtCore import Qt

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from ui.startup_tab import StartupTab


class TestStartupTab:
    """Test StartupTab class."""

    @pytest.fixture
    def startup_tab(self, qapp, mock_startup_manager, mock_process_monitor):
        """Create a StartupTab instance for testing."""
        mock_process_monitor.get_processes.return_value = [
            {
                'pid': 101,
                'name': 'Dropbox',
                'cpu_percent': 12.5,
                'memory_percent': 5.0,
            },
            {
                'pid': 202,
                'name': 'Slack Helper',
                'cpu_percent': 3.2,
                'memory_percent': 1.1,
            },
        ]
        mock_startup_manager.get_all_items.return_value = [
            {
                'name': 'Dropbox',
                'type': 'Login Item',
                'enabled': True,
                'location': '/Applications/Dropbox.app',
            },
            {
                'name': 'Slack',
                'type': 'Launch Agent',
                'enabled': False,
                'label': 'com.slack.agent',
                'location': '/Library/LaunchAgents/com.slack.agent.plist',
            },
        ]
        mock_startup_manager.get_summary.return_value = {
            'total': 10,
            'enabled': 6,
            'disabled': 4,
        }

        tab = StartupTab(mock_startup_manager, mock_process_monitor)
        return tab

    def test_initialization(self, startup_tab, mock_startup_manager):
        """Test StartupTab initialization."""
        assert startup_tab.startup_manager == mock_startup_manager
        assert startup_tab.current_items == []

    def test_setup_ui(self, startup_tab):
        """Test UI setup."""
        assert startup_tab.table is not None
        assert startup_tab.search_bar is not None
        assert startup_tab.refresh_btn is not None
        assert startup_tab.filter_combo is not None
        assert startup_tab.disable_btn is not None
        assert startup_tab.summary_panel is not None

    def test_create_summary_panel(self, startup_tab):
        """Test summary panel creation."""
        assert startup_tab.total_label is not None
        assert startup_tab.enabled_label is not None
        assert startup_tab.disabled_label is not None

    def test_create_table(self, startup_tab):
        """Test table creation."""
        table = startup_tab.table

        assert table is not None
        assert table.columnCount() == 7
        assert table.horizontalHeaderItem(0).text() == "Name"
        assert table.horizontalHeaderItem(1).text() == "Type"
        assert table.horizontalHeaderItem(2).text() == "Status"
        assert table.horizontalHeaderItem(3).text() == "CPU %"
        assert table.horizontalHeaderItem(4).text() == "Memory %"
        assert table.horizontalHeaderItem(5).text() == "Location"
        assert table.horizontalHeaderItem(6).text() == "Toggle"

    def test_update_data(self, startup_tab, mock_startup_manager):
        """Test data update."""
        startup_tab.update_data()

        mock_startup_manager.get_all_items.assert_called()
        assert len(startup_tab.current_items) > 0

    def test_update_summary(self, startup_tab, mock_startup_manager):
        """Test summary update."""
        mock_startup_manager.get_summary.return_value = {
            'total': 15,
            'enabled': 10,
            'disabled': 5,
        }

        startup_tab.update_summary()

        assert startup_tab.total_label.text() == "15"
        assert startup_tab.enabled_label.text() == "10"
        assert startup_tab.disabled_label.text() == "5"

    def test_apply_filters_all_items(self, startup_tab):
        """Test filter application for all items."""
        startup_tab.current_items = [
            {
                'name': 'Dropbox',
                'type': 'Login Item',
                'enabled': True,
                'location': '/Applications/Dropbox.app',
            },
            {
                'name': 'Slack',
                'type': 'Launch Agent',
                'enabled': False,
                'label': 'com.slack.agent',
                'location': '/Library/LaunchAgents/com.slack.agent.plist',
            },
        ]

        startup_tab.filter_combo.setCurrentText("All Items")
        startup_tab.apply_filters()

        assert startup_tab.table.rowCount() == 2

    def test_apply_filters_login_items_only(self, startup_tab):
        """Test filter for login items only."""
        startup_tab.current_items = [
            {
                'name': 'Dropbox',
                'type': 'Login Item',
                'enabled': True,
                'location': '/Applications/Dropbox.app',
            },
            {
                'name': 'Slack',
                'type': 'Launch Agent',
                'enabled': False,
                'label': 'com.slack.agent',
                'location': '/Library/LaunchAgents/com.slack.agent.plist',
            },
        ]

        startup_tab.filter_combo.setCurrentText("Login Items")
        startup_tab.apply_filters()

        assert startup_tab.table.rowCount() == 1

    def test_apply_filters_enabled_only(self, startup_tab):
        """Test filter for enabled items only."""
        startup_tab.current_items = [
            {
                'name': 'Dropbox',
                'type': 'Login Item',
                'enabled': True,
                'location': '/Applications/Dropbox.app',
            },
            {
                'name': 'Slack',
                'type': 'Launch Agent',
                'enabled': False,
                'label': 'com.slack.agent',
                'location': '/Library/LaunchAgents/com.slack.agent.plist',
            },
        ]

        startup_tab.filter_combo.setCurrentText("Enabled Only")
        startup_tab.apply_filters()

        assert startup_tab.table.rowCount() == 1

    def test_apply_filters_search(self, startup_tab):
        """Test search filter."""
        startup_tab.current_items = [
            {
                'name': 'Dropbox',
                'type': 'Login Item',
                'enabled': True,
                'location': '/Applications/Dropbox.app',
            },
            {
                'name': 'Slack',
                'type': 'Launch Agent',
                'enabled': False,
                'label': 'com.slack.agent',
                'location': '/Library/LaunchAgents/com.slack.agent.plist',
            },
        ]

        startup_tab.search_bar.line_edit.setText("Dropbox")
        startup_tab.apply_filters()

        assert startup_tab.table.rowCount() == 1

    def test_populate_table(self, startup_tab):
        """Test table population."""
        items = [
            {
                'name': 'Dropbox',
                'type': 'Login Item',
                'enabled': True,
                'location': '/Applications/Dropbox.app',
            },
        ]

        startup_tab.populate_table(items)

        assert startup_tab.table.rowCount() == 1
        assert startup_tab.table.item(0, 0).text() == "Dropbox"
        assert startup_tab.table.item(0, 1).text() == "Login Item"
        assert startup_tab.table.item(0, 2).text() == "Enabled"
        assert startup_tab.table.item(0, 3).text() == "N/A"
        assert startup_tab.table.item(0, 4).text() == "N/A"
        assert startup_tab.table.item(0, 5).text() == "/Applications/Dropbox.app"

    def test_on_search(self, startup_tab):
        """Test search handler."""
        with patch.object(startup_tab, 'apply_filters') as mock_apply:
            startup_tab.on_search("test")
            mock_apply.assert_called_once()

    def test_on_refresh(self, startup_tab, mock_startup_manager):
        """Test refresh button handler."""
        startup_tab.on_refresh()

        mock_startup_manager.refresh.assert_called_once()
        assert not startup_tab.refresh_btn.isEnabled()
        assert startup_tab.refresh_btn.text() == "Refreshing..."

    def test_on_disable_selected_no_selection(self, startup_tab, qapp):
        """Test disable with no selection."""
        with patch.object(QMessageBox, 'information') as mock_msg:
            startup_tab.on_disable_selected()

            mock_msg.assert_called_once()
            assert "No Selection" in mock_msg.call_args[0][1]

    def test_on_disable_selected_with_confirmation(self, startup_tab, mock_startup_manager, qapp):
        """Test disable with confirmation."""
        # Populate table
        items = [
            {
                'name': 'Dropbox',
                'type': 'Login Item',
                'enabled': True,
                'location': '/Applications/Dropbox.app',
            },
        ]
        startup_tab.populate_table(items)
        startup_tab.table.selectRow(0)

        mock_startup_manager.disable_item.return_value = True

        with patch.object(QMessageBox, 'question', return_value=QMessageBox.StandardButton.Yes), \
             patch.object(QMessageBox, 'information') as mock_info, \
             patch.object(startup_tab, 'on_refresh'):

            startup_tab.on_disable_selected()

            # Should disable item and show success
            mock_startup_manager.disable_item.assert_called()
            mock_info.assert_called_once()

    def test_on_disable_selected_cancelled(self, startup_tab, qapp):
        """Test disable cancelled."""
        # Populate table
        items = [
            {
                'name': 'Dropbox',
                'type': 'Login Item',
                'enabled': True,
                'location': '/Applications/Dropbox.app',
            },
        ]
        startup_tab.populate_table(items)
        startup_tab.table.selectRow(0)

        with patch.object(QMessageBox, 'question', return_value=QMessageBox.StandardButton.No):
            startup_tab.on_disable_selected()

            # Should not proceed

    def test_on_item_double_clicked(self, startup_tab):
        """Test double-click on item."""
        # Populate table
        items = [
            {
                'name': 'Dropbox',
                'type': 'Login Item',
                'enabled': True,
                'location': '/Applications/Dropbox.app',
            },
        ]
        startup_tab.populate_table(items)

        with patch('ui.startup_tab.StartupDetailDialog') as mock_dialog:
            dialog_instance = MagicMock()
            mock_dialog.return_value = dialog_instance

            startup_tab.on_item_double_clicked(0, 0)

            mock_dialog.assert_called_once()
            dialog_instance.exec.assert_called_once()

    def test_on_item_double_clicked_no_data(self, startup_tab, qapp):
        """Test double-click on empty row."""
        startup_tab.on_item_double_clicked(0, 0)

        # Should handle gracefully (no exception)

    def test_on_item_double_clicked_error(self, startup_tab, qapp):
        """Test double-click with error."""
        # Populate table
        items = [
            {
                'name': 'Dropbox',
                'type': 'Login Item',
                'enabled': True,
                'location': '/Applications/Dropbox.app',
            },
        ]
        startup_tab.populate_table(items)

        with patch('ui.startup_tab.StartupDetailDialog', side_effect=Exception("Test error")), \
             patch.object(QMessageBox, 'warning') as mock_warn:

            startup_tab.on_item_double_clicked(0, 0)

            mock_warn.assert_called_once()
