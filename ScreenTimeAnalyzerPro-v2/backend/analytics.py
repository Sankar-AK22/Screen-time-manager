"""
Analytics and reporting functions
"""

import os
import io
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Any
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from loguru import logger

from database import UsageRecord

PRODUCTIVE_CATEGORIES = ["Development", "Productivity", "Design"]
ENTERTAINMENT_CATEGORIES = ["Entertainment", "Browser"]

def get_daily_summary(db: Session, date: datetime = None) -> Dict[str, Any]:
    """Get daily summary statistics"""
    if date is None:
        date = datetime.now()
    
    start_of_day = datetime(date.year, date.month, date.day, 0, 0, 0, tzinfo=timezone.utc)
    end_of_day = start_of_day + timedelta(days=1)
    
    records = db.query(UsageRecord).filter(
        and_(
            UsageRecord.start_time >= start_of_day,
            UsageRecord.start_time < end_of_day,
            UsageRecord.is_idle == False
        )
    ).all()
    
    total_seconds = sum(r.duration_seconds for r in records)
    productive_seconds = sum(r.duration_seconds for r in records if r.category in PRODUCTIVE_CATEGORIES)
    entertainment_seconds = sum(r.duration_seconds for r in records if r.category in ENTERTAINMENT_CATEGORIES)
    
    unique_apps = len(set(r.app_name for r in records))
    total_sessions = len(records)
    
    # Calculate productivity score
    if total_seconds > 0:
        productivity_score = productive_seconds / total_seconds
    else:
        productivity_score = 0.0
    
    # Find most productive hour
    hourly_productive = {}
    for record in records:
        if record.category in PRODUCTIVE_CATEGORIES:
            hour = record.start_time.hour
            hourly_productive[hour] = hourly_productive.get(hour, 0) + record.duration_seconds
    
    most_productive_hour = None
    if hourly_productive:
        most_productive_hour = max(hourly_productive, key=hourly_productive.get)
        most_productive_hour = f"{most_productive_hour:02d}:00"
    
    return {
        "date": date.strftime("%Y-%m-%d"),
        "total_seconds": total_seconds,
        "total_hours": round(total_seconds / 3600, 2),
        "productive_seconds": productive_seconds,
        "productive_hours": round(productive_seconds / 3600, 2),
        "entertainment_seconds": entertainment_seconds,
        "entertainment_hours": round(entertainment_seconds / 3600, 2),
        "productivity_score": round(productivity_score, 2),
        "unique_apps": unique_apps,
        "total_sessions": total_sessions,
        "most_productive_hour": most_productive_hour
    }

def get_top_apps(db: Session, date: datetime = None, limit: int = 10) -> List[Dict[str, Any]]:
    """Get top apps by usage time"""
    if date is None:
        date = datetime.now()
    
    start_of_day = datetime(date.year, date.month, date.day, 0, 0, 0, tzinfo=timezone.utc)
    end_of_day = start_of_day + timedelta(days=1)
    
    results = db.query(
        UsageRecord.app_name,
        UsageRecord.category,
        func.sum(UsageRecord.duration_seconds).label('total_seconds'),
        func.count(UsageRecord.id).label('session_count')
    ).filter(
        and_(
            UsageRecord.start_time >= start_of_day,
            UsageRecord.start_time < end_of_day,
            UsageRecord.is_idle == False
        )
    ).group_by(
        UsageRecord.app_name,
        UsageRecord.category
    ).order_by(
        func.sum(UsageRecord.duration_seconds).desc()
    ).limit(limit).all()
    
    apps = []
    for row in results:
        apps.append({
            "app": row.app_name,
            "category": row.category,
            "total_seconds": row.total_seconds,
            "total_hours": round(row.total_seconds / 3600, 2),
            "session_count": row.session_count,
            "percentage": 0  # Will be calculated later
        })
    
    # Calculate percentages
    total_time = sum(app["total_seconds"] for app in apps)
    if total_time > 0:
        for app in apps:
            app["percentage"] = round((app["total_seconds"] / total_time) * 100, 1)
    
    return apps

def get_hourly_distribution(db: Session, date: datetime = None) -> List[Dict[str, Any]]:
    """Get hourly usage distribution"""
    if date is None:
        date = datetime.now()
    
    start_of_day = datetime(date.year, date.month, date.day, 0, 0, 0, tzinfo=timezone.utc)
    end_of_day = start_of_day + timedelta(days=1)
    
    records = db.query(UsageRecord).filter(
        and_(
            UsageRecord.start_time >= start_of_day,
            UsageRecord.start_time < end_of_day,
            UsageRecord.is_idle == False
        )
    ).all()
    
    hourly = {}
    for record in records:
        hour = record.start_time.hour
        hourly[hour] = hourly.get(hour, 0) + record.duration_seconds
    
    result = []
    for hour in range(24):
        result.append({
            "hour": f"{hour:02d}:00",
            "seconds": hourly.get(hour, 0),
            "minutes": round(hourly.get(hour, 0) / 60, 1)
        })
    
    return result

def get_insights(db: Session) -> Dict[str, Any]:
    """Get usage insights and comparisons"""
    today = datetime.now()
    yesterday = today - timedelta(days=1)
    
    today_summary = get_daily_summary(db, today)
    yesterday_summary = get_daily_summary(db, yesterday)
    
    # Calculate changes
    time_change = today_summary["total_seconds"] - yesterday_summary["total_seconds"]
    time_change_percent = 0
    if yesterday_summary["total_seconds"] > 0:
        time_change_percent = (time_change / yesterday_summary["total_seconds"]) * 100
    
    productivity_change = today_summary["productivity_score"] - yesterday_summary["productivity_score"]
    
    # Get most used category today
    start_of_day = datetime(today.year, today.month, today.day, 0, 0, 0, tzinfo=timezone.utc)
    end_of_day = start_of_day + timedelta(days=1)
    
    category_usage = db.query(
        UsageRecord.category,
        func.sum(UsageRecord.duration_seconds).label('total_seconds')
    ).filter(
        and_(
            UsageRecord.start_time >= start_of_day,
            UsageRecord.start_time < end_of_day,
            UsageRecord.is_idle == False
        )
    ).group_by(UsageRecord.category).order_by(
        func.sum(UsageRecord.duration_seconds).desc()
    ).first()
    
    most_used_category = category_usage.category if category_usage else "None"
    
    return {
        "today": today_summary,
        "yesterday": yesterday_summary,
        "time_change_seconds": time_change,
        "time_change_percent": round(time_change_percent, 1),
        "productivity_change": round(productivity_change, 2),
        "most_used_category": most_used_category
    }

def export_to_csv(db: Session, date: datetime = None) -> str:
    """Export data to CSV"""
    if date is None:
        date = datetime.now()
    
    start_of_day = datetime(date.year, date.month, date.day, 0, 0, 0, tzinfo=timezone.utc)
    end_of_day = start_of_day + timedelta(days=1)
    
    records = db.query(UsageRecord).filter(
        and_(
            UsageRecord.start_time >= start_of_day,
            UsageRecord.start_time < end_of_day
        )
    ).all()
    
    data = []
    for record in records:
        data.append({
            "App": record.app_name,
            "Window Title": record.window_title,
            "Category": record.category,
            "Start Time": record.start_time.strftime("%Y-%m-%d %H:%M:%S"),
            "End Time": record.end_time.strftime("%Y-%m-%d %H:%M:%S"),
            "Duration (seconds)": record.duration_seconds,
            "Duration (minutes)": round(record.duration_seconds / 60, 2)
        })
    
    df = pd.DataFrame(data)
    return df.to_csv(index=False)

def export_to_pdf(db: Session, date: datetime = None) -> str:
    """Export data to PDF"""
    if date is None:
        date = datetime.now()
    
    # Create PDF
    filename = f"screentime_{date.strftime('%Y%m%d')}.pdf"
    filepath = os.path.join("data", filename)
    
    doc = SimpleDocTemplate(filepath, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()
    
    # Title
    title = Paragraph(f"ScreenTime Report - {date.strftime('%Y-%m-%d')}", styles['Title'])
    elements.append(title)
    elements.append(Spacer(1, 12))
    
    # Summary
    summary = get_daily_summary(db, date)
    summary_data = [
        ["Metric", "Value"],
        ["Total Screen Time", f"{summary['total_hours']} hours"],
        ["Productive Time", f"{summary['productive_hours']} hours"],
        ["Entertainment Time", f"{summary['entertainment_hours']} hours"],
        ["Productivity Score", f"{summary['productivity_score'] * 100:.0f}%"],
        ["Apps Used", str(summary['unique_apps'])],
        ["Sessions", str(summary['total_sessions'])]
    ]
    
    summary_table = Table(summary_data)
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    elements.append(summary_table)
    elements.append(Spacer(1, 20))
    
    # Top Apps
    top_apps = get_top_apps(db, date, limit=10)
    if top_apps:
        elements.append(Paragraph("Top Applications", styles['Heading2']))
        elements.append(Spacer(1, 12))
        
        app_data = [["App", "Category", "Time (hours)", "Sessions"]]
        for app in top_apps:
            app_data.append([
                app['app'],
                app['category'],
                f"{app['total_hours']}",
                str(app['session_count'])
            ])
        
        app_table = Table(app_data)
        app_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        elements.append(app_table)
    
    doc.build(elements)
    logger.info(f"PDF exported to {filepath}")
    
    return filepath

