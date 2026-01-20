#!/bin/bash

echo "===================================="
echo "EdTech NLP-to-SQL API - Quick Start"
echo "===================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python is not installed"
    echo "Please install Python 3.11 or higher"
    exit 1
fi

echo "Step 1: Creating virtual environment..."
python3 -m venv venv
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to create virtual environment"
    exit 1
fi

echo "Step 2: Activating virtual environment..."
source venv/bin/activate

echo "Step 3: Installing dependencies..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install dependencies"
    exit 1
fi

echo "Step 4: Checking for .env file..."
if [ ! -f .env ]; then
    echo "WARNING: .env file not found!"
    echo "Creating .env from .env.example..."
    cp .env.example .env
    echo ""
    echo "IMPORTANT: Edit .env and add your OpenAI API key before running the app!"
    echo ""
fi

echo "Step 5: Initializing database..."
python -m app.seed
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to initialize database"
    exit 1
fi

echo ""
echo "===================================="
echo "Setup Complete!"
echo "===================================="
echo ""
echo "To start the application, run:"
echo "  uvicorn app.main:app --reload"
echo ""
echo "Then visit:"
echo "  - API: http://localhost:8000"
echo "  - Docs: http://localhost:8000/docs"
echo ""
echo "To run tests:"
echo "  pytest"
echo ""
