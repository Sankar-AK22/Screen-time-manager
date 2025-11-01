"""
Analytics service for processing usage data and generating insights
"""
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from app.models.usage import AppUsage, DailySummary, AppCategory
import logging

logger = logging.getLogger(__name__)

class AnalyticsService:
    """
    Service for analyzing usage data and generating insights
    """
    
    @staticmethod
    def calculate_productivity_score(db: Session, start_date: datetime, end_date: datetime) -> float:
        """
        Calculate productivity score based on app categories and usage patterns
        Score: 0-10 scale
        """
        try:
            # Get all usage records in the period
            usage_records = db.query(AppUsage).filter(
                and_(
                    AppUsage.start_time >= start_date,
                    AppUsage.start_time <= end_date,
                    AppUsage.is_active == False
                )
            ).all()
            
            if not usage_records:
                return 5.0  # Default neutral score
            
            total_time = sum(record.duration_minutes for record in usage_records)
            if total_time == 0:
                return 5.0
            
            # Calculate weighted score based on categories
            productive_time = 0
            for record in usage_records:
                category = record.category or "Other"
                weight = AnalyticsService._get_category_weight(category)
                productive_time += record.duration_minutes * weight
            
            # Normalize to 0-10 scale
            score = (productive_time / total_time) * 10
            return min(10.0, max(0.0, score))
            
        except Exception as e:
            logger.error(f"Error calculating productivity score: {e}")
            return 5.0
    
    @staticmethod
    def _get_category_weight(category: str) -> float:
        """
        Get productivity weight for a category
        """
        weights = {
            "Development": 1.0,
            "Productivity": 0.9,
            "Communication": 0.7,
            "Browser": 0.5,
            "Design": 0.8,
            "Entertainment": 0.2,
            "Other": 0.5
        }
        return weights.get(category, 0.5)
    
    @staticmethod
    def get_usage_stats(db: Session, start_date: datetime, end_date: datetime) -> Dict:
        """
        Get comprehensive usage statistics for a period
        """
        try:
            # Get all completed usage records
            usage_records = db.query(AppUsage).filter(
                and_(
                    AppUsage.start_time >= start_date,
                    AppUsage.start_time <= end_date,
                    AppUsage.is_active == False
                )
            ).all()
            
            if not usage_records:
                return {
                    "total_screen_time": 0,
                    "total_apps": 0,
                    "most_used_apps": [],
                    "category_breakdown": {},
                    "hourly_distribution": {},
                    "productivity_score": 5.0
                }
            
            # Calculate total screen time
            total_screen_time = sum(record.duration_minutes for record in usage_records)
            
            # Get unique apps
            unique_apps = set(record.app_name for record in usage_records)
            total_apps = len(unique_apps)
            
            # Calculate most used apps
            app_usage = {}
            for record in usage_records:
                if record.app_name not in app_usage:
                    app_usage[record.app_name] = {
                        "app_name": record.app_name,
                        "duration": 0,
                        "category": record.category or "Other"
                    }
                app_usage[record.app_name]["duration"] += record.duration_minutes
            
            most_used_apps = sorted(
                app_usage.values(),
                key=lambda x: x["duration"],
                reverse=True
            )[:10]
            
            # Category breakdown
            category_breakdown = {}
            for record in usage_records:
                category = record.category or "Other"
                if category not in category_breakdown:
                    category_breakdown[category] = 0
                category_breakdown[category] += record.duration_minutes
            
            # Hourly distribution
            hourly_distribution = {}
            for record in usage_records:
                hour = record.start_time.hour
                if hour not in hourly_distribution:
                    hourly_distribution[hour] = 0
                hourly_distribution[hour] += record.duration_minutes
            
            # Calculate productivity score
            productivity_score = AnalyticsService.calculate_productivity_score(
                db, start_date, end_date
            )
            
            return {
                "total_screen_time": round(total_screen_time, 2),
                "total_apps": total_apps,
                "most_used_apps": most_used_apps,
                "category_breakdown": category_breakdown,
                "hourly_distribution": hourly_distribution,
                "productivity_score": round(productivity_score, 2)
            }
            
        except Exception as e:
            logger.error(f"Error getting usage stats: {e}")
            return {
                "total_screen_time": 0,
                "total_apps": 0,
                "most_used_apps": [],
                "category_breakdown": {},
                "hourly_distribution": {},
                "productivity_score": 5.0
            }
    
    @staticmethod
    def generate_daily_summary(db: Session, date: datetime) -> Optional[DailySummary]:
        """
        Generate daily summary for a specific date
        """
        try:
            # Set date range for the day
            start_of_day = date.replace(hour=0, minute=0, second=0, microsecond=0)
            end_of_day = start_of_day + timedelta(days=1)
            
            # Get usage stats
            stats = AnalyticsService.get_usage_stats(db, start_of_day, end_of_day)
            
            # Find most used app
            most_used_app = None
            most_used_duration = 0
            if stats["most_used_apps"]:
                most_used_app = stats["most_used_apps"][0]["app_name"]
                most_used_duration = stats["most_used_apps"][0]["duration"]
            
            # Calculate active hours
            active_hours = len([h for h, d in stats["hourly_distribution"].items() if d > 0])
            
            # Check if summary already exists
            existing_summary = db.query(DailySummary).filter(
                DailySummary.date == start_of_day
            ).first()
            
            if existing_summary:
                # Update existing summary
                existing_summary.total_screen_time_minutes = stats["total_screen_time"]
                existing_summary.total_apps_used = stats["total_apps"]
                existing_summary.most_used_app = most_used_app
                existing_summary.most_used_app_duration = most_used_duration
                existing_summary.productivity_score = stats["productivity_score"]
                existing_summary.active_hours = active_hours
                db.commit()
                db.refresh(existing_summary)
                return existing_summary
            else:
                # Create new summary
                summary = DailySummary(
                    date=start_of_day,
                    total_screen_time_minutes=stats["total_screen_time"],
                    total_apps_used=stats["total_apps"],
                    most_used_app=most_used_app,
                    most_used_app_duration=most_used_duration,
                    productivity_score=stats["productivity_score"],
                    active_hours=active_hours
                )
                db.add(summary)
                db.commit()
                db.refresh(summary)
                return summary
                
        except Exception as e:
            logger.error(f"Error generating daily summary: {e}")
            db.rollback()
            return None
    
    @staticmethod
    def get_insights(db: Session, start_date: datetime, end_date: datetime) -> Dict:
        """
        Generate insights and recommendations
        """
        stats = AnalyticsService.get_usage_stats(db, start_date, end_date)
        
        insights = []
        
        # Screen time insights
        total_hours = stats["total_screen_time"] / 60
        if total_hours > 8:
            insights.append({
                "type": "warning",
                "message": f"High screen time detected: {total_hours:.1f} hours. Consider taking more breaks."
            })
        elif total_hours < 2:
            insights.append({
                "type": "info",
                "message": f"Low screen time: {total_hours:.1f} hours. Great work-life balance!"
            })
        
        # Productivity insights
        if stats["productivity_score"] >= 7:
            insights.append({
                "type": "success",
                "message": f"Excellent productivity score: {stats['productivity_score']:.1f}/10"
            })
        elif stats["productivity_score"] < 5:
            insights.append({
                "type": "warning",
                "message": f"Low productivity score: {stats['productivity_score']:.1f}/10. Try focusing on productive apps."
            })
        
        # Peak hours
        if stats["hourly_distribution"]:
            peak_hour = max(stats["hourly_distribution"].items(), key=lambda x: x[1])
            insights.append({
                "type": "info",
                "message": f"Most active hour: {peak_hour[0]:02d}:00 with {peak_hour[1]:.0f} minutes"
            })
        
        return {
            "insights": insights,
            "stats": stats
        }

