"""
Real-time active window tracker with OS-specific implementations.
Tracks active window/app changes and emits events via WebSocket.
"""

import asyncio
import platform
import time
from datetime import datetime, timezone
from typing import Optional, Dict, Any, Callable, List
from loguru import logger

import psutil

from .utils import normalize_app_name, get_app_category, sanitize_window_title
from .idle_detector import IdleDetector


class RealtimeTracker:
    """
    Real-time tracker for active windows and applications.
    Supports Windows, macOS, and Linux (best-effort).
    """
    
    def __init__(self, db_save_callback: Callable, ws_broadcast_callback: Callable):
        """
        Initialize the realtime tracker.
        
        Args:
            db_save_callback: Async function to save usage records to database
            ws_broadcast_callback: Async function to broadcast events to WebSocket clients
        """
        self.db_save = db_save_callback
        self.ws_broadcast = ws_broadcast_callback
        
        self.current_app: Optional[str] = None
        self.current_window_title: Optional[str] = None
        self.session_start_time: Optional[float] = None
        self.last_heartbeat_time: Optional[float] = None
        
        self.is_tracking = False
        self.track_task: Optional[asyncio.Task] = None
        self.heartbeat_task: Optional[asyncio.Task] = None
        
        self.idle_detector = IdleDetector(idle_threshold_seconds=180)
        self.platform = platform.system()
        
        # Platform-specific setup
        self._setup_platform_specific()
        
        # Session deduplication
        self.last_saved_session: Optional[Dict[str, Any]] = None
        
        logger.info(f"RealtimeTracker initialized for {self.platform}")
    
    def _setup_platform_specific(self):
        """Setup platform-specific imports and configurations."""
        if self.platform == "Windows":
            try:
                import win32gui
                import win32process
                self.win32gui = win32gui
                self.win32process = win32process
                logger.info("Windows tracking modules loaded")
            except ImportError:
                logger.error("pywin32 not available - Windows tracking disabled")
                self.win32gui = None
                self.win32process = None
        
        elif self.platform == "Darwin":  # macOS
            try:
                from AppKit import NSWorkspace
                from Quartz import (
                    CGWindowListCopyWindowInfo,
                    kCGWindowListOptionOnScreenOnly,
                    kCGNullWindowID
                )
                self.NSWorkspace = NSWorkspace
                self.CGWindowListCopyWindowInfo = CGWindowListCopyWindowInfo
                self.kCGWindowListOptionOnScreenOnly = kCGWindowListOptionOnScreenOnly
                self.kCGNullWindowID = kCGNullWindowID
                logger.info("macOS tracking modules loaded")
            except ImportError:
                logger.error("PyObjC not available - macOS tracking disabled")
                self.NSWorkspace = None
    
    def _get_active_window_windows(self) -> Optional[Dict[str, str]]:
        """Get active window on Windows."""
        if not self.win32gui:
            return None
        
        try:
            # Get foreground window
            hwnd = self.win32gui.GetForegroundWindow()
            if not hwnd:
                return None
            
            # Get window title
            window_title = self.win32gui.GetWindowText(hwnd)
            
            # Get process ID
            _, pid = self.win32process.GetWindowThreadProcessId(hwnd)
            
            # Get process name
            try:
                process = psutil.Process(pid)
                app_name = process.name()
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                app_name = "UNKNOWN"
            
            return {
                "app_name": app_name,
                "window_title": window_title
            }
        
        except Exception as e:
            logger.error(f"Error getting active window on Windows: {e}")
            return None
    
    def _get_active_window_macos(self) -> Optional[Dict[str, str]]:
        """Get active window on macOS."""
        if not self.NSWorkspace:
            return None
        
        try:
            # Get active application
            workspace = self.NSWorkspace.sharedWorkspace()
            active_app = workspace.activeApplication()
            
            if not active_app:
                return None
            
            app_name = active_app.get('NSApplicationName', 'UNKNOWN')
            
            # Try to get window title from window list
            window_title = ""
            try:
                window_list = self.CGWindowListCopyWindowInfo(
                    self.kCGWindowListOptionOnScreenOnly,
                    self.kCGNullWindowID
                )
                
                for window in window_list:
                    if window.get('kCGWindowOwnerName') == app_name:
                        window_title = window.get('kCGWindowName', '')
                        if window_title:
                            break
            except Exception as e:
                logger.debug(f"Could not get window title: {e}")
            
            return {
                "app_name": app_name,
                "window_title": window_title
            }
        
        except Exception as e:
            logger.error(f"Error getting active window on macOS: {e}")
            return None
    
    def _get_active_window_linux(self) -> Optional[Dict[str, str]]:
        """Get active window on Linux (best-effort using psutil)."""
        try:
            # This is a fallback - try to find the most active process
            # In production, you'd use xdotool or wmctrl
            processes = []
            for proc in psutil.process_iter(['name', 'cpu_percent']):
                try:
                    info = proc.info
                    if info['cpu_percent'] and info['cpu_percent'] > 0:
                        processes.append(info)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
            
            if processes:
                # Sort by CPU usage
                processes.sort(key=lambda x: x['cpu_percent'], reverse=True)
                top_process = processes[0]
                
                return {
                    "app_name": top_process['name'],
                    "window_title": ""
                }
            
            return None
        
        except Exception as e:
            logger.error(f"Error getting active window on Linux: {e}")
            return None
    
    def get_active_window(self) -> Optional[Dict[str, str]]:
        """
        Get currently active window/app (platform-agnostic).
        
        Returns:
            Dict with 'app_name' and 'window_title', or None if unavailable
        """
        if self.platform == "Windows":
            return self._get_active_window_windows()
        elif self.platform == "Darwin":
            return self._get_active_window_macos()
        elif self.platform == "Linux":
            return self._get_active_window_linux()
        else:
            logger.warning(f"Unsupported platform: {self.platform}")
            return None
    
    async def _save_and_broadcast_session(self, app_name: str, window_title: str, 
                                         start_time: float, end_time: float):
        """Save session to database and broadcast to WebSocket clients."""
        duration_sec = int(end_time - start_time)
        
        if duration_sec < 1:
            return  # Ignore very short sessions
        
        # Normalize app name
        normalized_app = normalize_app_name(app_name)
        category = get_app_category(normalized_app)
        sanitized_title = sanitize_window_title(window_title)
        
        # Check for duplicate
        session_key = f"{normalized_app}_{int(start_time)}"
        if self.last_saved_session and self.last_saved_session.get("key") == session_key:
            logger.debug(f"Skipping duplicate session: {normalized_app}")
            return
        
        self.last_saved_session = {"key": session_key}
        
        # Save to database
        try:
            await self.db_save(
                app_name=normalized_app,
                window_title=sanitized_title,
                start_time=datetime.fromtimestamp(start_time, tz=timezone.utc),
                end_time=datetime.fromtimestamp(end_time, tz=timezone.utc),
                duration_sec=duration_sec,
                category=category
            )
            logger.info(f"Saved session: {normalized_app} ({duration_sec}s)")
        except Exception as e:
            logger.error(f"Failed to save session: {e}")
        
        # Broadcast session_end event
        try:
            await self.ws_broadcast({
                "event": "session_end",
                "app": normalized_app,
                "window_title": sanitized_title,
                "duration_sec": duration_sec,
                "start": datetime.fromtimestamp(start_time, tz=timezone.utc).isoformat(),
                "end": datetime.fromtimestamp(end_time, tz=timezone.utc).isoformat(),
                "source_os": self.platform,
                "category": category
            })
        except Exception as e:
            logger.error(f"Failed to broadcast session_end: {e}")

    async def _handle_idle(self, idle_duration: float):
        """Handle user becoming idle."""
        logger.info(f"User idle for {idle_duration:.0f}s - ending current session")

        # End current session if active
        if self.current_app and self.session_start_time:
            end_time = time.time()
            await self._save_and_broadcast_session(
                self.current_app,
                self.current_window_title or "",
                self.session_start_time,
                end_time
            )

            # Reset current session
            self.current_app = None
            self.current_window_title = None
            self.session_start_time = None

        # Broadcast idle event
        try:
            await self.ws_broadcast({
                "event": "idle",
                "idle_sec": int(idle_duration),
                "timestamp": datetime.now(timezone.utc).isoformat()
            })
        except Exception as e:
            logger.error(f"Failed to broadcast idle event: {e}")

    async def _tracking_loop(self):
        """Main tracking loop - checks active window every 1 second."""
        logger.info("Tracking loop started")

        while self.is_tracking:
            try:
                # Skip if user is idle
                if self.idle_detector.is_user_idle():
                    await asyncio.sleep(1)
                    continue

                # Get active window
                window_info = self.get_active_window()

                if not window_info:
                    await asyncio.sleep(1)
                    continue

                app_name = window_info["app_name"]
                window_title = window_info["window_title"]
                current_time = time.time()

                # Check if app changed
                if app_name != self.current_app:
                    # Save previous session if exists
                    if self.current_app and self.session_start_time:
                        await self._save_and_broadcast_session(
                            self.current_app,
                            self.current_window_title or "",
                            self.session_start_time,
                            current_time
                        )

                    # Start new session
                    self.current_app = app_name
                    self.current_window_title = window_title
                    self.session_start_time = current_time
                    self.last_heartbeat_time = current_time

                    normalized_app = normalize_app_name(app_name)
                    category = get_app_category(normalized_app)

                    logger.info(f"Switched to: {normalized_app}")

                    # Broadcast session_start
                    try:
                        await self.ws_broadcast({
                            "event": "session_start",
                            "app": normalized_app,
                            "window_title": sanitize_window_title(window_title),
                            "category": category,
                            "timestamp": datetime.fromtimestamp(current_time, tz=timezone.utc).isoformat()
                        })
                    except Exception as e:
                        logger.error(f"Failed to broadcast session_start: {e}")

                # Update window title if changed
                elif window_title != self.current_window_title:
                    self.current_window_title = window_title

                await asyncio.sleep(1)

            except Exception as e:
                logger.error(f"Error in tracking loop: {e}")
                await asyncio.sleep(1)

        logger.info("Tracking loop stopped")

    async def _heartbeat_loop(self):
        """Send heartbeat updates every 5 seconds for current session."""
        logger.info("Heartbeat loop started")

        while self.is_tracking:
            try:
                await asyncio.sleep(5)

                # Send heartbeat if session is active
                if self.current_app and self.session_start_time and not self.idle_detector.is_user_idle():
                    current_time = time.time()
                    elapsed_sec = int(current_time - self.session_start_time)

                    normalized_app = normalize_app_name(self.current_app)
                    category = get_app_category(normalized_app)

                    try:
                        await self.ws_broadcast({
                            "event": "heartbeat",
                            "app": normalized_app,
                            "window_title": sanitize_window_title(self.current_window_title or ""),
                            "elapsed_sec": elapsed_sec,
                            "category": category,
                            "timestamp": datetime.fromtimestamp(current_time, tz=timezone.utc).isoformat()
                        })
                    except Exception as e:
                        logger.error(f"Failed to broadcast heartbeat: {e}")

            except Exception as e:
                logger.error(f"Error in heartbeat loop: {e}")

        logger.info("Heartbeat loop stopped")

    async def start_tracking(self):
        """Start real-time tracking."""
        if self.is_tracking:
            logger.warning("Tracking already started")
            return

        self.is_tracking = True

        # Start idle detector
        self.idle_detector.start(
            idle_callback=self._handle_idle,
            active_callback=lambda: logger.info("User became active")
        )

        # Start tracking loop
        self.track_task = asyncio.create_task(self._tracking_loop())

        # Start heartbeat loop
        self.heartbeat_task = asyncio.create_task(self._heartbeat_loop())

        logger.info("Real-time tracking started")

    async def stop_tracking(self):
        """Stop real-time tracking."""
        if not self.is_tracking:
            return

        self.is_tracking = False

        # Save current session if active
        if self.current_app and self.session_start_time:
            end_time = time.time()
            await self._save_and_broadcast_session(
                self.current_app,
                self.current_window_title or "",
                self.session_start_time,
                end_time
            )

        # Stop idle detector
        self.idle_detector.stop()

        # Cancel tasks
        if self.track_task:
            self.track_task.cancel()
            try:
                await self.track_task
            except asyncio.CancelledError:
                pass

        if self.heartbeat_task:
            self.heartbeat_task.cancel()
            try:
                await self.heartbeat_task
            except asyncio.CancelledError:
                pass

        logger.info("Real-time tracking stopped")

    def get_current_session(self) -> Optional[Dict[str, Any]]:
        """Get current active session info."""
        if not self.current_app or not self.session_start_time:
            return None

        current_time = time.time()
        elapsed_sec = int(current_time - self.session_start_time)

        normalized_app = normalize_app_name(self.current_app)
        category = get_app_category(normalized_app)

        return {
            "app": normalized_app,
            "window_title": sanitize_window_title(self.current_window_title or ""),
            "elapsed_sec": elapsed_sec,
            "category": category,
            "start_time": datetime.fromtimestamp(self.session_start_time, tz=timezone.utc).isoformat(),
            "is_idle": self.idle_detector.is_user_idle()
        }

