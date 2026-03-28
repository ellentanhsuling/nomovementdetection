"""
Mock Camera Sensor for Raspberry Pi Camera Module

This simulates a real camera for testing without hardware.
When the Raspberry Pi arrives, we'll use real_camera.py that
uses picamera2 to capture actual images.
"""

import random
import numpy as np
from datetime import datetime
from typing import Optional, Tuple, Dict, Any
from shared.sensors.base_sensor import BaseSensor


class MockCameraSensor(BaseSensor):
    """
    Mock camera sensor that simulates image capture and analysis.
    
    This class simulates the behavior of a Raspberry Pi Camera Module:
    - Captures "images" (simulated)
    - Detects person presence
    - Detects movement between frames
    - Can simulate different scenarios (normal, fall, no person)
    """
    
    def __init__(self, config: dict):
        super().__init__("Mock Camera Sensor", config)
        
        # Configuration
        self.resolution = config.get('resolution', (640, 480))  # width, height
        self.fps = config.get('fps', 10)
        self.simulation_mode = config.get('simulation_mode', 'normal')
        
        # Detection parameters
        self.motion_threshold = config.get('motion_threshold', 0.1)  # 10% change = motion
        self.person_detection_confidence = config.get('person_detection_confidence', 0.7)
        self.include_frame_for_pose = config.get('include_frame_for_pose', False)
        
        # State tracking
        self.last_frame: Optional[np.ndarray] = None
        self.person_detected = False
        self.motion_detected = False
        self.last_motion_time: Optional[datetime] = None
        
        # Simulation state
        self.frame_count = 0
        self.person_present_probability = self._get_person_probability()
        self.motion_probability = self._get_motion_probability()
    
    def _get_person_probability(self) -> float:
        """Get person presence probability based on simulation mode."""
        probabilities = {
            'normal': 0.8,  # Person usually present
            'person_present': 0.95,  # Person definitely present
            'person_absent': 0.1,  # Person rarely/never present
            'fall': 0.3,  # Person on floor (harder to detect)
            'sleeping': 0.7,  # Person present but still
        }
        return probabilities.get(self.simulation_mode, 0.8)
    
    def _get_motion_probability(self) -> float:
        """Get motion probability based on simulation mode."""
        probabilities = {
            'normal': 0.6,  # Regular movement
            'person_present': 0.4,  # Some movement
            'person_absent': 0.0,  # No movement
            'fall': 0.0,  # No movement after fall
            'sleeping': 0.05,  # Minimal movement
        }
        return probabilities.get(self.simulation_mode, 0.6)
    
    def _initialize(self) -> bool:
        """Initialize the mock camera (nothing to do for mock)."""
        print(f"[Mock Camera] Initialized in '{self.simulation_mode}' mode")
        print(f"[Mock Camera] Resolution: {self.resolution[0]}x{self.resolution[1]}, FPS: {self.fps}")
        return True
    
    def _read(self) -> Optional[Dict[str, Any]]:
        """
        Capture and analyze a frame.
        
        Returns:
            Dictionary with detection results:
            {
                'person_detected': bool,
                'motion_detected': bool,
                'motion_level': float (0.0 to 1.0),
                'person_confidence': float (0.0 to 1.0),
            }
        """
        self.frame_count += 1
        
        # Simulate person detection
        person_detected = random.random() < self.person_present_probability
        
        # Add some consistency (person doesn't appear/disappear instantly)
        if self.frame_count > 1:
            if self.person_detected and random.random() < 0.9:
                person_detected = True  # Person tends to stay
            elif not self.person_detected and random.random() < 0.8:
                person_detected = False  # Absence tends to persist
        
        self.person_detected = person_detected
        
        # Simulate motion detection
        motion_detected = False
        motion_level = 0.0
        
        if person_detected:
            # Motion only happens if person is present
            motion_detected = random.random() < self.motion_probability
            
            if motion_detected:
                motion_level = random.uniform(0.2, 1.0)  # Motion intensity
                self.last_motion_time = datetime.now()
            else:
                motion_level = random.uniform(0.0, 0.1)  # Minimal/no motion
        
        self.motion_detected = motion_detected
        
        # Person detection confidence
        if person_detected:
            person_confidence = random.uniform(self.person_detection_confidence, 1.0)
        else:
            person_confidence = random.uniform(0.0, 0.3)
        
        out = {
            'person_detected': person_detected,
            'motion_detected': motion_detected,
            'motion_level': round(motion_level, 3),
            'person_confidence': round(person_confidence, 3),
            'timestamp': datetime.now().isoformat(),
        }
        if self.include_frame_for_pose and person_detected:
            h, w = int(self.resolution[1]), int(self.resolution[0])
            out['frame'] = np.zeros((h, w), dtype=np.uint8)
        return out
    
    def set_simulation_mode(self, mode: str):
        """
        Change simulation mode for testing different scenarios.
        
        Args:
            mode: 'normal', 'person_present', 'person_absent', 'fall', or 'sleeping'
        """
        self.simulation_mode = mode
        self.person_present_probability = self._get_person_probability()
        self.motion_probability = self._get_motion_probability()
        print(f"[Mock Camera] Simulation mode changed to '{mode}'")
    
    def simulate_person_present(self):
        """Manually set person as present for testing."""
        self.person_detected = True
        self.person_present_probability = 1.0
        print("[Mock Camera] Person set as present")
    
    def simulate_person_absent(self):
        """Manually set person as absent for testing."""
        self.person_detected = False
        self.person_present_probability = 0.0
        print("[Mock Camera] Person set as absent")
    
    def simulate_fall(self):
        """Simulate a fall scenario (person present but no movement)."""
        self.person_detected = True
        self.motion_detected = False
        self.motion_probability = 0.0
        self.person_present_probability = 0.3  # Harder to detect on floor
        print("[Mock Camera] Simulating fall scenario")
    
    def get_status(self) -> dict:
        """Get extended status including detection info."""
        status = super().get_status()
        status.update({
            'simulation_mode': self.simulation_mode,
            'resolution': self.resolution,
            'fps': self.fps,
            'person_detected': self.person_detected,
            'motion_detected': self.motion_detected,
            'last_motion_time': self.last_motion_time.isoformat() if self.last_motion_time else None,
            'frame_count': self.frame_count,
        })
        return status
