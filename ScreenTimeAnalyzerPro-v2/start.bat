@echo off
echo ========================================
echo  ScreenTime Analyzer Pro - Launcher
echo ========================================
echo.

echo [1/3] Checking Python virtual environment...
if not exist "backend\venv" (
    echo Creating Python virtual environment...
    cd backend
    python -m venv venv
    call venv\Scripts\activate
    echo Installing Python dependencies...
    pip install -r requirements.txt
    cd ..
) else (
    echo Virtual environment found!
)

echo.
echo [2/3] Checking Node.js dependencies...
if not exist "frontend\node_modules" (
    echo Installing frontend dependencies...
    cd frontend
    call npm install
    cd ..
) else (
    echo Node modules found!
)

echo.
echo [3/3] Starting application...
echo.
echo Backend: http://127.0.0.1:8000
echo Frontend: http://localhost:3000
echo.
echo Press Ctrl+C to stop
echo.

node scripts/start.js

