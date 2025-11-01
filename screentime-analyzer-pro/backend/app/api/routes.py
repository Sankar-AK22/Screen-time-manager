"""
API routes for ScreenTime Analyzer Pro
"""
from fastapi import APIRouter, Depends, HTTPException, Query, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from sqlalchemy import and_, func
from datetime import datetime, timedelta
from typing import List, Optional
from app.database.database import get_db
from app.models.usage import AppUsage, DailySummary, AppCategory
from app.models.schemas import (
    AppUsageResponse, DailySummaryResponse, UsageStatsResponse,
    ReportRequest, AppCategoryCreate, AppCategoryResponse,
    HealthCheckResponse
)
from app.services.tracker import tracker
from app.services.analytics import AnalyticsService
import logging
import json

logger = logging.getLogger(__name__)
router = APIRouter()

# Global realtime tracker instance (will be set by main.py)
realtime_tracker = None

def set_realtime_tracker(tracker_instance):
    """Set the global realtime tracker instance"""
    global realtime_tracker
    realtime_tracker = tracker_instance

# Health check endpoint
@router.get("/health", response_model=HealthCheckResponse)
async def health_check(db: Session = Depends(get_db)):
    """
    Health check endpoint
    """
    try:
        # Test database connection
        db.execute("SELECT 1")
        db_connected = True
    except:
        db_connected = False
    
    return {
        "status": "healthy" if db_connected else "unhealthy",
        "timestamp": datetime.utcnow(),
        "tracking_active": tracker.get_tracking_status(),
        "database_connected": db_connected
    }

# Tracking control endpoints
@router.post("/tracking/start")
async def start_tracking():
    """
    Start screen time tracking
    """
    tracker.start_tracking()
    return {"message": "Tracking started", "status": "active"}

@router.post("/tracking/stop")
async def stop_tracking():
    """
    Stop screen time tracking
    """
    tracker.stop_tracking()
    return {"message": "Tracking stopped", "status": "inactive"}

@router.get("/tracking/status")
async def get_tracking_status():
    """
    Get current tracking status
    """
    return {
        "tracking_active": tracker.get_tracking_status(),
        "timestamp": datetime.utcnow()
    }

# Usage data endpoints
@router.get("/usage", response_model=List[AppUsageResponse])
async def get_usage_data(
    limit: int = Query(default=100, le=1000),
    offset: int = Query(default=0, ge=0),
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    db: Session = Depends(get_db)
):
    """
    Get usage data with optional filtering
    """
    query = db.query(AppUsage)
    
    if start_date:
        query = query.filter(AppUsage.start_time >= start_date)
    if end_date:
        query = query.filter(AppUsage.start_time <= end_date)
    
    usage_data = query.order_by(AppUsage.start_time.desc()).offset(offset).limit(limit).all()
    return usage_data

@router.get("/usage/current")
async def get_current_usage(db: Session = Depends(get_db)):
    """
    Get currently active usage session
    """
    current_session = db.query(AppUsage).filter(AppUsage.is_active == True).first()
    
    if not current_session:
        return {"message": "No active session", "data": None}
    
    # Calculate current duration
    duration_seconds = (datetime.utcnow() - current_session.start_time).total_seconds()
    
    return {
        "app_name": current_session.app_name,
        "window_title": current_session.window_title,
        "category": current_session.category,
        "start_time": current_session.start_time,
        "duration_minutes": round(duration_seconds / 60, 2)
    }

# Statistics endpoints
@router.get("/stats")
async def get_statistics(
    period: str = Query(default="today", regex="^(today|week|month|custom)$"),
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    db: Session = Depends(get_db)
):
    """
    Get usage statistics for a period
    """
    # Determine date range
    now = datetime.utcnow()
    
    if period == "today":
        start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        end = now
    elif period == "week":
        start = now - timedelta(days=7)
        end = now
    elif period == "month":
        start = now - timedelta(days=30)
        end = now
    elif period == "custom":
        if not start_date or not end_date:
            raise HTTPException(status_code=400, detail="start_date and end_date required for custom period")
        start = start_date
        end = end_date
    else:
        start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        end = now
    
    stats = AnalyticsService.get_usage_stats(db, start, end)
    return stats

@router.get("/stats/daily", response_model=List[DailySummaryResponse])
async def get_daily_summaries(
    days: int = Query(default=7, le=90),
    db: Session = Depends(get_db)
):
    """
    Get daily summaries for the last N days
    """
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=days)
    
    summaries = db.query(DailySummary).filter(
        and_(
            DailySummary.date >= start_date,
            DailySummary.date <= end_date
        )
    ).order_by(DailySummary.date.desc()).all()
    
    return summaries

# Report endpoints
@router.post("/report")
async def generate_report(
    request: ReportRequest,
    db: Session = Depends(get_db)
):
    """
    Generate usage report for a period
    """
    # Determine date range
    now = datetime.utcnow()
    
    if request.period == "today":
        start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        end = now
    elif request.period == "week":
        start = now - timedelta(days=7)
        end = now
    elif request.period == "month":
        start = now - timedelta(days=30)
        end = now
    elif request.period == "custom":
        if not request.start_date or not request.end_date:
            raise HTTPException(status_code=400, detail="start_date and end_date required for custom period")
        start = request.start_date
        end = request.end_date
    else:
        start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        end = now
    
    # Get insights
    insights_data = AnalyticsService.get_insights(db, start, end)
    
    return {
        "period": request.period,
        "start_date": start,
        "end_date": end,
        "insights": insights_data["insights"],
        "statistics": insights_data["stats"]
    }

# App category endpoints
@router.post("/categories", response_model=AppCategoryResponse)
async def create_app_category(
    category: AppCategoryCreate,
    db: Session = Depends(get_db)
):
    """
    Create or update app category
    """
    existing = db.query(AppCategory).filter(AppCategory.app_name == category.app_name).first()
    
    if existing:
        existing.category = category.category
        existing.productivity_weight = category.productivity_weight
        db.commit()
        db.refresh(existing)
        return existing
    
    new_category = AppCategory(**category.dict())
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category

@router.get("/categories", response_model=List[AppCategoryResponse])
async def get_app_categories(db: Session = Depends(get_db)):
    """
    Get all app categories
    """
    categories = db.query(AppCategory).all()
    return categories

# Summary endpoint
@router.get("/summary")
async def get_summary(db: Session = Depends(get_db)):
    """
    Get quick summary of today's usage
    """
    now = datetime.utcnow()
    start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
    
    stats = AnalyticsService.get_usage_stats(db, start_of_day, now)
    
    # Get current active app
    current_session = db.query(AppUsage).filter(AppUsage.is_active == True).first()
    current_app = None
    if current_session:
        duration_seconds = (now - current_session.start_time).total_seconds()
        current_app = {
            "app_name": current_session.app_name,
            "category": current_session.category,
            "duration_minutes": round(duration_seconds / 60, 2)
        }
    
    return {
        "date": start_of_day.date(),
        "total_screen_time_minutes": stats["total_screen_time"],
        "total_screen_time_hours": round(stats["total_screen_time"] / 60, 2),
        "total_apps_used": stats["total_apps"],
        "productivity_score": stats["productivity_score"],
        "current_app": current_app,
        "top_apps": stats["most_used_apps"][:5],
        "category_breakdown": stats["category_breakdown"]
    }


# WebSocket endpoint for real-time tracking
@router.websocket("/ws/realtime")
async def websocket_realtime_tracking(websocket: WebSocket):
    """
    WebSocket endpoint for real-time screen time tracking
    Streams live updates of app usage to connected clients
    """
    await websocket.accept()

    if realtime_tracker is None:
        await websocket.send_json({
            "type": "error",
            "message": "Real-time tracker not initialized"
        })
        await websocket.close()
        return

    # Add client to tracker
    realtime_tracker.add_websocket_client(websocket)

    try:
        # Send initial current session info
        current_session = realtime_tracker.get_current_session()
        if current_session:
            await websocket.send_json({
                "type": "current_session",
                **current_session
            })
        else:
            await websocket.send_json({
                "type": "no_active_session",
                "message": "No active tracking session"
            })

        # Keep connection alive and handle incoming messages
        while True:
            try:
                # Receive messages from client (ping/pong, commands, etc.)
                data = await websocket.receive_text()
                message = json.loads(data)

                # Handle client commands
                if message.get("type") == "ping":
                    await websocket.send_json({"type": "pong"})

                elif message.get("type") == "get_current":
                    current_session = realtime_tracker.get_current_session()
                    if current_session:
                        await websocket.send_json({
                            "type": "current_session",
                            **current_session
                        })
                    else:
                        await websocket.send_json({
                            "type": "no_active_session",
                            "message": "No active tracking session"
                        })

            except WebSocketDisconnect:
                break
            except json.JSONDecodeError:
                await websocket.send_json({
                    "type": "error",
                    "message": "Invalid JSON format"
                })
            except Exception as e:
                logger.error(f"Error in WebSocket loop: {e}")
                break

    finally:
        # Remove client from tracker
        realtime_tracker.remove_websocket_client(websocket)
        try:
            await websocket.close()
        except:
            pass


# Real-time tracking control endpoints
@router.post("/realtime/start")
async def start_realtime_tracking():
    """
    Start real-time tracking with WebSocket broadcasting
    """
    if realtime_tracker is None:
        raise HTTPException(status_code=500, detail="Real-time tracker not initialized")

    await realtime_tracker.start_tracking()
    return {
        "message": "Real-time tracking started",
        "status": "active",
        "websocket_url": "/api/v1/ws/realtime"
    }


@router.post("/realtime/stop")
async def stop_realtime_tracking():
    """
    Stop real-time tracking
    """
    if realtime_tracker is None:
        raise HTTPException(status_code=500, detail="Real-time tracker not initialized")

    await realtime_tracker.stop_tracking()
    return {
        "message": "Real-time tracking stopped",
        "status": "inactive"
    }


@router.get("/realtime/status")
async def get_realtime_tracking_status():
    """
    Get real-time tracking status
    """
    if realtime_tracker is None:
        return {
            "is_tracking": False,
            "current_session": None,
            "connected_clients": 0
        }

    current_session = realtime_tracker.get_current_session()

    return {
        "is_tracking": realtime_tracker.is_tracking,
        "current_session": current_session,
        "connected_clients": len(realtime_tracker.websocket_clients)
    }


@router.get("/realtime/current")
async def get_current_realtime_session():
    """
    Get current active session from real-time tracker
    """
    if realtime_tracker is None:
        raise HTTPException(status_code=500, detail="Real-time tracker not initialized")

    current_session = realtime_tracker.get_current_session()

    if current_session is None:
        return {
            "active": False,
            "message": "No active session"
        }

    return {
        "active": True,
        **current_session
    }

