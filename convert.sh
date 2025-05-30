#!/bin/bash
# Quick setup and run script for CSV ID Converter

echo "🚀 CSV ID Converter - Quick Start"
echo "================================="

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Setting up for first time..."
    python3 setup.py
    if [ $? -ne 0 ]; then
        echo "❌ Setup failed!"
        exit 1
    fi
    echo ""
fi

echo "▶️  Running CSV ID Converter..."
echo "================================="

# Activate virtual environment and run main.py
source venv/bin/activate && python main.py

echo ""
echo "✅ Done! Check your 'input' folder for converted files."
