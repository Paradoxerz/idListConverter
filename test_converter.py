#!/usr/bin/env python3
"""
Test script for CSV ID Converter
Verifies all functionality works correctly
"""

import subprocess
import sys
import os
import tempfile
import shutil
from pathlib import Path


def create_test_files():
    """Create test input and merge files."""
    print("📄 Creating test files...")
    
    # Test input file
    test_input = '''"Name","ID Subjektu","Date","Type"
"Test Org 1","TEST-001","2025-05-30","Organization"
"Test Org 2","TEST-002","2025-05-30","Organization"
"Duplicate ID","MERGE-001","2025-05-30","Organization"'''
    
    with open("input/test_input.csv", "w") as f:
        f.write(test_input)
    
    # Test merge file
    test_merge = '''ID
MERGE-001
MERGE-002
MERGE-003'''
    
    with open("merge/test_merge.csv", "w") as f:
        f.write(test_merge)
    
    print("   ✅ Test files created")


def run_converter():
    """Run the converter and capture output."""
    print("🚀 Running converter...")
    
    result = subprocess.run(
        ["python3", "main.py"], 
        capture_output=True, 
        text=True,
        cwd=Path(__file__).parent
    )
    
    print("   ✅ Converter executed")
    return result


def verify_output():
    """Verify the output file is correct."""
    print("🔍 Verifying output...")
    
    output_file = "input/test_input_converted.csv"
    
    if not os.path.exists(output_file):
        print("   ❌ Output file not created")
        return False
    
    with open(output_file, "r") as f:
        content = f.read()
    
    # Check for expected IDs
    expected_ids = ["TEST-001", "TEST-002", "MERGE-001", "MERGE-002", "MERGE-003"]
    
    for id_val in expected_ids:
        if id_val not in content:
            print(f"   ❌ Missing ID: {id_val}")
            return False
    
    # Count occurrences of MERGE-001 (should be only 1, deduplicated)
    merge_001_count = content.count("MERGE-001")
    if merge_001_count != 1:
        print(f"   ❌ ID MERGE-001 appears {merge_001_count} times (should be 1)")
        return False
    
    lines = content.strip().split('\n')
    total_ids = len(lines) - 1  # Subtract header
    
    print(f"   ✅ Output verified: {total_ids} unique IDs")
    return True


def cleanup_test_files():
    """Remove test files."""
    print("🧹 Cleaning up test files...")
    
    test_files = [
        "input/test_input.csv",
        "input/test_input_converted.csv",
        "merge/test_merge.csv"
    ]
    
    for file_path in test_files:
        if os.path.exists(file_path):
            os.remove(file_path)
    
    print("   ✅ Test files cleaned up")


def main():
    """Run complete test suite."""
    print("🧪 CSV ID Converter - Test Suite")
    print("=" * 50)
    
    try:
        # Ensure we're in the right directory
        os.chdir(Path(__file__).parent)
        
        # Check if virtual environment exists
        if not os.path.exists("venv"):
            print("❌ Virtual environment not found. Run setup.py first!")
            return False
        
        # Create test files
        create_test_files()
        
        # Run converter
        result = run_converter()
        
        if result.returncode != 0:
            print(f"❌ Converter failed with return code {result.returncode}")
            print(f"Error: {result.stderr}")
            return False
        
        # Verify output
        if not verify_output():
            return False
        
        print("\n" + "=" * 50)
        print("🎉 All tests passed!")
        print("✅ Setup works correctly")
        print("✅ Conversion works correctly") 
        print("✅ Merge functionality works correctly")
        print("✅ Deduplication works correctly")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        return False
        
    finally:
        cleanup_test_files()


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
