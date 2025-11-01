@echo off
echo ========================================
echo  ScreenTime Analyzer Pro
echo  Starting All Services...
echo ========================================
echo.

echo Starting Backend Server...
start cmd /k "cd backend && pip install -r requirements.txt && python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"

timeout /t 5

echo Starting Frontend Server...
start cmd /k "cd frontend && npm install && npm run dev"

echo.
echo ========================================
echo  All services started!
echo  Backend: http://localhost:8000
echo  Frontend: http://localhost:3000
echo  API Docs: http://localhost:8000/docs
echo ========================================
echo.

pause

