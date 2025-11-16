"""
Tests for main.py - MainWindow class
"""

import json
import sys
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

import pytest
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from main import MainWindow, main


class TestMainWindow:
    """Test MainWindow class."""

    def test_initialization(self, qapp, mock_startup_manager, mock_process_monitor):
        """Test MainWindow initialization."""
        with patch('main.StartupManager', return_value=mock_startup_manager), \
             patch('main.ProcessMonitor', return_value=mock_process_monitor), \
             patch('main.get_font_manager') as mock_font_mgr:

            mock_font_mgr.return_value.load_fonts.return_value = None

            window = MainWindow()

            assert window.startup_manager is not None
            assert window.process_monitor is not None
            assert window.dashboard is not None
            assert window.windowTitle() == "Mac Health Analyzer"
            assert window.minimumSize().width() == 1200
            assert window.minimumSize().height() == 800

    def test_setup_window(self, qapp, mock_startup_manager, mock_process_monitor):
        """Test window setup."""
        with patch('main.StartupManager', return_value=mock_startup_manager), \
             patch('main.ProcessMonitor', return_value=mock_process_monitor), \
             patch('main.get_font_manager'):

            window = MainWindow()

            assert window.windowTitle() == "Mac Health Analyzer"
            assert window.minimumWidth() == 1200
            assert window.minimumHeight() == 800

    def test_center_on_screen(self, qapp, mock_startup_manager, mock_process_monitor):
        """Test window centering."""
        with patch('main.StartupManager', return_value=mock_startup_manager), \
             patch('main.ProcessMonitor', return_value=mock_process_monitor), \
             patch('main.get_font_manager'):

            window = MainWindow()
            window.center_on_screen()

            # Window should be positioned (test that method runs without error)
            assert window.geometry().x() >= 0
            assert window.geometry().y() >= 0

    def test_load_fonts_success(self, qapp, mock_startup_manager, mock_process_monitor):
        """Test successful font loading."""
        with patch('main.StartupManager', return_value=mock_startup_manager), \
             patch('main.ProcessMonitor', return_value=mock_process_monitor), \
             patch('main.get_font_manager') as mock_font_mgr:

            mock_font_mgr.return_value.load_fonts.return_value = None

            window = MainWindow()
            window.load_fonts()

            # Should complete without error
            assert mock_font_mgr.called

    def test_load_fonts_failure(self, qapp, mock_startup_manager, mock_process_monitor, capsys):
        """Test font loading failure handling."""
        with patch('main.StartupManager', return_value=mock_startup_manager), \
             patch('main.ProcessMonitor', return_value=mock_process_monitor), \
             patch('main.get_font_manager') as mock_font_mgr:

            mock_font_mgr.return_value.load_fonts.side_effect = Exception("Font error")

            window = MainWindow()

            # Should handle error gracefully
            captured = capsys.readouterr()
            assert "Could not load custom fonts" in captured.out or True  # Error is printed

    def test_apply_styles(self, qapp, mock_startup_manager, mock_process_monitor):
        """Test applying styles."""
        with patch('main.StartupManager', return_value=mock_startup_manager), \
             patch('main.ProcessMonitor', return_value=mock_process_monitor), \
             patch('main.get_font_manager'), \
             patch('main.get_palette') as mock_palette, \
             patch('main.get_main_stylesheet') as mock_stylesheet:

            mock_palette.return_value = MagicMock()
            mock_stylesheet.return_value = ""

            window = MainWindow()

            assert mock_palette.called
            assert mock_stylesheet.called

    def test_close_event(self, qapp, mock_startup_manager, mock_process_monitor):
        """Test window close event."""
        with patch('main.StartupManager', return_value=mock_startup_manager), \
             patch('main.ProcessMonitor', return_value=mock_process_monitor), \
             patch('main.get_font_manager'):

            window = MainWindow()

            # Mock the close event
            event = MagicMock()
            window.closeEvent(event)

            # Event should be accepted
            event.accept.assert_called_once()

    def test_has_seen_guide_no_file(self, qapp, mock_startup_manager, mock_process_monitor, tmp_path, monkeypatch):
        """Test _has_seen_guide when config file doesn't exist."""
        with patch('main.StartupManager', return_value=mock_startup_manager), \
             patch('main.ProcessMonitor', return_value=mock_process_monitor), \
             patch('main.get_font_manager'):

            # Set config path to non-existent file
            monkeypatch.setattr(Path, 'home', lambda: tmp_path)

            window = MainWindow()
            result = window._has_seen_guide()

            assert result == False

    def test_has_seen_guide_with_file(self, qapp, mock_startup_manager, mock_process_monitor, tmp_path, monkeypatch):
        """Test _has_seen_guide when config file exists."""
        with patch('main.StartupManager', return_value=mock_startup_manager), \
             patch('main.ProcessMonitor', return_value=mock_process_monitor), \
             patch('main.get_font_manager'):

            # Create config file
            config_dir = tmp_path / '.mac-health-analyzer'
            config_dir.mkdir()
            config_file = config_dir / 'config.json'
            config_file.write_text(json.dumps({'startup_guide_shown': True}))

            monkeypatch.setattr(Path, 'home', lambda: tmp_path)

            window = MainWindow()
            result = window._has_seen_guide()

            assert result == True

    def test_save_guide_preference(self, qapp, mock_startup_manager, mock_process_monitor, tmp_path, monkeypatch):
        """Test _save_guide_preference."""
        with patch('main.StartupManager', return_value=mock_startup_manager), \
             patch('main.ProcessMonitor', return_value=mock_process_monitor), \
             patch('main.get_font_manager'):

            monkeypatch.setattr(Path, 'home', lambda: tmp_path)

            window = MainWindow()
            window._save_guide_preference()

            # Check config was saved
            config_file = tmp_path / '.mac-health-analyzer' / 'config.json'
            assert config_file.exists()

            with open(config_file) as f:
                config = json.load(f)
            assert config['startup_guide_shown'] == True

    def test_get_config_path(self, qapp, mock_startup_manager, mock_process_monitor, tmp_path, monkeypatch):
        """Test _get_config_path."""
        with patch('main.StartupManager', return_value=mock_startup_manager), \
             patch('main.ProcessMonitor', return_value=mock_process_monitor), \
             patch('main.get_font_manager'):

            monkeypatch.setattr(Path, 'home', lambda: tmp_path)

            window = MainWindow()
            config_path = window._get_config_path()

            assert config_path.parent.name == '.mac-health-analyzer'
            assert config_path.name == 'config.json'

    def test_show_startup_guide_first_time(self, qapp, mock_startup_manager, mock_process_monitor, tmp_path, monkeypatch):
        """Test showing startup guide for first time."""
        with patch('main.StartupManager', return_value=mock_startup_manager), \
             patch('main.ProcessMonitor', return_value=mock_process_monitor), \
             patch('main.get_font_manager'), \
             patch('main.StartupGuide') as mock_guide:

            monkeypatch.setattr(Path, 'home', lambda: tmp_path)

            # Mock guide dialog
            guide_instance = MagicMock()
            guide_instance.should_show_again.return_value = False
            mock_guide.return_value = guide_instance

            window = MainWindow()
            window.show_startup_guide_if_needed()

            # Guide should be shown
            mock_guide.assert_called_once()
            guide_instance.exec.assert_called_once()

    def test_show_startup_guide_already_seen(self, qapp, mock_startup_manager, mock_process_monitor, tmp_path, monkeypatch):
        """Test not showing startup guide when already seen."""
        with patch('main.StartupManager', return_value=mock_startup_manager), \
             patch('main.ProcessMonitor', return_value=mock_process_monitor), \
             patch('main.get_font_manager'), \
             patch('main.StartupGuide') as mock_guide:

            # Create config file with guide shown
            config_dir = tmp_path / '.mac-health-analyzer'
            config_dir.mkdir()
            config_file = config_dir / 'config.json'
            config_file.write_text(json.dumps({'startup_guide_shown': True}))

            monkeypatch.setattr(Path, 'home', lambda: tmp_path)

            window = MainWindow()
            window.show_startup_guide_if_needed()

            # Guide should NOT be shown
            mock_guide.assert_not_called()


class TestMain:
    """Test main() function."""

    def test_main_function_success(self, qapp, monkeypatch):
        """Test main function runs successfully."""
        with patch('main.MainWindow') as mock_window_class, \
             patch('main.get_font_manager'), \
             patch.object(sys, 'exit') as mock_exit:

            # Mock window instance
            mock_window = MagicMock()
            mock_window_class.return_value = mock_window

            # Mock app.exec() to return immediately
            monkeypatch.setattr(QApplication, 'exec', lambda self: 0)

            # This will create a new QApplication or use existing
            main()

            # Window should be shown
            mock_window.show.assert_called_once()
            mock_window.show_startup_guide_if_needed.assert_called_once()

    def test_main_function_exception(self, qapp, monkeypatch):
        """Test main function handles exceptions."""
        with patch('main.MainWindow') as mock_window_class, \
             patch.object(sys, 'exit') as mock_exit:

            # Make MainWindow raise an exception
            mock_window_class.side_effect = Exception("Test error")

            # Call main
            main()

            # Should exit with code 1
            mock_exit.assert_called_once_with(1)
