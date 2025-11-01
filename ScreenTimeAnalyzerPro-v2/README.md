# ScreenTime Analyzer Pro v2.0

**Real-time screen time tracking with modern black + blue/orange UI**

## 🎯 Features

- ✅ **Real-time Windows app tracking** (1-second polling)
- ✅ **Smart idle detection** (2-minute threshold)
- ✅ **WebSocket live updates** + API polling fallback
- ✅ **Modern glassmorphism UI** (black theme, blue/orange accents)
- ✅ **Smart app categorization** (7 categories)
- ✅ **Productivity scoring** and insights
- ✅ **CSV/PDF export** functionality
- ✅ **Single-page dashboard** with live tracking
- ✅ **Hourly distribution** charts
- ✅ **Today vs Yesterday** comparisons

## 🚀 Quick Start

### Prerequisites

- **Python 3.8+** (with pip)
- **Node.js 16+** (with npm)
- **Windows OS** (for app tracking)

### Installation & Launch

**Option 1: One-Click Start (Windows)**

```bash
start.bat
```

This will:
1. Create Python virtual environment (if needed)
2. Install all dependencies (if needed)
3. Start backend server (port 8000)
4. Start frontend dev server (port 3000)
5. Open your browser automatically

**Option 2: Manual Start**

```bash
# 1. Setup backend
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

# 2. Setup frontend
cd ../frontend
npm install

# 3. Start both servers
cd ..
npm run start
```

## 📊 Access the Application

- **Frontend Dashboard:** http://localhost:3000
- **Backend API:** http://127.0.0.1:8000
- **API Docs:** http://127.0.0.1:8000/docs

## 🏗️ Architecture

```
ScreenTimeAnalyzerPro-v2/
├── backend/              # FastAPI + SQLite + Windows tracking
│   ├── main.py          # API endpoints & WebSocket
│   ├── database.py      # SQLAlchemy models
│   ├── tracker.py       # Windows app tracking
│   ├── analytics.py     # Data analysis & exports
│   └── requirements.txt
├── frontend/            # React + Vite + Tailwind
│   ├── src/
│   │   ├── pages/       # Dashboard, Today, Insights, Settings
│   │   ├── components/  # Navbar, Cards
│   │   └── api/         # API & WebSocket clients
│   └── package.json
├── electron/            # Electron wrapper (optional)
├── scripts/             # Startup scripts
└── start.bat           # Windows launcher
```

## 🎨 UI Features

### Dashboard Page
- **Live Now Card** - Real-time tracking with pulsing LIVE badge
- **Top 4 Stats** - Total time, Productive time, Entertainment, Score
- **Top Apps Chart** - Pie chart with top 5 apps
- **Real-time Updates** - WebSocket + 5-second polling

### Today Page
- Complete list of all apps used today
- Sortable table with time, sessions, percentage
- Category badges

### Insights Page
- Today vs Yesterday comparison
- Hourly distribution bar chart
- Productivity trends
- Most used category

### Settings Page
- Export to CSV/PDF
- Category explanations
- App information

## 🔧 Technologies

**Backend:**
- FastAPI (async web framework)
- SQLAlchemy (ORM)
- SQLite (database)
- psutil, pywin32, pygetwindow (Windows tracking)
- pynput (idle detection)
- pandas, reportlab (exports)

**Frontend:**
- React 18 + Vite
- Tailwind CSS (black theme)
- Recharts (charts)
- Framer Motion (animations)
- Axios (HTTP client)
- WebSocket (real-time)

## 📝 How It Works

1. **Tracking Loop** (1-second polling)
   - Detects active window using win32gui
   - Gets process name using psutil
   - Categorizes app automatically
   - Saves sessions to SQLite

2. **Idle Detection** (2-minute threshold)
   - Monitors mouse/keyboard using pynput
   - Pauses tracking when idle
   - Resumes on activity

3. **Real-time Updates**
   - WebSocket broadcasts every 5 seconds
   - Frontend polls API every 5 seconds (fallback)
   - Live Now card updates every 2 seconds

4. **Smart Categorization**
   - 7 categories: Development, Productivity, Browser, Communication, Entertainment, Design, Other
   - Automatic categorization based on app name
   - Productivity score calculation

## 🎯 Productivity Scoring

- **Productive:** Development, Productivity, Design
- **Entertainment:** Entertainment, Browser
- **Score:** Productive time / Total time × 100%

## 📤 Export Formats

- **CSV:** Spreadsheet with all sessions
- **PDF:** Formatted report with summary and top apps

## 🐛 Troubleshooting

**Backend won't start:**
- Check Python version: `python --version` (need 3.8+)
- Reinstall dependencies: `pip install -r requirements.txt`
- Check port 8000 is free

**Frontend won't start:**
- Check Node version: `node --version` (need 16+)
- Reinstall dependencies: `npm install`
- Check port 3000 is free

**No tracking data:**
- Make sure you're switching between apps
- Wait 10-30 seconds for first session
- Check backend logs for errors

**WebSocket not connecting:**
- Frontend will fallback to API polling automatically
- Check browser console for errors
- Verify backend is running on port 8000

## 📜 License

MIT License - Feel free to use and modify!

## 🎉 Version 2.0.0

**Production-ready with real-time tracking and modern UI!**

---

**Made with ❤️ for productivity tracking**

