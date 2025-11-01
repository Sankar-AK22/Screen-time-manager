@echo off
echo ========================================
echo  ScreenTime Analyzer Pro - Backend
echo ========================================
echo.

cd backend

echo Installing dependencies...
pip install -r requirements.txt

echo.
echo Starting FastAPI server...
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

pause

