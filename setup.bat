@echo off
echo ====================================
echo EdTech NLP-to-SQL API - Quick Start
echo ====================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.11 or higher
    pause
    exit /b 1
)

echo Step 1: Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo ERROR: Failed to create virtual environment
    pause
    exit /b 1
)

echo Step 2: Activating virtual environment...
call venv\Scripts\activate

echo Step 3: Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo Step 4: Checking for .env file...
if not exist .env (
    echo WARNING: .env file not found!
    echo Please create a .env file with your Gemini API key
    echo You can copy .env.example and update it
    echo.
    echo Creating .env from .env.example...
    copy .env.example .env
    echo.
    echo IMPORTANT: Edit .env and add your Gemini API key before running the app!
    echo.
)

echo Step 5: Initializing database...
python -m app.seed
if errorlevel 1 (
    echo ERROR: Failed to initialize database
    pause
    exit /b 1
)

echo.
echo ====================================
echo Setup Complete!
echo ====================================
echo.
echo To start the application, run:
echo   uvicorn app.main:app --reload
echo.
echo Then visit:
echo   - API: http://localhost:8000
echo   - Docs: http://localhost:8000/docs
echo.
echo To run tests:
echo   pytest
echo.
pause
