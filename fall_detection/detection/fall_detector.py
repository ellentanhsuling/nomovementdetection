"""
Fall Detection Algorithm

Detects immediate falls using real-time camera analysis.
Analyzes person position, sudden position changes, and floor detection.
"""

from datetime import datetime
from typing import Optional, Dict, Any
from enum import Enum


class FallStatus(Enum):
    """Status of fall detection"""
    NORMAL = "normal"  # Person standing/sitting normally
    SUSPICIOUS = "suspicious"  # Unusual position detected
    FALL_DETECTED = "fall_detected"  # Fall confirmed - alert needed
    UNKNOWN = "unknown"  # Cannot determine status


class FallDetector:
    """
    Detects falls using camera-based analysis.
    
    This class implements fall detection by:
    1. Analyzing person position (standing vs lying)
    2. Detecting sudden position changes
    3. Detecting person on floor
    4. Tracking time in unusual position
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the fall detector.
        
        Args:
            config: Configuration dictionary from config.yaml
        """
        self.config = config
        detection_config = config.get('detection', {})
        
        # Detection parameters
        self.position_change_threshold = detection_config.get('position_change_threshold', 0.5)
        self.floor_detection_enabled = detection_config.get('floor_detection_enabled', True)
        self.fall_confirmation_time = detection_config.get('fall_confirmation_time', 10)  # seconds
        self.prefer_pose = detection_config.get('prefer_pose_when_available', True)
        
        # State tracking
        self.last_position: Optional[str] = None  # 'standing', 'sitting', 'lying', 'unknown'
        self.position_change_time: Optional[datetime] = None
        self.consecutive_floor_detections = 0
        self.fall_detected_time: Optional[datetime] = None
    
    def analyze_frame(
        self,
        camera_data: Optional[Dict[str, Any]],
        pose_data: Optional[Dict[str, Any]] = None,
    ) -> FallStatus:
        """
        Analyze camera frame for fall detection.
        
        Args:
            camera_data: Dictionary from camera sensor with detection results
            pose_data: Optional pose dict from PoseAnalyzer (Hailo / mock)
        
        Returns:
            FallStatus indicating current state
        """
        if camera_data is None:
            return FallStatus.UNKNOWN
        
        # Extract camera detection results
        person_detected = camera_data.get('person_detected', False)
        
        if not person_detected:
            return FallStatus.UNKNOWN
        
        current_position = self._resolve_position(camera_data, pose_data)
        
        # Check for sudden position change (potential fall)
        if self.last_position and current_position != self.last_position:
            # Position changed - check if it's a fall
            if self.last_position in ('standing', 'sitting') and current_position == 'lying':
                # Potential fall: standing -> lying
                self.position_change_time = datetime.now()
                self.consecutive_floor_detections = 1
                return FallStatus.SUSPICIOUS
        
        # Check if person is on floor
        if current_position == 'lying':
            if self.position_change_time:
                time_on_floor = (datetime.now() - self.position_change_time).total_seconds()
                
                # If person has been on floor for confirmation time, it's a fall
                if time_on_floor >= self.fall_confirmation_time:
                    if not self.fall_detected_time:
                        self.fall_detected_time = datetime.now()
                    return FallStatus.FALL_DETECTED
                
                # Still confirming
                self.consecutive_floor_detections += 1
                return FallStatus.SUSPICIOUS
        
        # Reset if person is no longer on floor
        if current_position != 'lying':
            self.position_change_time = None
            self.consecutive_floor_detections = 0
            self.fall_detected_time = None
        
        self.last_position = current_position
        
        return FallStatus.NORMAL
    
    def _resolve_position(
        self,
        camera_data: Dict[str, Any],
        pose_data: Optional[Dict[str, Any]],
    ) -> str:
        """Use pose when available and trusted; otherwise motion heuristics."""
        if self.prefer_pose and pose_data and pose_data.get('pose_detected'):
            pos = pose_data.get('position', 'unknown')
            if pos in ('standing', 'sitting', 'lying', 'unknown'):
                return pos
        return self._determine_position(camera_data)
    
    def _determine_position(self, camera_data: Dict[str, Any]) -> str:
        """
        Determine person's position from camera data.
        
        In a real implementation, this would use:
        - Pose estimation (OpenPose, MediaPipe, etc.)
        - Position analysis (height, orientation)
        - Machine learning models
        
        For now, this is a simplified version using motion patterns.
        
        Args:
            camera_data: Camera detection results
        
        Returns:
            Position string: 'standing', 'sitting', 'lying', or 'unknown'
        """
        motion_level = camera_data.get('motion_level', 0.0)
        person_confidence = camera_data.get('person_confidence', 0.0)
        
        # Simplified position detection based on motion and confidence
        # In production, use proper pose estimation
        
        if person_confidence < 0.5:
            return 'unknown'
        
        # Low motion + high confidence might indicate lying (still person)
        if motion_level < 0.1 and person_confidence > 0.7:
            # Could be lying or sitting still
            # In real implementation, analyze pose/position
            return 'lying'  # Simplified - assume lying if very still
        
        # Medium motion - likely standing or sitting
        if 0.1 <= motion_level < 0.5:
            return 'standing'  # Simplified
        
        # High motion - definitely standing/moving
        return 'standing'
    
    def get_status(self) -> Dict[str, Any]:
        """Get current status of the fall detector."""
        return {
            'last_position': self.last_position,
            'position_change_time': self.position_change_time.isoformat() if self.position_change_time else None,
            'consecutive_floor_detections': self.consecutive_floor_detections,
            'fall_detected_time': self.fall_detected_time.isoformat() if self.fall_detected_time else None,
        }
    
    def reset(self):
        """Reset detector state."""
        self.last_position = None
        self.position_change_time = None
        self.consecutive_floor_detections = 0
        self.fall_detected_time = None
