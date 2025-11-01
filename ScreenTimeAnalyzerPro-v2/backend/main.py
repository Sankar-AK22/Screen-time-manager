"""
ScreenTime Analyzer Pro - FastAPI Backend
Real-time Windows app tracking with WebSocket support
"""

import asyncio
import platform
import time
from datetime import datetime, timezone, timedelta
from typing import Optional, Dict, Any, List
from contextlib import asynccontextmanager

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, StreamingResponse
from loguru import logger

from database import init_db, SessionLocal, UsageRecord
from tracker import WindowTracker
from analytics import (
    get_daily_summary,
    get_top_apps,
    get_hourly_distribution,
    get_insights,
    export_to_csv,
    export_to_pdf
)

# WebSocket connection manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info(f"WebSocket connected. Total connections: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
        logger.info(f"WebSocket disconnected. Total connections: {len(self.active_connections)}")

    async def broadcast(self, message: dict):
        """Broadcast message to all connected clients"""
        for connection in self.active_connections[:]:
            try:
                await connection.send_json(message)
            except Exception as e:
                logger.error(f"Error broadcasting to client: {e}")
                self.active_connections.remove(connection)

manager = ConnectionManager()
tracker: Optional[WindowTracker] = None

# Lifespan context manager
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events"""
    global tracker
    
    logger.info("🚀 Starting ScreenTime Analyzer Pro Backend...")
    
    # Initialize database
    init_db()
    logger.info("✅ Database initialized")
    
    # Initialize and start tracker
    tracker = WindowTracker(
        db_callback=save_usage_record,
        ws_callback=broadcast_update
    )
    await tracker.start()
    logger.info("✅ Tracker started")
    
    logger.info("🎉 ScreenTime Analyzer Pro is ready!")
    
    yield
    
    # Shutdown
    logger.info("🛑 Shutting down...")
    if tracker:
        await tracker.stop()
    logger.info("✅ Tracker stopped")

# Create FastAPI app
app = FastAPI(
    title="ScreenTime Analyzer Pro API",
    description="Real-time screen time tracking and analytics",
    version="2.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database callback
async def save_usage_record(app_name: str, window_title: str, start_time: datetime,
                           end_time: datetime, duration_sec: int, category: str):
    """Save usage record to database"""
    db = SessionLocal()
    try:
        record = UsageRecord(
            app_name=app_name,
            window_title=window_title,
            start_time=start_time,
            end_time=end_time,
            duration_seconds=duration_sec,
            category=category,
            source_os=platform.system()
        )
        db.add(record)
        db.commit()
        logger.info(f"Saved: {app_name} - {duration_sec}s")
    except Exception as e:
        logger.error(f"Error saving record: {e}")
        db.rollback()
    finally:
        db.close()

# WebSocket callback
async def broadcast_update(event_type: str, data: dict):
    """Broadcast update to all WebSocket clients"""
    message = {"event": event_type, **data}
    await manager.broadcast(message)

# WebSocket endpoint
@app.websocket("/ws/usage")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # Keep connection alive and listen for messages
            # Use asyncio.wait_for to prevent blocking and reduce CPU usage
            try:
                data = await asyncio.wait_for(websocket.receive_text(), timeout=1.0)
                if data == "ping":
                    await websocket.send_json({"event": "pong"})
                elif data == "get_current":
                    if tracker:
                        current = tracker.get_current_session()
                        if current:
                            await websocket.send_json({"event": "current_session", **current})
                        else:
                            await websocket.send_json({"event": "no_active_session"})
            except asyncio.TimeoutError:
                # No message received, continue loop (reduces CPU usage)
                continue
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        manager.disconnect(websocket)

# REST API Endpoints
@app.get("/")
async def root():
    return {
        "app": "ScreenTime Analyzer Pro",
        "version": "2.0.0",
        "status": "running",
        "tracking": tracker.is_tracking if tracker else False
    }

@app.get("/api/active-app")
async def get_active_app():
    """Get currently active application"""
    if not tracker:
        return {"active": False}
    
    current = tracker.get_current_session()
    if current:
        return {"active": True, "session": current}
    return {"active": False}

@app.get("/api/summary")
async def get_summary(date: Optional[str] = None):
    """Get daily summary statistics"""
    db = SessionLocal()
    try:
        target_date = datetime.fromisoformat(date) if date else datetime.now()
        summary = get_daily_summary(db, target_date)
        return summary
    finally:
        db.close()

@app.get("/api/apps")
async def get_apps(date: Optional[str] = None, limit: int = 10):
    """Get list of apps used today"""
    db = SessionLocal()
    try:
        target_date = datetime.fromisoformat(date) if date else datetime.now()
        apps = get_top_apps(db, target_date, limit)
        return {"apps": apps}
    finally:
        db.close()

@app.get("/api/hourly")
async def get_hourly(date: Optional[str] = None):
    """Get hourly usage distribution"""
    db = SessionLocal()
    try:
        target_date = datetime.fromisoformat(date) if date else datetime.now()
        hourly = get_hourly_distribution(db, target_date)
        return {"hourly": hourly}
    finally:
        db.close()

@app.get("/api/insights")
async def get_insights_endpoint():
    """Get usage insights and comparisons"""
    db = SessionLocal()
    try:
        insights = get_insights(db)
        return insights
    finally:
        db.close()

@app.get("/api/export/csv")
async def export_csv(date: Optional[str] = None):
    """Export data to CSV"""
    db = SessionLocal()
    try:
        target_date = datetime.fromisoformat(date) if date else datetime.now()
        csv_content = export_to_csv(db, target_date)
        
        filename = f"screentime_{target_date.strftime('%Y%m%d')}.csv"
        return StreamingResponse(
            iter([csv_content]),
            media_type="text/csv",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
    finally:
        db.close()

@app.get("/api/export/pdf")
async def export_pdf_endpoint(date: Optional[str] = None):
    """Export data to PDF"""
    db = SessionLocal()
    try:
        target_date = datetime.fromisoformat(date) if date else datetime.now()
        pdf_path = export_to_pdf(db, target_date)
        
        return FileResponse(
            pdf_path,
            media_type="application/pdf",
            filename=f"screentime_{target_date.strftime('%Y%m%d')}.pdf"
        )
    finally:
        db.close()

@app.get("/api/categories")
async def get_categories():
    """Get all app categories"""
    from tracker import APP_CATEGORIES
    return {"categories": APP_CATEGORIES}

@app.post("/api/categories/{app_name}")
async def update_category(app_name: str, category: str):
    """Update app category"""
    # TODO: Implement custom category storage
    return {"success": True, "app": app_name, "category": category}

if __name__ == "__main__":
    import uvicorn
    logger.info("Starting ScreenTime Analyzer Pro Backend...")
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")

