# ⚡ Quick Start Guide - ScreenTime Analyzer Pro

Get up and running in 5 minutes!

---

## 🎯 Prerequisites Check

Before starting, verify you have:

```bash
python --version   # Should be 3.8 or higher
node --version     # Should be 16 or higher
npm --version      # Should be 8 or higher
```

If any command fails, install the missing software:
- **Python**: https://www.python.org/downloads/
- **Node.js**: https://nodejs.org/

---

## 🚀 Installation (3 Steps)

### Step 1: Navigate to Project
```bash
cd ScreenTimeAnalyzerPro
```

### Step 2: Install Platform-Specific Dependencies

**Windows:**
```bash
pip install pywin32
```

**macOS:**
```bash
pip3 install pyobjc-framework-Cocoa pyobjc-framework-Quartz
```

**Linux:**
```bash
# No additional dependencies needed
```

### Step 3: Run the Application

**Windows:**
```bash
start_local.bat
```

**macOS/Linux:**
```bash
chmod +x start_local.sh
./start_local.sh
```

That's it! The application will:
1. Create a virtual environment
2. Install all dependencies
3. Start the backend server
4. Start the frontend server
5. Open your browser automatically

---

## 🌐 Access the Application

Once started, open your browser to:

**Dashboard**: http://localhost:3000

You should see:
- ✅ Header with "ScreenTime Analyzer Pro"
- ✅ Green "Live" indicator (connection status)
- ✅ Live Now card showing current app
- ✅ Stats cards (Total Screen Time, Productive Time, etc.)
- ✅ Top Apps pie chart

---

## 🎮 Quick Tour

### 1. Dashboard (Main Page)
- **Live Now Card**: Shows the app you're currently using
- **Stats**: Total screen time, productive time, entertainment time, productivity score
- **Top Apps**: Pie chart of your most-used apps
- **Quick Info**: Most productive hour, apps used, sessions

### 2. Today View
- **Hourly Chart**: Bar chart showing screen time by hour
- **Sessions Table**: Detailed list of all app sessions
- **Filters**: Filter by all, productive, or entertainment apps
- **Export**: Download data as CSV

### 3. Insights
- **Productivity Score**: Circular progress indicator
- **Category Breakdown**: Doughnut chart of time by category
- **Most Productive App**: Your top productive application
- **Top Distraction**: Your most distracting app
- **Recommendations**: Personalized tips to improve productivity

### 4. Settings
- **Theme**: Switch between blue and orange accent colors
- **About**: Version info and feature list
- **System**: API endpoints and configuration

---

## 🧪 Test It Out

### Test Real-Time Tracking

1. **Open the dashboard** (http://localhost:3000)
2. **Check the "Live Now" card** - it should show your current app
3. **Switch to a different app** (e.g., browser, text editor, Spotify)
4. **Wait 5-10 seconds**
5. **Check the dashboard again** - the "Live Now" card should update!

### Test Idle Detection

1. **Start using an app** (e.g., browser)
2. **Leave your computer idle** for 3+ minutes
3. **Come back and check** - the session should have ended

### Test Export

1. **Click the "Export" button** in the header
2. **A CSV file will download** with today's data
3. **Open it in Excel/Sheets** to see all sessions

---

## 🎨 Customize Your Experience

### Change Theme
1. Go to **Settings** page
2. Click on **Blue** or **Orange** theme
3. The entire UI will update instantly!

Or use the **sun/moon icon** in the header for quick switching.

### View API Documentation
Open: http://127.0.0.1:8000/docs

You'll see:
- All available API endpoints
- Request/response schemas
- Interactive API testing

---

## 📊 Understanding the Data

### Categories
Apps are automatically categorized into:
- **Development**: VS Code, PyCharm, IntelliJ, etc.
- **Productivity**: Excel, Word, Notion, etc.
- **Browser**: Chrome, Firefox, Edge, etc.
- **Communication**: Slack, Teams, Discord, Zoom, etc.
- **Entertainment**: Spotify, Netflix, YouTube, games, etc.
- **Design**: Figma, Photoshop, Illustrator, etc.
- **Other**: Everything else

### Productivity Score
Calculated based on time spent in productive vs. entertainment apps:
- **Development/Productivity**: 100% productive
- **Design**: 90% productive
- **Communication**: 70% productive
- **Browser**: 50% productive (mixed use)
- **Other**: 30% productive
- **Entertainment**: 0% productive

### Idle Detection
- **Threshold**: 3 minutes (180 seconds)
- **Detection**: Monitors keyboard and mouse activity
- **Behavior**: Automatically ends session when idle

---

## 🛑 Stopping the Application

### Using Start Scripts
Press `Ctrl+C` in the terminal where you ran the start script.

### Manual Stop
Close the terminal windows or press `Ctrl+C` in each terminal.

---

## 🐛 Common Issues

### "Connection Failed" (Red Dot)
**Solution**: Backend is not running. Restart `start_local.bat` or `start_local.sh`

### "No Active Session" in Live Now Card
**Solution**: 
1. Make sure you're actively using an application
2. Wait 5-10 seconds for the first detection
3. Check that tracking permissions are granted (macOS)

### Charts Not Showing
**Solution**: 
1. Use the app for a few minutes to generate data
2. Refresh the page
3. Check browser console for errors (F12)

### Export Button Not Working
**Solution**: 
1. Make sure backend is running
2. Check that you have data for today
3. Try a different browser

---

## 💡 Pro Tips

1. **First Run**: It takes 30-60 seconds for the first session to appear
2. **Accuracy**: The 1-second polling ensures ±1 second accuracy
3. **Privacy**: All data is stored locally in SQLite (no cloud sync)
4. **Performance**: Minimal CPU/memory usage (~50-100 MB total)
5. **Multi-tasking**: Only tracks the active (foreground) window
6. **Browser**: Works best in Chrome, Firefox, or Edge

---

## 📚 Next Steps

Now that you're up and running:

1. **Use it for a day** to collect meaningful data
2. **Check insights** to see your productivity patterns
3. **Export data** for deeper analysis
4. **Set goals** based on your productivity score
5. **Read the full README** for advanced features

---

## 🆘 Need Help?

- **Installation Issues**: See [INSTALLATION_GUIDE.md](INSTALLATION_GUIDE.md)
- **Feature Questions**: See [README.md](README.md)
- **Technical Details**: See [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)
- **API Reference**: http://127.0.0.1:8000/docs

---

## 🎉 You're All Set!

**ScreenTime Analyzer Pro** is now tracking your screen time in real-time!

Watch the dashboard update as you switch between applications, and start understanding your digital habits better.

**Track Smart, Work Smarter! 📊✨**

---

**Version 1.0.0 - Production Ready**

