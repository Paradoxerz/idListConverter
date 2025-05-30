#!/usr/bin/env python3
"""
CSV ID Converter
Converts CSV files with "ID Subjektu" column to a simple CSV with only "ID" column.
"""

import pandas as pd
import os
from pathlib import Path


def get_merge_ids():
    """
    Get all IDs from CSV files in the merge folder.
    
    Returns:
        set: Set of unique IDs from merge folder CSV files
    """
    merge_folder = Path("merge")
    merge_ids = set()
    
    if not merge_folder.exists():
        return merge_ids
    
    # Find all CSV files in merge folder
    csv_files = list(merge_folder.glob("*.csv"))
    
    if not csv_files:
        return merge_ids
    
    print(f"🔄 Found {len(csv_files)} CSV files in merge folder")
    
    for csv_file in csv_files:
        try:
            df = pd.read_csv(csv_file)
            
            # Look for ID column (could be "ID" or "ID Subjektu")
            id_column = None
            if "ID" in df.columns:
                id_column = "ID"
            elif "ID Subjektu" in df.columns:
                id_column = "ID Subjektu"
            
            if id_column:
                file_ids = set(df[id_column].dropna().astype(str))
                merge_ids.update(file_ids)
                print(f"   📄 {csv_file.name}: {len(file_ids)} IDs")
            else:
                print(f"   ⚠️  {csv_file.name}: No ID column found")
                
        except Exception as e:
            print(f"   ❌ Error reading {csv_file.name}: {e}")
    
    if merge_ids:
        print(f"🔄 Total unique IDs to merge: {len(merge_ids)}")
    
    return merge_ids


def convert_csv_with_merge(input_file, output_file=None, merge_ids=None):
    """
    Convert a CSV file with "ID Subjektu" column to a CSV with only "ID" column,
    and merge with additional IDs if provided.
    
    Args:
        input_file (str): Path to the input CSV file
        output_file (str, optional): Path to the output CSV file
        merge_ids (set, optional): Set of additional IDs to merge
    
    Returns:
        str: Path to the output file
    """
    try:
        # Read the input CSV file
        df = pd.read_csv(input_file)
        
        # Check if "ID Subjektu" column exists
        if "ID Subjektu" not in df.columns:
            raise ValueError(f"Column 'ID Subjektu' not found in {input_file}. Available columns: {list(df.columns)}")
        
        # Extract the ID column and convert to set for deduplication
        input_ids = set(df["ID Subjektu"].dropna().astype(str))
        
        # Merge with additional IDs if provided
        if merge_ids:
            original_count = len(input_ids)
            input_ids.update(merge_ids)
            merged_count = len(input_ids) - original_count
            if merged_count > 0:
                print(f"   🔄 Added {merged_count} new IDs from merge folder")
        
        # Create new dataframe with all unique IDs
        all_ids = sorted(list(input_ids))  # Sort for consistent output
        output_df = pd.DataFrame({"ID": all_ids})
        
        # Generate output file name if not provided
        if output_file is None:
            input_path = Path(input_file)
            output_file = input_path.parent / f"{input_path.stem}_converted{input_path.suffix}"
        
        # Save to CSV
        output_df.to_csv(output_file, index=False)
        
        print(f"✅ Successfully converted {len(output_df)} IDs from '{input_file}' to '{output_file}'")
        return str(output_file)
        
    except FileNotFoundError:
        print(f"❌ Error: File '{input_file}' not found.")
        return None
    except Exception as e:
        print(f"❌ Error converting file: {e}")
        return None


def is_already_converted(file_path):
    """
    Check if a file is already a converted file (ends with _converted.csv or has only ID column).
    
    Args:
        file_path (Path): Path to the CSV file
    
    Returns:
        bool: True if file is already converted, False otherwise
    """
    # Check if filename ends with "_converted"
    if file_path.stem.endswith("_converted"):
        return True
    
    # Check if file has only an "ID" column (and optionally "ID Subjektu")
    try:
        df = pd.read_csv(file_path)
        columns = df.columns.tolist()
        
        # If it only has "ID" column, it's already converted
        if len(columns) == 1 and columns[0] == "ID":
            return True
            
        # If it has "ID Subjektu" column, it's not converted yet
        if "ID Subjektu" in columns:
            return False
            
        # If it doesn't have "ID Subjektu" and has multiple columns, skip it
        return True
        
    except Exception:
        return False


def main():
    """Main function to automatically convert CSV files in the input folder and merge with IDs from merge folder."""
    
    input_folder = Path("input")
    
    # Check if input folder exists
    if not input_folder.exists():
        print(f"❌ Error: Input folder 'input' does not exist.")
        print("Please create an 'input' folder and place your CSV files there.")
        return
    
    # Get merge IDs from merge folder
    merge_ids = get_merge_ids()
    
    # Find all CSV files in input folder
    csv_files = list(input_folder.glob("*.csv"))
    
    if not csv_files:
        print(f"❌ No CSV files found in 'input' folder.")
        return
    
    print(f"🔍 Found {len(csv_files)} CSV files in input folder")
    
    converted_count = 0
    skipped_count = 0
    
    for csv_file in csv_files:
        print(f"\n📄 Processing: {csv_file.name}")
        
        # Check if already converted
        if is_already_converted(csv_file):
            print(f"⏭️  Skipping '{csv_file.name}' - already converted or no 'ID Subjektu' column")
            skipped_count += 1
            continue
        
        # Generate output file path
        output_file = csv_file.parent / f"{csv_file.stem}_converted{csv_file.suffix}"
        
        # Check if converted file already exists
        if output_file.exists():
            print(f"⏭️  Skipping '{csv_file.name}' - converted file already exists: {output_file.name}")
            skipped_count += 1
            continue
        
        # Convert the file with merge
        result = convert_csv_with_merge(str(csv_file), str(output_file), merge_ids)
        if result:
            converted_count += 1
    
    print(f"\n✅ Conversion complete!")
    print(f"   📊 Converted: {converted_count} files")
    print(f"   ⏭️  Skipped: {skipped_count} files")
    if merge_ids:
        print(f"   🔄 Merged IDs from: merge folder")


if __name__ == "__main__":
    main()