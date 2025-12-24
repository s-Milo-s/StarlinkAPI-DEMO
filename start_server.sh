#!/bin/bash

echo "🚀 Starting Starlink Enterprise Dashboard API Mock Server"
echo "=================================================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is required but not installed."
    exit 1
fi

# Install dependencies
echo "📦 Installing dependencies..."
pip3 install -r requirements.txt

# Start the server
echo "🌟 Starting FastAPI server on http://localhost:8000"
echo "📚 API Documentation: http://localhost:8000/docs"
echo "🔍 Alternative Docs: http://localhost:8000/redoc"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python3 main.py
