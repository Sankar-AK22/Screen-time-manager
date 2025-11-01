"""
Pydantic schemas for API request/response validation
"""
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List

class AppUsageBase(BaseModel):
    app_name: str
    window_title: Optional[str] = None
    process_name: Optional[str] = None
    category: Optional[str] = None

class AppUsageCreate(AppUsageBase):
    start_time: datetime = Field(default_factory=datetime.utcnow)

class AppUsageResponse(AppUsageBase):
    id: int
    start_time: datetime
    end_time: Optional[datetime] = None
    duration_seconds: float
    duration_minutes: float
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class DailySummaryResponse(BaseModel):
    id: int
    date: datetime
    total_screen_time_minutes: float
    total_apps_used: int
    most_used_app: Optional[str] = None
    most_used_app_duration: float
    productivity_score: float
    active_hours: int
    
    class Config:
        from_attributes = True

class UsageStatsResponse(BaseModel):
    total_screen_time: float
    total_apps: int
    most_used_apps: List[dict]
    category_breakdown: dict
    hourly_distribution: dict
    productivity_score: float

class ReportRequest(BaseModel):
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    period: str = Field(default="today", pattern="^(today|week|month|custom)$")

class AppCategoryCreate(BaseModel):
    app_name: str
    category: str
    productivity_weight: float = Field(default=0.5, ge=0.0, le=1.0)

class AppCategoryResponse(BaseModel):
    id: int
    app_name: str
    category: str
    productivity_weight: float
    created_at: datetime
    
    class Config:
        from_attributes = True

class HealthCheckResponse(BaseModel):
    status: str
    timestamp: datetime
    tracking_active: bool
    database_connected: bool

