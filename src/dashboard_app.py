"""
Streamlit Dashboard Application
Interactive UI for Screen Time vs Productivity Analysis
"""
import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
import seaborn as sns
import sys
import os

# Page configuration
st.set_page_config(
    page_title="Screen Time vs Productivity Analyzer",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        background-color: #f5f7fa;
    }
    .stApp {
        max-width: 1400px;
        margin: 0 auto;
    }
    h1 {
        color: #2c3e50;
        text-align: center;
        padding: 20px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    h2 {
        color: #34495e;
    }
    .stMetric {
        background-color: white;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .recommendation-box {
        background-color: #e8f5e9;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #4caf50;
        margin: 20px 0;
    }
    .warning-box {
        background-color: #fff3e0;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #ff9800;
        margin: 20px 0;
    }
    </style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Load the cleaned dataset"""
    try:
        df = pd.read_csv('data/cleaned_screen_time_data.csv')
        return df
    except Exception as e:
        st.error(f"❌ Error loading data: {e}")
        st.stop()

@st.cache_resource
def load_model():
    """Load the trained model"""
    try:
        model = joblib.load('models/linear_regression_model.pkl')
        return model
    except Exception as e:
        st.error(f"❌ Error loading model: {e}")
        st.stop()

def create_correlation_heatmap(df):
    """Create correlation heatmap using Plotly"""
    numeric_df = df.select_dtypes(include=[np.number])
    correlation = numeric_df.corr()
    
    fig = go.Figure(data=go.Heatmap(
        z=correlation.values,
        x=correlation.columns,
        y=correlation.columns,
        colorscale='RdBu',
        zmid=0,
        text=correlation.values,
        texttemplate='%{text:.3f}',
        textfont={"size": 12},
        colorbar=dict(title="Correlation")
    ))
    
    fig.update_layout(
        title='Correlation Heatmap',
        width=600,
        height=500,
        xaxis_title="",
        yaxis_title=""
    )
    
    return fig

def create_scatter_plot(df, model):
    """Create interactive scatter plot with regression line"""
    fig = go.Figure()
    
    # Scatter plot
    fig.add_trace(go.Scatter(
        x=df['Screen_Time_Hours'],
        y=df['Productivity_Score'],
        mode='markers',
        name='Actual Data',
        marker=dict(size=10, color='#3498db', line=dict(width=1, color='black')),
        text=[f'Screen: {s:.2f}h<br>Study: {st:.2f}h<br>Productivity: {p:.2f}' 
              for s, st, p in zip(df['Screen_Time_Hours'], df['Study_Hours'], df['Productivity_Score'])],
        hoverinfo='text'
    ))
    
    # Regression line
    screen_time_range = np.linspace(df['Screen_Time_Hours'].min(), 
                                   df['Screen_Time_Hours'].max(), 100)
    mean_study_hours = df['Study_Hours'].mean()
    X_pred = np.column_stack([screen_time_range, np.full(100, mean_study_hours)])
    y_pred = model.predict(X_pred)
    
    fig.add_trace(go.Scatter(
        x=screen_time_range,
        y=y_pred,
        mode='lines',
        name=f'Regression Line (Study Hours = {mean_study_hours:.2f})',
        line=dict(color='red', width=3, dash='dash')
    ))
    
    fig.update_layout(
        title='Screen Time vs Productivity',
        xaxis_title='Screen Time (Hours)',
        yaxis_title='Productivity Score',
        width=700,
        height=500,
        hovermode='closest'
    )
    
    return fig

def create_3d_plot(df):
    """Create 3D scatter plot"""
    fig = go.Figure(data=[go.Scatter3d(
        x=df['Screen_Time_Hours'],
        y=df['Study_Hours'],
        z=df['Productivity_Score'],
        mode='markers',
        marker=dict(
            size=8,
            color=df['Productivity_Score'],
            colorscale='Viridis',
            showscale=True,
            colorbar=dict(title="Productivity"),
            line=dict(color='black', width=1)
        ),
        text=[f'Screen: {s:.2f}h<br>Study: {st:.2f}h<br>Productivity: {p:.2f}' 
              for s, st, p in zip(df['Screen_Time_Hours'], df['Study_Hours'], df['Productivity_Score'])],
        hoverinfo='text'
    )])
    
    fig.update_layout(
        title='3D View: Screen Time, Study Hours & Productivity',
        scene=dict(
            xaxis_title='Screen Time (Hours)',
            yaxis_title='Study Hours',
            zaxis_title='Productivity Score'
        ),
        width=700,
        height=600
    )
    
    return fig

def get_recommendation(screen_time, study_hours, productivity):
    """Generate personalized recommendation"""
    recommendations = []
    
    if screen_time > 7:
        recommendations.append("🔴 Your screen time is quite high! Try reducing it by 1-2 hours for better focus.")
    elif screen_time > 5:
        recommendations.append("🟡 Your screen time is moderate. Consider taking regular breaks.")
    else:
        recommendations.append("🟢 Great! Your screen time is in a healthy range.")
    
    if study_hours < 3:
        recommendations.append("📚 Try to increase your study hours for better productivity.")
    elif study_hours < 5:
        recommendations.append("📖 Good study hours! Keep up the consistency.")
    else:
        recommendations.append("⭐ Excellent study hours! You're on the right track.")
    
    if productivity < 7:
        recommendations.append("💡 Focus on quality over quantity. Take breaks and stay hydrated.")
    elif productivity < 9:
        recommendations.append("✨ Good productivity! Small improvements can make a big difference.")
    else:
        recommendations.append("🎉 Outstanding productivity! Keep maintaining this balance.")
    
    return recommendations

def main():
    # Title
    st.title("📊 Screen Time vs Productivity Analyzer")
    st.markdown("### *A Data Science Approach to Optimize Your Daily Performance*")
    st.markdown("---")
    
    # Load data and model
    with st.spinner("Loading data and model..."):
        df = load_data()
        model = load_model()
    
    # Sidebar
    st.sidebar.header("🎯 Productivity Predictor")
    st.sidebar.markdown("Adjust the sliders to predict your productivity score:")
    
    screen_time = st.sidebar.slider(
        "📱 Screen Time (Hours)",
        min_value=1.0,
        max_value=12.0,
        value=5.0,
        step=0.5,
        help="Total hours spent on screens per day"
    )
    
    study_hours = st.sidebar.slider(
        "📚 Study Hours",
        min_value=0.0,
        max_value=10.0,
        value=4.0,
        step=0.5,
        help="Total hours spent studying per day"
    )
    
    # Make prediction
    X_input = np.array([[screen_time, study_hours]])
    predicted_productivity = model.predict(X_input)[0]
    predicted_productivity = max(1, min(10, predicted_productivity))  # Clamp between 1-10
    
    st.sidebar.markdown("---")
    st.sidebar.metric(
        label="🎯 Predicted Productivity Score",
        value=f"{predicted_productivity:.2f}/10",
        delta=f"{predicted_productivity - df['Productivity_Score'].mean():.2f} vs avg"
    )
    
    # Main content
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "📈 Analysis", "🔮 Predictions", "💡 Insights"])
    
    with tab1:
        st.header("📊 Dataset Overview")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("📅 Total Days", len(df))
        with col2:
            st.metric("⏱️ Avg Screen Time", f"{df['Screen_Time_Hours'].mean():.2f}h")
        with col3:
            st.metric("📚 Avg Study Hours", f"{df['Study_Hours'].mean():.2f}h")
        with col4:
            st.metric("🎯 Avg Productivity", f"{df['Productivity_Score'].mean():.2f}/10")
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📋 Sample Data")
            st.dataframe(df.head(10), use_container_width=True)
        
        with col2:
            st.subheader("📊 Statistical Summary")
            st.dataframe(df.describe(), use_container_width=True)
    
    with tab2:
        st.header("📈 Data Analysis & Visualizations")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.plotly_chart(create_correlation_heatmap(df), use_container_width=True)
        
        with col2:
            st.plotly_chart(create_scatter_plot(df, model), use_container_width=True)
        
        st.markdown("---")
        st.plotly_chart(create_3d_plot(df), use_container_width=True)
    
    with tab3:
        st.header("🔮 Productivity Prediction")
        
        st.markdown(f"""
        <div class="recommendation-box">
            <h3>📊 Your Input:</h3>
            <ul>
                <li><strong>Screen Time:</strong> {screen_time} hours</li>
                <li><strong>Study Hours:</strong> {study_hours} hours</li>
            </ul>
            <h3>🎯 Predicted Productivity: {predicted_productivity:.2f}/10</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Recommendations
        recommendations = get_recommendation(screen_time, study_hours, predicted_productivity)
        
        st.subheader("💡 Personalized Recommendations")
        for rec in recommendations:
            st.markdown(f"- {rec}")
    
    with tab4:
        st.header("💡 Key Insights")
        
        correlation = df[['Screen_Time_Hours', 'Study_Hours', 'Productivity_Score']].corr()
        
        st.markdown(f"""
        ### 🔍 Correlation Analysis:
        
        - **Screen Time vs Productivity:** {correlation.loc['Screen_Time_Hours', 'Productivity_Score']:.3f}
          - {'Negative correlation - More screen time tends to reduce productivity' if correlation.loc['Screen_Time_Hours', 'Productivity_Score'] < 0 else 'Positive correlation'}
        
        - **Study Hours vs Productivity:** {correlation.loc['Study_Hours', 'Productivity_Score']:.3f}
          - {'Positive correlation - More study hours improve productivity' if correlation.loc['Study_Hours', 'Productivity_Score'] > 0 else 'Negative correlation'}
        
        ### 🎯 Optimal Ranges (Based on Data):
        
        - **Screen Time:** {df[df['Productivity_Score'] >= 9]['Screen_Time_Hours'].mean():.2f} hours (for high productivity)
        - **Study Hours:** {df[df['Productivity_Score'] >= 9]['Study_Hours'].mean():.2f} hours (for high productivity)
        
        ### 📈 Model Performance:
        
        - **Model Type:** Linear Regression
        - **Features:** Screen Time Hours, Study Hours
        - **Target:** Productivity Score
        """)
    
    # Footer
    st.markdown("---")
    st.markdown("""
        <div style='text-align: center; color: #7f8c8d; padding: 20px;'>
            <p>📊 Developed by Data Science Team – Screen Time vs Productivity Analyzer 2025</p>
            <p>🚀 Built with Streamlit, Scikit-learn, Plotly & Python</p>
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()

