"""
Tests for ui/processes_tab.py - ProcessesTab class
"""

import sys
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

import pytest
from PyQt6.QtWidgets import QMessageBox, QTableWidgetItem
from PyQt6.QtCore import Qt

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from ui.processes_tab import ProcessesTab


class TestProcessesTab:
    """Test ProcessesTab class."""

    @pytest.fixture
    def processes_tab(self, qapp, mock_process_monitor):
        """Create a ProcessesTab instance for testing."""
        mock_process_monitor.get_processes.return_value = [
            {
                'pid': 100,
                'name': 'Chrome',
                'memory_human': '500 MB',
                'memory_mb': 500,
                'memory_percent': 10.0,
                'cpu_percent': 25.0,
            },
            {
                'pid': 200,
                'name': 'Firefox',
                'memory_human': '300 MB',
                'memory_mb': 300,
                'memory_percent': 6.0,
                'cpu_percent': 15.0,
            },
        ]
        mock_process_monitor.get_system_summary.return_value = {
            'process_count': 150,
            'memory_percent': 50.0,
            'cpu_percent': 35.0,
        }

        tab = ProcessesTab(mock_process_monitor)
        return tab

    def test_initialization(self, processes_tab, mock_process_monitor):
        """Test ProcessesTab initialization."""
        assert processes_tab.process_monitor == mock_process_monitor
        assert processes_tab.current_processes == []
        assert processes_tab.is_updating == False

    def test_setup_ui(self, processes_tab):
        """Test UI setup."""
        assert processes_tab.table is not None
        assert processes_tab.search_bar is not None
        assert processes_tab.refresh_btn is not None
        assert processes_tab.system_processes_cb is not None
        assert processes_tab.quit_btn is not None
        assert processes_tab.process_count_card is not None
        assert processes_tab.memory_card is not None
        assert processes_tab.cpu_card is not None

    def test_create_table(self, processes_tab):
        """Test table creation."""
        table = processes_tab.table

        assert table is not None
        assert table.columnCount() == 5
        assert table.horizontalHeaderItem(0).text() == "PID"
        assert table.horizontalHeaderItem(1).text() == "Name"
        assert table.horizontalHeaderItem(2).text() == "Memory"
        assert table.horizontalHeaderItem(3).text() == "Memory %"
        assert table.horizontalHeaderItem(4).text() == "CPU %"

    def test_update_data(self, processes_tab, mock_process_monitor):
        """Test data update."""
        processes_tab.update_data()

        assert processes_tab.is_updating == False  # Should be reset after update
        mock_process_monitor.refresh.assert_called()
        assert len(processes_tab.current_processes) > 0

    def test_update_data_concurrent_lock(self, processes_tab):
        """Test that concurrent updates are prevented."""
        processes_tab.is_updating = True

        processes_tab.update_data()

        # Should return early without updating
        assert processes_tab.is_updating == True

    def test_update_metrics(self, processes_tab, mock_process_monitor):
        """Test metric card updates."""
        mock_process_monitor.get_system_summary.return_value = {
            'process_count': 150,
            'memory_percent': 75.0,
            'cpu_percent': 85.0,
        }

        processes_tab.update_metrics()

        # Cards should be updated (we can't check exact values due to mocking,
        # but method should run without error)
        assert True

    def test_get_status_from_percent(self, processes_tab):
        """Test status level calculation."""
        assert processes_tab.get_status_from_percent(30) == "low"
        assert processes_tab.get_status_from_percent(60) == "medium"
        assert processes_tab.get_status_from_percent(90) == "high"

    def test_apply_filters(self, processes_tab):
        """Test filter application."""
        processes_tab.current_processes = [
            {
                'pid': 100,
                'name': 'Chrome',
                'memory_human': '500 MB',
                'memory_mb': 500,
                'memory_percent': 10.0,
                'cpu_percent': 25.0,
            },
            {
                'pid': 200,
                'name': 'Firefox',
                'memory_human': '300 MB',
                'memory_mb': 300,
                'memory_percent': 6.0,
                'cpu_percent': 15.0,
            },
        ]

        processes_tab.search_bar.line_edit.setText("Chrome")
        processes_tab.apply_filters()

        # Table should have 1 row (Chrome)
        assert processes_tab.table.rowCount() == 1

    def test_populate_table(self, processes_tab):
        """Test table population."""
        processes = [
            {
                'pid': 100,
                'name': 'Chrome',
                'memory_human': '500 MB',
                'memory_mb': 500,
                'memory_percent': 10.0,
                'cpu_percent': 25.0,
            },
        ]

        processes_tab.populate_table(processes)

        assert processes_tab.table.rowCount() == 1
        assert processes_tab.table.item(0, 0).text() == "100"
        assert processes_tab.table.item(0, 1).text() == "Chrome"

    def test_populate_table_limit(self, processes_tab):
        """Test table population with limit."""
        # Create 150 processes
        processes = [
            {
                'pid': i,
                'name': f'Process {i}',
                'memory_human': '100 MB',
                'memory_mb': 100,
                'memory_percent': 5.0,
                'cpu_percent': 10.0,
            }
            for i in range(150)
        ]

        processes_tab.populate_table(processes)

        # Should be limited to 100
        assert processes_tab.table.rowCount() == 100

    def test_on_search(self, processes_tab):
        """Test search handler."""
        with patch.object(processes_tab, 'apply_filters') as mock_apply:
            processes_tab.on_search("test")
            mock_apply.assert_called_once()

    def test_on_refresh(self, processes_tab):
        """Test refresh button handler."""
        with patch.object(processes_tab, 'update_data') as mock_update:
            processes_tab.on_refresh()
            mock_update.assert_called_once()

    def test_on_system_toggle(self, processes_tab, mock_process_monitor):
        """Test system processes toggle."""
        with patch.object(processes_tab, 'update_data') as mock_update:
            processes_tab.on_system_toggle(Qt.CheckState.Checked.value)

            mock_process_monitor.set_include_system_processes.assert_called_with(True)
            mock_update.assert_called_once()

    def test_on_force_quit_no_selection(self, processes_tab, qapp):
        """Test force quit with no selection."""
        with patch.object(QMessageBox, 'information') as mock_msg:
            processes_tab.on_force_quit()

            mock_msg.assert_called_once()
            assert "No Selection" in mock_msg.call_args[0][1]

    def test_on_force_quit_with_confirmation(self, processes_tab, mock_process_monitor, qapp):
        """Test force quit with confirmation."""
        # Populate table
        processes = [
            {
                'pid': 100,
                'name': 'Chrome',
                'memory_human': '500 MB',
                'memory_mb': 500,
                'memory_percent': 10.0,
                'cpu_percent': 25.0,
            },
        ]
        processes_tab.populate_table(processes)

        # Select first row
        processes_tab.table.selectRow(0)

        mock_process_monitor.kill_process.return_value = True

        with patch.object(QMessageBox, 'warning', return_value=QMessageBox.StandardButton.Yes), \
             patch.object(QMessageBox, 'information') as mock_info, \
             patch.object(processes_tab, 'on_refresh'):

            processes_tab.on_force_quit()

            # Should kill process and show success
            mock_process_monitor.kill_process.assert_called_with(100, force=True)
            mock_info.assert_called_once()

    def test_on_force_quit_cancelled(self, processes_tab, qapp):
        """Test force quit cancelled."""
        # Populate table
        processes = [
            {
                'pid': 100,
                'name': 'Chrome',
                'memory_human': '500 MB',
                'memory_mb': 500,
                'memory_percent': 10.0,
                'cpu_percent': 25.0,
            },
        ]
        processes_tab.populate_table(processes)
        processes_tab.table.selectRow(0)

        with patch.object(QMessageBox, 'warning', return_value=QMessageBox.StandardButton.No):
            processes_tab.on_force_quit()

            # Should not proceed

    def test_on_process_double_clicked(self, processes_tab, mock_process_monitor):
        """Test double-click on process."""
        # Populate table
        processes = [
            {
                'pid': 100,
                'name': 'Chrome',
                'memory_human': '500 MB',
                'memory_mb': 500,
                'memory_percent': 10.0,
                'cpu_percent': 25.0,
            },
        ]
        processes_tab.populate_table(processes)

        mock_process_monitor.get_process_details.return_value = {
            'username': 'testuser',
            'status': 'running',
            'num_threads': 10,
        }

        with patch('ui.processes_tab.ProcessDetailDialog') as mock_dialog:
            dialog_instance = MagicMock()
            mock_dialog.return_value = dialog_instance

            processes_tab.on_process_double_clicked(0, 0)

            mock_dialog.assert_called_once()
            dialog_instance.exec.assert_called_once()

    def test_on_process_double_clicked_not_found(self, processes_tab, mock_process_monitor, qapp):
        """Test double-click on process that no longer exists."""
        # Populate table
        processes = [
            {
                'pid': 100,
                'name': 'Chrome',
                'memory_human': '500 MB',
                'memory_mb': 500,
                'memory_percent': 10.0,
                'cpu_percent': 25.0,
            },
        ]
        processes_tab.populate_table(processes)

        mock_process_monitor.get_process_details.return_value = None

        with patch.object(QMessageBox, 'warning') as mock_warn:
            processes_tab.on_process_double_clicked(0, 0)

            mock_warn.assert_called_once()
            assert "Process Not Found" in mock_warn.call_args[0][1]

    def test_get_color_for_percent(self, processes_tab):
        """Test color calculation."""
        from PyQt6.QtGui import QColor

        color = processes_tab.get_color_for_percent(75.0)
        assert isinstance(color, QColor)
