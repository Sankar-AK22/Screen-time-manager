"""
Database connection and session management with retry logic.
"""

import os
import time
from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import OperationalError
from loguru import logger

from .models import Base

# Database file path
DB_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
os.makedirs(DB_DIR, exist_ok=True)
DB_PATH = os.path.join(DB_DIR, "screentime.db")

# SQLite connection string
SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_PATH}"

# Create engine with connection pooling
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={
        "check_same_thread": False,  # Allow multiple threads
        "timeout": 30  # 30 second timeout for locked database
    },
    pool_pre_ping=True,  # Verify connections before using
    pool_recycle=3600,  # Recycle connections after 1 hour
)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    """Initialize database - create all tables."""
    try:
        Base.metadata.create_all(bind=engine)
        logger.info(f"Database initialized at {DB_PATH}")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        raise


def get_db() -> Generator[Session, None, None]:
    """
    Dependency for FastAPI to get database session.
    
    Yields:
        Database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def save_usage_with_retry(
    db: Session,
    app_name: str,
    window_title: str,
    start_time,
    end_time,
    duration_sec: int,
    category: str,
    source_os: str,
    max_retries: int = 3
) -> bool:
    """
    Save usage record with retry logic for database locks.
    
    Args:
        db: Database session
        app_name: Application name
        window_title: Window title
        start_time: Session start time
        end_time: Session end time
        duration_sec: Duration in seconds
        category: App category
        source_os: Source operating system
        max_retries: Maximum retry attempts
        
    Returns:
        True if saved successfully, False otherwise
    """
    from .models import UsageRecord
    
    for attempt in range(max_retries):
        try:
            record = UsageRecord(
                app_name=app_name,
                window_title=window_title,
                start_time=start_time,
                end_time=end_time,
                duration_sec=duration_sec,
                category=category,
                source_os=source_os
            )
            
            db.add(record)
            db.commit()
            db.refresh(record)
            
            logger.debug(f"Saved usage record: {app_name} ({duration_sec}s)")
            return True
            
        except OperationalError as e:
            if "database is locked" in str(e).lower():
                logger.warning(f"Database locked, retry {attempt + 1}/{max_retries}")
                db.rollback()
                
                # Exponential backoff
                wait_time = (2 ** attempt) * 0.1  # 0.1s, 0.2s, 0.4s
                time.sleep(wait_time)
                
                if attempt == max_retries - 1:
                    logger.error(f"Failed to save after {max_retries} retries")
                    return False
            else:
                logger.error(f"Database error: {e}")
                db.rollback()
                return False
                
        except Exception as e:
            logger.error(f"Unexpected error saving usage: {e}")
            db.rollback()
            return False
    
    return False


def get_db_session() -> Session:
    """
    Get a new database session (for use outside FastAPI).
    
    Returns:
        Database session (must be closed by caller)
    """
    return SessionLocal()

