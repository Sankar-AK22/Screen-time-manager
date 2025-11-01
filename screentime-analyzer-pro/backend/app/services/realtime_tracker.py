"""
Real-time Screen Time Tracker with WebSocket Broadcasting
Tracks active window changes instantly and broadcasts to connected clients
"""

import asyncio
import time
import platform
from datetime import datetime
from typing import Optional, Callable, Dict, Any, Set
from sqlalchemy.orm import Session

# Platform-specific imports
system = platform.system()
if system == "Windows":
    import win32gui
    import win32process
    import psutil
elif system == "Darwin":  # macOS
    try:
        from AppKit import NSWorkspace
        from Quartz import (
            CGWindowListCopyWindowInfo,
            kCGWindowListOptionOnScreenOnly,
            kCGNullWindowID
        )
    except ImportError:
        print("⚠️  macOS tracking requires: pip install pyobjc-framework-Cocoa pyobjc-framework-Quartz")
else:  # Linux
    import psutil


class RealtimeTracker:
    """
    Real-time screen time tracker with WebSocket broadcasting
    Detects active window changes instantly and streams updates
    """
    
    def __init__(self, db_session_factory: Callable):
        self.db_session_factory = db_session_factory
        self.is_tracking = False
        self.current_app = None
        self.current_window_title = None
        self.start_time = None
        self.websocket_clients: Set = set()
        self.tracking_task = None
        
        # Category mapping for productivity scoring
        self.categories = {
            'Development': ['code.exe', 'pycharm', 'visual studio', 'intellij', 'sublime', 'atom', 'vim', 'emacs', 'vscode'],
            'Productivity': ['excel', 'word', 'powerpoint', 'onenote', 'notion', 'evernote', 'obsidian', 'roam'],
            'Browser': ['chrome', 'firefox', 'edge', 'safari', 'brave', 'opera', 'vivaldi'],
            'Communication': ['slack', 'teams', 'discord', 'zoom', 'skype', 'telegram', 'whatsapp'],
            'Entertainment': ['spotify', 'netflix', 'youtube', 'vlc', 'media player', 'steam', 'epic games'],
            'Design': ['photoshop', 'illustrator', 'figma', 'sketch', 'canva', 'gimp', 'inkscape'],
        }
    
    def categorize_app(self, app_name: str) -> str:
        """Categorize app based on name"""
        app_lower = app_name.lower()
        for category, keywords in self.categories.items():
            if any(keyword in app_lower for keyword in keywords):
                return category
        return 'Other'
    
    def get_active_window_windows(self) -> Optional[Dict[str, str]]:
        """Get active window on Windows using win32gui"""
        try:
            window = win32gui.GetForegroundWindow()
            window_title = win32gui.GetWindowText(window)
            _, pid = win32process.GetWindowThreadProcessId(window)
            
            try:
                process = psutil.Process(pid)
                app_name = process.name()
                return {
                    'app_name': app_name,
                    'window_title': window_title,
                    'process_name': process.name()
                }
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                return None
                
        except Exception as e:
            print(f"❌ Error getting active window (Windows): {e}")
            return None
    
    def get_active_window_macos(self) -> Optional[Dict[str, str]]:
        """Get active window on macOS using AppKit"""
        try:
            active_app = NSWorkspace.sharedWorkspace().activeApplication()
            app_name = active_app['NSApplicationName']
            
            # Get window title from Quartz
            window_list = CGWindowListCopyWindowInfo(
                kCGWindowListOptionOnScreenOnly,
                kCGNullWindowID
            )
            
            window_title = ""
            for window in window_list:
                if window.get('kCGWindowOwnerName') == app_name:
                    window_title = window.get('kCGWindowName', '')
                    if window_title:
                        break
            
            return {
                'app_name': app_name,
                'window_title': window_title,
                'process_name': app_name
            }
            
        except Exception as e:
            print(f"❌ Error getting active window (macOS): {e}")
            return None
    
    def get_active_window_linux(self) -> Optional[Dict[str, str]]:
        """Get active window on Linux using psutil"""
        try:
            # Get all running processes
            for proc in psutil.process_iter(['pid', 'name']):
                try:
                    # Simple heuristic: get the most recently active process
                    return {
                        'app_name': proc.info['name'],
                        'window_title': proc.info['name'],
                        'process_name': proc.info['name']
                    }
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            return None
        except Exception as e:
            print(f"❌ Error getting active window (Linux): {e}")
            return None
    
    def get_active_window(self) -> Optional[Dict[str, str]]:
        """Get active window based on platform"""
        system = platform.system()
        
        if system == "Windows":
            return self.get_active_window_windows()
        elif system == "Darwin":
            return self.get_active_window_macos()
        else:
            return self.get_active_window_linux()
    
    async def save_session(self, app_name: str, window_title: str, duration_seconds: float):
        """Save completed session to database"""
        try:
            from app.models.usage import AppUsage
            
            db = self.db_session_factory()
            try:
                category = self.categorize_app(app_name)
                
                usage = AppUsage(
                    app_name=app_name,
                    window_title=window_title,
                    process_name=app_name,
                    start_time=datetime.fromtimestamp(self.start_time),
                    end_time=datetime.now(),
                    duration_seconds=duration_seconds,
                    duration_minutes=duration_seconds / 60,
                    is_active=False,
                    category=category
                )
                
                db.add(usage)
                db.commit()
                print(f"💾 Saved session: {app_name} ({duration_seconds:.1f}s)")
                
            finally:
                db.close()
                
        except Exception as e:
            print(f"❌ Error saving session: {e}")
    
    async def broadcast_to_clients(self, data: Dict[str, Any]):
        """Broadcast data to all connected WebSocket clients"""
        if not self.websocket_clients:
            return
        
        disconnected_clients = set()
        
        for client in self.websocket_clients:
            try:
                await client.send_json(data)
            except Exception as e:
                print(f"❌ Error broadcasting to client: {e}")
                disconnected_clients.add(client)
        
        # Remove disconnected clients
        self.websocket_clients -= disconnected_clients
    
    async def track_loop(self):
        """Main tracking loop - runs continuously"""
        print("🔄 Real-time tracking loop started")
        
        while self.is_tracking:
            try:
                # Get current active window
                window_info = self.get_active_window()
                
                if window_info:
                    app_name = window_info['app_name']
                    window_title = window_info['window_title']
                    
                    # Check if app changed
                    if app_name != self.current_app:
                        # Save previous session if exists
                        if self.current_app and self.start_time:
                            duration = time.time() - self.start_time
                            
                            # Save to database
                            await self.save_session(
                                self.current_app,
                                self.current_window_title,
                                duration
                            )
                            
                            # Broadcast session end
                            await self.broadcast_to_clients({
                                'type': 'session_end',
                                'app_name': self.current_app,
                                'window_title': self.current_window_title,
                                'duration_seconds': duration,
                                'category': self.categorize_app(self.current_app),
                                'timestamp': datetime.now().isoformat()
                            })
                        
                        # Start new session
                        self.current_app = app_name
                        self.current_window_title = window_title
                        self.start_time = time.time()
                        
                        # Broadcast session start
                        await self.broadcast_to_clients({
                            'type': 'session_start',
                            'app_name': app_name,
                            'window_title': window_title,
                            'category': self.categorize_app(app_name),
                            'timestamp': datetime.now().isoformat()
                        })
                        
                        print(f"🔄 Switched to: {app_name}")
                    
                    else:
                        # Same app, broadcast duration update
                        if self.start_time:
                            current_duration = time.time() - self.start_time
                            
                            await self.broadcast_to_clients({
                                'type': 'duration_update',
                                'app_name': app_name,
                                'window_title': window_title,
                                'duration_seconds': current_duration,
                                'category': self.categorize_app(app_name),
                                'timestamp': datetime.now().isoformat()
                            })
                
                # Check every 1 second for instant detection
                await asyncio.sleep(1)
                
            except Exception as e:
                print(f"❌ Error in tracking loop: {e}")
                await asyncio.sleep(1)
        
        print("🛑 Real-time tracking loop stopped")
    
    async def start_tracking(self):
        """Start real-time tracking"""
        if self.is_tracking:
            print("⚠️  Tracking already running")
            return
        
        self.is_tracking = True
        self.tracking_task = asyncio.create_task(self.track_loop())
        print("🟢 Real-time tracking started")
    
    async def stop_tracking(self):
        """Stop real-time tracking"""
        if not self.is_tracking:
            print("⚠️  Tracking not running")
            return
        
        self.is_tracking = False
        
        # Save current session if exists
        if self.current_app and self.start_time:
            duration = time.time() - self.start_time
            await self.save_session(
                self.current_app,
                self.current_window_title,
                duration
            )
        
        # Cancel tracking task
        if self.tracking_task:
            self.tracking_task.cancel()
            try:
                await self.tracking_task
            except asyncio.CancelledError:
                pass
        
        self.current_app = None
        self.current_window_title = None
        self.start_time = None
        
        print("🔴 Real-time tracking stopped")
    
    def add_websocket_client(self, websocket):
        """Add WebSocket client for broadcasting"""
        self.websocket_clients.add(websocket)
        print(f"✅ WebSocket client connected (Total: {len(self.websocket_clients)})")
    
    def remove_websocket_client(self, websocket):
        """Remove WebSocket client"""
        self.websocket_clients.discard(websocket)
        print(f"❌ WebSocket client disconnected (Total: {len(self.websocket_clients)})")
    
    def get_current_session(self) -> Optional[Dict[str, Any]]:
        """Get current active session info"""
        if not self.current_app or not self.start_time:
            return None
        
        return {
            'app_name': self.current_app,
            'window_title': self.current_window_title,
            'duration_seconds': time.time() - self.start_time,
            'category': self.categorize_app(self.current_app),
            'start_time': datetime.fromtimestamp(self.start_time).isoformat()
        }

