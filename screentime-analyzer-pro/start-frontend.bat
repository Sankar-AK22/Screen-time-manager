@echo off
echo ========================================
echo  ScreenTime Analyzer Pro - Frontend
echo ========================================
echo.

cd frontend

echo Installing dependencies...
call npm install

echo.
echo Starting React development server...
call npm run dev

pause

