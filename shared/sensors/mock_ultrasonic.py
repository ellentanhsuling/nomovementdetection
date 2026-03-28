"""
Mock Ultrasonic Distance Sensor (HC-SR04)

This simulates a real ultrasonic sensor for testing without hardware.
When the Raspberry Pi arrives, we'll create a real_ultrasonic.py that
uses actual GPIO pins.
"""

import random
import time
from datetime import datetime
from typing import Optional
from .base_sensor import BaseSensor


class MockUltrasonicSensor(BaseSensor):
    """
    Mock ultrasonic sensor that simulates distance measurement.
    
    This class simulates the behavior of a real HC-SR04 sensor:
    - Measures distance in centimeters (2cm to 400cm)
    - Returns None if out of range or error
    - Can simulate presence detection (person in room)
    - Can simulate different scenarios
    """
    
    def __init__(self, config: dict):
        super().__init__("Mock Ultrasonic Sensor", config)
        
        # Configuration
        self.min_distance = config.get('min_distance', 2)  # cm
        self.max_distance = config.get('max_distance', 400)  # cm
        self.presence_threshold = config.get('presence_threshold', 200)  # cm
        
        # Simulation parameters
        self.simulation_mode = config.get('simulation_mode', 'normal')  # normal, person_present, person_absent, fall
        self.base_distance = self._get_base_distance()
        
        # State tracking
        self.current_distance: Optional[float] = None
        self.person_detected = False
        
        # For realistic simulation
        self.distance_variance = 5.0  # cm - natural variation
        self.error_rate = 0.02  # 2% chance of reading error
    
    def _get_base_distance(self) -> float:
        """Get base distance based on simulation mode."""
        base_distances = {
            'normal': 150.0,  # Person moving around, varying distance
            'person_present': 80.0,  # Person close to sensor
            'person_absent': 350.0,  # No one in room (far distance)
            'fall': 50.0,  # Person fell, closer to ground
        }
        return base_distances.get(self.simulation_mode, 150.0)
    
    def _initialize(self) -> bool:
        """Initialize the mock sensor (nothing to do for mock)."""
        print(f"[Mock Ultrasonic] Initialized in '{self.simulation_mode}' mode")
        print(f"[Mock Ultrasonic] Range: {self.min_distance}-{self.max_distance}cm, Presence threshold: {self.presence_threshold}cm")
        return True
    
    def _read(self) -> Optional[float]:
        """
        Read distance measurement.
        Returns distance in centimeters, or None if error/out of range.
        """
        # Simulate reading error
        if random.random() < self.error_rate:
            return None
        
        # Calculate distance based on simulation mode
        if self.simulation_mode == 'normal':
            # Person moving - distance varies
            distance = self.base_distance + random.uniform(-50, 50)
        elif self.simulation_mode == 'person_present':
            # Person in room - relatively close
            distance = self.base_distance + random.uniform(-20, 20)
        elif self.simulation_mode == 'person_absent':
            # No one in room - far distance
            distance = self.base_distance + random.uniform(-30, 30)
        elif self.simulation_mode == 'fall':
            # Person fell - closer to ground, less variation
            distance = self.base_distance + random.uniform(-10, 10)
        else:
            # Default
            distance = self.base_distance + random.uniform(-self.distance_variance, self.distance_variance)
        
        # Add natural sensor variance
        distance += random.uniform(-self.distance_variance, self.distance_variance)
        
        # Clamp to valid range
        distance = max(self.min_distance, min(self.max_distance, distance))
        
        # Check if out of range (simulate sensor limitations)
        if distance > self.max_distance * 0.95:
            return None  # Out of range
        
        self.current_distance = distance
        
        # Determine if person is present (closer than threshold)
        self.person_detected = distance < self.presence_threshold
        
        return round(distance, 2)
    
    def is_person_present(self) -> bool:
        """
        Check if a person is detected based on distance threshold.
        Returns True if distance is less than presence_threshold.
        """
        if self.current_distance is None:
            return False
        return self.current_distance < self.presence_threshold
    
    def set_simulation_mode(self, mode: str):
        """
        Change simulation mode for testing different scenarios.
        
        Args:
            mode: 'normal', 'person_present', 'person_absent', or 'fall'
        """
        self.simulation_mode = mode
        self.base_distance = self._get_base_distance()
        print(f"[Mock Ultrasonic] Simulation mode changed to '{mode}'")
    
    def set_distance(self, distance: float):
        """
        Manually set distance for testing.
        
        Args:
            distance: Distance in centimeters
        """
        self.current_distance = max(self.min_distance, min(self.max_distance, distance))
        self.person_detected = self.current_distance < self.presence_threshold
        print(f"[Mock Ultrasonic] Distance set to {self.current_distance}cm")
    
    def get_status(self) -> dict:
        """Get extended status including distance info."""
        status = super().get_status()
        status.update({
            'simulation_mode': self.simulation_mode,
            'current_distance_cm': self.current_distance,
            'person_detected': self.person_detected,
            'presence_threshold_cm': self.presence_threshold,
            'min_distance_cm': self.min_distance,
            'max_distance_cm': self.max_distance,
        })
        return status
