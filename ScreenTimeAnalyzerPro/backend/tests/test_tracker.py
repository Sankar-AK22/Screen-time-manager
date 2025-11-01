"""
Tests for tracker utilities and normalization.
"""

import pytest
from tracker.utils import (
    normalize_app_name,
    get_app_category,
    get_productivity_score,
    sanitize_window_title,
    format_duration
)


class TestNormalization:
    """Test app name normalization."""
    
    def test_normalize_chrome(self):
        assert normalize_app_name("chrome.exe") == "Google Chrome"
        assert normalize_app_name("Chrome.exe") == "Google Chrome"
        assert normalize_app_name("chrome") == "Google Chrome"
    
    def test_normalize_vscode(self):
        assert normalize_app_name("code.exe") == "Visual Studio Code"
        assert normalize_app_name("Code.exe") == "Visual Studio Code"
    
    def test_normalize_unknown(self):
        result = normalize_app_name("unknown_app.exe")
        assert result == "Unknown App"
    
    def test_normalize_empty(self):
        assert normalize_app_name("") == "UNKNOWN"
        assert normalize_app_name(None) == "UNKNOWN"


class TestCategorization:
    """Test app categorization."""
    
    def test_browser_category(self):
        assert get_app_category("Google Chrome") == "Browser"
        assert get_app_category("Firefox") == "Browser"
    
    def test_development_category(self):
        assert get_app_category("Visual Studio Code") == "Development"
        assert get_app_category("PyCharm") == "Development"
    
    def test_unknown_category(self):
        assert get_app_category("Unknown App") == "Other"


class TestProductivityScore:
    """Test productivity scoring."""
    
    def test_development_score(self):
        assert get_productivity_score("Development") == 1.0
    
    def test_entertainment_score(self):
        assert get_productivity_score("Entertainment") == 0.0
    
    def test_browser_score(self):
        assert get_productivity_score("Browser") == 0.5
    
    def test_unknown_score(self):
        assert get_productivity_score("Unknown") == 0.3


class TestWindowTitle:
    """Test window title sanitization."""
    
    def test_sanitize_normal(self):
        title = "main.py - Visual Studio Code"
        assert sanitize_window_title(title) == title
    
    def test_sanitize_long(self):
        title = "a" * 300
        result = sanitize_window_title(title, max_length=200)
        assert len(result) <= 203  # 200 + "..."
        assert result.endswith("...")
    
    def test_sanitize_empty(self):
        assert sanitize_window_title("") == ""
        assert sanitize_window_title(None) == ""


class TestDurationFormat:
    """Test duration formatting."""
    
    def test_format_seconds(self):
        assert format_duration(30) == "30s"
        assert format_duration(59) == "59s"
    
    def test_format_minutes(self):
        assert format_duration(60) == "1m"
        assert format_duration(90) == "1m 30s"
        assert format_duration(120) == "2m"
    
    def test_format_hours(self):
        assert format_duration(3600) == "1h"
        assert format_duration(3660) == "1h 1m"
        assert format_duration(7200) == "2h"

