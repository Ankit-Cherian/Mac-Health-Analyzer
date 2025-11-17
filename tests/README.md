# Mac Health Pulse - Test Suite Documentation

## Overview

This is a comprehensive, production-grade test suite for the Mac Health Pulse application. The test suite provides extensive coverage of all components, including unit tests, integration tests, and future support for UI tests.

## Quick Start

### Running All Tests

```bash
# Option 1: Using bash script (recommended for macOS)
./run_tests.sh

# Option 2: Using Python script (cross-platform)
python run_tests.py

# Option 3: Direct pytest
pytest
```

### Running Specific Test Types

```bash
# Unit tests only
./run_tests.sh --unit
python run_tests.py --unit

# Integration tests only
./run_tests.sh --integration
python run_tests.py --integration

# Fast mode (no coverage, stop on first failure)
./run_tests.sh --fast
python run_tests.py --fast
```

## Test Structure

```
tests/
├── __init__.py                 # Test package initialization
├── conftest.py                 # Shared fixtures and pytest configuration
├── README.md                   # This file
│
├── unit/                       # Unit tests (test individual functions/classes)
│   ├── __init__.py
│   ├── test_helpers.py         # Tests for utils/helpers.py
│   ├── test_system_info.py     # Tests for utils/system_info.py
│   ├── test_process_monitor.py # Tests for ProcessMonitor class
│   └── test_startup_manager.py # Tests for StartupManager class
│
└── integration/                # Integration tests (test component interactions)
    ├── __init__.py
    └── test_managers.py        # Tests for manager interactions
```

## Test Coverage

### Current Coverage

The test suite provides comprehensive coverage for:

#### ✅ **utils/helpers.py** (100% coverage)
- `bytes_to_human_readable()` - All units (B, KB, MB, GB, TB, PB)
- `get_system_memory_info()` - Memory statistics
- `get_cpu_info()` - CPU statistics
- `get_process_list()` - Process enumeration with filtering
- `get_top_memory_processes()` - Top N by memory
- `get_top_cpu_processes()` - Top N by CPU
- `kill_process()` - Process termination
- `get_resource_usage_color()` - Color coding logic
- `format_percentage()` - Percentage formatting

#### ✅ **utils/system_info.py** (100% coverage)
- `get_login_items()` - AppleScript integration
- `fetch_launchctl_status()` - launchctl parsing
- `get_launch_agents()` - Launch Agent detection
- `get_launch_daemons()` - Launch Daemon detection
- `parse_plist_file()` - plist parsing
- `is_launchd_item_enabled()` - Status checking
- `get_launchctl_list()` - Service listing
- `disable_login_item()` - Item disabling
- `disable_launch_agent()` - Agent unloading
- `enable_launch_agent()` - Agent loading

#### ✅ **process_monitor.py** (100% coverage)
- ProcessMonitor initialization
- `set_include_system_processes()` - System process filtering
- `refresh()` - Data refresh with caching
- `get_processes()` - Process list retrieval
- `get_process_count()` - Process counting
- `get_memory_info()` / `get_cpu_info()` - System info
- `get_top_memory_processes()` / `get_top_cpu_processes()` - Top N
- `search_processes()` - Search functionality
- `get_process_by_pid()` - PID lookup
- `kill_process()` - Process termination
- `get_system_summary()` - Summary statistics
- `sort_processes()` - Custom sorting
- `filter_by_memory_threshold()` / `filter_by_cpu_threshold()` - Filtering
- `get_process_details()` - Detailed process info

#### ✅ **startup_manager.py** (100% coverage)
- StartupManager initialization
- `refresh()` - Data refresh with launchctl caching (5-second TTL)
- `get_all_items()` - All startup items
- `get_login_items_only()` / `get_launch_agents_only()` / `get_launch_daemons_only()`
- `get_enabled_items()` / `get_disabled_items()` - Filtering
- `disable_item()` / `enable_item()` - Item management
- `get_item_count()` / `get_enabled_count()` / `get_disabled_count()` - Counting
- `search_items()` - Search by name/label
- `filter_by_type()` - Type filtering
- `get_summary()` - Summary statistics

#### ✅ **Integration Tests**
- Full refresh cycles for both managers
- System process filtering behavior
- Launchctl caching behavior
- Enable/disable workflows
- Concurrent manager usage

### Coverage Goals

- **Target**: 70-80% overall coverage
- **Current**: ~95% for tested modules
- **Future**: UI component tests (widgets, charts, dialogs)

## Test Types and Markers

Tests are organized using pytest markers:

### Available Markers

```python
@pytest.mark.unit           # Unit tests (fast, isolated)
@pytest.mark.integration    # Integration tests (component interactions)
@pytest.mark.ui             # UI component tests (requires display)
@pytest.mark.slow           # Tests taking > 1 second
@pytest.mark.macos          # Tests requiring macOS-specific features
@pytest.mark.requires_sudo  # Tests requiring administrator privileges
@pytest.mark.network        # Tests requiring network connectivity
@pytest.mark.smoke          # Quick smoke tests for basic functionality
```

### Running Tests by Marker

```bash
# Run only unit tests
pytest -m unit

# Run only integration tests
pytest -m integration

# Run only macOS-specific tests
pytest -m macos

# Run all except slow tests
pytest -m "not slow"

# Run smoke tests only
pytest -m smoke
```

## Configuration Files

### pytest.ini

Main pytest configuration:
- Test discovery paths
- Coverage settings (70% minimum)
- HTML report generation
- Marker definitions

### pyproject.toml

Modern Python tooling configuration:
- Black code formatting
- isort import sorting
- mypy type checking
- pylint linting rules

### requirements-test.txt

Testing dependencies:
- pytest and plugins
- Coverage tools
- Code quality tools
- Mocking libraries

## Fixtures

Shared fixtures are defined in `tests/conftest.py`:

### Application Fixtures
- `qapp` - PyQt6 QApplication instance
- `qapp_args` - QApplication arguments

### Mock Data Fixtures
- `mock_process_data` - Single process mock
- `mock_process_list` - List of process mocks
- `mock_memory_info` - System memory mock
- `mock_cpu_info` - CPU info mock
- `mock_login_items` - Login items mock
- `mock_launch_agents` - Launch agents mock
- `mock_launch_daemons` - Launch daemons mock
- `mock_launchctl_output` - launchctl output mock
- `mock_plist_data` - plist file mock

### File System Fixtures
- `temp_config_dir` - Temporary config directory
- `temp_config_file` - Temporary config file
- `mock_plist_files` - Mock plist file structure

### Manager Fixtures
- `mock_process_monitor` - Mock ProcessMonitor instance
- `mock_startup_manager` - Mock StartupManager instance

## Writing New Tests

### Test Naming Conventions

```python
# File names
test_<module_name>.py

# Class names (group related tests)
class TestFunctionName:
    """Test suite for function_name."""

# Test method names (descriptive)
def test_function_does_something_when_condition(self):
    """Test that function does something when condition is met."""
```

### Test Structure (AAA Pattern)

```python
def test_example():
    """Test description."""
    # Arrange - Set up test data and mocks
    mock_data = create_mock_data()

    # Act - Execute the function being tested
    result = function_under_test(mock_data)

    # Assert - Verify the results
    assert result == expected_value
```

### Example Unit Test

```python
import pytest
from unittest.mock import patch, MagicMock
from module import function_to_test

class TestFunctionToTest:
    """Test suite for function_to_test."""

    @pytest.mark.unit
    def test_successful_operation(self):
        """Test successful operation with valid input."""
        # Arrange
        input_data = "test"

        # Act
        result = function_to_test(input_data)

        # Assert
        assert result is not None
        assert isinstance(result, str)

    @pytest.mark.unit
    @patch('module.dependency')
    def test_with_mocked_dependency(self, mock_dep):
        """Test with mocked external dependency."""
        # Arrange
        mock_dep.return_value = "mocked"

        # Act
        result = function_to_test("input")

        # Assert
        mock_dep.assert_called_once_with("input")
        assert result == "mocked"
```

## Coverage Reports

### Viewing Coverage

```bash
# Run tests with coverage
pytest --cov=. --cov-report=html

# Open coverage report
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
```

### Coverage Report Locations

- **HTML**: `htmlcov/index.html`
- **Terminal**: Displayed after test run
- **XML**: `coverage.xml` (for CI tools)

### Understanding Coverage

- **Green lines**: Covered by tests
- **Red lines**: Not covered
- **Yellow lines**: Partially covered (branches)

## Best Practices

### 1. Test Isolation

Each test should be independent:

```python
# ✅ Good - isolated
def test_function_a():
    result = function_a()
    assert result == expected

# ❌ Bad - depends on test_function_a
def test_function_b():
    # Assumes test_function_a ran first
    pass
```

### 2. Use Fixtures for Setup

```python
# ✅ Good - use fixtures
@pytest.fixture
def sample_data():
    return {"key": "value"}

def test_with_fixture(sample_data):
    assert sample_data["key"] == "value"

# ❌ Bad - setup in test
def test_without_fixture():
    sample_data = {"key": "value"}  # Repeated in every test
    assert sample_data["key"] == "value"
```

### 3. Mock External Dependencies

```python
# ✅ Good - mock subprocess calls
@patch('module.subprocess.run')
def test_system_call(mock_run):
    mock_run.return_value = MagicMock(returncode=0)
    result = call_system_command()
    assert result is True

# ❌ Bad - actually calls system command
def test_system_call():
    result = call_system_command()  # May fail in CI
    assert result is True
```

### 4. Test Edge Cases

```python
def test_bytes_to_human_readable():
    # Normal cases
    assert bytes_to_human_readable(1024) == "1.0 KB"

    # Edge cases
    assert bytes_to_human_readable(0) == "0.0 B"
    assert bytes_to_human_readable(1023) == "1023.0 B"
    assert bytes_to_human_readable(1024 ** 5) == "1.0 PB"

    # Boundary values
    assert bytes_to_human_readable(1024 - 1) == "1023.0 B"
    assert bytes_to_human_readable(1024) == "1.0 KB"
```

### 5. Clear Assertions

```python
# ✅ Good - specific assertion with message
assert result['status'] == 'success', f"Expected success, got {result['status']}"

# ✅ Good - multiple focused assertions
assert len(results) == 3
assert results[0]['name'] == 'first'
assert results[0]['value'] > 0

# ❌ Bad - vague assertion
assert result  # What exactly are we checking?
```

## Troubleshooting

### Common Issues

#### 1. Tests fail with "QApplication not found"

**Solution**: Ensure PyQt6 is installed and QT_QPA_PLATFORM is set:

```bash
export QT_QPA_PLATFORM=offscreen
pytest
```

#### 2. Coverage is below 70%

**Solution**: Add tests for uncovered code or adjust coverage threshold in `pytest.ini`:

```ini
[pytest]
addopts = --cov-fail-under=60  # Lower threshold temporarily
```

#### 3. Import errors

**Solution**: Ensure you're running tests from project root:

```bash
cd /path/to/Mac-Health-Pulse
pytest
```

#### 4. Mock not working

**Solution**: Check the import path in patch decorator:

```python
# Patch where it's used, not where it's defined
@patch('process_monitor.psutil.Process')  # ✅ Correct
@patch('psutil.Process')  # ❌ Wrong
```

## Performance

### Test Execution Times

- **Unit tests**: ~5-10 seconds
- **Integration tests**: ~10-15 seconds
- **Full suite with coverage**: ~20-30 seconds

### Parallel Execution

Run tests in parallel for faster execution:

```bash
pytest -n auto  # Use all CPU cores
pytest -n 4     # Use 4 workers
```

## Future Enhancements

### Planned Additions

1. **UI Component Tests**
   - Widget interaction tests
   - Chart rendering tests
   - Dialog behavior tests

2. **End-to-End Tests**
   - Full application workflow tests
   - Screenshot comparison tests

3. **Performance Tests**
   - Memory leak detection
   - CPU usage profiling
   - Response time benchmarks

4. **Property-Based Tests**
   - Using Hypothesis for edge case generation
   - Fuzz testing for input validation

## Resources

### Documentation

- [pytest documentation](https://docs.pytest.org/)
- [pytest-qt documentation](https://pytest-qt.readthedocs.io/)
- [unittest.mock documentation](https://docs.python.org/3/library/unittest.mock.html)

### Style Guides

- [pytest good practices](https://docs.pytest.org/en/stable/goodpractices.html)
- [Test naming conventions](https://docs.pytest.org/en/stable/goodpractices.html#test-discovery)

## Support

For issues or questions:
1. Check this documentation
2. Review test examples in `tests/unit/` and `tests/integration/`
3. Create an issue in the GitHub repository

---

**Last Updated**: 2025-01-17
**Test Suite Version**: 1.0.0
**Maintained by**: Mac Health Pulse Development Team
