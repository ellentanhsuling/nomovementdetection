"""
Time utility functions
"""

from datetime import datetime, timedelta
from typing import Optional


def get_current_time() -> datetime:
    """Get current datetime."""
    return datetime.now()


def format_timedelta(td: timedelta) -> str:
    """
    Format timedelta as human-readable string.
    
    Args:
        td: Timedelta object
    
    Returns:
        Formatted string (e.g., "2 hours 30 minutes")
    """
    total_seconds = int(td.total_seconds())
    
    if total_seconds < 60:
        return f"{total_seconds} seconds"
    
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    
    parts = []
    if hours > 0:
        parts.append(f"{hours} hour{'s' if hours != 1 else ''}")
    if minutes > 0:
        parts.append(f"{minutes} minute{'s' if minutes != 1 else ''}")
    if seconds > 0 and hours == 0:  # Only show seconds if less than an hour
        parts.append(f"{seconds} second{'s' if seconds != 1 else ''}")
    
    return " ".join(parts)


def minutes_to_timedelta(minutes: float) -> timedelta:
    """Convert minutes to timedelta."""
    return timedelta(minutes=minutes)


def is_time_between(start_hour: int, end_hour: int, current_time: Optional[datetime] = None) -> bool:
    """
    Check if current time is between start and end hours.
    Handles cases where range spans midnight.
    
    Args:
        start_hour: Start hour (0-23)
        end_hour: End hour (0-23)
        current_time: Time to check (defaults to now)
    
    Returns:
        True if current time is in range
    """
    if current_time is None:
        current_time = datetime.now()
    
    hour = current_time.hour
    
    if start_hour <= end_hour:
        return start_hour <= hour < end_hour
    else:
        # Spans midnight
        return hour >= start_hour or hour < end_hour
