"""
Unit Tests for utils/system_info.py

Tests all system information functions with comprehensive coverage.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock, mock_open
import plistlib
import subprocess

from utils.system_info import (
    get_login_items,
    fetch_launchctl_status,
    get_launch_agents,
    get_launch_daemons,
    parse_plist_file,
    is_launchd_item_enabled,
    get_launchctl_list,
    disable_login_item,
    disable_launch_agent,
    enable_launch_agent,
)


# ========== Test get_login_items ==========

class TestGetLoginItems:
    """Test suite for get_login_items function."""

    @pytest.mark.unit
    @pytest.mark.macos
    @patch('utils.system_info.subprocess.run')
    def test_successful_retrieval(self, mock_run):
        """Test successful retrieval of login items."""
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout="Dropbox, Slack, Google Chrome",
            stderr=""
        )

        result = get_login_items()

        assert len(result) == 3
        assert result[0]['name'] == 'Dropbox'
        assert result[1]['name'] == 'Slack'
        assert result[2]['name'] == 'Google Chrome'
        assert all(item['type'] == 'Login Item' for item in result)
        assert all(item['enabled'] is True for item in result)

    @pytest.mark.unit
    @patch('utils.system_info.subprocess.run')
    def test_empty_result(self, mock_run):
        """Test handling of empty login items list."""
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout="",
            stderr=""
        )

        result = get_login_items()

        assert result == []

    @pytest.mark.unit
    @patch('utils.system_info.subprocess.run')
    def test_subprocess_error(self, mock_run):
        """Test handling of subprocess errors."""
        mock_run.return_value = MagicMock(
            returncode=1,
            stdout="",
            stderr="Error occurred"
        )

        result = get_login_items()

        assert result == []

    @pytest.mark.unit
    @patch('utils.system_info.subprocess.run')
    def test_timeout_handling(self, mock_run):
        """Test handling of subprocess timeout."""
        mock_run.side_effect = subprocess.TimeoutExpired(['osascript'], timeout=5)

        result = get_login_items()

        assert result == []

    @pytest.mark.unit
    @patch('utils.system_info.subprocess.run')
    def test_single_item(self, mock_run):
        """Test retrieval of single login item."""
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout="iTerm",
            stderr=""
        )

        result = get_login_items()

        assert len(result) == 1
        assert result[0]['name'] == 'iTerm'

    @pytest.mark.unit
    @patch('utils.system_info.subprocess.run')
    def test_osascript_called_correctly(self, mock_run):
        """Test that osascript is called with correct arguments."""
        mock_run.return_value = MagicMock(returncode=0, stdout="")

        get_login_items()

        mock_run.assert_called_once()
        args = mock_run.call_args[0][0]
        assert args[0] == 'osascript'
        assert args[1] == '-e'
        assert 'tell application "System Events"' in args[2]


# ========== Test fetch_launchctl_status ==========

class TestFetchLaunchctlStatus:
    """Test suite for fetch_launchctl_status function."""

    @pytest.mark.unit
    @patch('utils.system_info.subprocess.run')
    def test_successful_fetch(self, mock_run, mock_launchctl_output):
        """Test successful fetching of launchctl status."""
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout=mock_launchctl_output,
            stderr=""
        )

        result = fetch_launchctl_status()

        assert isinstance(result, set)
        assert 'com.apple.notificationcenterui' in result
        assert 'com.google.keystone.agent' in result
        assert 'com.apple.mDNSResponder' in result

    @pytest.mark.unit
    @patch('utils.system_info.subprocess.run')
    def test_empty_output(self, mock_run):
        """Test handling of empty launchctl output."""
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout="PID\tStatus\tLabel\n",
            stderr=""
        )

        result = fetch_launchctl_status()

        assert result == set()

    @pytest.mark.unit
    @patch('utils.system_info.subprocess.run')
    def test_command_failure(self, mock_run):
        """Test handling of failed launchctl command."""
        mock_run.return_value = MagicMock(
            returncode=1,
            stdout="",
            stderr="Error"
        )

        result = fetch_launchctl_status()

        assert result == set()

    @pytest.mark.unit
    @patch('utils.system_info.subprocess.run')
    def test_timeout(self, mock_run):
        """Test handling of timeout."""
        mock_run.side_effect = subprocess.TimeoutExpired(['launchctl'], timeout=5)

        result = fetch_launchctl_status()

        assert result == set()

    @pytest.mark.unit
    @patch('utils.system_info.subprocess.run')
    def test_malformed_lines(self, mock_run):
        """Test handling of malformed output lines."""
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout="PID\tStatus\tLabel\n123\t0\tcom.valid.service\nmalformed\n456\t0\tcom.another.service\n",
            stderr=""
        )

        result = fetch_launchctl_status()

        assert 'com.valid.service' in result
        assert 'com.another.service' in result
        # Should skip malformed line gracefully


# ========== Test get_launch_agents ==========

class TestGetLaunchAgents:
    """Test suite for get_launch_agents function."""

    @pytest.mark.unit
    @patch('utils.system_info.parse_plist_file')
    @patch('utils.system_info.os.listdir')
    @patch('utils.system_info.os.path.exists')
    @patch('utils.system_info.fetch_launchctl_status')
    def test_user_only_agents(self, mock_fetch, mock_exists, mock_listdir, mock_parse):
        """Test retrieval of user-only launch agents."""
        mock_fetch.return_value = {'com.test.agent'}
        mock_exists.return_value = True
        mock_listdir.return_value = ['com.test.agent.plist']
        mock_parse.return_value = {
            'name': 'TestAgent',
            'label': 'com.test.agent',
            'path': '/test/path.plist'
        }

        result = get_launch_agents(user_only=True)

        assert len(result) > 0
        assert result[0]['type'] == 'Launch Agent'
        assert result[0]['enabled'] is True

    @pytest.mark.unit
    @patch('utils.system_info.parse_plist_file')
    @patch('utils.system_info.os.listdir')
    @patch('utils.system_info.os.path.exists')
    @patch('utils.system_info.fetch_launchctl_status')
    def test_all_directories(self, mock_fetch, mock_exists, mock_listdir, mock_parse):
        """Test that all standard directories are checked."""
        mock_fetch.return_value = set()
        mock_exists.return_value = True
        mock_listdir.return_value = []
        mock_parse.return_value = None

        get_launch_agents(user_only=False)

        # Should check user, /Library, and /System/Library
        assert mock_exists.call_count >= 3

    @pytest.mark.unit
    @patch('utils.system_info.os.path.exists')
    @patch('utils.system_info.fetch_launchctl_status')
    def test_nonexistent_directory(self, mock_fetch, mock_exists):
        """Test handling of nonexistent directories."""
        mock_fetch.return_value = set()
        mock_exists.return_value = False

        result = get_launch_agents()

        assert result == []

    @pytest.mark.unit
    @patch('utils.system_info.parse_plist_file')
    @patch('utils.system_info.os.listdir')
    @patch('utils.system_info.os.path.exists')
    @patch('utils.system_info.fetch_launchctl_status')
    def test_enabled_status(self, mock_fetch, mock_exists, mock_listdir, mock_parse):
        """Test that enabled status is correctly determined."""
        mock_fetch.return_value = {'com.enabled.agent'}
        mock_exists.return_value = True
        mock_listdir.return_value = ['com.enabled.agent.plist', 'com.disabled.agent.plist']

        def parse_side_effect(path):
            if 'enabled' in path:
                return {'name': 'Enabled', 'label': 'com.enabled.agent', 'path': path}
            else:
                return {'name': 'Disabled', 'label': 'com.disabled.agent', 'path': path}

        mock_parse.side_effect = parse_side_effect

        result = get_launch_agents(user_only=True)

        enabled = [a for a in result if a['label'] == 'com.enabled.agent']
        disabled = [a for a in result if a['label'] == 'com.disabled.agent']

        assert enabled[0]['enabled'] is True
        assert disabled[0]['enabled'] is False

    @pytest.mark.unit
    @patch('utils.system_info.parse_plist_file')
    @patch('utils.system_info.os.listdir')
    @patch('utils.system_info.os.path.exists')
    @patch('utils.system_info.fetch_launchctl_status')
    def test_skips_non_plist_files(self, mock_fetch, mock_exists, mock_listdir, mock_parse):
        """Test that non-plist files are skipped."""
        mock_fetch.return_value = set()
        mock_exists.return_value = True
        mock_listdir.return_value = ['agent.plist', 'readme.txt', 'script.sh']
        mock_parse.return_value = {'name': 'Test', 'label': 'com.test', 'path': '/test'}

        get_launch_agents(user_only=True)

        # Should only parse .plist files
        assert mock_parse.call_count == 1


# ========== Test get_launch_daemons ==========

class TestGetLaunchDaemons:
    """Test suite for get_launch_daemons function."""

    @pytest.mark.unit
    @patch('utils.system_info.parse_plist_file')
    @patch('utils.system_info.os.listdir')
    @patch('utils.system_info.os.path.exists')
    @patch('utils.system_info.fetch_launchctl_status')
    def test_retrieval(self, mock_fetch, mock_exists, mock_listdir, mock_parse):
        """Test successful retrieval of launch daemons."""
        mock_fetch.return_value = {'com.test.daemon'}
        mock_exists.return_value = True
        mock_listdir.return_value = ['com.test.daemon.plist']
        mock_parse.return_value = {
            'name': 'TestDaemon',
            'label': 'com.test.daemon',
            'path': '/test/daemon.plist'
        }

        result = get_launch_daemons()

        assert len(result) > 0
        assert result[0]['type'] == 'Launch Daemon'
        assert result[0]['enabled'] is True

    @pytest.mark.unit
    @patch('utils.system_info.os.path.exists')
    @patch('utils.system_info.fetch_launchctl_status')
    def test_nonexistent_directories(self, mock_fetch, mock_exists):
        """Test handling of nonexistent daemon directories."""
        mock_fetch.return_value = set()
        mock_exists.return_value = False

        result = get_launch_daemons()

        assert result == []


# ========== Test parse_plist_file ==========

class TestParsePlistFile:
    """Test suite for parse_plist_file function."""

    @pytest.mark.unit
    def test_valid_plist(self, mock_plist_data, tmp_path):
        """Test parsing of valid plist file."""
        plist_file = tmp_path / "test.plist"

        # Write plist data
        with open(plist_file, 'wb') as f:
            plistlib.dump(mock_plist_data, f)

        result = parse_plist_file(str(plist_file))

        assert result is not None
        assert 'name' in result
        assert 'label' in result
        assert 'path' in result
        assert result['label'] == 'com.example.test'

    @pytest.mark.unit
    def test_plist_with_program(self, tmp_path):
        """Test plist with Program key."""
        plist_data = {
            'Label': 'com.test.program',
            'Program': '/usr/bin/test_program'
        }

        plist_file = tmp_path / "test.plist"
        with open(plist_file, 'wb') as f:
            plistlib.dump(plist_data, f)

        result = parse_plist_file(str(plist_file))

        assert result['name'] == 'test_program'
        assert result['label'] == 'com.test.program'

    @pytest.mark.unit
    def test_plist_with_program_arguments(self, tmp_path):
        """Test plist with ProgramArguments key."""
        plist_data = {
            'Label': 'com.test.args',
            'ProgramArguments': ['/usr/bin/python3', 'script.py']
        }

        plist_file = tmp_path / "test.plist"
        with open(plist_file, 'wb') as f:
            plistlib.dump(plist_data, f)

        result = parse_plist_file(str(plist_file))

        assert result['name'] == 'python3'

    @pytest.mark.unit
    def test_plist_without_program_info(self, tmp_path):
        """Test plist without Program or ProgramArguments."""
        plist_data = {'Label': 'com.test.noprog'}

        plist_file = tmp_path / "test.plist"
        with open(plist_file, 'wb') as f:
            plistlib.dump(plist_data, f)

        result = parse_plist_file(str(plist_file))

        assert result['name'] == 'com.test.noprog'

    @pytest.mark.unit
    def test_nonexistent_file(self):
        """Test handling of nonexistent file."""
        result = parse_plist_file('/nonexistent/file.plist')

        assert result is None

    @pytest.mark.unit
    def test_permission_denied(self, tmp_path):
        """Test handling of permission denied."""
        plist_file = tmp_path / "noperm.plist"
        plist_file.touch()

        with patch('builtins.open', side_effect=PermissionError()):
            result = parse_plist_file(str(plist_file))

        assert result is None

    @pytest.mark.unit
    def test_invalid_plist_format(self, tmp_path):
        """Test handling of invalid plist format."""
        plist_file = tmp_path / "invalid.plist"
        plist_file.write_text("This is not a valid plist file")

        result = parse_plist_file(str(plist_file))

        assert result is None

    @pytest.mark.unit
    def test_plist_with_all_keys(self, tmp_path):
        """Test plist with all optional keys."""
        plist_data = {
            'Label': 'com.test.full',
            'Program': '/usr/bin/test',
            'RunAtLoad': True,
            'KeepAlive': True
        }

        plist_file = tmp_path / "test.plist"
        with open(plist_file, 'wb') as f:
            plistlib.dump(plist_data, f)

        result = parse_plist_file(str(plist_file))

        assert result['run_at_load'] is True
        assert result['keep_alive'] is True


# ========== Test is_launchd_item_enabled ==========

class TestIsLaunchdItemEnabled:
    """Test suite for is_launchd_item_enabled function."""

    @pytest.mark.unit
    @patch('utils.system_info.subprocess.run')
    def test_enabled_item(self, mock_run):
        """Test detection of enabled item."""
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout="123\t0\tcom.test.enabled\n",
            stderr=""
        )

        result = is_launchd_item_enabled('com.test.enabled')

        assert result is True

    @pytest.mark.unit
    @patch('utils.system_info.subprocess.run')
    def test_disabled_item(self, mock_run):
        """Test detection of disabled item."""
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout="123\t0\tcom.other.service\n",
            stderr=""
        )

        result = is_launchd_item_enabled('com.test.disabled')

        assert result is False

    @pytest.mark.unit
    @patch('utils.system_info.subprocess.run')
    def test_command_failure(self, mock_run):
        """Test handling of command failure."""
        mock_run.return_value = MagicMock(
            returncode=1,
            stdout="",
            stderr="Error"
        )

        result = is_launchd_item_enabled('com.test.service')

        assert result is False


# ========== Test get_launchctl_list ==========

class TestGetLaunchctlList:
    """Test suite for get_launchctl_list function."""

    @pytest.mark.unit
    @patch('utils.system_info.subprocess.run')
    def test_successful_list(self, mock_run, mock_launchctl_output):
        """Test successful retrieval of service list."""
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout=mock_launchctl_output,
            stderr=""
        )

        result = get_launchctl_list()

        assert isinstance(result, list)
        assert 'com.apple.notificationcenterui' in result
        assert 'com.google.keystone.agent' in result

    @pytest.mark.unit
    @patch('utils.system_info.subprocess.run')
    def test_empty_list(self, mock_run):
        """Test handling of empty service list."""
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout="PID\tStatus\tLabel\n",
            stderr=""
        )

        result = get_launchctl_list()

        assert result == []

    @pytest.mark.unit
    @patch('utils.system_info.subprocess.run')
    def test_command_failure(self, mock_run):
        """Test handling of command failure."""
        mock_run.return_value = MagicMock(
            returncode=1,
            stdout="",
            stderr="Error"
        )

        result = get_launchctl_list()

        assert result == []


# ========== Test disable_login_item ==========

class TestDisableLoginItem:
    """Test suite for disable_login_item function."""

    @pytest.mark.unit
    @pytest.mark.macos
    @patch('utils.system_info.subprocess.run')
    def test_successful_disable(self, mock_run):
        """Test successful disabling of login item."""
        mock_run.return_value = MagicMock(returncode=0)

        result = disable_login_item('TestApp')

        assert result is True
        mock_run.assert_called_once()

    @pytest.mark.unit
    @patch('utils.system_info.subprocess.run')
    def test_failed_disable(self, mock_run):
        """Test failed disable operation."""
        mock_run.return_value = MagicMock(returncode=1)

        result = disable_login_item('TestApp')

        assert result is False

    @pytest.mark.unit
    @patch('utils.system_info.subprocess.run')
    def test_exception_handling(self, mock_run):
        """Test exception handling."""
        mock_run.side_effect = Exception("Test error")

        result = disable_login_item('TestApp')

        assert result is False


# ========== Test disable_launch_agent ==========

class TestDisableLaunchAgent:
    """Test suite for disable_launch_agent function."""

    @pytest.mark.unit
    @patch('utils.system_info.subprocess.run')
    def test_successful_disable(self, mock_run):
        """Test successful unloading of agent."""
        mock_run.return_value = MagicMock(returncode=0)

        result = disable_launch_agent('com.test.agent')

        assert result is True
        args = mock_run.call_args[0][0]
        assert 'launchctl' in args
        assert 'unload' in args
        assert '-w' in args

    @pytest.mark.unit
    @patch('utils.system_info.subprocess.run')
    def test_failed_disable(self, mock_run):
        """Test failed disable operation."""
        mock_run.return_value = MagicMock(returncode=1)

        result = disable_launch_agent('com.test.agent')

        assert result is False

    @pytest.mark.unit
    @patch('utils.system_info.subprocess.run')
    def test_exception_handling(self, mock_run):
        """Test exception handling."""
        mock_run.side_effect = subprocess.TimeoutExpired(['launchctl'], timeout=5)

        result = disable_launch_agent('com.test.agent')

        assert result is False


# ========== Test enable_launch_agent ==========

class TestEnableLaunchAgent:
    """Test suite for enable_launch_agent function."""

    @pytest.mark.unit
    @patch('utils.system_info.subprocess.run')
    def test_successful_enable(self, mock_run):
        """Test successful loading of agent."""
        mock_run.return_value = MagicMock(returncode=0)

        result = enable_launch_agent('com.test.agent', '/path/to/agent.plist')

        assert result is True
        args = mock_run.call_args[0][0]
        assert 'launchctl' in args
        assert 'load' in args
        assert '-w' in args
        assert '/path/to/agent.plist' in args

    @pytest.mark.unit
    @patch('utils.system_info.subprocess.run')
    def test_failed_enable(self, mock_run):
        """Test failed enable operation."""
        mock_run.return_value = MagicMock(returncode=1)

        result = enable_launch_agent('com.test.agent', '/path/to/agent.plist')

        assert result is False

    @pytest.mark.unit
    @patch('utils.system_info.subprocess.run')
    def test_exception_handling(self, mock_run):
        """Test exception handling."""
        mock_run.side_effect = Exception("Test error")

        result = enable_launch_agent('com.test.agent', '/path/to/agent.plist')

        assert result is False
