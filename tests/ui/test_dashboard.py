"""
Tests for ui/dashboard.py - Dashboard class
"""

import sys
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock, PropertyMock

import pytest
from PyQt6.QtWidgets import QApplication, QMessageBox
from PyQt6.QtCore import QTimer

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from ui.dashboard import Dashboard


class TestDashboard:
    """Test Dashboard class."""

    @pytest.fixture
    def dashboard(self, qapp, mock_startup_manager, mock_process_monitor):
        """Create a Dashboard instance for testing."""
        with patch('ui.dashboard.StartupTab'), \
             patch('ui.dashboard.ProcessesTab'), \
             patch('ui.dashboard.GlassmorphicPanel'), \
             patch('ui.dashboard.MetricCard'), \
             patch('ui.dashboard.CircularGauge'), \
             patch('ui.dashboard.RealtimeLineChart'), \
             patch('ui.dashboard.BarChart'):

            mock_process_monitor.get_memory_info.return_value = {
                'percent': 50.0,
                'total_human': '16 GB',
                'used_human': '8 GB',
                'available_human': '8 GB',
            }
            mock_process_monitor.get_cpu_info.return_value = {
                'percent': 35.0,
                'count_logical': 16,
                'count_physical': 8,
            }
            mock_process_monitor.get_process_count.return_value = 150
            mock_process_monitor.get_top_memory_processes.return_value = []
            mock_process_monitor.get_top_cpu_processes.return_value = []

            mock_startup_manager.get_summary.return_value = {
                'total': 10,
                'enabled': 5,
                'disabled': 5,
            }

            dashboard = Dashboard(mock_startup_manager, mock_process_monitor)

            # Stop timers to prevent interference
            dashboard.process_timer.stop()
            dashboard.overview_timer.stop()

            return dashboard

    def test_initialization(self, dashboard, mock_startup_manager, mock_process_monitor):
        """Test Dashboard initialization."""
        assert dashboard.startup_manager == mock_startup_manager
        assert dashboard.process_monitor == mock_process_monitor
        assert dashboard.tab_widget is not None

    def test_setup_ui(self, dashboard):
        """Test UI setup."""
        assert dashboard.tab_widget is not None
        assert dashboard.tab_widget.count() == 3  # Startup, Processes, System tabs

    def test_create_enhanced_overview_tab(self, qapp, mock_startup_manager, mock_process_monitor):
        """Test overview tab creation."""
        with patch('ui.dashboard.StartupTab'), \
             patch('ui.dashboard.ProcessesTab'), \
             patch('ui.dashboard.GlassmorphicPanel') as mock_panel, \
             patch('ui.dashboard.MetricCard') as mock_card, \
             patch('ui.dashboard.CircularGauge') as mock_gauge, \
             patch('ui.dashboard.RealtimeLineChart') as mock_chart, \
             patch('ui.dashboard.BarChart') as mock_bar:

            mock_process_monitor.get_memory_info.return_value = {'percent': 50.0, 'total_human': '16 GB'}
            mock_process_monitor.get_cpu_info.return_value = {'percent': 35.0, 'count_logical': 16}
            mock_process_monitor.get_process_count.return_value = 150
            mock_startup_manager.get_summary.return_value = {'total': 10, 'enabled': 5, 'disabled': 5}

            dashboard = Dashboard(mock_startup_manager, mock_process_monitor)

            assert mock_gauge.call_count >= 3  # CPU, Memory, Processes gauges
            assert mock_chart.call_count >= 2  # CPU and Memory charts
            assert mock_bar.call_count >= 2  # Memory and CPU bar charts
            assert mock_card.call_count >= 3  # System info cards

    def test_setup_timers(self, qapp, mock_startup_manager, mock_process_monitor):
        """Test timer setup."""
        with patch('ui.dashboard.StartupTab'), \
             patch('ui.dashboard.ProcessesTab'), \
             patch('ui.dashboard.GlassmorphicPanel'), \
             patch('ui.dashboard.MetricCard'), \
             patch('ui.dashboard.CircularGauge'), \
             patch('ui.dashboard.RealtimeLineChart'), \
             patch('ui.dashboard.BarChart'):

            mock_process_monitor.get_memory_info.return_value = {'percent': 50.0, 'total_human': '16 GB'}
            mock_process_monitor.get_cpu_info.return_value = {'percent': 35.0, 'count_logical': 16}
            mock_process_monitor.get_process_count.return_value = 150
            mock_startup_manager.get_summary.return_value = {'total': 10, 'enabled': 5}

            dashboard = Dashboard(mock_startup_manager, mock_process_monitor)

            assert dashboard.process_timer is not None
            assert dashboard.overview_timer is not None
            assert isinstance(dashboard.process_timer, QTimer)
            assert isinstance(dashboard.overview_timer, QTimer)

    def test_on_tab_changed_processes(self, dashboard):
        """Test tab change to processes tab."""
        dashboard.tab_widget.setCurrentIndex(1)  # Processes tab
        dashboard.on_tab_changed(1)

        # Should trigger update_data on processes tab
        # (Implementation detail - may need adjustment based on actual tab indices)

    def test_on_tab_changed_overview(self, dashboard):
        """Test tab change to overview tab."""
        with patch.object(dashboard, 'refresh_overview') as mock_refresh:
            # Set to system/overview tab (index 2)
            dashboard.tab_widget.setCurrentIndex(2)
            dashboard.on_tab_changed(2)

            # Should refresh overview
            mock_refresh.assert_called_once()

    def test_load_initial_data(self, qapp, mock_startup_manager, mock_process_monitor):
        """Test initial data loading."""
        with patch('ui.dashboard.StartupTab') as mock_startup_tab, \
             patch('ui.dashboard.ProcessesTab') as mock_processes_tab, \
             patch('ui.dashboard.GlassmorphicPanel'), \
             patch('ui.dashboard.MetricCard'), \
             patch('ui.dashboard.CircularGauge'), \
             patch('ui.dashboard.RealtimeLineChart'), \
             patch('ui.dashboard.BarChart'):

            mock_process_monitor.get_memory_info.return_value = {'percent': 50.0, 'total_human': '16 GB'}
            mock_process_monitor.get_cpu_info.return_value = {'percent': 35.0, 'count_logical': 16}
            mock_process_monitor.get_process_count.return_value = 150
            mock_startup_manager.get_summary.return_value = {'total': 10, 'enabled': 5}

            # Mock tab instances
            startup_instance = MagicMock()
            processes_instance = MagicMock()
            mock_startup_tab.return_value = startup_instance
            mock_processes_tab.return_value = processes_instance

            dashboard = Dashboard(mock_startup_manager, mock_process_monitor)

            # Check that managers were refreshed
            mock_startup_manager.refresh.assert_called()
            mock_process_monitor.refresh.assert_called()

    def test_refresh_processes(self, dashboard):
        """Test process refresh."""
        dashboard.tab_widget.setCurrentWidget(dashboard.processes_tab)
        dashboard.processes_tab.update_data = Mock()

        dashboard.refresh_processes()

        # Should update data
        dashboard.processes_tab.update_data.assert_called_once()

    def test_refresh_processes_not_visible(self, dashboard):
        """Test process refresh when tab not visible."""
        dashboard.tab_widget.setCurrentWidget(dashboard.startup_tab)
        dashboard.processes_tab.update_data = Mock()

        dashboard.refresh_processes()

        # Should NOT update data
        dashboard.processes_tab.update_data.assert_not_called()

    def test_refresh_overview(self, dashboard, mock_process_monitor, mock_startup_manager):
        """Test overview refresh."""
        dashboard.tab_widget.setCurrentWidget(dashboard.overview_tab)

        # Mock all the gauge and chart update methods
        dashboard.cpu_gauge = MagicMock()
        dashboard.memory_gauge = MagicMock()
        dashboard.processes_gauge = MagicMock()
        dashboard.cpu_chart = MagicMock()
        dashboard.memory_chart = MagicMock()
        dashboard.memory_bar_chart = MagicMock()
        dashboard.cpu_bar_chart = MagicMock()
        dashboard.total_memory_card = MagicMock()
        dashboard.cpu_cores_card = MagicMock()
        dashboard.startup_items_card = MagicMock()
        dashboard.status_label = MagicMock()

        dashboard.refresh_overview()

        # Verify gauges were updated
        dashboard.cpu_gauge.set_value.assert_called()
        dashboard.memory_gauge.set_value.assert_called()
        dashboard.processes_gauge.set_value.assert_called()

    def test_refresh_overview_error(self, dashboard, mock_process_monitor):
        """Test overview refresh with error."""
        dashboard.tab_widget.setCurrentWidget(dashboard.overview_tab)
        dashboard.status_label = MagicMock()

        # Make get_memory_info raise an exception
        mock_process_monitor.get_memory_info.side_effect = Exception("Test error")

        dashboard.refresh_overview()

        # Should set status to error
        dashboard.status_label.setText.assert_called_with("● ERROR")

    def test_on_memory_bar_clicked(self, dashboard):
        """Test memory bar chart click handler."""
        with patch.object(dashboard, '_show_process_detail') as mock_show:
            process_data = {'pid': 123, 'name': 'test'}
            entry = {'payload': process_data}

            dashboard.on_memory_bar_clicked(entry)

            mock_show.assert_called_once_with(process_data)

    def test_on_cpu_bar_clicked(self, dashboard):
        """Test CPU bar chart click handler."""
        with patch.object(dashboard, '_show_process_detail') as mock_show:
            process_data = {'pid': 123, 'name': 'test'}
            entry = {'payload': process_data}

            dashboard.on_cpu_bar_clicked(entry)

            mock_show.assert_called_once_with(process_data)

    def test_show_process_detail(self, dashboard):
        """Test showing process detail dialog."""
        with patch('ui.dashboard.ProcessDetailDialog') as mock_dialog:
            dialog_instance = MagicMock()
            mock_dialog.return_value = dialog_instance

            process_data = {'pid': 123, 'name': 'test'}
            dashboard._show_process_detail(process_data)

            mock_dialog.assert_called_once_with(process_data, dashboard)
            dialog_instance.exec.assert_called_once()

    def test_show_memory_info(self, dashboard, mock_process_monitor):
        """Test showing memory info dialog."""
        mock_process_monitor.get_memory_info.return_value = {
            'total_human': '16 GB',
            'used_human': '8 GB',
            'available_human': '8 GB',
            'percent': 50.0,
        }

        with patch('ui.dashboard.QMessageBox.information') as mock_msg:
            dashboard._show_memory_info()

            mock_msg.assert_called_once()
            args = mock_msg.call_args[0]
            assert "16 GB" in args[2]  # Message contains total memory

    def test_show_cpu_info(self, dashboard, mock_process_monitor):
        """Test showing CPU info dialog."""
        mock_process_monitor.get_cpu_info.return_value = {
            'count_logical': 16,
            'count_physical': 8,
            'percent': 35.0,
        }

        with patch('ui.dashboard.QMessageBox.information') as mock_msg:
            dashboard._show_cpu_info()

            mock_msg.assert_called_once()
            args = mock_msg.call_args[0]
            assert "16" in args[2] or "8" in args[2]  # Message contains core count

    def test_show_startup_info_high(self, dashboard, mock_startup_manager):
        """Test showing startup info dialog with high item count."""
        mock_startup_manager.get_summary.return_value = {
            'total': 25,
            'enabled': 25,
            'disabled': 0,
        }

        with patch('ui.dashboard.QMessageBox.information') as mock_msg:
            dashboard._show_startup_info()

            mock_msg.assert_called_once()
            args = mock_msg.call_args[0]
            assert "25" in args[2]

    def test_show_startup_info_medium(self, dashboard, mock_startup_manager):
        """Test showing startup info dialog with medium item count."""
        mock_startup_manager.get_summary.return_value = {
            'total': 15,
            'enabled': 15,
            'disabled': 0,
        }

        with patch('ui.dashboard.QMessageBox.information') as mock_msg:
            dashboard._show_startup_info()

            mock_msg.assert_called_once()

    def test_show_startup_info_low(self, dashboard, mock_startup_manager):
        """Test showing startup info dialog with low item count."""
        mock_startup_manager.get_summary.return_value = {
            'total': 5,
            'enabled': 5,
            'disabled': 0,
        }

        with patch('ui.dashboard.QMessageBox.information') as mock_msg:
            dashboard._show_startup_info()

            mock_msg.assert_called_once()

    def test_cleanup(self, dashboard):
        """Test cleanup method."""
        # Start timers
        dashboard.process_timer.start(1000)
        dashboard.overview_timer.start(1000)

        # Cleanup
        dashboard.cleanup()

        # Timers should be stopped
        assert not dashboard.process_timer.isActive()
        assert not dashboard.overview_timer.isActive()
