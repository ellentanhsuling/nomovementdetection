"""
Real Camera Sensor for Raspberry Pi Camera Module

Uses picamera2 to capture images and OpenCV for analysis.
"""

import numpy as np
import cv2
from typing import Optional, Dict, Any, Tuple
from datetime import datetime
from shared.sensors.base_sensor import BaseSensor

try:
    from picamera2 import Picamera2
    PICAMERA2_AVAILABLE = True
except ImportError:
    PICAMERA2_AVAILABLE = False


class RealCameraSensor(BaseSensor):
    """
    Real camera sensor implementation using Raspberry Pi Camera Module.
    
    This class will be implemented when hardware is available.
    It will use picamera2 to capture images and OpenCV for:
    - Person detection (using simple motion detection or ML models)
    - Movement detection (frame differencing)
    - Fall detection (person on floor detection)
    """
    
    def __init__(self, config: dict):
        super().__init__("Real Camera Sensor", config)
        
        # Configuration
        self.resolution = config.get('resolution', (640, 480))
        self.fps = config.get('fps', 10)
        self.motion_threshold = config.get('motion_threshold', 0.1)
        self.person_detection_confidence = config.get('person_detection_confidence', 0.7)
        self.include_frame_for_pose = config.get('include_frame_for_pose', False)
        
        # Camera objects (will be initialized when Pi arrives)
        self.camera = None  # Will be picamera2.Picamera2
        self.last_frame: Optional[np.ndarray] = None
        
        # Detection state
        self.person_detected = False
        self.motion_detected = False
        self.last_motion_time: Optional[datetime] = None
    
    def _initialize(self) -> bool:
        """
        Initialize camera and start capture.
        """
        if not PICAMERA2_AVAILABLE:
            print("[Real Camera] ERROR: picamera2 not available. Install with: pip install picamera2")
            return False
        
        try:
            self.camera = Picamera2()
            config = self.camera.create_preview_configuration(
                main={"size": self.resolution}
            )
            self.camera.configure(config)
            self.camera.start()
            print(f"[Real Camera] Initialized - Resolution: {self.resolution[0]}x{self.resolution[1]}, FPS: {self.fps}")
            return True
        except Exception as e:
            print(f"[Real Camera] ERROR: Failed to initialize camera: {e}")
            return False
    
    def _read(self) -> Optional[Dict[str, Any]]:
        """
        Capture frame and analyze for person/movement.
        
        Returns:
            Dictionary with detection results:
            {
                'person_detected': bool,
                'motion_detected': bool,
                'motion_level': float (0.0 to 1.0),
                'person_confidence': float (0.0 to 1.0),
            }
        """
        if self.camera is None:
            return None
        
        try:
            # Capture frame
            frame = self.camera.capture_array()
            
            # Convert to grayscale for processing
            if len(frame.shape) == 3:
                gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            else:
                gray_frame = frame
            
            # Detect motion
            motion_detected, motion_level = self._detect_motion(gray_frame, self.last_frame)
            
            # Detect person (simplified: use motion as proxy)
            person_detected, person_confidence = self._detect_person(gray_frame)
            
            # Update state
            self.last_frame = gray_frame.copy()
            self.motion_detected = motion_detected
            self.person_detected = person_detected
            
            if motion_detected:
                self.last_motion_time = datetime.now()
            
            out = {
                'person_detected': person_detected,
                'motion_detected': motion_detected,
                'motion_level': round(motion_level, 3),
                'person_confidence': round(person_confidence, 3),
                'timestamp': datetime.now().isoformat(),
            }
            if self.include_frame_for_pose and person_detected:
                out['frame'] = gray_frame
            return out
        except Exception as e:
            print(f"[Real Camera] ERROR reading frame: {e}")
            return None
    
    def _detect_motion(self, current_frame: np.ndarray, previous_frame: Optional[np.ndarray]) -> Tuple[bool, float]:
        """
        Detect motion between frames using frame differencing.
        
        Args:
            current_frame: Current frame (grayscale)
            previous_frame: Previous frame (grayscale) or None
        
        Returns:
            Tuple of (motion_detected: bool, motion_level: float)
        """
        if previous_frame is None:
            return False, 0.0
        
        # Calculate frame difference
        diff = cv2.absdiff(current_frame, previous_frame)
        
        # Apply threshold to reduce noise
        _, thresh = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)
        
        # Calculate motion level (percentage of changed pixels)
        motion_level = np.sum(thresh > 0) / (thresh.shape[0] * thresh.shape[1])
        
        motion_detected = motion_level > self.motion_threshold
        
        return motion_detected, motion_level
    
    def _detect_person(self, frame: np.ndarray) -> Tuple[bool, float]:
        """
        Detect if a person is present in the frame.
        
        This is a simplified version. In production, you might use:
        - Motion detection (if motion detected, person likely present)
        - ML models (YOLO, MobileNet, etc.)
        - Background subtraction
        
        Args:
            frame: Current frame
        
        Returns:
            Tuple of (person_detected: bool, confidence: float)
        """
        # Simplified: Use motion detection as proxy for person presence
        # In production, use proper person detection model
        if self.last_frame is not None:
            motion_detected, motion_level = self._detect_motion(frame, self.last_frame)
            if motion_level > 0.05:  # Threshold for person presence
                return True, min(1.0, motion_level * 2)  # Scale up confidence
        
        return False, 0.0
    
    def _cleanup(self):
        """Clean up camera resources."""
        if self.camera:
            try:
                self.camera.stop()
                self.camera.close()
            except Exception as e:
                print(f"Error closing camera: {e}")
