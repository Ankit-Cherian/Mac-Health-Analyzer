"""
Unit Tests for process_monitor.py

Tests ProcessMonitor class with comprehensive coverage.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock

from process_monitor import ProcessMonitor


class TestProcessMonitorInit:
    """Test ProcessMonitor initialization."""

    @pytest.mark.unit
    def test_initialization(self):
        """Test that ProcessMonitor initializes with correct defaults."""
        monitor = ProcessMonitor()

        assert monitor.processes == []
        assert monitor.memory_info == {}
        assert monitor.cpu_info == {}
        assert monitor.include_system_processes is False


class TestSetIncludeSystemProcesses:
    """Test set_include_system_processes method."""

    @pytest.mark.unit
    def test_set_to_true(self):
        """Test setting include_system_processes to True."""
        monitor = ProcessMonitor()
        monitor.set_include_system_processes(True)

        assert monitor.include_system_processes is True

    @pytest.mark.unit
    def test_set_to_false(self):
        """Test setting include_system_processes to False."""
        monitor = ProcessMonitor()
        monitor.set_include_system_processes(True)
        monitor.set_include_system_processes(False)

        assert monitor.include_system_processes is False


class TestGetProcesses:
    """Test get_processes method."""

    @pytest.mark.unit
    def test_returns_processes_list(self, mock_process_list):
        """Test that get_processes returns the processes list."""
        monitor = ProcessMonitor()
        monitor.processes = mock_process_list

        result = monitor.get_processes()

        assert result == mock_process_list


class TestGetProcessCount:
    """Test get_process_count method."""

    @pytest.mark.unit
    def test_returns_correct_count(self, mock_process_list):
        """Test that get_process_count returns correct count."""
        monitor = ProcessMonitor()
        monitor.processes = mock_process_list

        result = monitor.get_process_count()

        assert result == len(mock_process_list)

    @pytest.mark.unit
    def test_empty_list(self):
        """Test count with empty process list."""
        monitor = ProcessMonitor()
        monitor.processes = []

        assert monitor.get_process_count() == 0


class TestGetMemoryInfo:
    """Test get_memory_info method."""

    @pytest.mark.unit
    def test_returns_memory_info(self, mock_memory_info):
        """Test that get_memory_info returns memory information."""
        monitor = ProcessMonitor()
        monitor.memory_info = mock_memory_info

        result = monitor.get_memory_info()

        assert result == mock_memory_info


class TestGetCpuInfo:
    """Test get_cpu_info method."""

    @pytest.mark.unit
    def test_returns_cpu_info(self, mock_cpu_info):
        """Test that get_cpu_info returns CPU information."""
        monitor = ProcessMonitor()
        monitor.cpu_info = mock_cpu_info

        result = monitor.get_cpu_info()

        assert result == mock_cpu_info


class TestGetTopMemoryProcesses:
    """Test get_top_memory_processes method."""

    @pytest.mark.unit
    def test_returns_top_n(self):
        """Test that returns exactly N processes."""
        monitor = ProcessMonitor()
        monitor.processes = [
            {'pid': i, 'name': f'proc_{i}', 'memory_mb': 100 - i, 'cpu_percent': 10.0}
            for i in range(10)
        ]

        result = monitor.get_top_memory_processes(n=5)

        assert len(result) == 5

    @pytest.mark.unit
    def test_sorted_by_memory(self):
        """Test that processes are sorted by memory usage."""
        monitor = ProcessMonitor()
        monitor.processes = [
            {'pid': 1, 'name': 'low', 'memory_mb': 100, 'cpu_percent': 10.0},
            {'pid': 2, 'name': 'high', 'memory_mb': 1000, 'cpu_percent': 20.0},
            {'pid': 3, 'name': 'medium', 'memory_mb': 500, 'cpu_percent': 15.0},
        ]

        result = monitor.get_top_memory_processes(n=3)

        assert result[0]['memory_mb'] == 1000
        assert result[1]['memory_mb'] == 500
        assert result[2]['memory_mb'] == 100

    @pytest.mark.unit
    def test_handles_fewer_than_n(self):
        """Test when there are fewer processes than requested."""
        monitor = ProcessMonitor()
        monitor.processes = [
            {'pid': 1, 'name': 'proc1', 'memory_mb': 100, 'cpu_percent': 10.0},
        ]

        result = monitor.get_top_memory_processes(n=10)

        assert len(result) == 1


class TestGetTopCpuProcesses:
    """Test get_top_cpu_processes method."""

    @pytest.mark.unit
    def test_returns_top_n(self):
        """Test that returns exactly N processes."""
        monitor = ProcessMonitor()
        monitor.processes = [
            {'pid': i, 'name': f'proc_{i}', 'cpu_percent': 10.0 * i, 'memory_mb': 100}
            for i in range(10)
        ]

        result = monitor.get_top_cpu_processes(n=5)

        assert len(result) == 5

    @pytest.mark.unit
    def test_sorted_by_cpu(self):
        """Test that processes are sorted by CPU usage."""
        monitor = ProcessMonitor()
        monitor.processes = [
            {'pid': 1, 'name': 'low', 'cpu_percent': 10.0, 'memory_mb': 100},
            {'pid': 2, 'name': 'high', 'cpu_percent': 90.0, 'memory_mb': 200},
            {'pid': 3, 'name': 'medium', 'cpu_percent': 50.0, 'memory_mb': 150},
        ]

        result = monitor.get_top_cpu_processes(n=3)

        assert result[0]['cpu_percent'] == 90.0
        assert result[1]['cpu_percent'] == 50.0
        assert result[2]['cpu_percent'] == 10.0


class TestSearchProcesses:
    """Test search_processes method."""

    @pytest.mark.unit
    def test_case_insensitive_search(self):
        """Test that search is case-insensitive."""
        monitor = ProcessMonitor()
        monitor.processes = [
            {'pid': 1, 'name': 'Google Chrome', 'memory_mb': 100, 'cpu_percent': 10.0},
            {'pid': 2, 'name': 'Firefox', 'memory_mb': 200, 'cpu_percent': 20.0},
        ]

        result = monitor.search_processes('chrome')

        assert len(result) == 1
        assert result[0]['name'] == 'Google Chrome'

    @pytest.mark.unit
    def test_partial_match(self):
        """Test that partial matches work."""
        monitor = ProcessMonitor()
        monitor.processes = [
            {'pid': 1, 'name': 'python3', 'memory_mb': 100, 'cpu_percent': 10.0},
            {'pid': 2, 'name': 'python2', 'memory_mb': 200, 'cpu_percent': 20.0},
            {'pid': 3, 'name': 'java', 'memory_mb': 300, 'cpu_percent': 30.0},
        ]

        result = monitor.search_processes('python')

        assert len(result) == 2

    @pytest.mark.unit
    def test_no_matches(self):
        """Test when search returns no matches."""
        monitor = ProcessMonitor()
        monitor.processes = [
            {'pid': 1, 'name': 'chrome', 'memory_mb': 100, 'cpu_percent': 10.0},
        ]

        result = monitor.search_processes('firefox')

        assert result == []


class TestGetProcessByPid:
    """Test get_process_by_pid method."""

    @pytest.mark.unit
    def test_finds_existing_process(self):
        """Test finding an existing process."""
        monitor = ProcessMonitor()
        monitor.processes = [
            {'pid': 100, 'name': 'proc1', 'memory_mb': 100, 'cpu_percent': 10.0},
            {'pid': 200, 'name': 'proc2', 'memory_mb': 200, 'cpu_percent': 20.0},
        ]

        result = monitor.get_process_by_pid(200)

        assert result is not None
        assert result['pid'] == 200
        assert result['name'] == 'proc2'

    @pytest.mark.unit
    def test_returns_none_for_nonexistent(self):
        """Test returns None for non-existent PID."""
        monitor = ProcessMonitor()
        monitor.processes = [
            {'pid': 100, 'name': 'proc1', 'memory_mb': 100, 'cpu_percent': 10.0},
        ]

        result = monitor.get_process_by_pid(999)

        assert result is None


class TestKillProcess:
    """Test kill_process method."""

    @pytest.mark.unit
    @patch('process_monitor.kill_process')
    def test_calls_kill_process_function(self, mock_kill):
        """Test that method calls the kill_process function."""
        mock_kill.return_value = True
        monitor = ProcessMonitor()

        result = monitor.kill_process(1234, force=False)

        assert result is True
        mock_kill.assert_called_once_with(1234, False)

    @pytest.mark.unit
    @patch('process_monitor.kill_process')
    def test_force_kill(self, mock_kill):
        """Test force kill."""
        mock_kill.return_value = True
        monitor = ProcessMonitor()

        monitor.kill_process(1234, force=True)

        mock_kill.assert_called_once_with(1234, True)


class TestGetMemoryUsagePercentage:
    """Test get_memory_usage_percentage method."""

    @pytest.mark.unit
    def test_returns_correct_percentage(self):
        """Test returns correct memory percentage."""
        monitor = ProcessMonitor()
        monitor.memory_info = {'percent': 75.5}

        result = monitor.get_memory_usage_percentage()

        assert result == 75.5

    @pytest.mark.unit
    def test_returns_zero_when_missing(self):
        """Test returns 0.0 when percent is missing."""
        monitor = ProcessMonitor()
        monitor.memory_info = {}

        result = monitor.get_memory_usage_percentage()

        assert result == 0.0


class TestGetCpuUsagePercentage:
    """Test get_cpu_usage_percentage method."""

    @pytest.mark.unit
    def test_returns_correct_percentage(self):
        """Test returns correct CPU percentage."""
        monitor = ProcessMonitor()
        monitor.cpu_info = {'percent': 42.5}

        result = monitor.get_cpu_usage_percentage()

        assert result == 42.5

    @pytest.mark.unit
    def test_returns_zero_when_missing(self):
        """Test returns 0.0 when percent is missing."""
        monitor = ProcessMonitor()
        monitor.cpu_info = {}

        result = monitor.get_cpu_usage_percentage()

        assert result == 0.0


class TestGetSystemSummary:
    """Test get_system_summary method."""

    @pytest.mark.unit
    def test_returns_complete_summary(self):
        """Test that summary contains all expected keys."""
        monitor = ProcessMonitor()
        monitor.processes = [{'pid': 1}, {'pid': 2}]
        monitor.memory_info = {
            'percent': 50.0,
            'used_human': '8.0 GB',
            'total_human': '16.0 GB'
        }
        monitor.cpu_info = {
            'percent': 35.0,
            'count': 8,
            'count_logical': 16
        }

        result = monitor.get_system_summary()

        assert result['process_count'] == 2
        assert result['memory_percent'] == 50.0
        assert result['memory_used_human'] == '8.0 GB'
        assert result['memory_total_human'] == '16.0 GB'
        assert result['cpu_percent'] == 35.0
        assert result['cpu_count'] == 8
        assert result['cpu_count_logical'] == 16


class TestSortProcesses:
    """Test sort_processes method."""

    @pytest.mark.unit
    def test_sort_by_memory(self):
        """Test sorting by memory."""
        monitor = ProcessMonitor()
        monitor.processes = [
            {'pid': 1, 'name': 'proc1', 'memory_mb': 100, 'cpu_percent': 10.0},
            {'pid': 2, 'name': 'proc2', 'memory_mb': 500, 'cpu_percent': 20.0},
            {'pid': 3, 'name': 'proc3', 'memory_mb': 200, 'cpu_percent': 15.0},
        ]

        result = monitor.sort_processes('memory_mb', reverse=True)

        assert result[0]['memory_mb'] == 500
        assert result[1]['memory_mb'] == 200
        assert result[2]['memory_mb'] == 100

    @pytest.mark.unit
    def test_sort_by_name(self):
        """Test sorting by name."""
        monitor = ProcessMonitor()
        monitor.processes = [
            {'pid': 1, 'name': 'chrome', 'memory_mb': 100, 'cpu_percent': 10.0},
            {'pid': 2, 'name': 'firefox', 'memory_mb': 200, 'cpu_percent': 20.0},
            {'pid': 3, 'name': 'safari', 'memory_mb': 150, 'cpu_percent': 15.0},
        ]

        result = monitor.sort_processes('name', reverse=False)

        assert result[0]['name'] == 'chrome'
        assert result[1]['name'] == 'firefox'
        assert result[2]['name'] == 'safari'

    @pytest.mark.unit
    def test_invalid_key_defaults_to_memory(self):
        """Test that invalid key defaults to memory_mb."""
        monitor = ProcessMonitor()
        monitor.processes = [
            {'pid': 1, 'name': 'proc1', 'memory_mb': 100, 'cpu_percent': 10.0},
            {'pid': 2, 'name': 'proc2', 'memory_mb': 500, 'cpu_percent': 20.0},
        ]

        result = monitor.sort_processes('invalid_key')

        assert result[0]['memory_mb'] == 500


class TestFilterByMemoryThreshold:
    """Test filter_by_memory_threshold method."""

    @pytest.mark.unit
    def test_filters_correctly(self):
        """Test filtering by memory threshold."""
        monitor = ProcessMonitor()
        monitor.processes = [
            {'pid': 1, 'name': 'proc1', 'memory_mb': 50, 'cpu_percent': 10.0},
            {'pid': 2, 'name': 'proc2', 'memory_mb': 150, 'cpu_percent': 20.0},
            {'pid': 3, 'name': 'proc3', 'memory_mb': 300, 'cpu_percent': 30.0},
        ]

        result = monitor.filter_by_memory_threshold(100)

        assert len(result) == 2
        assert all(p['memory_mb'] >= 100 for p in result)

    @pytest.mark.unit
    def test_no_matches(self):
        """Test when no processes meet threshold."""
        monitor = ProcessMonitor()
        monitor.processes = [
            {'pid': 1, 'name': 'proc1', 'memory_mb': 50, 'cpu_percent': 10.0},
        ]

        result = monitor.filter_by_memory_threshold(100)

        assert result == []


class TestFilterByCpuThreshold:
    """Test filter_by_cpu_threshold method."""

    @pytest.mark.unit
    def test_filters_correctly(self):
        """Test filtering by CPU threshold."""
        monitor = ProcessMonitor()
        monitor.processes = [
            {'pid': 1, 'name': 'proc1', 'memory_mb': 100, 'cpu_percent': 5.0},
            {'pid': 2, 'name': 'proc2', 'memory_mb': 200, 'cpu_percent': 25.0},
            {'pid': 3, 'name': 'proc3', 'memory_mb': 300, 'cpu_percent': 50.0},
        ]

        result = monitor.filter_by_cpu_threshold(20.0)

        assert len(result) == 2
        assert all(p['cpu_percent'] >= 20.0 for p in result)


class TestGetProcessDetails:
    """Test get_process_details method."""

    @pytest.mark.unit
    @patch('process_monitor.psutil.Process')
    def test_returns_detailed_info(self, mock_process_class):
        """Test returns detailed process information."""
        mock_proc = MagicMock()
        mock_proc.pid = 1234
        mock_proc.name.return_value = 'test_process'
        mock_proc.username.return_value = 'testuser'
        mock_proc.status.return_value = 'running'
        mock_proc.create_time.return_value = 1234567890.0
        mock_proc.cpu_percent.return_value = 25.5
        mock_proc.memory_info.return_value = MagicMock()
        mock_proc.num_threads.return_value = 4
        mock_proc.cmdline.return_value = ['/usr/bin/test', '--arg']

        mock_process_class.return_value = mock_proc

        monitor = ProcessMonitor()
        result = monitor.get_process_details(1234)

        assert result is not None
        assert result['pid'] == 1234
        assert result['name'] == 'test_process'
        assert result['username'] == 'testuser'
        assert result['status'] == 'running'
        assert result['num_threads'] == 4
        assert result['cmdline'] == '/usr/bin/test --arg'

    @pytest.mark.unit
    @patch('process_monitor.psutil.Process')
    def test_handles_no_such_process(self, mock_process_class):
        """Test handling of non-existent process."""
        import psutil
        mock_process_class.side_effect = psutil.NoSuchProcess(9999)

        monitor = ProcessMonitor()
        result = monitor.get_process_details(9999)

        assert result is None

    @pytest.mark.unit
    @patch('process_monitor.psutil.Process')
    def test_handles_access_denied(self, mock_process_class):
        """Test handling of access denied."""
        import psutil
        mock_process_class.side_effect = psutil.AccessDenied()

        monitor = ProcessMonitor()
        result = monitor.get_process_details(1)

        assert result is None
