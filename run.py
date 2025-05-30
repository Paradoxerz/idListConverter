#!/usr/bin/env python3
"""
Run script for CSV ID Converter
Automatically activates virtual environment and runs main.py
"""

import subprocess
import sys
import os
from pathlib import Path


def main():
    """Run the CSV ID Converter with virtual environment activated."""
    
    project_dir = Path(__file__).parent.absolute()
    venv_path = project_dir / "venv"
    
    # Check if virtual environment exists
    if not venv_path.exists():
        print("❌ Virtual environment not found!")
        print("Please run setup first:")
        print("   python3 setup.py")
        sys.exit(1)
    
    # Determine the correct activation script and python path
    if os.name == 'nt':  # Windows
        activate_script = venv_path / "Scripts" / "activate"
        python_path = venv_path / "Scripts" / "python"
    else:  # Unix/macOS
        activate_script = venv_path / "bin" / "activate"
        python_path = venv_path / "bin" / "python"
    
    # Run main.py with the virtual environment's Python
    try:
        print("🚀 Running CSV ID Converter...")
        print("=" * 50)
        
        # Use the virtual environment's Python directly
        result = subprocess.run([str(python_path), "main.py"], cwd=project_dir)
        
        print("\n" + "=" * 50)
        if result.returncode == 0:
            print("✅ CSV ID Converter completed successfully!")
        else:
            print("❌ CSV ID Converter finished with errors")
            
    except FileNotFoundError:
        print("❌ Could not find Python in virtual environment")
        print("Please run setup again:")
        print("   python3 setup.py")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n⚠️  Process interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error running CSV ID Converter: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
