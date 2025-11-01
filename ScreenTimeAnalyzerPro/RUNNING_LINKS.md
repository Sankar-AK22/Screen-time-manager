# 🚀 ScreenTime Analyzer Pro - Running Application Links

## ✅ Application is Running!

Your ScreenTime Analyzer Pro application is now live and tracking your screen time in real-time!

---

## 🌐 Access Links

### Frontend (Dashboard)
**Main Application**: http://localhost:3001

This is your main dashboard where you can:
- View real-time tracking of your current app
- See today's statistics (total time, productive time, entertainment time)
- View top apps pie chart
- Navigate to different pages (Today, Insights, Settings)
- Export data as CSV

### Backend API
**API Root**: http://127.0.0.1:8000

**API Documentation (Swagger UI)**: http://127.0.0.1:8000/docs

**Alternative API Docs (ReDoc)**: http://127.0.0.1:8000/redoc

---

## 📊 Pages Available

### 1. Dashboard (Home)
**URL**: http://localhost:3001/

Features:
- Live Now card (shows current app with real-time updates)
- Stats cards (Total Screen Time, Productive Time, Entertainment Time, Productivity Score)
- Top Apps pie chart
- Quick info section

### 2. Today View
**URL**: http://localhost:3001/today

Features:
- Hourly distribution bar chart
- Detailed sessions table
- Filter by category (All, Productive, Entertainment)
- Pagination for sessions
- Export button

### 3. Insights
**URL**: http://localhost:3001/insights

Features:
- Productivity score circle (0-100%)
- Category breakdown doughnut chart
- Most productive app
- Top distraction
- Personalized recommendations

### 4. Settings
**URL**: http://localhost:3001/settings

Features:
- Theme switcher (Blue/Orange)
- About section
- System information
- API endpoints list

---

## 🔌 API Endpoints

### REST API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | http://127.0.0.1:8000/ | Root endpoint (status check) |
| GET | http://127.0.0.1:8000/api/health | Health check |
| GET | http://127.0.0.1:8000/api/summary/today | Today's summary |
| GET | http://127.0.0.1:8000/api/usage/today | Today's sessions |
| GET | http://127.0.0.1:8000/api/usage/top | Top N apps |
| GET | http://127.0.0.1:8000/api/usage/hourly | Hourly distribution |
| GET | http://127.0.0.1:8000/api/usage/categories | Category breakdown |
| GET | http://127.0.0.1:8000/api/insights | Productivity insights |
| GET | http://127.0.0.1:8000/api/current | Current active session |
| GET | http://127.0.0.1:8000/api/export/csv | Export as CSV |

### WebSocket Endpoint

**WebSocket URL**: ws://127.0.0.1:8000/ws/usage

Real-time events:
- `session_start` - New app session started
- `session_end` - App session ended
- `heartbeat` - Current session update (every 5 seconds)
- `idle` - User became idle
- `summary_update` - Daily summary changed
- `current_session` - Current session info (sent on connect)

---

## 🎯 Quick Test

### Test Real-Time Tracking

1. **Open the dashboard**: http://localhost:3001
2. **Check the "Live Now" card** - it should show your current app (probably "Visual Studio Code")
3. **Switch to a different app** (e.g., browser, Notepad, Spotify)
4. **Wait 5-10 seconds**
5. **Check the dashboard again** - the "Live Now" card should update!

### Test API

1. **Open API docs**: http://127.0.0.1:8000/docs
2. **Click on any endpoint** (e.g., `/api/summary/today`)
3. **Click "Try it out"**
4. **Click "Execute"**
5. **See the response** with your screen time data!

---

## 📱 Connection Status

Check the connection status in the header:
- **Green dot + "Live"** = Connected to backend ✅
- **Red dot + "Disconnected"** = Connection lost ❌

If disconnected:
1. Check that backend is running (Terminal 35)
2. Check that frontend is running (Terminal 37)
3. Refresh the page

---

## 🛑 Stopping the Application

### To Stop Backend:
1. Go to Terminal 35 (backend terminal)
2. Press `Ctrl+C`

### To Stop Frontend:
1. Go to Terminal 37 (frontend terminal)
2. Press `Ctrl+C`

### To Stop Both:
Close both terminal windows or press `Ctrl+C` in each.

---

## 🔄 Restarting the Application

### Backend:
```bash
cd c:\Final_Project\Screen-Time_vs_Productivity-Analyzer\ScreenTimeAnalyzerPro\backend
.\venv\Scripts\activate
python main.py
```

### Frontend:
```bash
cd c:\Final_Project\Screen-Time_vs_Productivity-Analyzer\ScreenTimeAnalyzerPro\frontend
npm run dev
```

---

## 📊 Current Status

### Backend
- **Status**: ✅ Running
- **Terminal**: 35
- **Port**: 8000
- **URL**: http://127.0.0.1:8000
- **Tracking**: Active (1-second polling)
- **Database**: `backend/data/screentime.db`

### Frontend
- **Status**: ✅ Running
- **Terminal**: 37
- **Port**: 3001 (port 3000 was in use)
- **URL**: http://localhost:3001
- **WebSocket**: Connected to ws://127.0.0.1:8000/ws/usage

---

## 🎨 Features to Try

1. **Real-Time Tracking**: Switch apps and watch the "Live Now" card update
2. **Theme Switching**: Go to Settings and switch between Blue and Orange themes
3. **Export Data**: Click the Export button in the header to download CSV
4. **View Insights**: Go to Insights page to see your productivity score
5. **Hourly Chart**: Go to Today page to see hourly distribution
6. **Filter Sessions**: Use the filter buttons on Today page (All/Productive/Entertainment)

---

## 💡 Tips

- **First Run**: It may take 30-60 seconds for the first session to appear
- **Idle Detection**: If you're idle for 3+ minutes, the session will end automatically
- **Data Persistence**: All data is stored locally in SQLite database
- **Browser**: Works best in Chrome, Firefox, or Edge (latest versions)
- **Hot Reload**: Frontend has hot reload - changes will appear automatically

---

## 🐛 Troubleshooting

### "Connection Failed" in Dashboard
- Check that backend is running on port 8000
- Check browser console for errors (F12)
- Try refreshing the page

### "No Active Session" in Live Now Card
- Make sure you're actively using an application
- Wait 5-10 seconds for the first detection
- Check backend logs in Terminal 35

### Charts Not Showing
- Use the app for a few minutes to generate data
- Refresh the page
- Check that you have data for today

---

## 📚 Documentation

- **README**: [README.md](README.md)
- **Installation Guide**: [INSTALLATION_GUIDE.md](INSTALLATION_GUIDE.md)
- **Quick Start**: [QUICK_START.md](QUICK_START.md)
- **Project Summary**: [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)
- **File List**: [FILE_LIST.md](FILE_LIST.md)

---

## 🎉 Enjoy!

Your ScreenTime Analyzer Pro is now tracking your screen time in real-time!

**Track Smart, Work Smarter! 📊✨**

---

**Version 1.0.0 - Production Ready**
**Last Updated**: 2025-11-01

