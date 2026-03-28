"""
Mock PIR (Passive Infrared) Motion Sensor

This simulates a real PIR sensor for testing without hardware.
When the Raspberry Pi arrives, we'll create a real_pir.py that
uses actual GPIO pins.
"""

import random
import time
from datetime import datetime, timedelta
from typing import Optional
from .base_sensor import BaseSensor


class MockPIRSensor(BaseSensor):
    """
    Mock PIR sensor that simulates motion detection.
    
    This class simulates the behavior of a real HC-SR501 PIR sensor:
    - Returns True when motion is detected
    - Returns False when no motion
    - Can simulate false positives
    - Can simulate different activity patterns
    """
    
    def __init__(self, config: dict):
        super().__init__("Mock PIR Sensor", config)
        
        # Simulation parameters
        self.sensitivity = config.get('sensitivity', 'medium')
        self.simulation_mode = config.get('simulation_mode', 'normal')  # normal, active, inactive, fall
        self.motion_probability = self._get_motion_probability()
        
        # State tracking
        self.motion_detected = False
        self.last_motion_time: Optional[datetime] = None
        self.motion_duration = 0  # How long motion has been detected
        
        # For simulating realistic behavior
        self.false_positive_rate = 0.05  # 5% chance of false positive
        self.pet_detection_rate = 0.10  # 10% chance of detecting pets (smaller motion)
        
    def _get_motion_probability(self) -> float:
        """Get motion probability based on sensitivity and mode."""
        base_probabilities = {
            'normal': {'low': 0.3, 'medium': 0.5, 'high': 0.7},
            'active': {'low': 0.6, 'medium': 0.8, 'high': 0.9},
            'inactive': {'low': 0.05, 'medium': 0.1, 'high': 0.2},
            'fall': {'low': 0.0, 'medium': 0.0, 'high': 0.0},  # No motion after fall
        }
        return base_probabilities.get(self.simulation_mode, {}).get(self.sensitivity, 0.5)
    
    def _initialize(self) -> bool:
        """Initialize the mock sensor (nothing to do for mock)."""
        print(f"[Mock PIR] Initialized in '{self.simulation_mode}' mode with '{self.sensitivity}' sensitivity")
        return True
    
    def _read(self) -> Optional[bool]:
        """
        Read motion detection.
        Returns True if motion detected, False otherwise.
        """
        # Simulate motion based on probability
        rand = random.random()
        
        # Check for false positives (sensor glitch, heating system, etc.)
        if rand < self.false_positive_rate:
            # Brief false positive
            return random.choice([True, False])
        
        # Check for pet detection (smaller, intermittent motion)
        if rand < self.false_positive_rate + self.pet_detection_rate:
            # Simulate pet - occasional small movements
            return random.random() < 0.3
        
        # Normal motion detection based on simulation mode
        motion = rand < self.motion_probability
        
        # Update state
        if motion:
            self.motion_detected = True
            self.last_motion_time = datetime.now()
            self.motion_duration += 1
        else:
            # Motion stops, but keep last_motion_time for a bit
            if self.last_motion_time and (datetime.now() - self.last_motion_time).seconds > 5:
                self.motion_detected = False
                self.motion_duration = 0
        
        return motion
    
    def set_simulation_mode(self, mode: str):
        """
        Change simulation mode for testing different scenarios.
        
        Args:
            mode: 'normal', 'active', 'inactive', or 'fall'
        """
        self.simulation_mode = mode
        self.motion_probability = self._get_motion_probability()
        print(f"[Mock PIR] Simulation mode changed to '{mode}'")
    
    def simulate_motion(self, duration_seconds: int = 5):
        """
        Manually trigger motion for testing.
        
        Args:
            duration_seconds: How long to simulate motion
        """
        self.motion_detected = True
        self.last_motion_time = datetime.now()
        self.motion_duration = duration_seconds
        print(f"[Mock PIR] Simulating motion for {duration_seconds} seconds")
    
    def simulate_no_motion(self):
        """Manually stop motion for testing."""
        self.motion_detected = False
        self.last_motion_time = None
        self.motion_duration = 0
        print("[Mock PIR] Motion stopped")
    
    def get_status(self) -> dict:
        """Get extended status including simulation info."""
        status = super().get_status()
        status.update({
            'simulation_mode': self.simulation_mode,
            'sensitivity': self.sensitivity,
            'motion_detected': self.motion_detected,
            'last_motion_time': self.last_motion_time.isoformat() if self.last_motion_time else None,
            'motion_duration': self.motion_duration,
        })
        return status
