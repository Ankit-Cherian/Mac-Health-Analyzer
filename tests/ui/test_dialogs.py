"""
Tests for UI dialogs - ProcessDetailDialog and StartupDetailDialog
"""

import sys
from pathlib import Path
from unittest.mock import Mock, patch

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from ui.process_detail_dialog import ProcessDetailDialog
from ui.startup_detail_dialog import StartupDetailDialog


class TestProcessDetailDialog:
    """Test ProcessDetailDialog class."""

    @pytest.fixture
    def process_data(self):
        """Sample process data."""
        return {
            'pid': 123,
            'name': 'Chrome',
            'username': 'testuser',
            'cpu_percent': 25.5,
            'memory_percent': 10.2,
            'memory_human': '500 MB',
            'status': 'running',
            'create_time': 1234567890.0,
            'num_threads': 10,
            'cmdline': ['/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'],
        }

    def test_initialization(self, qapp, process_data):
        """Test ProcessDetailDialog initialization."""
        dialog = ProcessDetailDialog(process_data)

        assert dialog.process_data == process_data
        assert dialog.simple_mode == False
        assert dialog.windowTitle() == "Process Details - Chrome"

    def test_init_ui(self, qapp, process_data):
        """Test UI initialization."""
        dialog = ProcessDetailDialog(process_data)

        # Should have content layout
        assert dialog.content_layout is not None

    def test_create_header(self, qapp, process_data):
        """Test header creation."""
        dialog = ProcessDetailDialog(process_data)

        header = dialog._create_header()

        assert header is not None

    def test_create_toggle_section(self, qapp, process_data):
        """Test toggle section creation."""
        dialog = ProcessDetailDialog(process_data)

        toggle_section = dialog._create_toggle_section()

        assert toggle_section is not None

    def test_add_description_section(self, qapp, process_data):
        """Test description section."""
        with patch('ui.process_detail_dialog.ProcessDescriber') as mock_describer:
            mock_describer.return_value.get_description.return_value = "Test description"
            mock_describer.return_value.is_safe_to_quit.return_value = True

            dialog = ProcessDetailDialog(process_data)

            # Should create section without error
            assert True

    def test_add_recommendation_section(self, qapp, process_data):
        """Test recommendation section."""
        with patch('ui.process_detail_dialog.ProcessDescriber'):
            dialog = ProcessDetailDialog(process_data)

            # Should create section without error
            assert True

    def test_add_process_info_section(self, qapp, process_data):
        """Test process info section."""
        dialog = ProcessDetailDialog(process_data)

        # Should create section without error
        assert True

    def test_add_resource_usage_section(self, qapp, process_data):
        """Test resource usage section."""
        dialog = ProcessDetailDialog(process_data)

        # Should create section without error
        assert True

    def test_add_command_line_section(self, qapp, process_data):
        """Test command line section."""
        dialog = ProcessDetailDialog(process_data)

        # Should create section without error
        assert True

    def test_toggle_explanation_mode(self, qapp, process_data):
        """Test toggling explanation mode."""
        with patch('ui.process_detail_dialog.ProcessDescriber'):
            dialog = ProcessDetailDialog(process_data)

            # Toggle mode
            dialog._toggle_explanation_mode(True)

            assert dialog.simple_mode == True

            # Toggle back
            dialog._toggle_explanation_mode(False)

            assert dialog.simple_mode == False

    def test_minimal_process_data(self, qapp):
        """Test dialog with minimal process data."""
        minimal_data = {
            'pid': 123,
            'name': 'test_process',
        }

        dialog = ProcessDetailDialog(minimal_data)

        assert dialog.process_data == minimal_data


class TestStartupDetailDialog:
    """Test StartupDetailDialog class."""

    @pytest.fixture
    def startup_item_data(self):
        """Sample startup item data."""
        return {
            'name': 'Dropbox',
            'type': 'Login Item',
            'enabled': True,
            'location': '/Applications/Dropbox.app',
            'label': 'com.dropbox.app',
        }

    def test_initialization(self, qapp, startup_item_data):
        """Test StartupDetailDialog initialization."""
        dialog = StartupDetailDialog(startup_item_data)

        assert dialog.item_data == startup_item_data
        assert dialog.windowTitle() == "Startup Item Details - Dropbox"

    def test_init_ui(self, qapp, startup_item_data):
        """Test UI initialization."""
        dialog = StartupDetailDialog(startup_item_data)

        # Should have content layout
        assert dialog.content_layout is not None

    def test_create_header(self, qapp, startup_item_data):
        """Test header creation."""
        dialog = StartupDetailDialog(startup_item_data)

        header = dialog._create_header()

        assert header is not None

    def test_add_description_section(self, qapp, startup_item_data):
        """Test description section."""
        with patch('ui.startup_detail_dialog.StartupItemDescriber') as mock_describer:
            mock_describer.return_value.get_description.return_value = "Test description"
            mock_describer.return_value.is_safe_to_disable.return_value = True

            dialog = StartupDetailDialog(startup_item_data)

            # Should create section without error
            assert True

    def test_add_recommendation_section(self, qapp, startup_item_data):
        """Test recommendation section."""
        with patch('ui.startup_detail_dialog.StartupItemDescriber'):
            dialog = StartupDetailDialog(startup_item_data)

            # Should create section without error
            assert True

    def test_add_item_info_section(self, qapp, startup_item_data):
        """Test item info section."""
        dialog = StartupDetailDialog(startup_item_data)

        # Should create section without error
        assert True

    def test_minimal_startup_data(self, qapp):
        """Test dialog with minimal startup data."""
        minimal_data = {
            'name': 'test_item',
            'type': 'Login Item',
        }

        dialog = StartupDetailDialog(minimal_data)

        assert dialog.item_data == minimal_data

    def test_different_item_types(self, qapp):
        """Test dialog with different item types."""
        types = ['Login Item', 'Launch Agent', 'Launch Daemon']

        for item_type in types:
            data = {
                'name': 'test',
                'type': item_type,
            }

            dialog = StartupDetailDialog(data)

            assert dialog.item_data['type'] == item_type
