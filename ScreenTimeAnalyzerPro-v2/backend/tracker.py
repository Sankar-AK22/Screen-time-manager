"""
Windows application tracker with idle detection
"""

import asyncio
import platform
import time
from datetime import datetime, timezone
from typing import Optional, Dict, Any, Callable
from loguru import logger

import psutil
from pynput import mouse, keyboard

# Platform-specific imports
if platform.system() == "Windows":
    try:
        import win32gui
        import win32process
        import pygetwindow as gw
    except ImportError:
        logger.warning("Windows tracking modules not available")

# App categorization with enhanced rules
PRODUCTIVE_APPS = [
    "visual studio code", "code", "vscode",
    "postman",
    "spring tools", "spring tool suite", "sts",
    "android studio",
    "terminal", "cmd", "powershell", "bash",
    "pycharm", "intellij", "eclipse", "netbeans",
    "sublime", "atom", "notepad++",
    "git", "github desktop",
]

ENTERTAINMENT_APPS = [
    "whatsapp",
    "instagram",
    "youtube",
    "spotify",
    "netflix",
    "steam", "steamwebhelper",
    "epic games", "epicgameslauncher",
    "discord",  # Can be entertainment or communication
    "vlc", "media player",
    "twitch",
    "facebook", "twitter", "tiktok",
]

BROWSER_APPS = [
    "chrome", "msedge", "edge", "firefox", "brave", "opera", "safari"
]

PRODUCTIVITY_KEYWORDS = [
    "localhost", "github", "stackoverflow", "stack overflow",
    "gitlab", "bitbucket", "codepen", "jsfiddle",
    "dev.to", "medium.com", "docs.", "documentation"
]

def categorize_app(app_name: str, window_title: str = "") -> str:
    """
    Categorize app based on name and window title with enhanced rules

    Rules:
    - Productive: VS Code, Postman, Spring Tools, Android Studio, Terminal,
                  Chrome with localhost/github/stackoverflow
    - Entertainment: WhatsApp, Instagram, YouTube, Spotify, Netflix,
                     Games (Steam/Epic)
    - Browser: Edge, Brave, Chrome (general browsing)
    - Other: All unclassified apps
    """
    app_lower = app_name.lower()
    window_lower = window_title.lower()

    # Check for productive apps first
    for prod_app in PRODUCTIVE_APPS:
        if prod_app in app_lower:
            return "Productive"

    # Check if it's a browser with productive content
    is_browser = any(browser in app_lower for browser in BROWSER_APPS)
    if is_browser:
        # Check if window title contains productive keywords
        for keyword in PRODUCTIVITY_KEYWORDS:
            if keyword in window_lower:
                return "Productive"

        # Check if window title contains entertainment keywords
        entertainment_keywords = ["youtube", "netflix", "instagram", "facebook",
                                 "twitter", "tiktok", "reddit", "twitch"]
        for keyword in entertainment_keywords:
            if keyword in window_lower:
                return "Entertainment"

        # Default browser category
        return "Browser"

    # Check for entertainment apps
    for ent_app in ENTERTAINMENT_APPS:
        if ent_app in app_lower:
            return "Entertainment"

    # Check for games (any .exe from Steam or Epic Games directories)
    if "steam" in app_lower or "epic" in app_lower:
        return "Entertainment"

    # Check for productivity tools (Office, etc.)
    productivity_tools = ["excel", "word", "powerpoint", "outlook",
                         "onenote", "notion", "evernote", "trello", "asana"]
    for tool in productivity_tools:
        if tool in app_lower:
            return "Productive"

    # Default to Other
    return "Other"

class IdleDetector:
    """Detect user idle time"""
    
    def __init__(self, idle_threshold: int = 120):
        self.idle_threshold = idle_threshold  # seconds
        self.last_activity = time.time()
        self.mouse_listener = None
        self.keyboard_listener = None
        
    def on_activity(self, *args):
        """Reset idle timer on activity"""
        self.last_activity = time.time()
    
    def start(self):
        """Start monitoring"""
        self.mouse_listener = mouse.Listener(
            on_move=self.on_activity,
            on_click=self.on_activity,
            on_scroll=self.on_activity
        )
        self.keyboard_listener = keyboard.Listener(
            on_press=self.on_activity
        )
        self.mouse_listener.start()
        self.keyboard_listener.start()
        logger.info("Idle detector started")
    
    def stop(self):
        """Stop monitoring"""
        if self.mouse_listener:
            self.mouse_listener.stop()
        if self.keyboard_listener:
            self.keyboard_listener.stop()
        logger.info("Idle detector stopped")
    
    def is_idle(self) -> bool:
        """Check if user is idle"""
        return (time.time() - self.last_activity) > self.idle_threshold
    
    def get_idle_time(self) -> float:
        """Get current idle time in seconds"""
        return time.time() - self.last_activity

class WindowTracker:
    """Track active windows and applications"""
    
    def __init__(self, db_callback: Callable, ws_callback: Callable):
        self.db_callback = db_callback
        self.ws_callback = ws_callback
        
        self.current_app: Optional[str] = None
        self.current_window: Optional[str] = None
        self.session_start: Optional[float] = None
        self.last_heartbeat: Optional[float] = None
        
        self.is_tracking = False
        self.track_task: Optional[asyncio.Task] = None
        self.heartbeat_task: Optional[asyncio.Task] = None
        
        self.idle_detector = IdleDetector(idle_threshold=120)
        self.platform = platform.system()
        
        logger.info(f"WindowTracker initialized for {self.platform}")
    
    def get_active_window_windows(self) -> Optional[Dict[str, str]]:
        """Get active window on Windows"""
        try:
            hwnd = win32gui.GetForegroundWindow()
            if not hwnd:
                return None
            
            window_title = win32gui.GetWindowText(hwnd)
            _, pid = win32process.GetWindowThreadProcessId(hwnd)
            
            try:
                process = psutil.Process(pid)
                app_name = process.name().replace(".exe", "")
            except:
                app_name = "Unknown"
            
            return {
                "app": app_name,
                "window": window_title
            }
        except Exception as e:
            logger.error(f"Error getting active window: {e}")
            return None
    
    def get_active_window(self) -> Optional[Dict[str, str]]:
        """Get active window (platform-agnostic)"""
        if self.platform == "Windows":
            return self.get_active_window_windows()
        else:
            logger.warning(f"Platform {self.platform} not supported")
            return None
    
    async def save_session(self, app: str, window: str, start: float, end: float):
        """Save session to database"""
        duration = int(end - start)
        if duration < 1:
            return
        
        category = categorize_app(app)
        
        await self.db_callback(
            app_name=app,
            window_title=window,
            start_time=datetime.fromtimestamp(start, tz=timezone.utc),
            end_time=datetime.fromtimestamp(end, tz=timezone.utc),
            duration_sec=duration,
            category=category
        )
        
        # Broadcast session end
        await self.ws_callback("session_end", {
            "app": app,
            "window": window,
            "duration_sec": duration,
            "category": category,
            "timestamp": datetime.fromtimestamp(end, tz=timezone.utc).isoformat()
        })
    
    async def tracking_loop(self):
        """Main tracking loop"""
        logger.info("Tracking loop started")
        
        while self.is_tracking:
            try:
                # Check if idle
                if self.idle_detector.is_idle():
                    if self.current_app:
                        # End current session
                        await self.save_session(
                            self.current_app,
                            self.current_window or "",
                            self.session_start,
                            time.time()
                        )
                        self.current_app = None
                        self.current_window = None
                        self.session_start = None
                    
                    await asyncio.sleep(1)
                    continue
                
                # Get active window
                window_info = self.get_active_window()
                if not window_info:
                    await asyncio.sleep(1)
                    continue
                
                app = window_info["app"]
                window = window_info["window"]
                current_time = time.time()
                
                # Check if app changed
                if app != self.current_app:
                    # Save previous session
                    if self.current_app and self.session_start:
                        await self.save_session(
                            self.current_app,
                            self.current_window or "",
                            self.session_start,
                            current_time
                        )
                    
                    # Start new session
                    self.current_app = app
                    self.current_window = window
                    self.session_start = current_time
                    self.last_heartbeat = current_time
                    
                    category = categorize_app(app)
                    logger.info(f"Switched to: {app}")
                    
                    # Broadcast session start
                    await self.ws_callback("session_start", {
                        "app": app,
                        "window": window,
                        "category": category,
                        "timestamp": datetime.fromtimestamp(current_time, tz=timezone.utc).isoformat()
                    })
                
                # Update window title if changed
                elif window != self.current_window:
                    self.current_window = window
                
                await asyncio.sleep(1)
                
            except Exception as e:
                logger.error(f"Error in tracking loop: {e}")
                await asyncio.sleep(1)
    
    async def heartbeat_loop(self):
        """Send periodic heartbeats every 4 seconds"""
        while self.is_tracking:
            try:
                if self.current_app and self.session_start:
                    elapsed = int(time.time() - self.session_start)
                    category = categorize_app(self.current_app)

                    await self.ws_callback("heartbeat", {
                        "app": self.current_app,
                        "window": self.current_window or "",
                        "elapsed_sec": elapsed,
                        "category": category,
                        "is_idle": self.idle_detector.is_idle(),
                        "timestamp": datetime.now(timezone.utc).isoformat()
                    })

                await asyncio.sleep(4)  # Update every 4 seconds
            except Exception as e:
                logger.error(f"Error in heartbeat loop: {e}")
                await asyncio.sleep(4)
    
    async def start(self):
        """Start tracking"""
        if self.is_tracking:
            return
        
        self.is_tracking = True
        self.idle_detector.start()
        
        self.track_task = asyncio.create_task(self.tracking_loop())
        self.heartbeat_task = asyncio.create_task(self.heartbeat_loop())
        
        logger.info("Tracking started")
    
    async def stop(self):
        """Stop tracking"""
        self.is_tracking = False
        
        # Save current session
        if self.current_app and self.session_start:
            await self.save_session(
                self.current_app,
                self.current_window or "",
                self.session_start,
                time.time()
            )
        
        self.idle_detector.stop()
        
        if self.track_task:
            self.track_task.cancel()
        if self.heartbeat_task:
            self.heartbeat_task.cancel()
        
        logger.info("Tracking stopped")
    
    def get_current_session(self) -> Optional[Dict[str, Any]]:
        """Get current active session"""
        if not self.current_app or not self.session_start:
            return None
        
        return {
            "app": self.current_app,
            "window_title": self.current_window or "",
            "elapsed_sec": int(time.time() - self.session_start),
            "category": categorize_app(self.current_app),
            "start_time": datetime.fromtimestamp(self.session_start, tz=timezone.utc).isoformat(),
            "is_idle": self.idle_detector.is_idle()
        }

