# 🚀 QUICK START GUIDE

## ScreenTime Analyzer Pro v2.0

### ⚡ Fastest Way to Run

**Just double-click this file:**
```
start.bat
```

That's it! The script will:
1. ✅ Create Python virtual environment (first time only)
2. ✅ Install all dependencies (first time only)
3. ✅ Start backend server on port 8000
4. ✅ Start frontend on port 3000
5. ✅ Open your browser automatically

---

## 📋 Step-by-Step (First Time Setup)

### 1. Install Prerequisites

**Python 3.8+**
```bash
python --version
# Should show Python 3.8 or higher
```

**Node.js 16+**
```bash
node --version
# Should show v16 or higher
```

### 2. Setup Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Setup Frontend

```bash
cd frontend
npm install
```

### 4. Run the Application

**Option A: Use the batch file (Recommended)**
```bash
start.bat
```

**Option B: Use npm script**
```bash
npm run start
```

**Option C: Manual (two terminals)**

Terminal 1 (Backend):
```bash
cd backend
venv\Scripts\activate
python main.py
```

Terminal 2 (Frontend):
```bash
cd frontend
npm run dev
```

---

## 🌐 Access URLs

Once started, open these URLs:

- **🎨 Dashboard:** http://localhost:3000
- **📡 Backend API:** http://127.0.0.1:8000
- **📚 API Docs:** http://127.0.0.1:8000/docs

---

## ✅ Verify It's Working

### 1. Check Backend
Open http://127.0.0.1:8000 - you should see:
```json
{
  "message": "ScreenTime Analyzer Pro API",
  "version": "2.0.0",
  "status": "running"
}
```

### 2. Check Frontend
Open http://localhost:3000 - you should see:
- Black background with blue/orange accents
- "Online" status in top right (green)
- Dashboard with stats cards

### 3. Test Tracking
1. Switch to **Visual Studio Code** for 10 seconds
2. Switch to **Chrome** for 10 seconds
3. Go back to the dashboard
4. You should see:
   - "Live Now" card showing current app
   - Stats updating in real-time
   - Top Apps chart with your apps

---

## 🎯 What You'll See

### Dashboard (Main Page)
- **4 Stat Cards:**
  - Total Screen Time (blue)
  - Productive Time (green)
  - Entertainment (orange)
  - Productivity Score (purple)

- **Live Now Card:**
  - Current app name
  - Window title
  - Category badge
  - Duration counter (updates every second)
  - Pulsing "LIVE" badge

- **Top Apps Card:**
  - Pie chart with top 5 apps
  - List with time and percentage
  - Color-coded categories

### Today Page
- Complete table of all apps used
- Time, sessions, percentage for each
- Sortable columns

### Insights Page
- Today vs Yesterday comparison
- Hourly distribution bar chart
- Productivity trends
- Most used category

### Settings Page
- Export to CSV button
- Export to PDF button
- Category explanations
- App information

---

## 🔧 Troubleshooting

### Backend Issues

**"Python not found"**
```bash
# Install Python from python.org
# Make sure to check "Add to PATH" during installation
```

**"Port 8000 already in use"**
```bash
# Find and kill the process using port 8000
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

**"Module not found"**
```bash
cd backend
venv\Scripts\activate
pip install -r requirements.txt --upgrade
```

### Frontend Issues

**"Node not found"**
```bash
# Install Node.js from nodejs.org
```

**"Port 3000 already in use"**
```bash
# The script will automatically use port 3001 if 3000 is busy
# Or kill the process:
netstat -ano | findstr :3000
taskkill /PID <PID> /F
```

**"npm install fails"**
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### Tracking Issues

**"No data showing"**
- Wait 10-30 seconds after switching apps
- Make sure backend is running (check http://127.0.0.1:8000)
- Check browser console for errors (F12)

**"Live Now not updating"**
- WebSocket might be disconnected (check "Online" status)
- Frontend will fallback to API polling automatically
- Refresh the page (F5)

**"Apps not categorized correctly"**
- Categories are auto-assigned based on app name
- You can customize categories in `backend/tracker.py`

---

## 📊 How It Works

### Real-Time Tracking
1. Backend polls active window every **1 second**
2. Detects app name and window title using Windows API
3. Categorizes app automatically
4. Saves sessions to SQLite database

### Idle Detection
- Monitors mouse and keyboard activity
- Pauses tracking after **2 minutes** of inactivity
- Resumes automatically when you return

### Live Updates
- WebSocket broadcasts updates every **5 seconds**
- Frontend polls API every **5 seconds** (fallback)
- "Live Now" card updates every **2 seconds**

### Smart Categorization
- **Development:** VS Code, PyCharm, Visual Studio
- **Productivity:** Excel, Word, PowerPoint, Notion
- **Browser:** Chrome, Edge, Firefox, Brave
- **Communication:** WhatsApp, Discord, Slack, Teams
- **Entertainment:** Spotify, Netflix, YouTube
- **Design:** Photoshop, Figma, Illustrator
- **Other:** Everything else

---

## 🎨 UI Theme

- **Background:** #0B0B0B (pure black)
- **Cards:** #1E1E1E (dark gray) with glassmorphism
- **Primary:** #007BFF (blue)
- **Accent:** #FF8800 (orange)
- **Font:** Inter (Google Fonts)

---

## 📤 Exporting Data

### CSV Export
1. Click "Export" button in navbar
2. Or go to Settings → Export as CSV
3. Opens in Excel/Google Sheets

### PDF Export
1. Go to Settings → Export as PDF
2. Downloads formatted report with:
   - Daily summary table
   - Top apps table
   - Professional layout

---

## 🎉 You're All Set!

Your **ScreenTime Analyzer Pro** is now running and tracking your screen time in real-time!

### Next Steps:
1. ✅ Use your computer normally
2. ✅ Switch between different apps
3. ✅ Check the dashboard to see your usage
4. ✅ View insights to improve productivity
5. ✅ Export data for analysis

---

## 💡 Pro Tips

- **Leave it running:** The app tracks automatically in the background
- **Check insights daily:** Compare today vs yesterday
- **Set goals:** Use productivity score to improve focus
- **Export weekly:** Keep records of your progress
- **Customize categories:** Edit `backend/tracker.py` to add your apps

---

## 📞 Need Help?

- Check the **README.md** for detailed documentation
- View **API docs** at http://127.0.0.1:8000/docs
- Check browser console (F12) for frontend errors
- Check terminal for backend errors

---

**Happy Tracking! 📊✨**

**Version 2.0.0 - Production Ready**

