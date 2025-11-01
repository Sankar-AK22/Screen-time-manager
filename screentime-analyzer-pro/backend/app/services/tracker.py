"""
Screen time tracking service
Monitors active windows and tracks application usage
"""
import psutil
import platform
import time
from datetime import datetime, timedelta
from typing import Optional, Dict
import logging

# Platform-specific imports
if platform.system() == "Windows":
    try:
        import win32gui
        import win32process
        WINDOWS_AVAILABLE = True
    except ImportError:
        WINDOWS_AVAILABLE = False
        logging.warning("win32gui not available. Install pywin32 for Windows support.")
elif platform.system() == "Darwin":
    try:
        from AppKit import NSWorkspace
        MACOS_AVAILABLE = True
    except ImportError:
        MACOS_AVAILABLE = False
        logging.warning("AppKit not available. Install pyobjc for macOS support.")
else:
    WINDOWS_AVAILABLE = False
    MACOS_AVAILABLE = False

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ScreenTimeTracker:
    """
    Tracks active windows and application usage
    """
    
    def __init__(self):
        self.current_app = None
        self.current_window = None
        self.start_time = None
        self.is_tracking = False
        
    def get_active_window_windows(self) -> Optional[Dict[str, str]]:
        """
        Get active window information on Windows
        """
        if not WINDOWS_AVAILABLE:
            return None
            
        try:
            window = win32gui.GetForegroundWindow()
            if window == 0:
                return None
                
            window_title = win32gui.GetWindowText(window)
            
            # Get process info
            _, pid = win32process.GetWindowThreadProcessId(window)
            
            try:
                process = psutil.Process(pid)
                app_name = process.name()
                process_name = process.name()
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                app_name = "Unknown"
                process_name = "Unknown"
            
            return {
                "app_name": app_name,
                "window_title": window_title,
                "process_name": process_name,
                "pid": pid
            }
        except Exception as e:
            logger.error(f"Error getting active window (Windows): {e}")
            return None
    
    def get_active_window_macos(self) -> Optional[Dict[str, str]]:
        """
        Get active window information on macOS
        """
        if not MACOS_AVAILABLE:
            return None
            
        try:
            workspace = NSWorkspace.sharedWorkspace()
            active_app = workspace.activeApplication()
            
            app_name = active_app.get('NSApplicationName', 'Unknown')
            process_name = active_app.get('NSApplicationProcessIdentifier', 'Unknown')
            
            return {
                "app_name": app_name,
                "window_title": app_name,  # macOS doesn't easily provide window titles
                "process_name": str(process_name),
                "pid": process_name
            }
        except Exception as e:
            logger.error(f"Error getting active window (macOS): {e}")
            return None
    
    def get_active_window_linux(self) -> Optional[Dict[str, str]]:
        """
        Get active window information on Linux (basic implementation)
        """
        try:
            # Get the most CPU-intensive GUI process as a fallback
            gui_processes = []
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
                try:
                    if proc.info['cpu_percent'] > 0:
                        gui_processes.append(proc.info)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
            
            if gui_processes:
                # Sort by CPU usage
                gui_processes.sort(key=lambda x: x['cpu_percent'], reverse=True)
                top_process = gui_processes[0]
                
                return {
                    "app_name": top_process['name'],
                    "window_title": top_process['name'],
                    "process_name": top_process['name'],
                    "pid": top_process['pid']
                }
        except Exception as e:
            logger.error(f"Error getting active window (Linux): {e}")
        
        return None
    
    def get_active_window(self) -> Optional[Dict[str, str]]:
        """
        Get active window information (platform-independent)
        """
        system = platform.system()
        
        if system == "Windows":
            return self.get_active_window_windows()
        elif system == "Darwin":
            return self.get_active_window_macos()
        elif system == "Linux":
            return self.get_active_window_linux()
        else:
            logger.warning(f"Unsupported platform: {system}")
            return None
    
    def categorize_app(self, app_name: str) -> str:
        """
        Categorize application based on name
        """
        app_name_lower = app_name.lower()
        
        # Development tools
        if any(x in app_name_lower for x in ['vscode', 'visual studio', 'pycharm', 'intellij', 'eclipse', 'sublime', 'atom', 'code.exe']):
            return "Development"
        
        # Browsers
        if any(x in app_name_lower for x in ['chrome', 'firefox', 'edge', 'safari', 'brave', 'opera']):
            return "Browser"
        
        # Communication
        if any(x in app_name_lower for x in ['slack', 'teams', 'discord', 'zoom', 'skype', 'telegram', 'whatsapp']):
            return "Communication"
        
        # Entertainment
        if any(x in app_name_lower for x in ['spotify', 'netflix', 'youtube', 'vlc', 'media player', 'steam', 'game']):
            return "Entertainment"
        
        # Productivity
        if any(x in app_name_lower for x in ['word', 'excel', 'powerpoint', 'outlook', 'notion', 'evernote', 'onenote']):
            return "Productivity"
        
        # Design
        if any(x in app_name_lower for x in ['photoshop', 'illustrator', 'figma', 'sketch', 'canva']):
            return "Design"
        
        # Terminal/Command Line
        if any(x in app_name_lower for x in ['terminal', 'cmd', 'powershell', 'bash', 'iterm']):
            return "Development"
        
        return "Other"
    
    def start_tracking(self):
        """
        Start tracking screen time
        """
        self.is_tracking = True
        logger.info("🟢 Screen time tracking started")
    
    def stop_tracking(self):
        """
        Stop tracking screen time
        """
        self.is_tracking = False
        logger.info("🔴 Screen time tracking stopped")
    
    def get_tracking_status(self) -> bool:
        """
        Get current tracking status
        """
        return self.is_tracking

# Global tracker instance
tracker = ScreenTimeTracker()

