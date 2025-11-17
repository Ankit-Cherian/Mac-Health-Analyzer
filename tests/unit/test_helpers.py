"""
Unit Tests for utils/helpers.py

Tests all helper functions with comprehensive coverage including edge cases.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
import psutil

from utils.helpers import (
    bytes_to_human_readable,
    get_system_memory_info,
    get_cpu_info,
    get_process_list,
    get_top_memory_processes,
    get_top_cpu_processes,
    kill_process,
    get_resource_usage_color,
    format_percentage,
)


# ========== Test bytes_to_human_readable ==========

class TestBytesToHumanReadable:
    """Test suite for bytes_to_human_readable function."""

    @pytest.mark.unit
    def test_bytes(self):
        """Test byte conversion for values less than 1KB."""
        assert bytes_to_human_readable(0) == "0.0 B"
        assert bytes_to_human_readable(512) == "512.0 B"
        assert bytes_to_human_readable(1023) == "1023.0 B"

    @pytest.mark.unit
    def test_kilobytes(self):
        """Test conversion to KB."""
        assert bytes_to_human_readable(1024) == "1.0 KB"
        assert bytes_to_human_readable(1536) == "1.5 KB"
        assert bytes_to_human_readable(1024 * 500) == "500.0 KB"

    @pytest.mark.unit
    def test_megabytes(self):
        """Test conversion to MB."""
        assert bytes_to_human_readable(1024 * 1024) == "1.0 MB"
        assert bytes_to_human_readable(1024 * 1024 * 100) == "100.0 MB"
        assert bytes_to_human_readable(1024 * 1024 * 512) == "512.0 MB"

    @pytest.mark.unit
    def test_gigabytes(self):
        """Test conversion to GB."""
        assert bytes_to_human_readable(1024 ** 3) == "1.0 GB"
        assert bytes_to_human_readable(1024 ** 3 * 16) == "16.0 GB"
        assert bytes_to_human_readable(1024 ** 3 * 64) == "64.0 GB"

    @pytest.mark.unit
    def test_terabytes(self):
        """Test conversion to TB."""
        assert bytes_to_human_readable(1024 ** 4) == "1.0 TB"
        assert bytes_to_human_readable(1024 ** 4 * 5) == "5.0 TB"

    @pytest.mark.unit
    def test_petabytes(self):
        """Test conversion to PB for very large values."""
        assert bytes_to_human_readable(1024 ** 5) == "1.0 PB"
        assert bytes_to_human_readable(1024 ** 5 * 10) == "10.0 PB"

    @pytest.mark.unit
    def test_edge_cases(self):
        """Test edge cases and boundary values."""
        # Exactly at boundaries
        assert bytes_to_human_readable(1024) == "1.0 KB"
        assert bytes_to_human_readable(1024 ** 2) == "1.0 MB"

        # Just below boundaries
        assert "1023.0 B" in bytes_to_human_readable(1023)
        assert "1023.0 KB" in bytes_to_human_readable(1024 * 1023)


# ========== Test get_system_memory_info ==========

class TestGetSystemMemoryInfo:
    """Test suite for get_system_memory_info function."""

    @pytest.mark.unit
    @patch('utils.helpers.psutil.virtual_memory')
    def test_returns_dict_with_expected_keys(self, mock_vm):
        """Test that function returns dict with all expected keys."""
        mock_vm.return_value = MagicMock(
            total=16 * 1024 ** 3,
            available=8 * 1024 ** 3,
            used=8 * 1024 ** 3,
            percent=50.0
        )

        result = get_system_memory_info()

        assert isinstance(result, dict)
        assert 'total' in result
        assert 'available' in result
        assert 'used' in result
        assert 'percent' in result
        assert 'total_human' in result
        assert 'available_human' in result
        assert 'used_human' in result

    @pytest.mark.unit
    @patch('utils.helpers.psutil.virtual_memory')
    def test_correct_values(self, mock_vm):
        """Test that values are correctly extracted from psutil."""
        mock_vm.return_value = MagicMock(
            total=16 * 1024 ** 3,
            available=8 * 1024 ** 3,
            used=8 * 1024 ** 3,
            percent=50.0
        )

        result = get_system_memory_info()

        assert result['total'] == 16 * 1024 ** 3
        assert result['available'] == 8 * 1024 ** 3
        assert result['used'] == 8 * 1024 ** 3
        assert result['percent'] == 50.0

    @pytest.mark.unit
    @patch('utils.helpers.psutil.virtual_memory')
    def test_human_readable_formatting(self, mock_vm):
        """Test that human-readable values are properly formatted."""
        mock_vm.return_value = MagicMock(
            total=16 * 1024 ** 3,
            available=8 * 1024 ** 3,
            used=8 * 1024 ** 3,
            percent=50.0
        )

        result = get_system_memory_info()

        assert "16.0 GB" in result['total_human']
        assert "8.0 GB" in result['available_human']
        assert "8.0 GB" in result['used_human']


# ========== Test get_cpu_info ==========

class TestGetCpuInfo:
    """Test suite for get_cpu_info function."""

    @pytest.mark.unit
    @patch('utils.helpers.psutil.cpu_count')
    @patch('utils.helpers.psutil.cpu_percent')
    def test_returns_dict_with_expected_keys(self, mock_cpu_percent, mock_cpu_count):
        """Test that function returns dict with all expected keys."""
        mock_cpu_percent.return_value = 35.5
        mock_cpu_count.side_effect = [8, 16]  # physical, logical

        result = get_cpu_info()

        assert isinstance(result, dict)
        assert 'percent' in result
        assert 'count' in result
        assert 'count_logical' in result

    @pytest.mark.unit
    @patch('utils.helpers.psutil.cpu_count')
    @patch('utils.helpers.psutil.cpu_percent')
    def test_correct_values(self, mock_cpu_percent, mock_cpu_count):
        """Test that values are correctly extracted."""
        mock_cpu_percent.return_value = 42.5
        mock_cpu_count.side_effect = [8, 16]

        result = get_cpu_info()

        assert result['percent'] == 42.5
        assert result['count'] == 8
        assert result['count_logical'] == 16

    @pytest.mark.unit
    @patch('utils.helpers.psutil.cpu_count')
    @patch('utils.helpers.psutil.cpu_percent')
    def test_cpu_percent_called_with_interval(self, mock_cpu_percent, mock_cpu_count):
        """Test that cpu_percent is called with 0.1 interval."""
        mock_cpu_percent.return_value = 50.0
        mock_cpu_count.side_effect = [4, 8]

        get_cpu_info()

        mock_cpu_percent.assert_called_once_with(interval=0.1)


# ========== Test get_process_list ==========

class TestGetProcessList:
    """Test suite for get_process_list function."""

    @pytest.mark.unit
    @patch('utils.helpers.psutil.virtual_memory')
    @patch('utils.helpers.psutil.cpu_percent')
    @patch('utils.helpers.psutil.process_iter')
    def test_returns_list(self, mock_process_iter, mock_cpu_percent, mock_vm):
        """Test that function returns a list."""
        mock_vm.return_value = MagicMock(total=16 * 1024 ** 3)
        mock_cpu_percent.return_value = 10.0
        mock_process_iter.return_value = []

        result = get_process_list()

        assert isinstance(result, list)

    @pytest.mark.unit
    @patch('utils.helpers.psutil.virtual_memory')
    @patch('utils.helpers.psutil.cpu_percent')
    @patch('utils.helpers.psutil.process_iter')
    def test_process_structure(self, mock_process_iter, mock_cpu_percent, mock_vm):
        """Test that each process has the expected structure."""
        mock_vm.return_value = MagicMock(total=16 * 1024 ** 3)
        mock_cpu_percent.return_value = 10.0

        # Create mock process
        mock_proc = MagicMock()
        mock_proc.info = {
            'pid': 1234,
            'name': 'test_process',
            'username': 'testuser',
            'memory_info': MagicMock(rss=100 * 1024 * 1024),
            'cpu_percent': 25.0
        }
        mock_proc.cpu_percent.return_value = 25.0

        mock_process_iter.return_value = [mock_proc]

        result = get_process_list(include_system=True)

        assert len(result) == 1
        proc = result[0]
        assert 'pid' in proc
        assert 'name' in proc
        assert 'username' in proc
        assert 'memory_mb' in proc
        assert 'memory_percent' in proc
        assert 'memory_human' in proc
        assert 'cpu_percent' in proc

    @pytest.mark.unit
    @patch('utils.helpers.psutil.virtual_memory')
    @patch('utils.helpers.psutil.cpu_percent')
    @patch('utils.helpers.psutil.process_iter')
    def test_filters_system_processes(self, mock_process_iter, mock_cpu_percent, mock_vm):
        """Test that system processes are filtered when include_system=False."""
        mock_vm.return_value = MagicMock(total=16 * 1024 ** 3)
        mock_cpu_percent.return_value = 10.0

        # Create system and user processes
        system_proc = MagicMock()
        system_proc.info = {
            'pid': 1,
            'name': 'system_process',
            'username': 'root',
            'memory_info': MagicMock(rss=100 * 1024 * 1024),
            'cpu_percent': 10.0
        }
        system_proc.cpu_percent.return_value = 10.0

        user_proc = MagicMock()
        user_proc.info = {
            'pid': 1234,
            'name': 'user_process',
            'username': 'testuser',
            'memory_info': MagicMock(rss=100 * 1024 * 1024),
            'cpu_percent': 20.0
        }
        user_proc.cpu_percent.return_value = 20.0

        mock_process_iter.return_value = [system_proc, user_proc]

        # Test with system processes excluded
        result = get_process_list(include_system=False)
        assert len(result) == 1
        assert result[0]['username'] == 'testuser'

        # Test with system processes included
        result = get_process_list(include_system=True)
        assert len(result) == 2

    @pytest.mark.unit
    @patch('utils.helpers.psutil.virtual_memory')
    @patch('utils.helpers.psutil.cpu_percent')
    @patch('utils.helpers.psutil.process_iter')
    def test_handles_process_exceptions(self, mock_process_iter, mock_cpu_percent, mock_vm):
        """Test that exceptions for individual processes are handled gracefully."""
        mock_vm.return_value = MagicMock(total=16 * 1024 ** 3)
        mock_cpu_percent.return_value = 10.0

        # Process that raises exception
        bad_proc = MagicMock()
        bad_proc.info = {'pid': 999}
        bad_proc.cpu_percent.side_effect = psutil.NoSuchProcess(999)

        # Good process
        good_proc = MagicMock()
        good_proc.info = {
            'pid': 1234,
            'name': 'good_process',
            'username': 'testuser',
            'memory_info': MagicMock(rss=100 * 1024 * 1024),
            'cpu_percent': 25.0
        }
        good_proc.cpu_percent.return_value = 25.0

        mock_process_iter.return_value = [bad_proc, good_proc]

        result = get_process_list(include_system=True)

        # Should only return the good process
        assert len(result) == 1
        assert result[0]['pid'] == 1234


# ========== Test get_top_memory_processes ==========

class TestGetTopMemoryProcesses:
    """Test suite for get_top_memory_processes function."""

    @pytest.mark.unit
    @patch('utils.helpers.get_process_list')
    def test_returns_top_n_processes(self, mock_get_process_list):
        """Test that function returns exactly N processes."""
        mock_processes = [
            {'pid': i, 'name': f'proc_{i}', 'memory_mb': 100 - i}
            for i in range(10)
        ]
        mock_get_process_list.return_value = mock_processes

        result = get_top_memory_processes(n=5)

        assert len(result) == 5

    @pytest.mark.unit
    @patch('utils.helpers.get_process_list')
    def test_sorts_by_memory_usage(self, mock_get_process_list):
        """Test that processes are sorted by memory usage (highest first)."""
        mock_processes = [
            {'pid': 1, 'name': 'low_mem', 'memory_mb': 100},
            {'pid': 2, 'name': 'high_mem', 'memory_mb': 1000},
            {'pid': 3, 'name': 'medium_mem', 'memory_mb': 500},
        ]
        mock_get_process_list.return_value = mock_processes

        result = get_top_memory_processes(n=3)

        assert result[0]['memory_mb'] == 1000
        assert result[1]['memory_mb'] == 500
        assert result[2]['memory_mb'] == 100

    @pytest.mark.unit
    @patch('utils.helpers.get_process_list')
    def test_respects_include_system_flag(self, mock_get_process_list):
        """Test that include_system flag is passed correctly."""
        mock_get_process_list.return_value = []

        get_top_memory_processes(n=5, include_system=True)
        mock_get_process_list.assert_called_with(include_system=True)

        get_top_memory_processes(n=5, include_system=False)
        mock_get_process_list.assert_called_with(include_system=False)


# ========== Test get_top_cpu_processes ==========

class TestGetTopCpuProcesses:
    """Test suite for get_top_cpu_processes function."""

    @pytest.mark.unit
    @patch('utils.helpers.get_process_list')
    def test_returns_top_n_processes(self, mock_get_process_list):
        """Test that function returns exactly N processes."""
        mock_processes = [
            {'pid': i, 'name': f'proc_{i}', 'cpu_percent': 10.0 * i}
            for i in range(10)
        ]
        mock_get_process_list.return_value = mock_processes

        result = get_top_cpu_processes(n=5)

        assert len(result) == 5

    @pytest.mark.unit
    @patch('utils.helpers.get_process_list')
    def test_sorts_by_cpu_usage(self, mock_get_process_list):
        """Test that processes are sorted by CPU usage (highest first)."""
        mock_processes = [
            {'pid': 1, 'name': 'low_cpu', 'cpu_percent': 10.0},
            {'pid': 2, 'name': 'high_cpu', 'cpu_percent': 90.0},
            {'pid': 3, 'name': 'medium_cpu', 'cpu_percent': 50.0},
        ]
        mock_get_process_list.return_value = mock_processes

        result = get_top_cpu_processes(n=3)

        assert result[0]['cpu_percent'] == 90.0
        assert result[1]['cpu_percent'] == 50.0
        assert result[2]['cpu_percent'] == 10.0

    @pytest.mark.unit
    @patch('utils.helpers.get_process_list')
    def test_respects_include_system_flag(self, mock_get_process_list):
        """Test that include_system flag is passed correctly."""
        mock_get_process_list.return_value = []

        get_top_cpu_processes(n=5, include_system=True)
        mock_get_process_list.assert_called_with(include_system=True)

        get_top_cpu_processes(n=5, include_system=False)
        mock_get_process_list.assert_called_with(include_system=False)


# ========== Test kill_process ==========

class TestKillProcess:
    """Test suite for kill_process function."""

    @pytest.mark.unit
    @patch('utils.helpers.psutil.Process')
    def test_successful_terminate(self, mock_process_class):
        """Test successful process termination."""
        mock_proc = MagicMock()
        mock_process_class.return_value = mock_proc

        result = kill_process(1234, force=False)

        assert result is True
        mock_proc.terminate.assert_called_once()
        mock_proc.kill.assert_not_called()

    @pytest.mark.unit
    @patch('utils.helpers.psutil.Process')
    def test_successful_kill(self, mock_process_class):
        """Test successful force kill."""
        mock_proc = MagicMock()
        mock_process_class.return_value = mock_proc

        result = kill_process(1234, force=True)

        assert result is True
        mock_proc.kill.assert_called_once()
        mock_proc.terminate.assert_not_called()

    @pytest.mark.unit
    @patch('utils.helpers.psutil.Process')
    def test_handles_no_such_process(self, mock_process_class):
        """Test handling of non-existent process."""
        mock_process_class.side_effect = psutil.NoSuchProcess(9999)

        result = kill_process(9999)

        assert result is False

    @pytest.mark.unit
    @patch('utils.helpers.psutil.Process')
    def test_handles_access_denied(self, mock_process_class):
        """Test handling of permission denied."""
        mock_proc = MagicMock()
        mock_proc.terminate.side_effect = psutil.AccessDenied()
        mock_process_class.return_value = mock_proc

        result = kill_process(1234)

        assert result is False


# ========== Test get_resource_usage_color ==========

class TestGetResourceUsageColor:
    """Test suite for get_resource_usage_color function."""

    @pytest.mark.unit
    def test_low_usage(self):
        """Test color for low usage (< 50%)."""
        assert get_resource_usage_color(0.0) == 'low'
        assert get_resource_usage_color(25.0) == 'low'
        assert get_resource_usage_color(49.9) == 'low'

    @pytest.mark.unit
    def test_medium_usage(self):
        """Test color for medium usage (50% - 79.9%)."""
        assert get_resource_usage_color(50.0) == 'medium'
        assert get_resource_usage_color(65.0) == 'medium'
        assert get_resource_usage_color(79.9) == 'medium'

    @pytest.mark.unit
    def test_high_usage(self):
        """Test color for high usage (>= 80%)."""
        assert get_resource_usage_color(80.0) == 'high'
        assert get_resource_usage_color(90.0) == 'high'
        assert get_resource_usage_color(100.0) == 'high'

    @pytest.mark.unit
    def test_boundary_values(self):
        """Test exact boundary values."""
        assert get_resource_usage_color(49.99) == 'low'
        assert get_resource_usage_color(50.0) == 'medium'
        assert get_resource_usage_color(79.99) == 'medium'
        assert get_resource_usage_color(80.0) == 'high'


# ========== Test format_percentage ==========

class TestFormatPercentage:
    """Test suite for format_percentage function."""

    @pytest.mark.unit
    def test_default_decimals(self):
        """Test formatting with default 1 decimal place."""
        assert format_percentage(50.0) == "50.0%"
        assert format_percentage(75.5) == "75.5%"
        assert format_percentage(99.9) == "99.9%"

    @pytest.mark.unit
    def test_custom_decimals(self):
        """Test formatting with custom decimal places."""
        assert format_percentage(50.0, decimals=0) == "50%"
        assert format_percentage(75.123, decimals=2) == "75.12%"
        assert format_percentage(99.9999, decimals=3) == "100.000%"

    @pytest.mark.unit
    def test_zero_value(self):
        """Test formatting zero percentage."""
        assert format_percentage(0.0) == "0.0%"
        assert format_percentage(0.0, decimals=2) == "0.00%"

    @pytest.mark.unit
    def test_hundred_percent(self):
        """Test formatting 100%."""
        assert format_percentage(100.0) == "100.0%"
        assert format_percentage(100.0, decimals=2) == "100.00%"

    @pytest.mark.unit
    def test_rounding(self):
        """Test that values are properly rounded."""
        assert format_percentage(66.666, decimals=1) == "66.7%"
        assert format_percentage(66.666, decimals=2) == "66.67%"
