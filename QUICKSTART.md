# 🚀 Quick Start Guide - Screen Time vs Productivity Analyzer

## ⚡ Fast Setup (3 Steps)

### 1️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 2️⃣ Run the Dashboard
```bash
streamlit run src/dashboard_app.py
```

### 3️⃣ Open Browser
The dashboard will automatically open at: **http://localhost:8501**

---

## 📊 What You'll See

### Dashboard Features:
- **📊 Overview Tab**: Dataset statistics and summary
- **📈 Analysis Tab**: Interactive visualizations and correlations
- **🔮 Predictions Tab**: Real-time productivity predictions
- **💡 Insights Tab**: Key findings and recommendations

### Interactive Controls:
- **📱 Screen Time Slider**: Adjust daily screen time (1-12 hours)
- **📚 Study Hours Slider**: Adjust daily study hours (0-10 hours)
- **🎯 Live Predictions**: See productivity score update in real-time

---

## 🔄 Re-run Data Pipeline (Optional)

If you want to regenerate everything from scratch:

```bash
# Step 1: Generate new dataset
python data/generate_data.py

# Step 2: Preprocess data
python src/data_preprocessing.py

# Step 3: Train model
python src/model_training.py

# Step 4: Launch dashboard
streamlit run src/dashboard_app.py
```

---

## 🎯 Key Insights from the Analysis

### Correlation Results:
- **Screen Time vs Productivity**: -0.352 (Negative correlation)
  - More screen time → Lower productivity
  
- **Study Hours vs Productivity**: +0.645 (Strong positive correlation)
  - More study hours → Higher productivity

### Optimal Ranges for High Productivity:
- **Screen Time**: 4-5 hours/day
- **Study Hours**: 5-6 hours/day
- **Expected Productivity**: 9-10/10

---

## 🛠️ Troubleshooting

### Issue: Dependencies not installed
```bash
pip install -r requirements.txt
```

### Issue: Model file not found
```bash
python src/model_training.py
```

### Issue: Data file not found
```bash
python data/generate_data.py
python src/data_preprocessing.py
```

### Issue: Port 8501 already in use
```bash
streamlit run src/dashboard_app.py --server.port 8502
```

---

## 📱 Using the Dashboard

1. **Adjust Sliders**: Use the sidebar to set your screen time and study hours
2. **View Prediction**: See your predicted productivity score instantly
3. **Explore Tabs**: Navigate through different sections for insights
4. **Interactive Charts**: Hover over charts for detailed information
5. **Get Recommendations**: Read personalized tips to improve productivity

---

## 🎨 Dashboard Highlights

- ✨ Modern, clean UI with gradient headers
- 📊 Interactive Plotly visualizations
- 🎯 Real-time predictions with ML model
- 💡 Personalized recommendations
- 📈 3D scatter plots for multi-dimensional analysis
- 🔍 Correlation heatmaps
- 📋 Statistical summaries

---

## 📞 Need Help?

Check the main **README.md** for detailed documentation.

---

**Happy Analyzing! 📊✨**

