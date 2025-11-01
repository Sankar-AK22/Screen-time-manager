"""
Main FastAPI application for ScreenTime Analyzer Pro
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging
from app.database.database import init_db, SessionLocal
from app.api.routes import router, set_realtime_tracker
from app.services.scheduler import task_scheduler
from app.services.tracker import tracker
from app.services.realtime_tracker import RealtimeTracker

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize realtime tracker
realtime_tracker = RealtimeTracker(db_session_factory=SessionLocal)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for startup and shutdown events
    """
    # Startup
    logger.info("🚀 Starting ScreenTime Analyzer Pro Backend...")

    # Initialize database
    init_db()
    logger.info("✅ Database initialized")

    # Set realtime tracker in routes
    set_realtime_tracker(realtime_tracker)
    logger.info("✅ Real-time tracker initialized")

    # Start tracking (legacy tracker)
    tracker.start_tracking()
    logger.info("✅ Legacy tracker started")

    # Start real-time tracking
    await realtime_tracker.start_tracking()
    logger.info("✅ Real-time tracker started")

    # Start scheduler
    task_scheduler.start()
    logger.info("✅ Scheduler started")

    logger.info("🎉 ScreenTime Analyzer Pro is ready with real-time tracking!")

    yield

    # Shutdown
    logger.info("🛑 Shutting down ScreenTime Analyzer Pro...")
    tracker.stop_tracking()
    await realtime_tracker.stop_tracking()
    task_scheduler.stop()
    logger.info("👋 Shutdown complete")

# Create FastAPI app
app = FastAPI(
    title="ScreenTime Analyzer Pro API",
    description="Backend API for tracking and analyzing screen time and app usage",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(router, prefix="/api/v1", tags=["ScreenTime Analyzer"])

@app.get("/")
async def root():
    """
    Root endpoint
    """
    return {
        "message": "Welcome to ScreenTime Analyzer Pro API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/api/v1/health"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

