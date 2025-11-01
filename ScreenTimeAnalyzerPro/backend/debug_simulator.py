"""
Debug simulator for testing frontend without actual app switching.
Simulates app switches and sends WebSocket events.
"""

import asyncio
import random
from datetime import datetime, timezone
from typing import List, Dict

# Simulated apps
SIMULATED_APPS = [
    {"app": "Google Chrome", "window": "Stack Overflow - Google Chrome", "category": "Browser"},
    {"app": "Visual Studio Code", "window": "main.py - VS Code", "category": "Development"},
    {"app": "Slack", "window": "General - Slack", "category": "Communication"},
    {"app": "Spotify", "window": "Liked Songs - Spotify", "category": "Entertainment"},
    {"app": "Microsoft Excel", "window": "Budget.xlsx - Excel", "category": "Productivity"},
    {"app": "Firefox", "window": "GitHub - Firefox", "category": "Browser"},
    {"app": "PyCharm", "window": "project - PyCharm", "category": "Development"},
    {"app": "Discord", "window": "General - Discord", "category": "Communication"},
]


class DebugSimulator:
    """Simulates app switches for testing."""
    
    def __init__(self, broadcast_callback):
        self.broadcast = broadcast_callback
        self.current_app = None
        self.session_start = None
        self.is_running = False
    
    async def simulate_app_switch(self):
        """Simulate switching to a random app."""
        # End current session
        if self.current_app and self.session_start:
            end_time = datetime.now(timezone.utc)
            duration_sec = int((end_time - self.session_start).total_seconds())
            
            await self.broadcast({
                "event": "session_end",
                "app": self.current_app["app"],
                "window_title": self.current_app["window"],
                "duration_sec": duration_sec,
                "start": self.session_start.isoformat(),
                "end": end_time.isoformat(),
                "source_os": "Simulator",
                "category": self.current_app["category"]
            })
        
        # Start new session
        self.current_app = random.choice(SIMULATED_APPS)
        self.session_start = datetime.now(timezone.utc)
        
        await self.broadcast({
            "event": "session_start",
            "app": self.current_app["app"],
            "window_title": self.current_app["window"],
            "category": self.current_app["category"],
            "timestamp": self.session_start.isoformat()
        })
    
    async def send_heartbeat(self):
        """Send heartbeat for current session."""
        if self.current_app and self.session_start:
            elapsed_sec = int((datetime.now(timezone.utc) - self.session_start).total_seconds())
            
            await self.broadcast({
                "event": "heartbeat",
                "app": self.current_app["app"],
                "window_title": self.current_app["window"],
                "elapsed_sec": elapsed_sec,
                "category": self.current_app["category"],
                "timestamp": datetime.now(timezone.utc).isoformat()
            })
    
    async def simulate_idle(self):
        """Simulate idle event."""
        idle_duration = random.randint(180, 600)
        
        await self.broadcast({
            "event": "idle",
            "idle_sec": idle_duration,
            "timestamp": datetime.now(timezone.utc).isoformat()
        })
    
    async def run_simulation(self):
        """Run continuous simulation."""
        self.is_running = True
        
        print("🎮 Debug Simulator Started")
        print("Simulating app switches every 10-30 seconds...")
        
        # Start with an app
        await self.simulate_app_switch()
        
        heartbeat_counter = 0
        
        while self.is_running:
            # Send heartbeat every 5 seconds
            if heartbeat_counter % 5 == 0:
                await self.send_heartbeat()
            
            # Switch app every 10-30 seconds
            if heartbeat_counter >= random.randint(10, 30):
                # Occasionally simulate idle instead
                if random.random() < 0.1:  # 10% chance
                    await self.simulate_idle()
                else:
                    await self.simulate_app_switch()
                
                heartbeat_counter = 0
            
            await asyncio.sleep(1)
            heartbeat_counter += 1
    
    def stop(self):
        """Stop simulation."""
        self.is_running = False
        print("🛑 Debug Simulator Stopped")


# Standalone simulator for testing
if __name__ == "__main__":
    async def mock_broadcast(message):
        """Mock broadcast function for testing."""
        print(f"📡 {message['event']}: {message.get('app', 'N/A')}")
    
    simulator = DebugSimulator(mock_broadcast)
    
    try:
        asyncio.run(simulator.run_simulation())
    except KeyboardInterrupt:
        simulator.stop()
        print("\n✅ Simulator stopped")

