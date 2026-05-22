"""
Airport Settings Management
"""

import json
import os

SETTINGS_FILE = os.path.join(os.path.dirname(__file__), "settings.json")

DEFAULT_SETTINGS = {
    "current_airport": "Chennai",
    "auto_checkin_enabled": True,
    "crew_rest_time": 30,  # minutes
    "fueling_time": 45,  # minutes
    "checkin_threshold": 50  # percentage
}

def load_settings():
    """Load settings from file or return defaults."""
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, 'r') as f:
                return json.load(f)
        except:
            return DEFAULT_SETTINGS.copy()
    return DEFAULT_SETTINGS.copy()

def save_settings(settings):
    """Save settings to file."""
    with open(SETTINGS_FILE, 'w') as f:
        json.dump(settings, f, indent=2)

def get_airport():
    """Get current airport setting."""
    settings = load_settings()
    return settings.get("current_airport", "Chennai")

def set_airport(airport_name):
    """Set current airport."""
    settings = load_settings()
    settings["current_airport"] = airport_name
    save_settings(settings)

def get_crew_rest_time():
    """Get crew rest time in minutes."""
    settings = load_settings()
    return settings.get("crew_rest_time", 30)

def set_crew_rest_time(minutes):
    """Set crew rest time in minutes."""
    settings = load_settings()
    settings["crew_rest_time"] = int(minutes)
    save_settings(settings)

def get_fueling_time():
    """Get fueling time in minutes."""
    settings = load_settings()
    return settings.get("fueling_time", 45)

def set_fueling_time(minutes):
    """Set fueling time in minutes."""
    settings = load_settings()
    settings["fueling_time"] = int(minutes)
    save_settings(settings)

def get_checkin_threshold():
    """Get check-in threshold percentage."""
    settings = load_settings()
    return settings.get("checkin_threshold", 50)

def set_checkin_threshold(threshold):
    """Set check-in threshold percentage."""
    settings = load_settings()
    settings["checkin_threshold"] = int(threshold)
    save_settings(settings)

def is_auto_checkin_enabled():
    """Check if auto check-in is enabled."""
    settings = load_settings()
    return settings.get("auto_checkin_enabled", True)

def set_auto_checkin(enabled):
    """Set auto check-in setting."""
    settings = load_settings()
    settings["auto_checkin_enabled"] = enabled
    save_settings(settings)
