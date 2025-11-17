#!/bin/bash

# Test Runner Script for Mac Health Pulse
# Comprehensive test execution with multiple options

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Print header
echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  Mac Health Pulse - Test Suite${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: Python 3 is not installed${NC}"
    exit 1
fi

# Check if virtual environment exists, create if not
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}Creating virtual environment...${NC}"
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install/upgrade testing dependencies
echo -e "${YELLOW}Installing test dependencies...${NC}"
pip install -q --upgrade pip
pip install -q -r requirements.txt
pip install -q -r requirements-test.txt

# Default test command
TEST_CMD="pytest"

# Parse command line arguments
MODE="all"
VERBOSE=false
COVERAGE=true
MARKERS=""

while [[ $# -gt 0 ]]; do
    case $1 in
        -u|--unit)
            MODE="unit"
            MARKERS="-m unit"
            shift
            ;;
        -i|--integration)
            MODE="integration"
            MARKERS="-m integration"
            shift
            ;;
        -v|--verbose)
            VERBOSE=true
            shift
            ;;
        --no-cov|--no-coverage)
            COVERAGE=false
            shift
            ;;
        -f|--fast)
            COVERAGE=false
            TEST_CMD="pytest -x"  # Stop on first failure
            shift
            ;;
        --smoke)
            MODE="smoke"
            MARKERS="-m smoke"
            shift
            ;;
        -h|--help)
            echo "Usage: $0 [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  -u, --unit           Run only unit tests"
            echo "  -i, --integration    Run only integration tests"
            echo "  -v, --verbose        Verbose output"
            echo "  --no-cov             Disable coverage reporting"
            echo "  -f, --fast           Fast mode (no coverage, stop on first failure)"
            echo "  --smoke              Run only smoke tests"
            echo "  -h, --help           Show this help message"
            echo ""
            echo "Examples:"
            echo "  $0                   # Run all tests with coverage"
            echo "  $0 -u                # Run only unit tests"
            echo "  $0 -v --no-cov       # Verbose mode without coverage"
            echo "  $0 -f                # Fast mode"
            exit 0
            ;;
        *)
            echo -e "${RED}Unknown option: $1${NC}"
            echo "Use -h or --help for usage information"
            exit 1
            ;;
    esac
done

# Build test command
if [ "$VERBOSE" = true ]; then
    TEST_CMD="$TEST_CMD -vv"
fi

if [ "$COVERAGE" = true ]; then
    TEST_CMD="$TEST_CMD --cov=. --cov-report=html --cov-report=term-missing"
fi

# Add markers if specified
if [ -n "$MARKERS" ]; then
    TEST_CMD="$TEST_CMD $MARKERS"
fi

# Print test configuration
echo -e "${BLUE}Test Configuration:${NC}"
echo -e "  Mode: ${GREEN}$MODE${NC}"
echo -e "  Coverage: ${GREEN}$([ "$COVERAGE" = true ] && echo "Enabled" || echo "Disabled")${NC}"
echo -e "  Verbose: ${GREEN}$([ "$VERBOSE" = true ] && echo "Yes" || echo "No")${NC}"
echo ""

# Run tests
echo -e "${YELLOW}Running tests...${NC}"
echo -e "${BLUE}Command: $TEST_CMD${NC}"
echo ""

if eval $TEST_CMD; then
    echo ""
    echo -e "${GREEN}========================================${NC}"
    echo -e "${GREEN}  ✓ All tests passed!${NC}"
    echo -e "${GREEN}========================================${NC}"

    if [ "$COVERAGE" = true ]; then
        echo ""
        echo -e "${BLUE}Coverage report generated in: htmlcov/index.html${NC}"
        echo -e "${BLUE}To view: open htmlcov/index.html${NC}"
    fi

    exit 0
else
    echo ""
    echo -e "${RED}========================================${NC}"
    echo -e "${RED}  ✗ Tests failed!${NC}"
    echo -e "${RED}========================================${NC}"
    exit 1
fi
