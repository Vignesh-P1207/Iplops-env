@echo off
REM Quick start script for IPLOps-Env (Windows)

echo ==========================================
echo IPLOps-Env - Quick Start
echo ==========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo X Python is not installed
    exit /b 1
)

echo √ Python found

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
pip install -q -r requirements.txt

echo.
echo ==========================================
echo Starting IPLOps-Env Server
echo ==========================================
echo.
echo Server will start on http://localhost:8000
echo Press Ctrl+C to stop
echo.

REM Start server
python app/main.py
