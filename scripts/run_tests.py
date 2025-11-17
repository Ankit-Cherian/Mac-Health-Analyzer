#!/usr/bin/env python3
"""
Simple Python Test Runner for Mac Health Pulse

Provides a cross-platform way to run tests with sensible defaults.
"""

import sys
import subprocess
import argparse
from pathlib import Path


def main():
    """Main entry point for test runner."""
    parser = argparse.ArgumentParser(
        description='Run tests for Mac Health Pulse',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  python run_tests.py                  # Run all tests
  python run_tests.py --unit           # Run only unit tests
  python run_tests.py --fast           # Fast mode (no coverage)
  python run_tests.py --verbose        # Verbose output
        '''
    )

    parser.add_argument('-u', '--unit', action='store_true',
                       help='Run only unit tests')
    parser.add_argument('-i', '--integration', action='store_true',
                       help='Run only integration tests')
    parser.add_argument('-v', '--verbose', action='store_true',
                       help='Verbose output')
    parser.add_argument('--no-cov', '--no-coverage', action='store_true',
                       help='Disable coverage reporting')
    parser.add_argument('-f', '--fast', action='store_true',
                       help='Fast mode (no coverage, stop on first failure)')
    parser.add_argument('--smoke', action='store_true',
                       help='Run only smoke tests')
    parser.add_argument('--html', action='store_true',
                       help='Generate HTML test report')

    args = parser.parse_args()

    # Build pytest command
    cmd = ['pytest']

    # Add verbosity
    if args.verbose:
        cmd.append('-vv')
    else:
        cmd.append('-v')

    # Add markers
    if args.unit:
        cmd.extend(['-m', 'unit'])
    elif args.integration:
        cmd.extend(['-m', 'integration'])
    elif args.smoke:
        cmd.extend(['-m', 'smoke'])

    # Add coverage
    if not args.no_cov and not args.fast:
        cmd.extend([
            '--cov=src',
            '--cov-report=html',
            '--cov-report=term-missing',
            '--cov-report=xml'
        ])

    # Add HTML report
    if args.html:
        cmd.extend(['--html=test-reports/report.html', '--self-contained-html'])

    # Fast mode
    if args.fast:
        cmd.append('-x')  # Stop on first failure

    # Print configuration
    print("=" * 60)
    print("Mac Health Pulse - Test Suite")
    print("=" * 60)
    print(f"\nRunning: {' '.join(cmd)}\n")

    # Run tests
    try:
        result = subprocess.run(cmd, check=False)
        if result.returncode == 0:
            print("\n" + "=" * 60)
            print("✓ All tests passed!")
            print("=" * 60)
            if not args.no_cov and not args.fast:
                print("\nCoverage report: htmlcov/index.html")
        else:
            print("\n" + "=" * 60)
            print("✗ Tests failed!")
            print("=" * 60)
            sys.exit(1)
    except FileNotFoundError:
        print("Error: pytest not found. Please install test dependencies:")
        print("  pip install -r requirements-test.txt")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\nTests interrupted by user")
        sys.exit(1)


if __name__ == '__main__':
    main()
