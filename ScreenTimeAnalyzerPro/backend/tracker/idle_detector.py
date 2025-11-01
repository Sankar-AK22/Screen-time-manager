"""
Idle detection module using mouse and keyboard activity monitoring.
"""

import asyncio
import time
from typing import Optional, Callable
from loguru import logger

try:
    from pynput import mouse, keyboard
    PYNPUT_AVAILABLE = True
except ImportError:
    PYNPUT_AVAILABLE = False
    logger.warning("pynput not available - idle detection disabled")


class IdleDetector:
    """
    Detects user idle state based on mouse and keyboard activity.
    """
    
    def __init__(self, idle_threshold_seconds: int = 180):
        """
        Initialize idle detector.
        
        Args:
            idle_threshold_seconds: Seconds of inactivity before considering idle (default: 180 = 3 minutes)
        """
        self.idle_threshold = idle_threshold_seconds
        self.last_activity_time = time.time()
        self.is_idle = False
        self.idle_callback: Optional[Callable] = None
        self.active_callback: Optional[Callable] = None
        
        self._mouse_listener: Optional[mouse.Listener] = None
        self._keyboard_listener: Optional[keyboard.Listener] = None
        self._monitor_task: Optional[asyncio.Task] = None
        self._running = False
    
    def _on_activity(self):
        """Called when any mouse or keyboard activity is detected."""
        current_time = time.time()
        was_idle = self.is_idle
        
        self.last_activity_time = current_time
        
        # If was idle and now active, trigger callback
        if was_idle:
            self.is_idle = False
            logger.info("User became active")
            if self.active_callback:
                try:
                    self.active_callback()
                except Exception as e:
                    logger.error(f"Error in active callback: {e}")
    
    def _on_mouse_move(self, x, y):
        """Mouse move event handler."""
        self._on_activity()
    
    def _on_mouse_click(self, x, y, button, pressed):
        """Mouse click event handler."""
        if pressed:
            self._on_activity()
    
    def _on_mouse_scroll(self, x, y, dx, dy):
        """Mouse scroll event handler."""
        self._on_activity()
    
    def _on_keyboard_press(self, key):
        """Keyboard press event handler."""
        self._on_activity()
    
    async def _monitor_idle_state(self):
        """Background task to monitor idle state."""
        logger.info(f"Idle monitor started (threshold: {self.idle_threshold}s)")
        
        while self._running:
            try:
                current_time = time.time()
                idle_duration = current_time - self.last_activity_time
                
                # Check if user became idle
                if not self.is_idle and idle_duration >= self.idle_threshold:
                    self.is_idle = True
                    logger.info(f"User became idle after {idle_duration:.0f}s")
                    
                    if self.idle_callback:
                        try:
                            await self.idle_callback(idle_duration)
                        except Exception as e:
                            logger.error(f"Error in idle callback: {e}")
                
                # Check every 5 seconds
                await asyncio.sleep(5)
                
            except Exception as e:
                logger.error(f"Error in idle monitor: {e}")
                await asyncio.sleep(5)
    
    def start(self, idle_callback: Optional[Callable] = None, active_callback: Optional[Callable] = None):
        """
        Start idle detection.
        
        Args:
            idle_callback: Async function to call when user becomes idle
            active_callback: Function to call when user becomes active
        """
        if not PYNPUT_AVAILABLE:
            logger.warning("Cannot start idle detection - pynput not available")
            return
        
        if self._running:
            logger.warning("Idle detector already running")
            return
        
        self.idle_callback = idle_callback
        self.active_callback = active_callback
        self._running = True
        
        # Start mouse listener
        try:
            self._mouse_listener = mouse.Listener(
                on_move=self._on_mouse_move,
                on_click=self._on_mouse_click,
                on_scroll=self._on_mouse_scroll
            )
            self._mouse_listener.start()
            logger.info("Mouse listener started")
        except Exception as e:
            logger.error(f"Failed to start mouse listener: {e}")
        
        # Start keyboard listener
        try:
            self._keyboard_listener = keyboard.Listener(
                on_press=self._on_keyboard_press
            )
            self._keyboard_listener.start()
            logger.info("Keyboard listener started")
        except Exception as e:
            logger.error(f"Failed to start keyboard listener: {e}")
        
        # Start monitor task
        self._monitor_task = asyncio.create_task(self._monitor_idle_state())
        
        logger.info("Idle detector started successfully")
    
    def stop(self):
        """Stop idle detection."""
        if not self._running:
            return
        
        self._running = False
        
        # Stop listeners
        if self._mouse_listener:
            self._mouse_listener.stop()
            self._mouse_listener = None
        
        if self._keyboard_listener:
            self._keyboard_listener.stop()
            self._keyboard_listener = None
        
        # Cancel monitor task
        if self._monitor_task:
            self._monitor_task.cancel()
            self._monitor_task = None
        
        logger.info("Idle detector stopped")
    
    def get_idle_duration(self) -> float:
        """
        Get current idle duration in seconds.
        
        Returns:
            Seconds since last activity
        """
        return time.time() - self.last_activity_time
    
    def is_user_idle(self) -> bool:
        """
        Check if user is currently idle.
        
        Returns:
            True if idle, False if active
        """
        return self.is_idle

