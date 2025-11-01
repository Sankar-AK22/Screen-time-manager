"""
Visualization Module
Create static and interactive visualizations for the screen time analysis
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import joblib
import sys

# Set style for matplotlib
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

def load_data(filepath='data/cleaned_screen_time_data.csv'):
    """Load the cleaned dataset"""
    try:
        df = pd.read_csv(filepath)
        return df
    except Exception as e:
        print(f"❌ Error loading data: {e}")
        sys.exit(1)

def load_model(filepath='models/linear_regression_model.pkl'):
    """Load the trained model"""
    try:
        model = joblib.load(filepath)
        return model
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        sys.exit(1)

def plot_correlation_heatmap(df, save_path=None):
    """
    Create a correlation heatmap
    
    Args:
        df (pd.DataFrame): Input dataset
        save_path (str): Path to save the figure
        
    Returns:
        matplotlib.figure.Figure: The figure object
    """
    numeric_df = df.select_dtypes(include=[np.number])
    correlation = numeric_df.corr()
    
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(correlation, annot=True, fmt='.3f', cmap='coolwarm', 
                center=0, square=True, linewidths=1, cbar_kws={"shrink": 0.8},
                ax=ax)
    ax.set_title('Correlation Heatmap - Screen Time vs Productivity', 
                 fontsize=16, fontweight='bold', pad=20)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    return fig

def plot_screen_time_vs_productivity(df, model=None, save_path=None):
    """
    Create scatter plot with regression line for Screen Time vs Productivity
    
    Args:
        df (pd.DataFrame): Input dataset
        model: Trained model (optional)
        save_path (str): Path to save the figure
        
    Returns:
        matplotlib.figure.Figure: The figure object
    """
    fig, ax = plt.subplots(figsize=(12, 7))
    
    # Scatter plot
    ax.scatter(df['Screen_Time_Hours'], df['Productivity_Score'], 
               alpha=0.6, s=100, c='#3498db', edgecolors='black', linewidth=1.5,
               label='Actual Data')
    
    # Add regression line if model is provided
    if model is not None:
        # Create prediction line
        screen_time_range = np.linspace(df['Screen_Time_Hours'].min(), 
                                       df['Screen_Time_Hours'].max(), 100)
        mean_study_hours = df['Study_Hours'].mean()
        
        X_pred = np.column_stack([screen_time_range, 
                                  np.full(100, mean_study_hours)])
        y_pred = model.predict(X_pred)
        
        ax.plot(screen_time_range, y_pred, 'r--', linewidth=2.5, 
                label=f'Regression Line (Study Hours = {mean_study_hours:.2f})')
    
    ax.set_xlabel('Screen Time (Hours)', fontsize=14, fontweight='bold')
    ax.set_ylabel('Productivity Score', fontsize=14, fontweight='bold')
    ax.set_title('Screen Time vs Productivity Analysis', 
                 fontsize=16, fontweight='bold', pad=20)
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    return fig

def plot_study_hours_vs_productivity(df, save_path=None):
    """
    Create scatter plot for Study Hours vs Productivity
    
    Args:
        df (pd.DataFrame): Input dataset
        save_path (str): Path to save the figure
        
    Returns:
        matplotlib.figure.Figure: The figure object
    """
    fig, ax = plt.subplots(figsize=(12, 7))
    
    ax.scatter(df['Study_Hours'], df['Productivity_Score'], 
               alpha=0.6, s=100, c='#2ecc71', edgecolors='black', linewidth=1.5)
    
    # Add trend line
    z = np.polyfit(df['Study_Hours'], df['Productivity_Score'], 1)
    p = np.poly1d(z)
    ax.plot(df['Study_Hours'], p(df['Study_Hours']), 
            "r--", linewidth=2.5, label='Trend Line')
    
    ax.set_xlabel('Study Hours', fontsize=14, fontweight='bold')
    ax.set_ylabel('Productivity Score', fontsize=14, fontweight='bold')
    ax.set_title('Study Hours vs Productivity Analysis', 
                 fontsize=16, fontweight='bold', pad=20)
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    return fig

def create_interactive_3d_plot(df):
    """
    Create interactive 3D scatter plot using Plotly
    
    Args:
        df (pd.DataFrame): Input dataset
        
    Returns:
        plotly.graph_objects.Figure: Interactive figure
    """
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
            colorbar=dict(title="Productivity<br>Score"),
            line=dict(color='black', width=1)
        ),
        text=[f'Screen: {s:.2f}h<br>Study: {st:.2f}h<br>Productivity: {p:.2f}' 
              for s, st, p in zip(df['Screen_Time_Hours'], 
                                 df['Study_Hours'], 
                                 df['Productivity_Score'])],
        hoverinfo='text'
    )])
    
    fig.update_layout(
        title='3D Interactive View: Screen Time, Study Hours & Productivity',
        scene=dict(
            xaxis_title='Screen Time (Hours)',
            yaxis_title='Study Hours',
            zaxis_title='Productivity Score',
            camera=dict(eye=dict(x=1.5, y=1.5, z=1.3))
        ),
        width=900,
        height=700,
        font=dict(size=12)
    )
    
    return fig

def create_interactive_scatter(df):
    """
    Create interactive scatter plot using Plotly
    
    Args:
        df (pd.DataFrame): Input dataset
        
    Returns:
        plotly.graph_objects.Figure: Interactive figure
    """
    fig = px.scatter(df, x='Screen_Time_Hours', y='Productivity_Score',
                     size='Study_Hours', color='Study_Hours',
                     hover_data=['Screen_Time_Hours', 'Study_Hours', 'Productivity_Score'],
                     title='Interactive: Screen Time vs Productivity (Size = Study Hours)',
                     labels={'Screen_Time_Hours': 'Screen Time (Hours)',
                            'Productivity_Score': 'Productivity Score',
                            'Study_Hours': 'Study Hours'},
                     color_continuous_scale='Viridis')
    
    fig.update_traces(marker=dict(line=dict(width=1, color='DarkSlateGrey')))
    fig.update_layout(width=900, height=600, font=dict(size=12))
    
    return fig

def create_time_series_plot(df):
    """
    Create time series plot showing trends over time
    
    Args:
        df (pd.DataFrame): Input dataset
        
    Returns:
        plotly.graph_objects.Figure: Interactive figure
    """
    fig = make_subplots(rows=2, cols=1, 
                        subplot_titles=('Screen Time & Study Hours Over Time',
                                       'Productivity Score Over Time'),
                        vertical_spacing=0.15)
    
    # Add traces for screen time and study hours
    fig.add_trace(go.Scatter(x=df.index, y=df['Screen_Time_Hours'],
                            mode='lines+markers', name='Screen Time',
                            line=dict(color='#e74c3c', width=2)),
                 row=1, col=1)
    
    fig.add_trace(go.Scatter(x=df.index, y=df['Study_Hours'],
                            mode='lines+markers', name='Study Hours',
                            line=dict(color='#3498db', width=2)),
                 row=1, col=1)
    
    # Add trace for productivity
    fig.add_trace(go.Scatter(x=df.index, y=df['Productivity_Score'],
                            mode='lines+markers', name='Productivity',
                            line=dict(color='#2ecc71', width=2),
                            fill='tozeroy'),
                 row=2, col=1)
    
    fig.update_xaxes(title_text="Day", row=2, col=1)
    fig.update_yaxes(title_text="Hours", row=1, col=1)
    fig.update_yaxes(title_text="Score", row=2, col=1)
    
    fig.update_layout(height=700, width=900, 
                     title_text="Trends Over 30 Days",
                     showlegend=True)
    
    return fig

if __name__ == "__main__":
    print("📊 Generating visualizations...")
    
    # Load data and model
    df = load_data()
    model = load_model()
    
    # Create visualizations
    print("Creating correlation heatmap...")
    plot_correlation_heatmap(df)
    
    print("Creating screen time vs productivity plot...")
    plot_screen_time_vs_productivity(df, model)
    
    print("Creating study hours vs productivity plot...")
    plot_study_hours_vs_productivity(df)
    
    print("✅ Visualizations created successfully!")
    plt.show()

