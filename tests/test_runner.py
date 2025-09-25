#!/usr/bin/env python3
"""
Test runner script for Furby Therapist.
Provides various ways to run tests with proper configuration.
"""

import unittest
import sys
import os
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))


def run_all_tests():
    """Run all tests with verbose output."""
    loader = unittest.TestLoader()
    start_dir = 'tests'
    suite = loader.discover(start_dir, pattern='test_*.py')
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


def run_specific_test(test_module):
    """Run a specific test module."""
    loader = unittest.TestLoader()
    
    # Handle both old format (test_library) and new format (core.test_library)
    if '.' not in test_module:
        # Try to find the test in the new structure
        possible_locations = [
            f'tests.core.{test_module}',
            f'tests.cli.{test_module}', 
            f'tests.models.{test_module}',
            f'tests.features.{test_module}',
            f'tests.integration.{test_module}',
            f'tests.{test_module}'  # fallback to old location
        ]
        
        for location in possible_locations:
            try:
                suite = loader.loadTestsFromName(location)
                if suite.countTestCases() > 0:
                    break
            except (ImportError, AttributeError):
                continue
        else:
            # If not found, use the original format
            suite = loader.loadTestsFromName(f'tests.{test_module}')
    else:
        # Already has package path
        suite = loader.loadTestsFromName(f'tests.{test_module}')
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


def run_integration_tests():
    """Run only integration tests."""
    loader = unittest.TestLoader()
    suite = loader.discover('tests/integration', pattern='test_*.py')
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


def run_unit_tests():
    """Run unit tests (core, cli, models, features - excluding integration tests)."""
    loader = unittest.TestLoader()
    
    # Load tests from unit test directories
    unit_dirs = ['tests/core', 'tests/cli', 'tests/models', 'tests/features']
    suite = unittest.TestSuite()
    
    for test_dir in unit_dirs:
        try:
            dir_suite = loader.discover(test_dir, pattern='test_*.py')
            suite.addTest(dir_suite)
        except ImportError:
            continue  # Skip if directory doesn't exist or has no tests
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Run Furby Therapist tests')
    parser.add_argument('--module', '-m', help='Run specific test module (e.g., test_library)')
    parser.add_argument('--integration', '-i', action='store_true', help='Run only integration tests')
    parser.add_argument('--unit', '-u', action='store_true', help='Run only unit tests')
    
    args = parser.parse_args()
    
    if args.module:
        success = run_specific_test(args.module)
    elif args.integration:
        success = run_integration_tests()
    elif args.unit:
        success = run_unit_tests()
    else:
        success = run_all_tests()
    
    sys.exit(0 if success else 1)