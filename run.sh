#!/bin/bash
# Quick start script for IPLOps-Env

echo "=========================================="
echo "IPLOps-Env - Quick Start"
echo "=========================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed"
    exit 1
fi

echo "✅ Python 3 found"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -q -r requirements.txt

echo ""
echo "=========================================="
echo "Starting IPLOps-Env Server"
echo "=========================================="
echo ""
echo "Server will start on http://localhost:8000"
echo "Press Ctrl+C to stop"
echo ""

# Start server
python app/main.py
