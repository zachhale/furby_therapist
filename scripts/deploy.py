#!/usr/bin/env python3
"""
Deployment script for Furby Therapist.

This script handles building and deploying the Furby Therapist package
without requiring external build tools to be pre-installed.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def run_command(cmd, description=""):
    """Run a command and handle errors."""
    if description:
        print(f"→ {description}")
    
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        if result.stdout:
            print(result.stdout.strip())
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        if e.stderr:
            print(f"Error output: {e.stderr.strip()}")
        return False

def check_python_version():
    """Check if Python version is compatible."""
    if sys.version_info < (3, 8):
        print("Error: Python 3.8 or higher is required")
        return False
    print(f"✓ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    return True

def install_build_tools():
    """Install build tools if not available."""
    print("Checking build tools...")
    
    # Check if build tools are available
    try:
        import build
        import twine
        print("✓ Build tools already available")
        return True
    except ImportError:
        pass
    
    print("Installing build tools...")
    
    # Try different installation methods
    methods = [
        "pip install build twine setuptools wheel",
        "python3 -m pip install build twine setuptools wheel",
        "python3 -m pip install --user build twine setuptools wheel"
    ]
    
    for method in methods:
        print(f"Trying: {method}")
        if run_command(method):
            print("✓ Build tools installed successfully")
            return True
    
    print("Error: Could not install build tools")
    print("Please install manually or use a virtual environment:")
    print("  python3 -m venv venv")
    print("  source venv/bin/activate")
    print("  pip install build twine setuptools wheel")
    return False

def clean_build():
    """Clean previous build artifacts."""
    print("Cleaning build artifacts...")
    
    dirs_to_remove = ["build", "dist", "*.egg-info"]
    for pattern in dirs_to_remove:
        for path in Path(".").glob(pattern):
            if path.is_dir():
                shutil.rmtree(path)
                print(f"Removed {path}")
    
    print("✓ Build artifacts cleaned")

def build_package():
    """Build the package."""
    print("Building package...")
    
    if not run_command("python3 -m build", "Building distributions"):
        return False
    
    print("✓ Package built successfully")
    return True

def check_package():
    """Check the built package."""
    print("Checking package...")
    
    if not Path("dist").exists():
        print("Error: No dist directory found")
        return False
    
    dist_files = list(Path("dist").glob("*"))
    if not dist_files:
        print("Error: No distribution files found")
        return False
    
    print(f"Found {len(dist_files)} distribution files:")
    for file in dist_files:
        print(f"  - {file.name}")
    
    if not run_command("python3 -m twine check dist/*", "Checking package integrity"):
        return False
    
    print("✓ Package check passed")
    return True

def test_installation():
    """Test the package installation."""
    print("Testing installation...")
    
    # Find the wheel file
    wheel_files = list(Path("dist").glob("*.whl"))
    if not wheel_files:
        print("Error: No wheel file found for testing")
        return False
    
    wheel_file = wheel_files[0]
    
    # Test installation in a temporary environment
    test_commands = [
        f"pip install {wheel_file}",
        "furby_therapist --query 'Installation test'",
        "python3 -c 'from furby_therapist import process_single_query; print(\"Library import successful\")'",
        "pip uninstall -y furby-therapist"
    ]
    
    print("Running installation test...")
    for cmd in test_commands:
        if not run_command(cmd):
            print(f"Installation test failed at: {cmd}")
            return False
    
    print("✓ Installation test passed")
    return True

def main():
    """Main deployment function."""
    print("Furby Therapist Deployment Script")
    print("=" * 40)
    
    # Check requirements
    if not check_python_version():
        sys.exit(1)
    
    # Change to project root
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    os.chdir(project_root)
    print(f"Working directory: {project_root}")
    
    # Install build tools
    if not install_build_tools():
        sys.exit(1)
    
    # Clean previous builds
    clean_build()
    
    # Build package
    if not build_package():
        sys.exit(1)
    
    # Check package
    if not check_package():
        sys.exit(1)
    
    # Test installation (optional)
    if "--test" in sys.argv:
        if not test_installation():
            sys.exit(1)
    
    print("\n" + "=" * 40)
    print("✓ Deployment completed successfully!")
    print("\nNext steps:")
    print("  - Review files in dist/ directory")
    print("  - Test installation: python3 scripts/deploy.py --test")
    print("  - Upload to Test PyPI: python3 -m twine upload --repository testpypi dist/*")
    print("  - Upload to PyPI: python3 -m twine upload dist/*")

if __name__ == "__main__":
    main()