# 🚀 Installation Guide - ScreenTime Analyzer Pro

Complete step-by-step installation instructions for Windows, macOS, and Linux.

---

## 📋 Prerequisites

### All Platforms
- **Python 3.8 or higher**
- **Node.js 16 or higher**
- **npm** (comes with Node.js)

### Check Your Versions
```bash
python --version  # or python3 --version
node --version
npm --version
```

---

## 🪟 Windows Installation

### Step 1: Install Python
1. Download Python from https://www.python.org/downloads/
2. **Important**: Check "Add Python to PATH" during installation
3. Verify: `python --version`

### Step 2: Install Node.js
1. Download Node.js from https://nodejs.org/
2. Run the installer (use default settings)
3. Verify: `node --version`

### Step 3: Install Windows-Specific Dependencies
```bash
pip install pywin32
```

### Step 4: Clone/Download Project
```bash
cd C:\Users\YourName\Documents
# If you have the project folder, navigate to it
cd ScreenTimeAnalyzerPro
```

### Step 5: Run the Application
```bash
start_local.bat
```

This will:
- Create a Python virtual environment
- Install all backend dependencies
- Install all frontend dependencies
- Start both servers
- Open your browser automatically

### Manual Start (Windows)
If the batch file doesn't work:

**Terminal 1 - Backend:**
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm install
npm run dev
```

---

## 🍎 macOS Installation

### Step 1: Install Homebrew (if not installed)
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### Step 2: Install Python
```bash
brew install python@3.11
```

### Step 3: Install Node.js
```bash
brew install node
```

### Step 4: Install macOS-Specific Dependencies
```bash
pip3 install pyobjc-framework-Cocoa pyobjc-framework-Quartz
```

### Step 5: Grant Accessibility Permissions
1. Open **System Preferences** → **Security & Privacy** → **Privacy**
2. Select **Accessibility** from the left sidebar
3. Click the lock icon to make changes
4. Add **Terminal** (or your terminal app) to the list
5. Check the box next to it

### Step 6: Clone/Download Project
```bash
cd ~/Documents
# If you have the project folder, navigate to it
cd ScreenTimeAnalyzerPro
```

### Step 7: Run the Application
```bash
chmod +x start_local.sh
./start_local.sh
```

### Manual Start (macOS)
If the shell script doesn't work:

**Terminal 1 - Backend:**
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm install
npm run dev
```

---

## 🐧 Linux Installation

### Step 1: Install Python
**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
```

**Fedora:**
```bash
sudo dnf install python3 python3-pip
```

**Arch:**
```bash
sudo pacman -S python python-pip
```

### Step 2: Install Node.js
**Ubuntu/Debian:**
```bash
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs
```

**Fedora:**
```bash
sudo dnf install nodejs npm
```

**Arch:**
```bash
sudo pacman -S nodejs npm
```

### Step 3: Install Linux Dependencies
```bash
# For X11-based systems
sudo apt install python3-xlib  # Ubuntu/Debian
sudo dnf install python3-xlib  # Fedora
sudo pacman -S python-xlib     # Arch
```

### Step 4: Clone/Download Project
```bash
cd ~/Documents
# If you have the project folder, navigate to it
cd ScreenTimeAnalyzerPro
```

### Step 5: Run the Application
```bash
chmod +x start_local.sh
./start_local.sh
```

### Manual Start (Linux)
If the shell script doesn't work:

**Terminal 1 - Backend:**
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm install
npm run dev
```

---

## 🔍 Verification

After starting the application, verify everything is working:

### 1. Check Backend
Open: http://127.0.0.1:8000

You should see:
```json
{
  "app": "ScreenTime Analyzer Pro",
  "version": "1.0.0",
  "status": "running",
  "tracking": true
}
```

### 2. Check API Documentation
Open: http://127.0.0.1:8000/docs

You should see the Swagger UI with all API endpoints.

### 3. Check Frontend
Open: http://localhost:3000

You should see the dashboard with:
- Header with "ScreenTime Analyzer Pro" logo
- Connection status (green dot = connected)
- Live Now card
- Stats cards (Total Screen Time, Productive Time, etc.)
- Top Apps chart

### 4. Test Real-Time Tracking
1. Switch to a different application (e.g., browser, text editor)
2. Wait 5-10 seconds
3. Check the "Live Now" card - it should update with the current app
4. Check the "Top Apps" chart - it should update after you switch apps

---

## 🐛 Troubleshooting

### Backend Issues

#### "Python not found"
- **Windows**: Reinstall Python and check "Add to PATH"
- **macOS/Linux**: Use `python3` instead of `python`

#### "Module not found" errors
```bash
cd backend
pip install -r requirements.txt --force-reinstall
```

#### "Port 8000 already in use"
Find and kill the process:
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# macOS/Linux
lsof -ti:8000 | xargs kill -9
```

#### "Database is locked"
```bash
cd backend
rm screentime.db
# Restart the backend
```

### Frontend Issues

#### "npm not found"
Reinstall Node.js from https://nodejs.org/

#### "Port 3000 already in use"
```bash
# Windows
netstat -ano | findstr :3000
taskkill /PID <PID> /F

# macOS/Linux
lsof -ti:3000 | xargs kill -9
```

#### "Module not found" errors
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### Tracking Issues

#### Windows: "Access denied" errors
Run terminal as Administrator

#### macOS: Tracking not working
Grant Accessibility permissions (see Step 5 in macOS installation)

#### Linux: Window detection not working
The Linux implementation uses psutil fallback which may have limited accuracy. This is a known limitation.

---

## 🔄 Updating

To update to a new version:

```bash
# Update backend dependencies
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt --upgrade

# Update frontend dependencies
cd ../frontend
npm install
```

---

## 🛑 Stopping the Application

### Using Start Scripts
Press `Ctrl+C` in the terminal where you ran the start script.

### Manual Stop
**Windows:**
Close the terminal windows or press `Ctrl+C` in each terminal.

**macOS/Linux:**
```bash
# If you saved PIDs
kill $(cat backend.pid frontend.pid)

# Or find and kill manually
ps aux | grep "python main.py"
ps aux | grep "npm run dev"
kill <PID>
```

---

## 📚 Next Steps

After successful installation:
1. Read the [README.md](README.md) for feature overview
2. Explore the dashboard at http://localhost:3000
3. Check API documentation at http://127.0.0.1:8000/docs
4. Customize settings in the Settings page

---

## 💡 Tips

- **First Run**: It may take 30-60 seconds for the first session to appear
- **Idle Detection**: If you're idle for 3+ minutes, the session will end automatically
- **Data Export**: Use the Export button in the header to download CSV
- **Theme**: Switch between blue and orange themes in Settings
- **Browser**: Works best in Chrome, Firefox, or Edge (latest versions)

---

**Need help? Check the troubleshooting section or open an issue on GitHub.**

