#!/usr/bin/env python3
"""
Setup script for CSV ID Converter
Creates virtual environment and installs dependencies
"""

import subprocess
import sys
import os
from pathlib import Path


def run_command(command, description):
    """Run a shell command and handle errors."""
    print(f"🔧 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        if result.stdout:
            print(f"   ✅ {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"   ❌ Error: {e}")
        if e.stderr:
            print(f"   ❌ Details: {e.stderr.strip()}")
        return False


def check_python_version():
    """Check if Python version is 3.6 or higher."""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 6):
        print(f"❌ Python 3.6+ required. Current version: {version.major}.{version.minor}")
        return False
    print(f"✅ Python version: {version.major}.{version.minor}.{version.micro}")
    return True


def setup_environment():
    """Set up the virtual environment and install dependencies."""
    
    print("🚀 CSV ID Converter Setup")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        return False
    
    # Get current directory
    project_dir = Path(__file__).parent.absolute()
    venv_path = project_dir / "venv"
    
    print(f"📁 Project directory: {project_dir}")
    
    # Create virtual environment if it doesn't exist
    if not venv_path.exists():
        if not run_command("python3 -m venv venv", "Creating virtual environment"):
            return False
    else:
        print("✅ Virtual environment already exists")
    
    # Determine the correct activation script and pip path
    if os.name == 'nt':  # Windows
        activate_script = venv_path / "Scripts" / "activate"
        pip_path = venv_path / "Scripts" / "pip"
    else:  # Unix/macOS
        activate_script = venv_path / "bin" / "activate"
        pip_path = venv_path / "bin" / "pip"
    
    # Install requirements
    if (project_dir / "requirements.txt").exists():
        install_cmd = f"source {activate_script} && {pip_path} install -r requirements.txt"
        if not run_command(install_cmd, "Installing requirements"):
            return False
    else:
        print("⚠️  No requirements.txt found, skipping dependency installation")
    
    # Create necessary directories
    input_dir = project_dir / "input"
    merge_dir = project_dir / "merge"
    
    if not input_dir.exists():
        input_dir.mkdir()
        print("📁 Created 'input' directory")
    else:
        print("✅ 'input' directory already exists")
    
    if not merge_dir.exists():
        merge_dir.mkdir()
        print("📁 Created 'merge' directory")
    else:
        print("✅ 'merge' directory already exists")
    
    print("\n" + "=" * 50)
    print("🎉 Setup complete!")
    print("\nTo use the CSV ID Converter:")
    print("1. Activate the virtual environment:")
    print(f"   source {activate_script}")
    print("2. Place CSV files in the 'input' folder")
    print("3. (Optional) Place merge CSV files in the 'merge' folder")
    print("4. Run the converter:")
    print("   python3 main.py")
    print("\nOr use the run script:")
    print("   python3 run.py")
    
    return True


def main():
    """Main setup function."""
    try:
        success = setup_environment()
        if not success:
            print("\n❌ Setup failed!")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n⚠️  Setup interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error during setup: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
