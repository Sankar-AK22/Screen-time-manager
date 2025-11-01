# 🚀 ScreenTime Analyzer Pro

**A Complete, End-to-End Data Science Project for Screen Time Analysis**

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.8+-green)
![React](https://img.shields.io/badge/react-18.2-blue)
![FastAPI](https://img.shields.io/badge/fastapi-0.104-teal)

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Screenshots](#screenshots)
- [Architecture](#architecture)

---

## 🎯 Overview

**ScreenTime Analyzer Pro** is a complete full-stack application that automatically tracks, analyzes, and visualizes your laptop screen time and application usage. It provides real-time insights into productivity patterns, helping you optimize your digital habits.

### Key Capabilities:
- ✅ **Automatic Tracking**: Real-time monitoring of active applications
- ✅ **Smart Analytics**: AI-powered productivity scoring and insights
- ✅ **Beautiful UI**: Glassmorphism design with smooth animations
- ✅ **Cross-Platform**: Works on Windows, macOS, and Linux
- ✅ **Privacy-First**: All data stored locally on your device

---

## ✨ Features

### 🔍 Real-Time Tracking
- Automatic detection of active windows and applications
- Background service running every minute
- Platform-specific tracking (Windows/macOS/Linux)
- App categorization (Development, Productivity, Entertainment, etc.)

### 📊 Advanced Analytics
- Daily, weekly, and monthly usage statistics
- Productivity scoring algorithm (0-10 scale)
- Category breakdown and time distribution
- Hourly usage heatmaps
- Trend analysis and pattern detection

### 🎨 Beautiful Dashboard
- Modern glassmorphism UI design
- Interactive charts (Doughnut, Bar, Line)
- Real-time updates
- Responsive design
- Smooth animations with Framer Motion

### 💡 Smart Insights
- Personalized productivity recommendations
- Peak performance time identification
- Usage pattern analysis
- Break reminders and health tips

---

## 🛠️ Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **SQLAlchemy** - ORM for database operations
- **SQLite** - Lightweight database
- **psutil** - System and process utilities
- **pywin32** - Windows API access (Windows only)
- **APScheduler** - Background task scheduling

### Frontend
- **React 18** - UI library
- **Vite** - Build tool
- **Tailwind CSS** - Utility-first CSS framework
- **Chart.js** - Data visualization
- **Framer Motion** - Animation library
- **Axios** - HTTP client
- **React Router** - Navigation

### Data Science
- **Pandas** - Data manipulation
- **NumPy** - Numerical computing
- **Plotly** - Interactive visualizations
- **Scikit-learn** - Machine learning utilities

---

## 📁 Project Structure

```
screentime-analyzer-pro/
│
├── backend/                    # Python FastAPI Backend
│   ├── app/
│   │   ├── api/               # API routes
│   │   │   └── routes.py
│   │   ├── database/          # Database configuration
│   │   │   └── database.py
│   │   ├── models/            # SQLAlchemy models & schemas
│   │   │   ├── usage.py
│   │   │   └── schemas.py
│   │   ├── services/          # Business logic
│   │   │   ├── tracker.py     # Screen time tracking
│   │   │   ├── analytics.py   # Analytics engine
│   │   │   └── scheduler.py   # Background tasks
│   │   └── main.py            # FastAPI app
│   ├── data/                  # SQLite database
│   └── requirements.txt       # Python dependencies
│
├── frontend/                   # React Frontend
│   ├── src/
│   │   ├── components/        # React components
│   │   │   ├── Dashboard.jsx
│   │   │   ├── Analytics.jsx
│   │   │   ├── Settings.jsx
│   │   │   ├── Layout.jsx
│   │   │   └── ...
│   │   ├── services/          # API services
│   │   │   └── api.js
│   │   ├── utils/             # Utility functions
│   │   │   └── formatters.js
│   │   ├── App.jsx            # Main app component
│   │   ├── main.jsx           # Entry point
│   │   └── index.css          # Global styles
│   ├── package.json
│   ├── vite.config.js
│   └── tailwind.config.js
│
├── data-science/              # Data Science Modules
│   └── visualizations.py      # Advanced visualizations
│
├── start-backend.bat          # Backend startup script
├── start-frontend.bat         # Frontend startup script
├── start-all.bat              # Start all services
└── README.md                  # This file
```

---

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- Node.js 16 or higher
- npm or yarn
- Git

### Step 1: Clone the Repository
```bash
git clone <repository-url>
cd screentime-analyzer-pro
```

### Step 2: Backend Setup
```bash
cd backend
pip install -r requirements.txt
```

### Step 3: Frontend Setup
```bash
cd frontend
npm install
```

---

## 💻 Usage

### Option 1: Start All Services (Recommended)
**Windows:**
```bash
start-all.bat
```

This will start both backend and frontend servers automatically.

### Option 2: Start Services Separately

**Backend:**
```bash
cd backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Frontend:**
```bash
cd frontend
npm run dev
```

### Access the Application
- **Frontend Dashboard**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/api/v1/health

---

## 📡 API Documentation

### Tracking Endpoints

#### Start Tracking
```http
POST /api/v1/tracking/start
```

#### Stop Tracking
```http
POST /api/v1/tracking/stop
```

#### Get Tracking Status
```http
GET /api/v1/tracking/status
```

### Usage Data Endpoints

#### Get Usage Data
```http
GET /api/v1/usage?limit=100&offset=0
```

#### Get Current Usage
```http
GET /api/v1/usage/current
```

### Statistics Endpoints

#### Get Statistics
```http
GET /api/v1/stats?period=today
```
Parameters: `today`, `week`, `month`, `custom`

#### Get Daily Summaries
```http
GET /api/v1/stats/daily?days=7
```

### Report Endpoints

#### Generate Report
```http
POST /api/v1/report
Body: {
  "period": "week",
  "start_date": "2024-01-01T00:00:00",
  "end_date": "2024-01-07T23:59:59"
}
```

#### Get Summary
```http
GET /api/v1/summary
```

---

## 🏗️ Architecture

### System Flow

```
┌─────────────────┐
│  Active Window  │
│   Detection     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Tracker       │
│   Service       │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   SQLite DB     │
│   (Local)       │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Analytics     │
│   Engine        │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   FastAPI       │
│   REST API      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   React UI      │
│   Dashboard     │
└─────────────────┘
```

### Database Schema

**AppUsage Table:**
- id (Primary Key)
- app_name
- window_title
- process_name
- start_time
- end_time
- duration_seconds
- duration_minutes
- is_active
- category
- created_at

**DailySummary Table:**
- id (Primary Key)
- date
- total_screen_time_minutes
- total_apps_used
- most_used_app
- most_used_app_duration
- productivity_score
- active_hours

**AppCategory Table:**
- id (Primary Key)
- app_name
- category
- productivity_weight

---

## 🎨 UI Features

### Dashboard Page
- Real-time current activity display
- Screen time statistics
- Productivity score gauge
- Category distribution pie chart
- Top applications bar chart
- Smart insights and recommendations

### Analytics Page
- Screen time trend line chart
- Productivity trend line chart
- Daily summary table
- Customizable time periods (7/14/30 days)

### Settings Page
- Data management options
- Notification preferences
- Privacy settings
- About information

---

## 🔒 Privacy & Security

- ✅ All data stored locally on your device
- ✅ No cloud uploads or external data sharing
- ✅ No personal information collected
- ✅ Open-source and transparent
- ✅ Full control over your data

---

## 🐛 Troubleshooting

### Backend Issues

**Issue: Module not found**
```bash
pip install -r requirements.txt
```

**Issue: Port 8000 already in use**
```bash
# Change port in app/main.py or kill the process
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### Frontend Issues

**Issue: Dependencies not installed**
```bash
cd frontend
npm install
```

**Issue: Port 3000 already in use**
```bash
# Vite will automatically use next available port
# Or change port in vite.config.js
```

---

## 📈 Future Enhancements

- [ ] Machine learning predictions for productivity
- [ ] Multi-device synchronization
- [ ] Mobile app (React Native)
- [ ] Browser extension for web tracking
- [ ] Team collaboration features
- [ ] Export reports to PDF/CSV
- [ ] Custom app categorization
- [ ] Focus mode with app blocking

---

## 👨‍💻 Development

### Running Tests
```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

### Building for Production
```bash
# Backend
cd backend
pip install -r requirements.txt

# Frontend
cd frontend
npm run build
```

---

## 📄 License

This project is licensed under the MIT License.

---

## 🙏 Acknowledgments

- FastAPI for the amazing web framework
- React team for the powerful UI library
- Chart.js for beautiful visualizations
- Tailwind CSS for the utility-first approach

---

## 📞 Support

For issues, questions, or contributions, please open an issue on GitHub.

---

**Made with ❤️ by Data Science & AI**

**ScreenTime Analyzer Pro - Track Smart, Work Smarter! 🚀**

