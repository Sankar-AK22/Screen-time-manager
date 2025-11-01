"""
Pydantic schemas for request/response validation.
"""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field


class UsageRecordSchema(BaseModel):
    """Schema for usage record."""
    id: int
    app_name: str
    window_title: Optional[str] = None
    start_time: datetime
    end_time: datetime
    duration_sec: int
    category: Optional[str] = None
    source_os: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


class DailySummarySchema(BaseModel):
    """Schema for daily summary."""
    date: str
    total_seconds: int
    total_hours: float
    session_count: int
    productive_seconds: int
    productive_hours: float
    entertainment_seconds: int
    entertainment_hours: float
    productivity_score: float
    unique_apps: int = 0
    total_sessions: int = 0
    most_productive_hour: Optional[str] = None


class TopAppSchema(BaseModel):
    """Schema for top app."""
    app: str
    category: str
    total_seconds: int
    total_hours: float
    session_count: int


class CategoryBreakdownSchema(BaseModel):
    """Schema for category breakdown."""
    category: str
    total_seconds: int
    percentage: float


class ProductivityInsightsSchema(BaseModel):
    """Schema for productivity insights."""
    productivity_score: float
    top_productive_app: Optional[str] = None
    top_distraction: Optional[str] = None
    recommendations: List[str] = []


class CurrentSessionSchema(BaseModel):
    """Schema for current active session."""
    app: str
    window_title: str
    elapsed_sec: int
    category: str
    start_time: str
    is_idle: bool


class WebSocketEventSchema(BaseModel):
    """Schema for WebSocket events."""
    event: str = Field(..., description="Event type: session_start, session_end, heartbeat, idle, summary_update")
    app: Optional[str] = None
    window_title: Optional[str] = None
    duration_sec: Optional[int] = None
    elapsed_sec: Optional[int] = None
    start: Optional[str] = None
    end: Optional[str] = None
    category: Optional[str] = None
    source_os: Optional[str] = None
    timestamp: Optional[str] = None
    idle_sec: Optional[int] = None
    today_total_sec: Optional[int] = None
    top_apps: Optional[List[TopAppSchema]] = None
    hourly: Optional[List[int]] = None

