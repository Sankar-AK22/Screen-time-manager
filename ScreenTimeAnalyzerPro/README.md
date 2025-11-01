# 📊 ScreenTime Analyzer Pro

**Real-time screen time tracking and productivity analytics for Windows, macOS, and Linux.**

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.8+-green)
![React](https://img.shields.io/badge/react-18.2-blue)
![License](https://img.shields.io/badge/license-MIT-green)

---

## 🎯 Features

- ✅ **Real-time Tracking**: 1-second polling for accurate app usage tracking
- ✅ **Idle Detection**: Automatic idle detection with 3-minute threshold
- ✅ **WebSocket Streaming**: Live updates to dashboard without refresh
- ✅ **Productivity Scoring**: AI-powered productivity analysis
- ✅ **Category Analytics**: Automatic app categorization (7 categories)
- ✅ **Hourly Distribution**: Visual breakdown of screen time by hour
- ✅ **Export Functionality**: CSV export for further analysis
- ✅ **Cross-Platform**: Windows, macOS, and Linux support
- ✅ **Beautiful UI**: Glassmorphism design with blue/orange themes

---

## 🏗️ Architecture

### Backend (Python + FastAPI)
- **FastAPI** - Async web framework with WebSocket support
- **SQLAlchemy** - ORM for SQLite database
- **psutil** - Cross-platform system utilities
- **pywin32** (Windows) - Windows API access
- **AppKit/Quartz** (macOS) - macOS window detection
- **pynput** - Keyboard and mouse monitoring for idle detection

### Frontend (React + Vite)
- **React 18** - Component-based UI
- **Vite** - Fast build tool
- **Tailwind CSS** - Utility-first styling
- **Chart.js** - Canvas-based charts
- **Framer Motion** - Smooth animations
- **WebSocket API** - Real-time communication

---

## 📦 Installation

### Prerequisites
- **Python 3.8+**
- **Node.js 16+**
- **npm or yarn**

### Platform-Specific Requirements

#### Windows
```bash
pip install pywin32
```

#### macOS
```bash
pip install pyobjc-framework-Cocoa pyobjc-framework-Quartz
```

#### Linux
No additional requirements (uses psutil fallback)

---

## 🚀 Quick Start

### Option 1: Automated Start (Recommended)

#### Windows
```bash
cd ScreenTimeAnalyzerPro
start_local.bat
```

#### macOS/Linux
```bash
cd ScreenTimeAnalyzerPro
chmod +x start_local.sh
./start_local.sh
```

### Option 2: Manual Start

#### 1. Start Backend
```bash
cd backend
pip install -r requirements.txt
python main.py
```

Backend will run on: **http://127.0.0.1:8000**

#### 2. Start Frontend
```bash
cd frontend
npm install
npm run dev
```

Frontend will run on: **http://localhost:3000**

---

## 📖 Usage

### Dashboard
- View real-time tracking of current app
- See total screen time, productive time, and productivity score
- Monitor top 5 apps by usage time
- Check connection status (green = live, red = offline)

### Today View
- Detailed list of all sessions
- Hourly distribution chart
- Filter by category (all, productive, entertainment)
- Export data as CSV

### Insights
- Productivity score with circular progress
- Category breakdown pie chart
- Most productive app and top distraction
- Personalized recommendations

### Settings
- Switch between blue and orange themes
- View system information
- Check API endpoints and configuration

---

## 🔧 Configuration

### Backend Configuration
Edit `backend/.env` (create from `.env.example`):
```env
DATABASE_URL=sqlite:///./screentime.db
LOG_LEVEL=INFO
IDLE_THRESHOLD_SECONDS=180
TRACKING_INTERVAL_SECONDS=1
HEARTBEAT_INTERVAL_SECONDS=5
```

### Frontend Configuration
Edit `frontend/vite.config.js` to change API URL:
```javascript
proxy: {
  '/api': {
    target: 'http://127.0.0.1:8000',
  },
}
```

---

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest tests/ -v
```

### Frontend Tests
```bash
cd frontend
npm test
```

---

## 📊 API Documentation

Once the backend is running, visit:
- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc

### Key Endpoints

#### REST API
- `GET /api/summary/today` - Get today's summary
- `GET /api/usage/today` - Get today's sessions
- `GET /api/usage/top` - Get top apps
- `GET /api/usage/hourly` - Get hourly distribution
- `GET /api/insights` - Get productivity insights
- `GET /api/export/csv` - Export as CSV

#### WebSocket
- `ws://127.0.0.1:8000/ws/usage` - Real-time updates

### WebSocket Events
- `session_start` - New app session started
- `session_end` - App session ended
- `heartbeat` - Current session update (every 5s)
- `idle` - User became idle
- `summary_update` - Daily summary changed

---

## 🎨 Themes

### Blue Theme (Default)
- Accent color: `#00aaff`
- Modern, professional look

### Orange Theme
- Accent color: `#ff8a00`
- Warm, energetic feel

Switch themes in Settings or using the sun/moon icon in the header.

---

## 📁 Project Structure

```
ScreenTimeAnalyzerPro/
├── backend/
│   ├── main.py                 # FastAPI application
│   ├── requirements.txt        # Python dependencies
│   ├── tracker/
│   │   ├── realtime_tracker.py # Core tracking logic
│   │   ├── idle_detector.py    # Idle detection
│   │   └── utils.py            # Utilities
│   ├── db/
│   │   ├── database.py         # Database connection
│   │   └── models.py           # SQLAlchemy models
│   ├── analytics.py            # Analytics functions
│   ├── schemas.py              # Pydantic schemas
│   ├── debug_simulator.py      # Testing simulator
│   └── tests/                  # Unit tests
├── frontend/
│   ├── src/
│   │   ├── App.jsx             # Main app component
│   │   ├── api/
│   │   │   ├── socketClient.js # WebSocket client
│   │   │   └── apiClient.js    # REST API client
│   │   ├── pages/
│   │   │   ├── Dashboard.jsx   # Dashboard page
│   │   │   ├── TodayView.jsx   # Today's activity
│   │   │   ├── AppInsights.jsx # Insights page
│   │   │   └── Settings.jsx    # Settings page
│   │   ├── components/
│   │   │   ├── Header.jsx      # Header component
│   │   │   ├── LiveNowCard.jsx # Live tracking card
│   │   │   └── TopAppsCard.jsx # Top apps chart
│   │   └── styles/
│   │       └── theme.css       # Global styles
│   ├── package.json            # Node dependencies
│   └── vite.config.js          # Vite configuration
├── .env.example                # Environment template
├── start_local.sh              # Start script (Mac/Linux)
├── start_local.bat             # Start script (Windows)
└── README.md                   # This file
```

---

## 🐛 Troubleshooting

### Backend won't start
- Check Python version: `python --version` (must be 3.8+)
- Install dependencies: `pip install -r requirements.txt`
- Check port 8000 is not in use: `netstat -an | grep 8000`

### Frontend won't start
- Check Node version: `node --version` (must be 16+)
- Clear cache: `rm -rf node_modules package-lock.json && npm install`
- Check port 3000 is not in use

### WebSocket not connecting
- Ensure backend is running
- Check browser console for errors
- Verify WebSocket URL in `socketClient.js`

### Tracking not working
- **Windows**: Ensure pywin32 is installed
- **macOS**: Grant accessibility permissions in System Preferences
- **Linux**: Check X11 or Wayland compatibility

---

## 📝 License

MIT License - feel free to use this project for personal or commercial purposes.

---

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

## 📧 Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Check the troubleshooting section
- Review API documentation

---

## 🎉 Acknowledgments

Built with:
- FastAPI by Sebastián Ramírez
- React by Meta
- Chart.js by Chart.js Team
- Tailwind CSS by Tailwind Labs
- Framer Motion by Framer

---

**Made with ❤️ for productivity enthusiasts**

**Track Smart, Work Smarter! 📊✨**

