# 🚀 ScreenTime Analyzer Pro - Quick Start Guide

## ⚡ Get Started in 3 Minutes!

---

## 📋 Prerequisites

Before you begin, make sure you have:
- ✅ Python 3.8+ installed
- ✅ Node.js 16+ installed
- ✅ npm or yarn installed
- ✅ Windows/macOS/Linux operating system

---

## 🎯 Quick Start (Windows)

### Option 1: One-Click Start (Easiest!)

1. **Open the project folder**
   ```bash
   cd screentime-analyzer-pro
   ```

2. **Double-click the startup script**
   ```
   start-all.bat
   ```

3. **Wait for both servers to start** (about 30 seconds)

4. **Open your browser**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000/docs

**That's it! You're done! 🎉**

---

### Option 2: Manual Start

#### Step 1: Start Backend
```bash
cd screentime-analyzer-pro/backend
pip install -r requirements.txt
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Wait for this message:
```
🎉 ScreenTime Analyzer Pro is ready!
```

#### Step 2: Start Frontend (in a new terminal)
```bash
cd screentime-analyzer-pro/frontend
npm install
npm run dev
```

Wait for this message:
```
➜  Local:   http://localhost:3000/
```

#### Step 3: Open Browser
Navigate to: http://localhost:3000

---

## 🎮 Using the Application

### 1. **Dashboard Page** (Home)
- View your current active application
- See today's screen time statistics
- Check your productivity score
- View category breakdown
- See top 5 most used apps
- Get personalized insights

### 2. **Analytics Page**
- View screen time trends over time
- Track productivity score changes
- See daily summary table
- Switch between 7/14/30 day views

### 3. **Settings Page**
- Configure data retention
- Set up notifications
- View privacy information
- Check app version

### 4. **Tracking Controls** (Sidebar)
- **Green indicator** = Tracking active
- **Red indicator** = Tracking stopped
- Click "Start" to begin tracking
- Click "Stop" to pause tracking

---

## 📊 Understanding Your Data

### Productivity Score (0-10)
- **7-10**: Excellent! You're very productive
- **5-7**: Good! Room for improvement
- **0-5**: Low productivity, consider focusing more

### App Categories
- **Development** (💻): IDEs, code editors
- **Productivity** (📊): Office apps, note-taking
- **Browser** (🌐): Web browsers
- **Communication** (💬): Email, chat apps
- **Entertainment** (🎮): Games, streaming
- **Design** (🎨): Design tools
- **Other** (📱): Everything else

---

## 🔧 Troubleshooting

### Backend Won't Start

**Problem**: Port 8000 already in use
```bash
# Find and kill the process
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

**Problem**: Module not found
```bash
cd backend
pip install -r requirements.txt
```

### Frontend Won't Start

**Problem**: Dependencies not installed
```bash
cd frontend
npm install
```

**Problem**: Port 3000 already in use
- Vite will automatically use the next available port (3001, 3002, etc.)

### No Data Showing

**Problem**: Tracking not started
- Check the sidebar indicator
- Click "Start" button to begin tracking
- Wait 1-2 minutes for data to appear

**Problem**: Database not initialized
- Restart the backend server
- Check for `data/usage_data.db` file

---

## 📡 API Endpoints

### Quick Reference

**Health Check**
```bash
curl http://localhost:8000/api/v1/health
```

**Get Summary**
```bash
curl http://localhost:8000/api/v1/summary
```

**Start Tracking**
```bash
curl -X POST http://localhost:8000/api/v1/tracking/start
```

**Stop Tracking**
```bash
curl -X POST http://localhost:8000/api/v1/tracking/stop
```

**Full API Documentation**
Visit: http://localhost:8000/docs

---

## 🎯 Tips for Best Results

### 1. **Let it Run**
- Keep the application running in the background
- The longer it runs, the more accurate your insights

### 2. **Check Daily**
- Review your dashboard every morning
- Track your productivity trends
- Adjust your habits based on insights

### 3. **Set Goals**
- Aim for a productivity score of 7+
- Limit entertainment apps during work hours
- Take breaks every 2 hours

### 4. **Customize Categories**
- Add your frequently used apps to categories
- Adjust productivity weights
- Create custom reports

---

## 📁 Project Structure

```
screentime-analyzer-pro/
│
├── backend/              # Python FastAPI backend
│   ├── app/
│   │   ├── api/         # REST API routes
│   │   ├── database/    # Database config
│   │   ├── models/      # Data models
│   │   ├── services/    # Business logic
│   │   └── main.py      # FastAPI app
│   └── data/            # SQLite database
│
├── frontend/            # React frontend
│   ├── src/
│   │   ├── components/  # React components
│   │   ├── services/    # API client
│   │   └── utils/       # Helper functions
│   └── public/          # Static assets
│
├── data-science/        # Analytics modules
│   └── visualizations.py
│
├── start-all.bat        # Start everything
├── start-backend.bat    # Start backend only
├── start-frontend.bat   # Start frontend only
├── README.md            # Full documentation
└── QUICKSTART.md        # This file
```

---

## 🔒 Privacy & Data

### Where is my data stored?
- All data is stored locally in `backend/data/usage_data.db`
- No cloud uploads or external sharing
- You have full control over your data

### What data is collected?
- Application names
- Window titles
- Start and end times
- Duration of usage
- Automatically assigned categories

### Can I delete my data?
- Yes! Simply delete the `usage_data.db` file
- Or use the Settings page to configure data retention

---

## 🆘 Need Help?

### Common Issues

**Q: The dashboard shows "No data available"**
A: Make sure tracking is started and wait 1-2 minutes for data to appear.

**Q: Charts are not loading**
A: Check that the backend is running at http://localhost:8000

**Q: Tracking stopped automatically**
A: The scheduler runs every minute. If the app crashes, restart it.

**Q: How do I export my data?**
A: Currently, data is in SQLite format. Use a SQLite browser or export via API.

---

## 🎉 You're All Set!

Your ScreenTime Analyzer Pro is now running and tracking your screen time!

### What's Next?
1. ✅ Let it run for a few hours to collect data
2. ✅ Check your dashboard regularly
3. ✅ Review your productivity insights
4. ✅ Optimize your digital habits

---

## 📞 Quick Links

- **Dashboard**: http://localhost:3000
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/api/v1/health
- **Full README**: [README.md](README.md)

---

**Happy Tracking! 📊✨**

**ScreenTime Analyzer Pro - Track Smart, Work Smarter!**

