#!/bin/bash

echo "========================================"
echo " ScreenTime Analyzer Pro - Mac/Linux"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python 3 is not installed"
    echo "Please install Python 3.8+ from https://www.python.org/"
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "[ERROR] Node.js is not installed"
    echo "Please install Node.js 16+ from https://nodejs.org/"
    exit 1
fi

echo "[1/4] Installing backend dependencies..."
cd backend

if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

source venv/bin/activate
pip install -r requirements.txt > /dev/null 2>&1

if [ $? -ne 0 ]; then
    echo "[ERROR] Failed to install backend dependencies"
    exit 1
fi

echo "[2/4] Installing frontend dependencies..."
cd ../frontend

if [ ! -d "node_modules" ]; then
    echo "Installing npm packages..."
    npm install
    
    if [ $? -ne 0 ]; then
        echo "[ERROR] Failed to install frontend dependencies"
        exit 1
    fi
fi

echo "[3/4] Starting backend server..."
cd ../backend

# Start backend in background
source venv/bin/activate
python main.py > backend.log 2>&1 &
BACKEND_PID=$!
echo "Backend PID: $BACKEND_PID"

# Wait for backend to start
sleep 5

echo "[4/4] Starting frontend server..."
cd ../frontend

# Start frontend in background
npm run dev > frontend.log 2>&1 &
FRONTEND_PID=$!
echo "Frontend PID: $FRONTEND_PID"

# Wait for frontend to start
sleep 3

echo ""
echo "========================================"
echo " ScreenTime Analyzer Pro is running!"
echo "========================================"
echo ""
echo "Backend:  http://127.0.0.1:8000"
echo "Frontend: http://localhost:3000"
echo "API Docs: http://127.0.0.1:8000/docs"
echo ""
echo "Backend PID:  $BACKEND_PID"
echo "Frontend PID: $FRONTEND_PID"
echo ""
echo "To stop the servers, run:"
echo "  kill $BACKEND_PID $FRONTEND_PID"
echo ""

# Save PIDs to file for easy cleanup
echo "$BACKEND_PID" > ../backend.pid
echo "$FRONTEND_PID" > ../frontend.pid

# Open browser (macOS)
if [[ "$OSTYPE" == "darwin"* ]]; then
    sleep 2
    open http://localhost:3000
fi

# Open browser (Linux with xdg-open)
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    if command -v xdg-open &> /dev/null; then
        sleep 2
        xdg-open http://localhost:3000
    fi
fi

echo "Press Ctrl+C to stop all servers..."

# Wait for Ctrl+C
trap "echo ''; echo 'Stopping servers...'; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; rm -f ../backend.pid ../frontend.pid; echo 'Servers stopped.'; exit 0" INT

# Keep script running
wait

