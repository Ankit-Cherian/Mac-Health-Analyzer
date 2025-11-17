"""
Pytest Configuration and Shared Fixtures

This module contains pytest configuration, fixtures, and test utilities
that are shared across all test modules.
"""

import importlib.util
import json
import os
import sys
from pathlib import Path
from typing import Dict, List
from unittest.mock import MagicMock, Mock

import psutil
import pytest

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))


# ========== Application Fixtures ==========


def _plugin_available(module_name: str) -> bool:
    """Check whether an optional pytest plugin is importable."""

    return importlib.util.find_spec(module_name) is not None


def pytest_addoption(parser):
    """Register placeholder options when optional plugins are missing."""

    if not _plugin_available("pytest_cov"):
        parser.addoption("--cov", action="store", default=None, help="(placeholder)")
        parser.addoption(
            "--cov-report", action="append", default=[], help="(placeholder)"
        )
        parser.addoption(
            "--cov-fail-under", action="store", default=None, help="(placeholder)"
        )

    if not _plugin_available("pytest_html"):
        parser.addoption("--html", action="store", default=None, help="(placeholder)")
        parser.addoption(
            "--self-contained-html",
            action="store_true",
            default=False,
            help="(placeholder)",
        )

@pytest.fixture(scope="session")
def qapp():
    """Create a QApplication instance for Qt tests."""
    QtWidgets = pytest.importorskip(
        "PyQt6.QtWidgets", reason="PyQt6 not installed or missing GUI dependencies"
    )
    QApplication = QtWidgets.QApplication
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    yield app
    # Don't quit - let Qt handle cleanup


@pytest.fixture
def qapp_args():
    """Provide QApplication arguments."""
    return []


# ========== Mock Process Data ==========

@pytest.fixture
def mock_process_data():
    """Mock process data matching psutil.Process structure."""
    return {
        "pid": 1234,
        "name": "test_process",
        "username": "testuser",
        "cpu_percent": 25.5,
        "memory_percent": 10.2,
        "memory_info": MagicMock(rss=1024 * 1024 * 100),  # 100 MB
        "status": "running",
        "create_time": 1234567890.0,
        "num_threads": 4,
    }


@pytest.fixture
def mock_process_list():
    """Mock list of processes."""
    processes = []
    test_processes = [
        {"pid": 1, "name": "kernel_task", "cpu": 5.0, "memory": 2.5, "rss": 1024**3},
        {"pid": 100, "name": "systemd", "cpu": 1.0, "memory": 0.5, "rss": 1024**2 * 50},
        {"pid": 200, "name": "Google Chrome", "cpu": 45.0, "memory": 15.0, "rss": 1024**3 * 2},
        {"pid": 300, "name": "python3", "cpu": 10.0, "memory": 5.0, "rss": 1024**2 * 500},
        {"pid": 400, "name": "Slack", "cpu": 5.5, "memory": 8.0, "rss": 1024**3},
    ]

    for proc_data in test_processes:
        mock_proc = MagicMock()
        mock_proc.pid = proc_data["pid"]
        mock_proc.name.return_value = proc_data["name"]
        mock_proc.cpu_percent.return_value = proc_data["cpu"]
        mock_proc.memory_percent.return_value = proc_data["memory"]
        mock_proc.memory_info.return_value = MagicMock(rss=proc_data["rss"])
        mock_proc.username.return_value = "testuser"
        mock_proc.status.return_value = "running"
        mock_proc.create_time.return_value = 1234567890.0
        mock_proc.num_threads.return_value = 4
        processes.append(mock_proc)

    return processes


# ========== Mock System Info Data ==========

@pytest.fixture
def mock_memory_info():
    """Mock system memory information."""
    return {
        "total": 16 * 1024**3,  # 16 GB
        "available": 8 * 1024**3,  # 8 GB
        "percent": 50.0,
        "used": 8 * 1024**3,
        "free": 8 * 1024**3,
    }


@pytest.fixture
def mock_cpu_info():
    """Mock CPU information."""
    return {
        "percent": 35.5,
        "count": 8,
        "count_logical": 16,
        "freq_current": 2400.0,
        "freq_min": 800.0,
        "freq_max": 3600.0,
    }


# ========== Mock Startup Items Data ==========

@pytest.fixture
def mock_login_items():
    """Mock login items data."""
    return [
        {
            "name": "Dropbox",
            "path": "/Applications/Dropbox.app",
            "hidden": False,
            "type": "Login Item",
        },
        {
            "name": "Slack",
            "path": "/Applications/Slack.app",
            "hidden": False,
            "type": "Login Item",
        },
    ]


@pytest.fixture
def mock_launch_agents():
    """Mock launch agents data."""
    return [
        {
            "label": "com.apple.notificationcenterui",
            "path": "/System/Library/LaunchAgents/com.apple.notificationcenterui.plist",
            "type": "Launch Agent",
            "enabled": True,
            "status": "loaded",
        },
        {
            "label": "com.google.keystone.agent",
            "path": "/Library/LaunchAgents/com.google.keystone.agent.plist",
            "type": "Launch Agent",
            "enabled": True,
            "status": "loaded",
        },
    ]


@pytest.fixture
def mock_launch_daemons():
    """Mock launch daemons data."""
    return [
        {
            "label": "com.apple.mDNSResponder",
            "path": "/System/Library/LaunchDaemons/com.apple.mDNSResponder.plist",
            "type": "Launch Daemon",
            "enabled": True,
            "status": "loaded",
        },
    ]


@pytest.fixture
def mock_launchctl_output():
    """Mock launchctl list output."""
    return """PID	Status	Label
123	0	com.apple.notificationcenterui
-	0	com.google.keystone.agent
456	0	com.apple.mDNSResponder
"""


# ========== Mock Plist Data ==========

@pytest.fixture
def mock_plist_data():
    """Mock plist file data."""
    return {
        "Label": "com.example.test",
        "ProgramArguments": ["/usr/bin/test", "--arg"],
        "RunAtLoad": True,
        "KeepAlive": False,
        "StandardErrorPath": "/tmp/test.err",
        "StandardOutPath": "/tmp/test.out",
    }


# ========== File System Fixtures ==========

@pytest.fixture
def temp_config_dir(tmp_path):
    """Create a temporary config directory."""
    config_dir = tmp_path / ".mac-health-analyzer"
    config_dir.mkdir(exist_ok=True)
    return config_dir


@pytest.fixture
def temp_config_file(temp_config_dir):
    """Create a temporary config file."""
    config_file = temp_config_dir / "config.json"
    config_data = {"show_startup_guide": False}
    config_file.write_text(json.dumps(config_data))
    return config_file


@pytest.fixture
def mock_plist_files(tmp_path):
    """Create mock plist files in a temporary directory."""
    launch_agents_dir = tmp_path / "LaunchAgents"
    launch_agents_dir.mkdir()

    launch_daemons_dir = tmp_path / "LaunchDaemons"
    launch_daemons_dir.mkdir()

    # Create sample plist files
    agent_plist = launch_agents_dir / "com.example.agent.plist"
    daemon_plist = launch_daemons_dir / "com.example.daemon.plist"

    # Note: In real tests, we'd create actual plist XML, but for now mock
    agent_plist.touch()
    daemon_plist.touch()

    return {
        "agents_dir": launch_agents_dir,
        "daemons_dir": launch_daemons_dir,
        "agent_plist": agent_plist,
        "daemon_plist": daemon_plist,
    }


# ========== Mock Subprocess Results ==========

@pytest.fixture
def mock_subprocess_success():
    """Mock successful subprocess result."""
    mock_result = MagicMock()
    mock_result.returncode = 0
    mock_result.stdout = "Success output"
    mock_result.stderr = ""
    return mock_result


@pytest.fixture
def mock_subprocess_failure():
    """Mock failed subprocess result."""
    mock_result = MagicMock()
    mock_result.returncode = 1
    mock_result.stdout = ""
    mock_result.stderr = "Error occurred"
    return mock_result


# ========== Chart Data Fixtures ==========

@pytest.fixture
def mock_chart_data():
    """Mock data for chart testing."""
    return {
        "cpu_history": [10.0, 15.0, 20.0, 25.0, 30.0, 25.0, 20.0, 15.0, 10.0, 5.0],
        "memory_history": [40.0, 42.0, 45.0, 48.0, 50.0, 52.0, 55.0, 53.0, 50.0, 48.0],
        "timestamps": list(range(10)),
    }


@pytest.fixture
def mock_top_processes():
    """Mock top processes data for bar charts."""
    return [
        {"name": "Chrome", "value": 45.0},
        {"name": "Python", "value": 30.0},
        {"name": "Slack", "value": 25.0},
        {"name": "VSCode", "value": 20.0},
        {"name": "Terminal", "value": 15.0},
    ]


# ========== Utility Functions ==========

@pytest.fixture
def assert_called_with_timeout():
    """Helper to assert mock was called within timeout."""
    def _assert(mock_obj, timeout=1.0):
        import time
        start = time.time()
        while time.time() - start < timeout:
            if mock_obj.called:
                return True
            time.sleep(0.01)
        return False
    return _assert


# ========== Pytest Hooks ==========

def pytest_configure(config):
    """Configure pytest with custom settings."""
    # Set QT_QPA_PLATFORM for headless testing
    os.environ["QT_QPA_PLATFORM"] = "offscreen"

    # Add custom markers
    config.addinivalue_line(
        "markers", "unit: Unit tests for individual functions"
    )
    config.addinivalue_line(
        "markers", "integration: Integration tests for component interactions"
    )
    config.addinivalue_line(
        "markers", "ui: UI component tests"
    )


def pytest_collection_modifyitems(config, items):
    """Modify test collection to add markers automatically."""
    for item in items:
        # Auto-mark tests based on path
        if "unit" in str(item.fspath):
            item.add_marker(pytest.mark.unit)
        elif "integration" in str(item.fspath):
            item.add_marker(pytest.mark.integration)
        elif "ui" in str(item.fspath):
            item.add_marker(pytest.mark.ui)


# ========== Mock Manager Instances ==========

@pytest.fixture
def mock_process_monitor():
    """Mock ProcessMonitor instance."""
    from unittest.mock import Mock
    monitor = Mock()
    monitor.processes = []
    monitor.refresh = Mock()
    monitor.get_processes = Mock(return_value=[])
    monitor.get_top_cpu_processes = Mock(return_value=[])
    monitor.get_top_memory_processes = Mock(return_value=[])
    monitor.kill_process = Mock(return_value=True)
    return monitor


@pytest.fixture
def mock_startup_manager():
    """Mock StartupManager instance."""
    from unittest.mock import Mock
    manager = Mock()
    manager.all_items = []
    manager.refresh = Mock()
    manager.get_all_items = Mock(return_value=[])
    manager.disable_item = Mock(return_value=True)
    manager.enable_item = Mock(return_value=True)
    manager.search_items = Mock(return_value=[])
    return manager
