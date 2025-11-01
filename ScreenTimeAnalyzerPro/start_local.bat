@echo off
echo ========================================
echo  ScreenTime Analyzer Pro - Windows
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org/
    pause
    exit /b 1
)

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Node.js is not installed or not in PATH
    echo Please install Node.js 16+ from https://nodejs.org/
    pause
    exit /b 1
)

echo [1/4] Installing backend dependencies...
cd backend
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

call venv\Scripts\activate.bat
pip install -r requirements.txt >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Failed to install backend dependencies
    pause
    exit /b 1
)

echo [2/4] Installing frontend dependencies...
cd ..\frontend
if not exist "node_modules" (
    echo Installing npm packages...
    call npm install
    if errorlevel 1 (
        echo [ERROR] Failed to install frontend dependencies
        pause
        exit /b 1
    )
)

echo [3/4] Starting backend server...
cd ..\backend
start "ScreenTime Backend" cmd /k "venv\Scripts\activate.bat && python main.py"

REM Wait for backend to start
timeout /t 5 /nobreak >nul

echo [4/4] Starting frontend server...
cd ..\frontend
start "ScreenTime Frontend" cmd /k "npm run dev"

echo.
echo ========================================
echo  ScreenTime Analyzer Pro is starting!
echo ========================================
echo.
echo Backend:  http://127.0.0.1:8000
echo Frontend: http://localhost:3000
echo API Docs: http://127.0.0.1:8000/docs
echo.
echo Press any key to open the dashboard...
pause >nul

REM Open browser
start http://localhost:3000

echo.
echo To stop the servers, close the terminal windows.
echo.
pause

