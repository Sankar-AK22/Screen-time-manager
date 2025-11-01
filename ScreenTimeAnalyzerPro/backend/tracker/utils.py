"""
Utility functions for app name normalization and categorization.
"""

import re
from typing import Dict, Optional

# App name normalization mapping
APP_NAME_MAPPING = {
    "chrome.exe": "Google Chrome",
    "chrome": "Google Chrome",
    "firefox.exe": "Firefox",
    "firefox": "Firefox",
    "msedge.exe": "Microsoft Edge",
    "msedge": "Microsoft Edge",
    "brave.exe": "Brave Browser",
    "brave": "Brave Browser",
    "code.exe": "Visual Studio Code",
    "code": "Visual Studio Code",
    "slack.exe": "Slack",
    "slack": "Slack",
    "teams.exe": "Microsoft Teams",
    "teams": "Microsoft Teams",
    "spotify.exe": "Spotify",
    "spotify": "Spotify",
    "vlc.exe": "VLC Media Player",
    "vlc": "VLC Media Player",
    "notepad++.exe": "Notepad++",
    "notepad++": "Notepad++",
    "pycharm64.exe": "PyCharm",
    "pycharm": "PyCharm",
    "idea64.exe": "IntelliJ IDEA",
    "idea": "IntelliJ IDEA",
    "excel.exe": "Microsoft Excel",
    "excel": "Microsoft Excel",
    "word.exe": "Microsoft Word",
    "word": "Microsoft Word",
    "powerpoint.exe": "Microsoft PowerPoint",
    "powerpoint": "Microsoft PowerPoint",
    "outlook.exe": "Microsoft Outlook",
    "outlook": "Microsoft Outlook",
    "discord.exe": "Discord",
    "discord": "Discord",
    "zoom.exe": "Zoom",
    "zoom": "Zoom",
    "notion.exe": "Notion",
    "notion": "Notion",
    "figma.exe": "Figma",
    "figma": "Figma",
    "photoshop.exe": "Adobe Photoshop",
    "photoshop": "Adobe Photoshop",
}

# App category mapping
APP_CATEGORIES = {
    "Google Chrome": "Browser",
    "Firefox": "Browser",
    "Microsoft Edge": "Browser",
    "Brave Browser": "Browser",
    "Safari": "Browser",
    "Visual Studio Code": "Development",
    "PyCharm": "Development",
    "IntelliJ IDEA": "Development",
    "Sublime Text": "Development",
    "Atom": "Development",
    "Slack": "Communication",
    "Microsoft Teams": "Communication",
    "Discord": "Communication",
    "Zoom": "Communication",
    "Skype": "Communication",
    "Microsoft Excel": "Productivity",
    "Microsoft Word": "Productivity",
    "Microsoft PowerPoint": "Productivity",
    "Microsoft Outlook": "Productivity",
    "Notion": "Productivity",
    "Evernote": "Productivity",
    "Spotify": "Entertainment",
    "VLC Media Player": "Entertainment",
    "Netflix": "Entertainment",
    "YouTube": "Entertainment",
    "Figma": "Design",
    "Adobe Photoshop": "Design",
    "Adobe Illustrator": "Design",
    "Sketch": "Design",
}

# Productivity scoring (work vs entertainment)
PRODUCTIVITY_WEIGHTS = {
    "Development": 1.0,
    "Productivity": 1.0,
    "Design": 0.9,
    "Communication": 0.7,
    "Browser": 0.5,  # Depends on content
    "Entertainment": 0.0,
    "Other": 0.3,
}


def normalize_app_name(raw_name: str) -> str:
    """
    Normalize application name to a friendly, consistent format.
    
    Args:
        raw_name: Raw application name from OS (e.g., "chrome.exe", "Code.exe")
        
    Returns:
        Normalized app name (e.g., "Google Chrome", "Visual Studio Code")
    """
    if not raw_name:
        return "UNKNOWN"
    
    # Convert to lowercase for matching
    lower_name = raw_name.lower().strip()
    
    # Remove .exe extension if present
    if lower_name.endswith(".exe"):
        lower_name = lower_name[:-4]
    
    # Check mapping
    if lower_name in APP_NAME_MAPPING:
        return APP_NAME_MAPPING[lower_name]
    
    # If not in mapping, capitalize first letter of each word
    # Remove special characters
    clean_name = re.sub(r'[^a-zA-Z0-9\s]', ' ', raw_name)
    return ' '.join(word.capitalize() for word in clean_name.split())


def get_app_category(app_name: str) -> str:
    """
    Get the category for an application.
    
    Args:
        app_name: Normalized application name
        
    Returns:
        Category name (e.g., "Development", "Browser", "Entertainment")
    """
    return APP_CATEGORIES.get(app_name, "Other")


def get_productivity_score(category: str) -> float:
    """
    Get productivity weight for a category.
    
    Args:
        category: App category
        
    Returns:
        Productivity score (0.0 to 1.0)
    """
    return PRODUCTIVITY_WEIGHTS.get(category, 0.3)


def sanitize_window_title(title: str, max_length: int = 200) -> str:
    """
    Sanitize window title for storage.
    
    Args:
        title: Raw window title
        max_length: Maximum length to truncate to
        
    Returns:
        Sanitized title
    """
    if not title:
        return ""
    
    # Remove control characters
    sanitized = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', title)
    
    # Truncate if too long
    if len(sanitized) > max_length:
        sanitized = sanitized[:max_length] + "..."
    
    return sanitized.strip()


def format_duration(seconds: int) -> str:
    """
    Format duration in seconds to human-readable string.
    
    Args:
        seconds: Duration in seconds
        
    Returns:
        Formatted string (e.g., "2h 30m", "45m", "30s")
    """
    if seconds < 60:
        return f"{seconds}s"
    
    minutes = seconds // 60
    if minutes < 60:
        remaining_seconds = seconds % 60
        if remaining_seconds > 0:
            return f"{minutes}m {remaining_seconds}s"
        return f"{minutes}m"
    
    hours = minutes // 60
    remaining_minutes = minutes % 60
    if remaining_minutes > 0:
        return f"{hours}h {remaining_minutes}m"
    return f"{hours}h"

