"""
SQLAlchemy models for usage tracking.
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class UsageRecord(Base):
    """
    Model for storing app usage sessions.
    """
    __tablename__ = "usage_records"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    app_name = Column(String(200), nullable=False, index=True)
    window_title = Column(String(500), nullable=True)
    start_time = Column(DateTime(timezone=True), nullable=False, index=True)
    end_time = Column(DateTime(timezone=True), nullable=False)
    duration_sec = Column(Integer, nullable=False)
    category = Column(String(50), nullable=True, index=True)
    source_os = Column(String(50), nullable=True)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<UsageRecord(app={self.app_name}, duration={self.duration_sec}s)>"

    def to_dict(self):
        """Convert record to dictionary."""
        return {
            "id": self.id,
            "app_name": self.app_name,
            "window_title": self.window_title,
            "start_time": self.start_time.isoformat() if self.start_time else None,
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "duration_sec": self.duration_sec,
            "category": self.category,
            "source_os": self.source_os,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
    
    def to_dict(self):
        """Convert to dictionary for JSON serialization."""
        return {
            "id": self.id,
            "app_name": self.app_name,
            "window_title": self.window_title,
            "start_time": self.start_time.isoformat() if self.start_time else None,
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "duration_sec": self.duration_sec,
            "category": self.category,
            "source_os": self.source_os,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }

