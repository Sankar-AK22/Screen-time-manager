"""
Analytics module for computing daily summaries, top apps, and productivity scores.
"""

from datetime import datetime, date, timedelta, timezone
from typing import List, Dict, Any, Optional
from sqlalchemy import func
from sqlalchemy.orm import Session
from loguru import logger

from db.models import UsageRecord
from tracker.utils import get_productivity_score


def compute_daily_summary(db: Session, target_date: Optional[date] = None) -> Dict[str, Any]:
    """
    Compute daily summary for a specific date.
    
    Args:
        db: Database session
        target_date: Date to compute summary for (default: today)
        
    Returns:
        Dictionary with summary statistics
    """
    if target_date is None:
        target_date = date.today()
    
    # Get start and end of day in UTC
    start_of_day = datetime.combine(target_date, datetime.min.time()).replace(tzinfo=timezone.utc)
    end_of_day = datetime.combine(target_date, datetime.max.time()).replace(tzinfo=timezone.utc)
    
    try:
        # Total screen time
        total_seconds = db.query(func.sum(UsageRecord.duration_sec)).filter(
            UsageRecord.start_time >= start_of_day,
            UsageRecord.start_time <= end_of_day
        ).scalar() or 0
        
        # Count of sessions
        session_count = db.query(func.count(UsageRecord.id)).filter(
            UsageRecord.start_time >= start_of_day,
            UsageRecord.start_time <= end_of_day
        ).scalar() or 0
        
        # Productive vs entertainment time
        productive_seconds = 0
        entertainment_seconds = 0
        
        records = db.query(UsageRecord).filter(
            UsageRecord.start_time >= start_of_day,
            UsageRecord.start_time <= end_of_day
        ).all()
        
        for record in records:
            category = record.category or "Other"
            productivity_weight = get_productivity_score(category)
            
            if productivity_weight >= 0.7:
                productive_seconds += record.duration_sec
            elif productivity_weight <= 0.2:
                entertainment_seconds += record.duration_sec
        
        # Calculate productivity score as decimal (0.0 to 1.0)
        productivity_score = (productive_seconds / total_seconds) if total_seconds > 0 else 0.0

        return {
            "date": target_date.isoformat(),
            "total_seconds": int(total_seconds),
            "total_hours": round(total_seconds / 3600, 2),
            "session_count": session_count,
            "productive_seconds": productive_seconds,
            "productive_hours": round(productive_seconds / 3600, 2),
            "entertainment_seconds": entertainment_seconds,
            "entertainment_hours": round(entertainment_seconds / 3600, 2),
            "productivity_score": round(productivity_score, 3),
            "unique_apps": len(set(r.app_name for r in records)),
            "total_sessions": session_count,
            "most_productive_hour": None  # Can be calculated if needed
        }
    
    except Exception as e:
        logger.error(f"Error computing daily summary: {e}")
        return {
            "date": target_date.isoformat(),
            "total_seconds": 0,
            "total_hours": 0,
            "session_count": 0,
            "productive_seconds": 0,
            "productive_hours": 0,
            "entertainment_seconds": 0,
            "entertainment_hours": 0,
            "productivity_score": 0.0,
            "unique_apps": 0,
            "total_sessions": 0,
            "most_productive_hour": None
        }


def get_top_apps(db: Session, target_date: Optional[date] = None, limit: int = 5) -> List[Dict[str, Any]]:
    """
    Get top N apps by total usage time.
    
    Args:
        db: Database session
        target_date: Date to get top apps for (default: today)
        limit: Number of top apps to return
        
    Returns:
        List of dictionaries with app name and total seconds
    """
    if target_date is None:
        target_date = date.today()
    
    start_of_day = datetime.combine(target_date, datetime.min.time()).replace(tzinfo=timezone.utc)
    end_of_day = datetime.combine(target_date, datetime.max.time()).replace(tzinfo=timezone.utc)
    
    try:
        results = db.query(
            UsageRecord.app_name,
            UsageRecord.category,
            func.sum(UsageRecord.duration_sec).label('total_seconds'),
            func.count(UsageRecord.id).label('session_count')
        ).filter(
            UsageRecord.start_time >= start_of_day,
            UsageRecord.start_time <= end_of_day
        ).group_by(
            UsageRecord.app_name,
            UsageRecord.category
        ).order_by(
            func.sum(UsageRecord.duration_sec).desc()
        ).limit(limit).all()
        
        top_apps = []
        for result in results:
            top_apps.append({
                "app": result.app_name,
                "category": result.category or "Other",
                "total_seconds": int(result.total_seconds),
                "total_hours": round(result.total_seconds / 3600, 2),
                "session_count": result.session_count
            })
        
        return top_apps
    
    except Exception as e:
        logger.error(f"Error getting top apps: {e}")
        return []


def get_hourly_distribution(db: Session, target_date: Optional[date] = None) -> List[int]:
    """
    Get hourly distribution of screen time (24 buckets).
    
    Args:
        db: Database session
        target_date: Date to get distribution for (default: today)
        
    Returns:
        List of 24 integers representing seconds per hour
    """
    if target_date is None:
        target_date = date.today()
    
    start_of_day = datetime.combine(target_date, datetime.min.time()).replace(tzinfo=timezone.utc)
    end_of_day = datetime.combine(target_date, datetime.max.time()).replace(tzinfo=timezone.utc)
    
    # Initialize 24-hour array
    hourly = [0] * 24
    
    try:
        records = db.query(UsageRecord).filter(
            UsageRecord.start_time >= start_of_day,
            UsageRecord.start_time <= end_of_day
        ).all()
        
        for record in records:
            # Get hour of start time (in local time for display)
            hour = record.start_time.hour
            hourly[hour] += record.duration_sec
        
        return hourly
    
    except Exception as e:
        logger.error(f"Error getting hourly distribution: {e}")
        return hourly


def get_category_breakdown(db: Session, target_date: Optional[date] = None) -> Dict[str, int]:
    """
    Get breakdown of time by category.
    
    Args:
        db: Database session
        target_date: Date to get breakdown for (default: today)
        
    Returns:
        Dictionary mapping category to total seconds
    """
    if target_date is None:
        target_date = date.today()
    
    start_of_day = datetime.combine(target_date, datetime.min.time()).replace(tzinfo=timezone.utc)
    end_of_day = datetime.combine(target_date, datetime.max.time()).replace(tzinfo=timezone.utc)
    
    try:
        results = db.query(
            UsageRecord.category,
            func.sum(UsageRecord.duration_sec).label('total_seconds')
        ).filter(
            UsageRecord.start_time >= start_of_day,
            UsageRecord.start_time <= end_of_day
        ).group_by(
            UsageRecord.category
        ).all()
        
        breakdown = {}
        for result in results:
            category = result.category or "Other"
            breakdown[category] = int(result.total_seconds)
        
        return breakdown
    
    except Exception as e:
        logger.error(f"Error getting category breakdown: {e}")
        return {}


def get_usage_sessions(
    db: Session,
    target_date: Optional[date] = None,
    limit: int = 100,
    offset: int = 0
) -> List[Dict[str, Any]]:
    """
    Get list of usage sessions for a date.
    
    Args:
        db: Database session
        target_date: Date to get sessions for (default: today)
        limit: Maximum number of sessions to return
        offset: Offset for pagination
        
    Returns:
        List of session dictionaries
    """
    if target_date is None:
        target_date = date.today()
    
    start_of_day = datetime.combine(target_date, datetime.min.time()).replace(tzinfo=timezone.utc)
    end_of_day = datetime.combine(target_date, datetime.max.time()).replace(tzinfo=timezone.utc)
    
    try:
        records = db.query(UsageRecord).filter(
            UsageRecord.start_time >= start_of_day,
            UsageRecord.start_time <= end_of_day
        ).order_by(
            UsageRecord.start_time.desc()
        ).limit(limit).offset(offset).all()
        
        return [record.to_dict() for record in records]
    
    except Exception as e:
        logger.error(f"Error getting usage sessions: {e}")
        return []


def compute_productivity_insights(db: Session, target_date: Optional[date] = None) -> Dict[str, Any]:
    """
    Compute productivity insights and recommendations.
    
    Args:
        db: Database session
        target_date: Date to analyze (default: today)
        
    Returns:
        Dictionary with insights and recommendations
    """
    summary = compute_daily_summary(db, target_date)
    top_apps = get_top_apps(db, target_date, limit=3)
    
    insights = {
        "productivity_score": summary["productivity_score"],
        "top_productive_app": None,
        "top_distraction": None,
        "recommendations": []
    }
    
    # Find top productive app and distraction
    for app in top_apps:
        category = app["category"]
        productivity_weight = get_productivity_score(category)
        
        if productivity_weight >= 0.7 and not insights["top_productive_app"]:
            insights["top_productive_app"] = app["app"]
        elif productivity_weight <= 0.2 and not insights["top_distraction"]:
            insights["top_distraction"] = app["app"]
    
    # Generate recommendations (productivity_score is 0.0 to 1.0)
    if summary["productivity_score"] < 0.5:
        insights["recommendations"].append("Consider reducing entertainment app usage")

    if summary["entertainment_hours"] > 3:
        insights["recommendations"].append("Entertainment time is high - try setting limits")

    if summary["productive_hours"] > 6:
        insights["recommendations"].append("Great focus today! Keep it up!")

    if not insights["recommendations"]:
        insights["recommendations"].append("Keep tracking your screen time to get personalized insights")

    return insights

