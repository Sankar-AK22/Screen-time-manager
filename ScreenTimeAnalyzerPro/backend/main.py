"""
FastAPI main application for ScreenTime Analyzer Pro.
Provides REST API endpoints and WebSocket streaming for real-time tracking.
"""

import asyncio
import platform
from contextlib import asynccontextmanager
from datetime import date, datetime
from typing import List, Set
import io
import csv

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends, Query, HTTPException
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from loguru import logger

# Configure logger
logger.add(
    "logs/screentime_{time:YYYY-MM-DD}.log",
    rotation="1 day",
    retention="30 days",
    level="INFO",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}"
)

from db import init_db, get_db, SessionLocal
from db.database import save_usage_with_retry
from db.models import UsageRecord
from tracker import RealtimeTracker
from analytics import (
    compute_daily_summary,
    get_top_apps,
    get_hourly_distribution,
    get_category_breakdown,
    get_usage_sessions,
    compute_productivity_insights
)
from schemas import (
    DailySummarySchema,
    TopAppSchema,
    UsageRecordSchema,
    CurrentSessionSchema,
    ProductivityInsightsSchema
)

# Global tracker instance
tracker: RealtimeTracker = None

# WebSocket connection manager
class ConnectionManager:
    """Manages WebSocket connections."""
    
    def __init__(self):
        self.active_connections: Set[WebSocket] = set()
    
    async def connect(self, websocket: WebSocket):
        """Accept and register a new WebSocket connection."""
        await websocket.accept()
        self.active_connections.add(websocket)
        logger.info(f"WebSocket connected. Total connections: {len(self.active_connections)}")
    
    def disconnect(self, websocket: WebSocket):
        """Remove a WebSocket connection."""
        self.active_connections.discard(websocket)
        logger.info(f"WebSocket disconnected. Total connections: {len(self.active_connections)}")
    
    async def broadcast(self, message: dict):
        """Broadcast message to all connected clients."""
        if not self.active_connections:
            return
        
        disconnected = set()
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception as e:
                logger.error(f"Error broadcasting to client: {e}")
                disconnected.add(connection)
        
        # Remove disconnected clients
        for conn in disconnected:
            self.disconnect(conn)

manager = ConnectionManager()


# Database callback for tracker
async def save_usage_callback(app_name: str, window_title: str, start_time: datetime,
                              end_time: datetime, duration_sec: int, category: str):
    """Callback to save usage record to database."""
    db = SessionLocal()
    try:
        success = save_usage_with_retry(
            db=db,
            app_name=app_name,
            window_title=window_title,
            start_time=start_time,
            end_time=end_time,
            duration_sec=duration_sec,
            category=category,
            source_os=platform.system()
        )
        
        if success:
            # Broadcast summary update
            summary = compute_daily_summary(db)
            top_apps = get_top_apps(db, limit=5)
            hourly = get_hourly_distribution(db)
            
            await manager.broadcast({
                "event": "summary_update",
                "today_total_sec": summary["total_seconds"],
                "top_apps": [{"app": app["app"], "sec": app["total_seconds"]} for app in top_apps],
                "hourly": hourly
            })
    finally:
        db.close()


# WebSocket broadcast callback for tracker
async def ws_broadcast_callback(message: dict):
    """Callback to broadcast messages to WebSocket clients."""
    await manager.broadcast(message)


# Application lifespan
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    global tracker
    
    # Startup
    logger.info("🚀 Starting ScreenTime Analyzer Pro Backend...")
    
    # Initialize database
    init_db()
    logger.info("✅ Database initialized")
    
    # Initialize tracker
    tracker = RealtimeTracker(
        db_save_callback=save_usage_callback,
        ws_broadcast_callback=ws_broadcast_callback
    )
    logger.info("✅ Tracker initialized")
    
    # Start tracking
    await tracker.start_tracking()
    logger.info("✅ Real-time tracking started")
    
    logger.info("🎉 ScreenTime Analyzer Pro is ready!")
    
    yield
    
    # Shutdown
    logger.info("🛑 Shutting down...")
    if tracker:
        await tracker.stop_tracking()
    logger.info("✅ Tracker stopped")


# Create FastAPI app
app = FastAPI(
    title="ScreenTime Analyzer Pro API",
    description="Real-time screen time tracking and analytics",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================================
# REST API ENDPOINTS
# ============================================================================

@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "app": "ScreenTime Analyzer Pro",
        "version": "1.0.0",
        "status": "running",
        "tracking": tracker.is_tracking if tracker else False
    }


@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "tracking": tracker.is_tracking if tracker else False,
        "platform": platform.system()
    }


@app.get("/api/summary/today", response_model=DailySummarySchema)
async def get_today_summary(db: Session = Depends(get_db)):
    """Get summary for today."""
    summary = compute_daily_summary(db)
    return summary


@app.get("/api/summary/{date_str}", response_model=DailySummarySchema)
async def get_summary_by_date(date_str: str, db: Session = Depends(get_db)):
    """Get summary for a specific date (YYYY-MM-DD)."""
    try:
        target_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        summary = compute_daily_summary(db, target_date)
        return summary
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")


@app.get("/api/usage/today", response_model=List[UsageRecordSchema])
async def get_today_usage(
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    """Get usage sessions for today."""
    sessions = get_usage_sessions(db, limit=limit, offset=offset)
    return sessions


@app.get("/api/usage/top", response_model=List[TopAppSchema])
async def get_top_apps_endpoint(
    limit: int = Query(5, ge=1, le=20),
    db: Session = Depends(get_db)
):
    """Get top N apps by usage time."""
    top_apps = get_top_apps(db, limit=limit)
    return top_apps


@app.get("/api/usage/hourly")
async def get_hourly_usage(db: Session = Depends(get_db)):
    """Get hourly distribution of screen time."""
    hourly = get_hourly_distribution(db)
    return {"hourly": hourly}


@app.get("/api/usage/categories")
async def get_category_usage(db: Session = Depends(get_db)):
    """Get usage breakdown by category."""
    breakdown = get_category_breakdown(db)
    return {"categories": breakdown}


@app.get("/api/insights", response_model=ProductivityInsightsSchema)
async def get_insights(db: Session = Depends(get_db)):
    """Get productivity insights and recommendations."""
    insights = compute_productivity_insights(db)
    return insights


@app.get("/api/current")
async def get_current_session():
    """Get current active session."""
    if not tracker:
        return {"active": False}

    session = tracker.get_current_session()
    if session:
        return {"active": True, "session": session}
    else:
        return {"active": False}


@app.get("/api/export/csv")
async def export_csv(
    date_str: str = Query(None, description="Date in YYYY-MM-DD format (default: today)"),
    db: Session = Depends(get_db)
):
    """Export usage data as CSV."""
    try:
        if date_str:
            target_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        else:
            target_date = date.today()

        sessions = get_usage_sessions(db, target_date, limit=10000)

        # Create CSV in memory
        output = io.StringIO()
        writer = csv.writer(output)

        # Write header
        writer.writerow([
            "App Name", "Window Title", "Start Time", "End Time",
            "Duration (seconds)", "Duration (formatted)", "Category", "OS"
        ])

        # Write data
        for session in sessions:
            duration_sec = session["duration_sec"]
            hours = duration_sec // 3600
            minutes = (duration_sec % 3600) // 60
            seconds = duration_sec % 60

            if hours > 0:
                duration_formatted = f"{hours}h {minutes}m {seconds}s"
            elif minutes > 0:
                duration_formatted = f"{minutes}m {seconds}s"
            else:
                duration_formatted = f"{seconds}s"

            writer.writerow([
                session["app_name"],
                session["window_title"] or "",
                session["start_time"],
                session["end_time"],
                duration_sec,
                duration_formatted,
                session["category"] or "Other",
                session["source_os"] or ""
            ])

        # Prepare response
        output.seek(0)
        filename = f"screentime_{target_date.isoformat()}.csv"

        return StreamingResponse(
            iter([output.getvalue()]),
            media_type="text/csv",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )

    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")
    except Exception as e:
        logger.error(f"Error exporting CSV: {e}")
        raise HTTPException(status_code=500, detail="Failed to export CSV")


# ============================================================================
# WEBSOCKET ENDPOINT
# ============================================================================

@app.websocket("/ws/usage")
async def websocket_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint for real-time usage updates.

    Clients will receive:
    - session_start: When a new app session starts
    - session_end: When an app session ends
    - heartbeat: Every 5 seconds with current session info
    - idle: When user becomes idle
    - summary_update: When daily summary changes
    """
    await manager.connect(websocket)

    try:
        # Send current session on connect
        if tracker:
            session = tracker.get_current_session()
            if session:
                await websocket.send_json({
                    "event": "current_session",
                    **session
                })

            # Send current summary
            db = get_db_session()
            try:
                summary = compute_daily_summary(db)
                top_apps = get_top_apps(db, limit=5)
                hourly = get_hourly_distribution(db)

                await websocket.send_json({
                    "event": "summary_update",
                    "today_total_sec": summary["total_seconds"],
                    "top_apps": [{"app": app["app"], "sec": app["total_seconds"]} for app in top_apps],
                    "hourly": hourly
                })
            finally:
                db.close()

        # Keep connection alive and handle incoming messages
        while True:
            try:
                data = await websocket.receive_text()

                # Handle ping/pong
                if data == "ping":
                    await websocket.send_json({"event": "pong"})

                # Handle get_current request
                elif data == "get_current":
                    if tracker:
                        session = tracker.get_current_session()
                        if session:
                            await websocket.send_json({
                                "event": "current_session",
                                **session
                            })
                        else:
                            await websocket.send_json({
                                "event": "no_active_session"
                            })

            except WebSocketDisconnect:
                break
            except Exception as e:
                logger.error(f"Error in WebSocket message handling: {e}")
                break

    except Exception as e:
        logger.error(f"WebSocket error: {e}")

    finally:
        manager.disconnect(websocket)


# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    import uvicorn

    logger.info("Starting ScreenTime Analyzer Pro Backend...")

    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=False,  # Set to True for development
        log_level="info"
    )

