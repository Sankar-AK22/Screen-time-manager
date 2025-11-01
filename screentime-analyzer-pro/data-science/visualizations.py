"""
Data Science Visualization Module
Advanced visualizations for screen time analysis
"""
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List

class ScreenTimeVisualizer:
    """
    Advanced visualization class for screen time data
    """
    
    @staticmethod
    def create_usage_timeline(usage_data: List[Dict]) -> go.Figure:
        """
        Create interactive timeline of app usage
        """
        df = pd.DataFrame(usage_data)
        
        if df.empty:
            return go.Figure().add_annotation(
                text="No data available",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False
            )
        
        fig = px.timeline(
            df,
            x_start="start_time",
            x_end="end_time",
            y="app_name",
            color="category",
            title="Application Usage Timeline",
            labels={"app_name": "Application", "category": "Category"}
        )
        
        fig.update_layout(
            height=600,
            xaxis_title="Time",
            yaxis_title="Application",
            showlegend=True
        )
        
        return fig
    
    @staticmethod
    def create_category_pie_chart(category_data: Dict) -> go.Figure:
        """
        Create pie chart for category breakdown
        """
        if not category_data:
            return go.Figure().add_annotation(
                text="No data available",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False
            )
        
        labels = list(category_data.keys())
        values = list(category_data.values())
        
        colors = {
            "Development": "#667eea",
            "Productivity": "#4ade80",
            "Browser": "#60a5fa",
            "Communication": "#f59e0b",
            "Entertainment": "#ec4899",
            "Design": "#8b5cf6",
            "Other": "#94a3b8"
        }
        
        color_list = [colors.get(label, "#94a3b8") for label in labels]
        
        fig = go.Figure(data=[go.Pie(
            labels=labels,
            values=values,
            hole=0.4,
            marker=dict(colors=color_list),
            textinfo='label+percent',
            textposition='outside'
        )])
        
        fig.update_layout(
            title="Usage by Category",
            height=500,
            showlegend=True
        )
        
        return fig
    
    @staticmethod
    def create_hourly_heatmap(hourly_data: Dict) -> go.Figure:
        """
        Create heatmap of hourly usage patterns
        """
        if not hourly_data:
            return go.Figure().add_annotation(
                text="No data available",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False
            )
        
        # Create 24-hour array
        hours = list(range(24))
        values = [hourly_data.get(h, 0) for h in hours]
        
        # Reshape for heatmap (4 rows x 6 cols)
        heatmap_data = np.array(values).reshape(4, 6)
        
        hour_labels = [
            [f"{h:02d}:00" for h in hours[i*6:(i+1)*6]]
            for i in range(4)
        ]
        
        fig = go.Figure(data=go.Heatmap(
            z=heatmap_data,
            text=hour_labels,
            texttemplate="%{text}<br>%{z:.0f}min",
            colorscale="Viridis",
            showscale=True
        ))
        
        fig.update_layout(
            title="Hourly Usage Heatmap",
            height=400,
            xaxis_title="",
            yaxis_title="",
            xaxis=dict(showticklabels=False),
            yaxis=dict(showticklabels=False)
        )
        
        return fig
    
    @staticmethod
    def create_productivity_gauge(score: float) -> go.Figure:
        """
        Create gauge chart for productivity score
        """
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=score,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Productivity Score", 'font': {'size': 24}},
            delta={'reference': 7.0, 'increasing': {'color': "green"}},
            gauge={
                'axis': {'range': [None, 10], 'tickwidth': 1, 'tickcolor': "darkblue"},
                'bar': {'color': "darkblue"},
                'bgcolor': "white",
                'borderwidth': 2,
                'bordercolor': "gray",
                'steps': [
                    {'range': [0, 4], 'color': '#fee2e2'},
                    {'range': [4, 7], 'color': '#fef3c7'},
                    {'range': [7, 10], 'color': '#d1fae5'}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 7
                }
            }
        ))
        
        fig.update_layout(
            height=400,
            font={'color': "darkblue", 'family': "Arial"}
        )
        
        return fig
    
    @staticmethod
    def create_top_apps_bar_chart(top_apps: List[Dict]) -> go.Figure:
        """
        Create bar chart for top applications
        """
        if not top_apps:
            return go.Figure().add_annotation(
                text="No data available",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False
            )
        
        df = pd.DataFrame(top_apps)
        df = df.sort_values('duration', ascending=True)
        
        fig = go.Figure(data=[
            go.Bar(
                x=df['duration'],
                y=df['app_name'],
                orientation='h',
                marker=dict(
                    color=df['duration'],
                    colorscale='Viridis',
                    showscale=True
                ),
                text=[f"{d:.1f} min" for d in df['duration']],
                textposition='auto'
            )
        ])
        
        fig.update_layout(
            title="Top Applications by Usage Time",
            xaxis_title="Duration (minutes)",
            yaxis_title="Application",
            height=500,
            showlegend=False
        )
        
        return fig
    
    @staticmethod
    def create_weekly_trend(daily_summaries: List[Dict]) -> go.Figure:
        """
        Create line chart for weekly trends
        """
        if not daily_summaries:
            return go.Figure().add_annotation(
                text="No data available",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False
            )
        
        df = pd.DataFrame(daily_summaries)
        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values('date')
        
        fig = make_subplots(
            rows=2, cols=1,
            subplot_titles=("Screen Time Trend", "Productivity Score Trend"),
            vertical_spacing=0.15
        )
        
        # Screen time trend
        fig.add_trace(
            go.Scatter(
                x=df['date'],
                y=df['total_screen_time_minutes'] / 60,
                mode='lines+markers',
                name='Screen Time',
                line=dict(color='#667eea', width=3),
                marker=dict(size=8)
            ),
            row=1, col=1
        )
        
        # Productivity trend
        fig.add_trace(
            go.Scatter(
                x=df['date'],
                y=df['productivity_score'],
                mode='lines+markers',
                name='Productivity',
                line=dict(color='#4ade80', width=3),
                marker=dict(size=8),
                fill='tozeroy'
            ),
            row=2, col=1
        )
        
        fig.update_xaxes(title_text="Date", row=2, col=1)
        fig.update_yaxes(title_text="Hours", row=1, col=1)
        fig.update_yaxes(title_text="Score (0-10)", row=2, col=1)
        
        fig.update_layout(
            height=700,
            showlegend=True,
            title_text="Weekly Usage Trends"
        )
        
        return fig
    
    @staticmethod
    def create_dashboard_summary(stats: Dict) -> go.Figure:
        """
        Create comprehensive dashboard summary
        """
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=(
                "Category Distribution",
                "Productivity Score",
                "Top 5 Apps",
                "Hourly Activity"
            ),
            specs=[
                [{"type": "pie"}, {"type": "indicator"}],
                [{"type": "bar"}, {"type": "bar"}]
            ]
        )
        
        # Category pie chart
        if stats.get('category_breakdown'):
            labels = list(stats['category_breakdown'].keys())
            values = list(stats['category_breakdown'].values())
            
            fig.add_trace(
                go.Pie(labels=labels, values=values, hole=0.3),
                row=1, col=1
            )
        
        # Productivity gauge
        fig.add_trace(
            go.Indicator(
                mode="gauge+number",
                value=stats.get('productivity_score', 5.0),
                domain={'x': [0, 1], 'y': [0, 1]},
                gauge={'axis': {'range': [None, 10]}}
            ),
            row=1, col=2
        )
        
        # Top apps bar chart
        if stats.get('most_used_apps'):
            top_5 = stats['most_used_apps'][:5]
            fig.add_trace(
                go.Bar(
                    x=[app['app_name'] for app in top_5],
                    y=[app['duration'] for app in top_5],
                    marker_color='#667eea'
                ),
                row=2, col=1
            )
        
        # Hourly activity
        if stats.get('hourly_distribution'):
            hours = sorted(stats['hourly_distribution'].keys())
            values = [stats['hourly_distribution'][h] for h in hours]
            
            fig.add_trace(
                go.Bar(
                    x=[f"{h:02d}:00" for h in hours],
                    y=values,
                    marker_color='#4ade80'
                ),
                row=2, col=2
            )
        
        fig.update_layout(
            height=800,
            showlegend=False,
            title_text="Dashboard Summary"
        )
        
        return fig

