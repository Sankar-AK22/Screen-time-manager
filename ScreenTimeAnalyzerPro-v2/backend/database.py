"""
Database models and session management
"""

import os
from datetime import datetime, timezone
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from loguru import logger

# Database setup
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)

DATABASE_URL = f"sqlite:///{os.path.join(DATA_DIR, 'screentime.db')}"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    echo=False
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Models
class UsageRecord(Base):
    """Usage record model"""
    __tablename__ = "usage_records"

    id = Column(Integer, primary_key=True, index=True)
    app_name = Column(String, index=True, nullable=False)
    window_title = Column(String, nullable=True)
    start_time = Column(DateTime(timezone=True), nullable=False, index=True)
    end_time = Column(DateTime(timezone=True), nullable=False)
    duration_seconds = Column(Integer, nullable=False)
    category = Column(String, index=True, nullable=False)
    source_os = Column(String, nullable=False)
    is_idle = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {
            "id": self.id,
            "app_name": self.app_name,
            "window_title": self.window_title,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat(),
            "duration_seconds": self.duration_seconds,
            "category": self.category,
            "source_os": self.source_os,
            "is_idle": self.is_idle
        }

def init_db():
    """Initialize database"""
    Base.metadata.create_all(bind=engine)
    logger.info(f"Database initialized at {DATABASE_URL}")

def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

