"""
Core movement detection algorithm

This is the heart of the system - it analyzes sensor data to determine
if there's a concerning lack of movement that requires an alert.
"""

from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List
from enum import Enum


class MovementStatus(Enum):
    """Status of movement detection"""
    ACTIVE = "active"  # Normal movement detected
    INACTIVE = "inactive"  # No movement, but within normal threshold
    CONCERNING = "concerning"  # No movement beyond threshold - needs alert
    UNKNOWN = "unknown"  # Sensor error or insufficient data


class MovementDetector:
    """
    Detects periods of non-movement and determines if alerts are needed.
    
    This class implements the core algorithm that:
    1. Tracks movement events from sensors
    2. Calculates time since last movement
    3. Applies time-based rules (active hours vs sleep hours)
    4. Determines if alert threshold is exceeded
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the movement detector.
        
        Args:
            config: Configuration dictionary from config.yaml
        """
        self.config = config
        monitoring_config = config.get('monitoring', {})
        
        # Time thresholds (in minutes)
        self.threshold_active = monitoring_config.get('no_movement_threshold_active', 30)
        self.threshold_sleep = monitoring_config.get('no_movement_threshold_sleep', 120)
        self.threshold_anytime = monitoring_config.get('no_movement_threshold_anytime', 60)
        
        # Active and sleep hours
        self.active_start = monitoring_config.get('active_hours', {}).get('start', 7)
        self.active_end = monitoring_config.get('active_hours', {}).get('end', 22)
        self.sleep_start = monitoring_config.get('sleep_hours', {}).get('start', 22)
        self.sleep_end = monitoring_config.get('sleep_hours', {}).get('end', 7)
        
        # Camera-based detection settings
        self.require_person_confirmation = monitoring_config.get('require_person_confirmation', True)
        self.motion_consensus_frames = monitoring_config.get('motion_consensus_frames', 3)
        
        # Legacy multi-sensor support (for backward compatibility)
        self.require_multiple_sensors = monitoring_config.get('require_multiple_sensors', False)
        self.sensor_agreement_timeout = monitoring_config.get('sensor_agreement_timeout', 60)
        
        # State tracking
        self.last_movement_time: Optional[datetime] = None
        self.movement_history: List[Dict[str, Any]] = []  # Store recent movement events
        self.consecutive_no_movement_checks = 0
        
    def is_active_hours(self, current_time: Optional[datetime] = None) -> bool:
        """
        Check if current time is during active hours.
        
        Args:
            current_time: Time to check (defaults to now)
        
        Returns:
            True if during active hours
        """
        if current_time is None:
            current_time = datetime.now()
        
        hour = current_time.hour
        
        # Handle case where active hours span midnight
        if self.active_start <= self.active_end:
            return self.active_start <= hour < self.active_end
        else:
            # Spans midnight (e.g., 22:00 to 7:00)
            return hour >= self.active_start or hour < self.active_end
    
    def is_sleep_hours(self, current_time: Optional[datetime] = None) -> bool:
        """
        Check if current time is during sleep hours.
        
        Args:
            current_time: Time to check (defaults to now)
        
        Returns:
            True if during sleep hours
        """
        if current_time is None:
            current_time = datetime.now()
        
        hour = current_time.hour
        
        # Handle case where sleep hours span midnight
        if self.sleep_start <= self.sleep_end:
            return self.sleep_start <= hour < self.sleep_end
        else:
            # Spans midnight (e.g., 22:00 to 7:00)
            return hour >= self.sleep_start or hour < self.sleep_end
    
    def record_movement(self, sensor_name: str, sensor_value: Any, timestamp: Optional[datetime] = None):
        """
        Record a movement event from a sensor.
        
        Args:
            sensor_name: Name of the sensor (e.g., "PIR", "Ultrasonic")
            sensor_value: Value from sensor (True/False for PIR, distance for Ultrasonic)
            timestamp: When movement occurred (defaults to now)
        """
        if timestamp is None:
            timestamp = datetime.now()
        
        # Determine if this indicates movement
        is_movement = self._interpret_sensor_value(sensor_name, sensor_value)
        
        if is_movement:
            self.last_movement_time = timestamp
            self.consecutive_no_movement_checks = 0
            
            # Add to history (keep last 100 events)
            self.movement_history.append({
                'timestamp': timestamp,
                'sensor': sensor_name,
                'value': sensor_value,
                'is_movement': True,
            })
            
            # Limit history size
            if len(self.movement_history) > 100:
                self.movement_history.pop(0)
        else:
            self.consecutive_no_movement_checks += 1
    
    def _interpret_sensor_value(self, sensor_name: str, value: Any) -> bool:
        """
        Interpret sensor value to determine if movement is detected.
        
        Args:
            sensor_name: Name of the sensor
            value: Sensor reading
        
        Returns:
            True if movement detected, False otherwise
        """
        if value is None:
            return False
        
        # Camera sensor returns a dictionary with detection results
        if sensor_name.lower() == 'camera' or 'camera' in sensor_name.lower():
            if isinstance(value, dict):
                # Camera provides person_detected and motion_detected
                person_detected = value.get('person_detected', False)
                motion_detected = value.get('motion_detected', False)
                
                # Require both person presence and motion for movement
                # This reduces false positives from pets, shadows, etc.
                monitoring_config = self.config.get('monitoring', {})
                require_person_confirmation = monitoring_config.get('require_person_confirmation', True)
                
                if require_person_confirmation:
                    return person_detected and motion_detected
                else:
                    # Just motion is enough (less strict)
                    return motion_detected
        
        # Legacy sensor support (PIR, Ultrasonic)
        elif sensor_name.lower() == 'pir' or 'pir' in sensor_name.lower():
            # PIR returns True/False directly
            return bool(value)
        
        elif sensor_name.lower() == 'ultrasonic' or 'ultrasonic' in sensor_name.lower():
            # Ultrasonic returns distance - check if person is present
            # If distance is less than threshold, person is present (movement)
            if isinstance(value, (int, float)):
                presence_threshold = self.config.get('sensors', {}).get('ultrasonic', {}).get('presence_threshold', 200)
                return value < presence_threshold
        
        return False
    
    def check_movement_status(self, sensor_readings: Dict[str, Any], current_time: Optional[datetime] = None) -> MovementStatus:
        """
        Check current movement status based on sensor readings.
        
        Args:
            sensor_readings: Dictionary of sensor_name -> sensor_value
            current_time: Current time (defaults to now)
        
        Returns:
            MovementStatus indicating current state
        """
        if current_time is None:
            current_time = datetime.now()
        
        # Process sensor readings
        movement_detected = []
        for sensor_name, sensor_value in sensor_readings.items():
            is_movement = self._interpret_sensor_value(sensor_name, sensor_value)
            movement_detected.append(is_movement)
            self.record_movement(sensor_name, sensor_value, current_time)
        
        # For camera, we use the interpretation from _interpret_sensor_value
        # which already handles person + motion confirmation
        # For legacy multi-sensor, use the old logic
        if self.require_multiple_sensors and len(movement_detected) > 1:
            # Require at least one sensor to detect movement
            any_movement = any(movement_detected)
        else:
            # Single sensor (camera) or multi-sensor not required
            any_movement = any(movement_detected) if movement_detected else False
        
        # If movement detected, we're active
        if any_movement:
            return MovementStatus.ACTIVE
        
        # No movement detected - check how long since last movement
        if self.last_movement_time is None:
            # No movement ever recorded - unknown status
            return MovementStatus.UNKNOWN
        
        time_since_movement = (current_time - self.last_movement_time).total_seconds() / 60  # Convert to minutes
        
        # Determine appropriate threshold based on time of day
        if self.is_active_hours(current_time):
            threshold = self.threshold_active
        elif self.is_sleep_hours(current_time):
            threshold = self.threshold_sleep
        else:
            # Between active and sleep hours - use anytime threshold
            threshold = self.threshold_anytime
        
        # Also check against absolute anytime threshold
        threshold = min(threshold, self.threshold_anytime)
        
        # Check if threshold exceeded
        if time_since_movement >= threshold:
            return MovementStatus.CONCERNING
        else:
            return MovementStatus.INACTIVE
    
    def get_time_since_last_movement(self, current_time: Optional[datetime] = None) -> Optional[float]:
        """
        Get minutes since last detected movement.
        
        Args:
            current_time: Current time (defaults to now)
        
        Returns:
            Minutes since last movement, or None if no movement recorded
        """
        if self.last_movement_time is None:
            return None
        
        if current_time is None:
            current_time = datetime.now()
        
        return (current_time - self.last_movement_time).total_seconds() / 60
    
    def get_status(self) -> Dict[str, Any]:
        """Get current status of the detector."""
        current_time = datetime.now()
        time_since = self.get_time_since_last_movement(current_time)
        
        return {
            'last_movement_time': self.last_movement_time.isoformat() if self.last_movement_time else None,
            'minutes_since_last_movement': time_since,
            'consecutive_no_movement_checks': self.consecutive_no_movement_checks,
            'is_active_hours': self.is_active_hours(current_time),
            'is_sleep_hours': self.is_sleep_hours(current_time),
            'current_threshold_minutes': self._get_current_threshold(current_time),
            'movement_history_count': len(self.movement_history),
        }
    
    def _get_current_threshold(self, current_time: datetime) -> float:
        """Get the current threshold based on time of day."""
        if self.is_active_hours(current_time):
            return self.threshold_active
        elif self.is_sleep_hours(current_time):
            return self.threshold_sleep
        else:
            return self.threshold_anytime
    
    def reset(self):
        """Reset detector state (useful for testing or manual reset)."""
        self.last_movement_time = None
        self.movement_history = []
        self.consecutive_no_movement_checks = 0
