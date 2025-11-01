"""
Background scheduler for tracking and analytics tasks
"""
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.database.database import SessionLocal
from app.models.usage import AppUsage
from app.services.tracker import tracker
from app.services.analytics import AnalyticsService
import logging

logger = logging.getLogger(__name__)

class TaskScheduler:
    """
    Manages background tasks for tracking and analytics
    """
    
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.current_session_id = None
        self.last_app_info = None
        
    def track_active_window(self):
        """
        Track currently active window (runs every minute)
        """
        if not tracker.get_tracking_status():
            return
        
        try:
            db: Session = SessionLocal()
            
            # Get current active window
            current_app_info = tracker.get_active_window()
            
            if not current_app_info:
                db.close()
                return
            
            # Check if app changed
            if self.last_app_info and self.last_app_info["app_name"] == current_app_info["app_name"]:
                # Same app, update duration
                if self.current_session_id:
                    session = db.query(AppUsage).filter(AppUsage.id == self.current_session_id).first()
                    if session and session.is_active:
                        session.end_time = datetime.utcnow()
                        duration_seconds = (session.end_time - session.start_time).total_seconds()
                        session.duration_seconds = duration_seconds
                        session.duration_minutes = duration_seconds / 60
                        db.commit()
            else:
                # App changed, close previous session and start new one
                if self.current_session_id:
                    session = db.query(AppUsage).filter(AppUsage.id == self.current_session_id).first()
                    if session and session.is_active:
                        session.end_time = datetime.utcnow()
                        duration_seconds = (session.end_time - session.start_time).total_seconds()
                        session.duration_seconds = duration_seconds
                        session.duration_minutes = duration_seconds / 60
                        session.is_active = False
                        db.commit()
                
                # Start new session
                category = tracker.categorize_app(current_app_info["app_name"])
                new_session = AppUsage(
                    app_name=current_app_info["app_name"],
                    window_title=current_app_info.get("window_title", ""),
                    process_name=current_app_info.get("process_name", ""),
                    start_time=datetime.utcnow(),
                    is_active=True,
                    category=category
                )
                db.add(new_session)
                db.commit()
                db.refresh(new_session)
                self.current_session_id = new_session.id
                
                logger.info(f"📊 Tracking: {current_app_info['app_name']} ({category})")
            
            self.last_app_info = current_app_info
            db.close()
            
        except Exception as e:
            logger.error(f"Error in track_active_window: {e}")
    
    def generate_daily_summaries(self):
        """
        Generate daily summaries (runs once per day)
        """
        try:
            db: Session = SessionLocal()
            
            # Generate summary for yesterday
            yesterday = datetime.utcnow() - timedelta(days=1)
            summary = AnalyticsService.generate_daily_summary(db, yesterday)
            
            if summary:
                logger.info(f"✅ Generated daily summary for {yesterday.date()}")
            
            db.close()
            
        except Exception as e:
            logger.error(f"Error generating daily summaries: {e}")
    
    def start(self):
        """
        Start the scheduler
        """
        # Track active window every 60 seconds
        self.scheduler.add_job(
            func=self.track_active_window,
            trigger=IntervalTrigger(seconds=60),
            id='track_window',
            name='Track active window',
            replace_existing=True
        )
        
        # Generate daily summaries at midnight
        self.scheduler.add_job(
            func=self.generate_daily_summaries,
            trigger='cron',
            hour=0,
            minute=5,
            id='daily_summary',
            name='Generate daily summary',
            replace_existing=True
        )
        
        self.scheduler.start()
        logger.info("🚀 Scheduler started successfully")
    
    def stop(self):
        """
        Stop the scheduler
        """
        self.scheduler.shutdown()
        logger.info("🛑 Scheduler stopped")

# Global scheduler instance
task_scheduler = TaskScheduler()

