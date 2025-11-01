"""
Database models for usage tracking
"""
from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean
from sqlalchemy.sql import func
from datetime import datetime
from app.database.database import Base

class AppUsage(Base):
    """
    Model for tracking application usage
    """
    __tablename__ = "app_usage"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    app_name = Column(String, nullable=False, index=True)
    window_title = Column(String, nullable=True)
    process_name = Column(String, nullable=True)
    start_time = Column(DateTime, nullable=False, default=datetime.utcnow)
    end_time = Column(DateTime, nullable=True)
    duration_seconds = Column(Float, default=0.0)
    duration_minutes = Column(Float, default=0.0)
    is_active = Column(Boolean, default=True)
    category = Column(String, nullable=True)  # e.g., "Productivity", "Entertainment"
    created_at = Column(DateTime, server_default=func.now())
    
    def __repr__(self):
        return f"<AppUsage(app={self.app_name}, duration={self.duration_minutes}min)>"

class DailySummary(Base):
    """
    Model for daily usage summaries
    """
    __tablename__ = "daily_summary"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    date = Column(DateTime, nullable=False, unique=True, index=True)
    total_screen_time_minutes = Column(Float, default=0.0)
    total_apps_used = Column(Integer, default=0)
    most_used_app = Column(String, nullable=True)
    most_used_app_duration = Column(Float, default=0.0)
    productivity_score = Column(Float, default=0.0)  # 0-10 scale
    active_hours = Column(Integer, default=0)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    
    def __repr__(self):
        return f"<DailySummary(date={self.date}, screen_time={self.total_screen_time_minutes}min)>"

class AppCategory(Base):
    """
    Model for app categorization
    """
    __tablename__ = "app_categories"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    app_name = Column(String, nullable=False, unique=True, index=True)
    category = Column(String, nullable=False)  # Productivity, Entertainment, Development, etc.
    productivity_weight = Column(Float, default=0.5)  # 0-1 scale
    created_at = Column(DateTime, server_default=func.now())
    
    def __repr__(self):
        return f"<AppCategory(app={self.app_name}, category={self.category})>"

