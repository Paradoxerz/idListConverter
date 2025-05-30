# CSV ID Converter

Python script to automatically convert CSV files with "ID Subjektu" column into simple CSV files with only "ID" column, with optional ID merging functionality.

## Features

- Automatically processes all CSV files in the `input` folder
- Converts files containing "ID Subjektu" column to CSV with just "ID" column
- Merge functionality - automatically adds IDs from `merge` folder to converted files
- Automatic output file naming with "\_converted" suffix
- Smart duplicate detection - skips already converted files and deduplicates IDs
- Error handling and validation

## Quick Start

### Option 1: Automated Setup (Recommended)

```bash
# One-time setup (creates virtual environment and installs dependencies)
python3 setup.py

# Run the converter
python3 run.py
```

### Option 2: Super Quick (Shell Script)

```bash
# Automatically sets up and runs (first time setup + run in one command)
./convert.sh
```

### Option 3: Manual Setup

```bash
# Manual virtual environment setup
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run manually
python3 main.py
```

## Installation

The setup script (`python3 setup.py`) will automatically:

- Create a virtual environment in `venv/`
- Install required dependencies from `requirements.txt`
- Create necessary folders (`input/` and `merge/`)

## Usage

### Running the Converter

**Easiest way:**

```bash
./convert.sh
```

**Or using the Python run script:**

```bash
python3 run.py
```

**Or manually with virtual environment:**

```bash
source venv/bin/activate
python3 main.py
```

The script will:

1. Look for CSV files in the `input` folder
2. Check for CSV files in the `merge` folder (optional)
3. Convert each input file and merge with IDs from merge folder
4. Skip files that are already converted or don't have the required column
5. Create new files with "\_converted" suffix containing all unique IDs

## Merge Functionality

Create a `merge` folder and add CSV files containing IDs you want to merge with all converted files:

```
project/
├── setup.py         # Run this first: python3 setup.py
├── run.py          # Run converter with venv: python3 run.py
├── convert.sh      # One-command setup+run: ./convert.sh
├── main.py         # Main converter script
├── requirements.txt
├── input/          # Put files to convert here
│   └── data.csv
├── merge/          # Put additional IDs here (optional)
│   ├── extra_ids.csv
│   └── more_ids.csv
└── venv/           # Virtual environment (created by setup.py)
```

The script will:

- Extract IDs from both input files (with "ID Subjektu" column) and merge files (with "ID" or "ID Subjektu" column)
- Automatically deduplicate IDs
- Sort the final output alphabetically

### Example

**Input CSV (input/data.csv):**

```csv
"Name","ID Subjektu","Date"
"Person 1","SUBJ-001","2025-05-30"
"Person 2","SUBJ-002","2025-05-30"
```

**Merge CSV (merge/additional.csv):**

```csv
ID
EXTRA-001
EXTRA-002
SUBJ-001
```

**Output CSV (input/data_converted.csv):**

```csv
ID
EXTRA-001
EXTRA-002
SUBJ-001
SUBJ-002
```

## Smart Duplicate Detection

The script automatically skips:

- Files already ending with "\_converted.csv"
- Files that only have an "ID" column (already converted)
- Files without "ID Subjektu" column
- Cases where the converted file already exists

## Requirements

- Python 3.6+
- pandas (automatically installed by setup.py)

## Setup Files

- **`setup.py`** - One-time setup script that creates virtual environment and installs dependencies
- **`run.py`** - Convenient runner that activates virtual environment and runs main.py
- **`convert.sh`** - Shell script for one-command setup and execution
- **`main.py`** - Core converter script (can be run manually with activated venv)

## Error Handling

The script will:

- Check if the input folder exists
- Verify that files have "ID Subjektu" column
- Remove any empty/NaN values from the ID column
- Provide clear status messages for each file processed
