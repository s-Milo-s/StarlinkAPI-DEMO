#!/bin/bash
"""
Development startup script
"""
# Set environment variables for development
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# Run the development server with auto-reload
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
