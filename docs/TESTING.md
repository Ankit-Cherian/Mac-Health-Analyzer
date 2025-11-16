# Testing Guide for Mac Health Pulse

## 🎯 Quick Start

Run the complete test suite with a single command:

```bash
./run_tests.sh
```

That's it! The test runner will:
- ✅ Check dependencies
- ✅ Run all tests
- ✅ Generate coverage reports
- ✅ Show results in color-coded output

## 📋 Prerequisites

### Install Test Dependencies

```bash
# Install application dependencies
pip install -r requirements.txt

# Install test dependencies
pip install -r requirements-test.txt
```

### Verify Installation

```bash
# Check pytest is installed
pytest --version

# Check coverage is installed
coverage --version
```

## 🚀 Running Tests

### Basic Commands

```bash
# Run all tests (recommended)
./run_tests.sh

# Run with Python script (cross-platform)
python run_tests.py

# Run with pytest directly
pytest
```

### Test Filtering

```bash
# Run only unit tests
./run_tests.sh --unit

# Run only integration tests
./run_tests.sh --integration

# Run in fast mode (no coverage, stop on first failure)
./run_tests.sh --fast

# Run with verbose output
./run_tests.sh --verbose

# Run without coverage
./run_tests.sh --no-cov
```

### Advanced Filtering

```bash
# Run specific test file
pytest tests/unit/test_helpers.py

# Run specific test class
pytest tests/unit/test_helpers.py::TestBytesToHumanReadable

# Run specific test method
pytest tests/unit/test_helpers.py::TestBytesToHumanReadable::test_bytes

# Run tests matching pattern
pytest -k "memory"

# Run tests with specific marker
pytest -m unit
pytest -m integration
pytest -m "not slow"
```

## 📊 Coverage Reports

### Generate Coverage

```bash
# Run tests with HTML coverage report
pytest --cov=. --cov-report=html

# Open coverage report (macOS)
open htmlcov/index.html

# Open coverage report (Linux)
xdg-open htmlcov/index.html
```

### Coverage Locations

- **HTML Report**: `htmlcov/index.html` - Interactive, detailed coverage report
- **Terminal Report**: Shown after test run - Quick summary
- **XML Report**: `coverage.xml` - For CI/CD tools

### Understanding Coverage

```
Name                      Stmts   Miss  Cover   Missing
-------------------------------------------------------
utils/helpers.py             50      0   100%
process_monitor.py           75      3    96%   142-144
startup_manager.py           80      5    94%   98-102
-------------------------------------------------------
TOTAL                       205      8    96%
```

- **Stmts**: Total lines of code
- **Miss**: Lines not covered by tests
- **Cover**: Percentage covered
- **Missing**: Line numbers not covered

## 🎨 Test Structure

```
tests/
├── conftest.py           # Shared fixtures and configuration
├── README.md             # Detailed testing documentation
│
├── unit/                 # Unit tests (test individual functions)
│   ├── test_helpers.py
│   ├── test_system_info.py
│   ├── test_process_monitor.py
│   └── test_startup_manager.py
│
└── integration/          # Integration tests (test interactions)
    └── test_managers.py
```

## 🏷️ Test Markers

Tests are categorized with markers:

```python
@pytest.mark.unit           # Fast, isolated unit tests
@pytest.mark.integration    # Component interaction tests
@pytest.mark.ui             # UI component tests
@pytest.mark.slow           # Tests taking > 1 second
@pytest.mark.macos          # macOS-specific tests
@pytest.mark.requires_sudo  # Requires administrator privileges
```

Run tests by marker:

```bash
pytest -m unit              # Only unit tests
pytest -m "unit or integration"  # Unit or integration
pytest -m "not slow"        # All except slow tests
```

## ✍️ Writing Tests

### Test File Template

```python
"""
Unit Tests for module_name.py

Description of what is being tested.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock

from module_name import function_to_test


class TestFunctionName:
    """Test suite for function_name."""

    @pytest.mark.unit
    def test_successful_case(self):
        """Test description."""
        # Arrange
        input_data = "test"

        # Act
        result = function_to_test(input_data)

        # Assert
        assert result == "expected"

    @pytest.mark.unit
    def test_edge_case(self):
        """Test edge case handling."""
        result = function_to_test(None)
        assert result is None
```

### Using Fixtures

Fixtures provide reusable test data:

```python
def test_with_mock_data(mock_process_list):
    """Test using a predefined fixture."""
    # mock_process_list is automatically provided
    assert len(mock_process_list) > 0
```

Available fixtures in `conftest.py`:
- `mock_process_data` - Single process
- `mock_process_list` - List of processes
- `mock_memory_info` - System memory
- `mock_cpu_info` - CPU information
- Many more...

### Mocking External Calls

```python
@patch('module.subprocess.run')
def test_system_call(mock_run):
    """Test function that calls subprocess."""
    # Setup mock
    mock_run.return_value = MagicMock(returncode=0, stdout="success")

    # Call function
    result = function_that_calls_subprocess()

    # Verify
    assert result is True
    mock_run.assert_called_once()
```

## 🐛 Troubleshooting

### Common Issues

#### Import Errors

```bash
# Error: ModuleNotFoundError
# Solution: Run tests from project root
cd /path/to/Mac-Health-Pulse
pytest
```

#### Qt Platform Errors

```bash
# Error: QApplication not found
# Solution: Set Qt platform to offscreen
export QT_QPA_PLATFORM=offscreen
pytest
```

#### Permission Errors (macOS)

```bash
# Some tests may need permissions
# Run with appropriate permissions or skip with markers
pytest -m "not requires_sudo"
```

#### Slow Tests

```bash
# Skip slow tests
pytest -m "not slow"

# Run tests in parallel (faster)
pytest -n auto
```

### Debug Failing Tests

```bash
# Show print statements
pytest -s

# Stop on first failure
pytest -x

# Show local variables on failure
pytest -l

# Drop into debugger on failure
pytest --pdb

# Verbose output
pytest -vv
```

## 📈 Performance

### Test Execution Times

- **Unit Tests**: ~5-10 seconds
- **Integration Tests**: ~10-15 seconds
- **Full Suite**: ~20-30 seconds with coverage

### Speed Optimization

```bash
# Run in parallel
pytest -n auto

# Skip coverage for speed
pytest --no-cov

# Fast mode (stop on first failure, no coverage)
./run_tests.sh --fast
```

## 📚 Best Practices

### 1. Write Tests First (TDD)

```python
# 1. Write the test
def test_new_feature():
    assert new_feature() == expected_result

# 2. Run test (it fails)
# 3. Implement new_feature()
# 4. Run test (it passes)
```

### 2. Test Edge Cases

```python
def test_function_with_edge_cases():
    # Normal case
    assert function(10) == 20

    # Edge cases
    assert function(0) == 0
    assert function(-1) == -2
    assert function(None) is None

    # Boundary cases
    assert function(sys.maxsize) > 0
```

### 3. One Assertion Per Test (Guideline)

```python
# ✅ Good - focused test
def test_returns_correct_type():
    result = function()
    assert isinstance(result, dict)

def test_has_required_keys():
    result = function()
    assert 'key1' in result
    assert 'key2' in result

# ⚠️ Less ideal - multiple unrelated assertions
def test_function():
    result = function()
    assert isinstance(result, dict)
    assert result['key1'] == 'value1'
    assert result['key2'] == 'value2'
```

### 4. Use Descriptive Names

```python
# ✅ Good - describes what is tested
def test_returns_empty_list_when_no_processes_found():
    pass

# ❌ Bad - vague name
def test_processes():
    pass
```

### 5. Mock External Dependencies

```python
# ✅ Good - mocked
@patch('module.requests.get')
def test_api_call(mock_get):
    mock_get.return_value.json.return_value = {'status': 'ok'}
    result = call_api()
    assert result['status'] == 'ok'

# ❌ Bad - makes real API call
def test_api_call():
    result = call_api()  # Actually calls external API
    assert result is not None
```

## 🎓 Learning Resources

### Official Documentation

- [Pytest Documentation](https://docs.pytest.org/)
- [Pytest-Qt Documentation](https://pytest-qt.readthedocs.io/)
- [unittest.mock Guide](https://docs.python.org/3/library/unittest.mock.html)
- [Coverage.py Documentation](https://coverage.readthedocs.io/)

### Testing Best Practices

- [Test-Driven Development](https://en.wikipedia.org/wiki/Test-driven_development)
- [Arrange-Act-Assert Pattern](http://wiki.c2.com/?ArrangeActAssert)
- [Given-When-Then](https://martinfowler.com/bliki/GivenWhenThen.html)

## 📞 Getting Help

### Quick Help

```bash
# Show all pytest options
pytest --help

# Show available markers
pytest --markers

# Show available fixtures
pytest --fixtures
```

### Need More Help?

1. Check `tests/README.md` for detailed documentation
2. Review example tests in `tests/unit/`
3. Open an issue on GitHub

---

## Summary

✨ **Key Commands to Remember**:

```bash
./run_tests.sh              # Run all tests
./run_tests.sh --unit       # Unit tests only
./run_tests.sh --fast       # Fast mode
pytest -v                   # Verbose output
open htmlcov/index.html     # View coverage
```

**Happy Testing!** 🚀

---

*For detailed documentation, see [tests/README.md](tests/README.md)*
