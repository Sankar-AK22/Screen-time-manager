"""
Generate synthetic screen time and productivity data for 30 days
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Set random seed for reproducibility
np.random.seed(42)

# Generate 30 days of data
num_days = 30
start_date = datetime(2025, 1, 1)

# Initialize lists to store data
dates = []
screen_times = []
study_hours = []
productivity_scores = []

for i in range(num_days):
    # Generate date
    current_date = start_date + timedelta(days=i)
    dates.append(current_date.strftime("%d-%m-%Y"))
    
    # Generate screen time (2-10 hours with some randomness)
    screen_time = np.random.uniform(2, 10)
    screen_times.append(round(screen_time, 2))
    
    # Generate study hours (1-8 hours with some randomness)
    study_hour = np.random.uniform(1, 8)
    study_hours.append(round(study_hour, 2))
    
    # Calculate productivity score based on logic:
    # - Higher screen time -> Lower productivity
    # - Higher study hours -> Higher productivity
    # Base formula: Productivity = 10 - (0.5 * screen_time) + (0.8 * study_hours) + noise
    base_productivity = 10 - (0.5 * screen_time) + (0.8 * study_hour)
    
    # Add some random noise
    noise = np.random.uniform(-0.5, 0.5)
    productivity = base_productivity + noise
    
    # Ensure productivity is between 1 and 10
    productivity = max(1, min(10, productivity))
    productivity_scores.append(round(productivity, 2))

# Create DataFrame
df = pd.DataFrame({
    'Date': dates,
    'Screen_Time_Hours': screen_times,
    'Study_Hours': study_hours,
    'Productivity_Score': productivity_scores
})

# Save to CSV
df.to_csv('data/screen_time_data.csv', index=False)
print("✅ Dataset generated successfully!")
print(f"📊 Total records: {len(df)}")
print("\n📈 Sample data:")
print(df.head(10))
print("\n📊 Statistical Summary:")
print(df.describe())

