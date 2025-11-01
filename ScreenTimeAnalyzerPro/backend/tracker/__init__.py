"""
Screen time tracker module for ScreenTime Analyzer Pro.
Provides real-time tracking of active windows and applications.
"""

from .realtime_tracker import RealtimeTracker
from .idle_detector import IdleDetector
from .utils import normalize_app_name, get_app_category

__all__ = ["RealtimeTracker", "IdleDetector", "normalize_app_name", "get_app_category"]

