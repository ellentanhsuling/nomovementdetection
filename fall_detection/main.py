#!/usr/bin/env python3
"""
Fall Detection System
Main application entry point

Detects immediate falls and emergencies using real-time camera analysis.
"""

import sys
from pathlib import Path

# Add shared and project paths
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / 'shared'))

from shared.base.monitoring_base import BaseMonitoringSystem
from fall_detection.detection.alert_manager import AlertManager, AlertLevel
from fall_detection.detection.fall_detector import FallDetector, FallStatus
from fall_detection.detection.pose_analyzer import PoseAnalyzer


class FallDetectionSystem(BaseMonitoringSystem):
    """
    Fall detection monitoring system.
    
    Detects immediate falls using real-time camera analysis.
    """
    
    def __init__(self, config_path: str = 'config.yaml'):
        super().__init__(config_path, "Fall Detection System")
        
        self.fall_detector: FallDetector = None
        self.pose_analyzer: PoseAnalyzer = None
        self.alert_manager: AlertManager = None
    
    def initialize_project(self):
        """Initialize project-specific components."""
        # Initialize fall detector
        self.fall_detector = FallDetector(self.config)
        
        # Initialize pose analyzer
        self.pose_analyzer = PoseAnalyzer(self.config)
        
        # Initialize alert manager
        self.alert_manager = AlertManager(
            self.config.get('alerts', {}),
            self.alert_channels
        )
        
        self.logger.info("Fall detection components initialized")
    
    def run_cycle(self):
        """Run one monitoring cycle."""
        from datetime import datetime
        
        # Read camera sensor
        camera_data = None
        for sensor_name, sensor in self.sensors.items():
            try:
                value = sensor.read()
                if sensor_name == 'Camera':
                    camera_data = value
                
                # Log sensor reading
                self.logger.log_sensor_reading(sensor_name, value)
            except Exception as e:
                self.logger.error(f"Error reading {sensor_name} sensor: {e}")
        
        pose_data = None
        if self.pose_analyzer is not None and self.pose_analyzer.is_active():
            frame = camera_data.get('frame') if camera_data else None
            pose_data = self.pose_analyzer.analyze_pose(
                frame=frame,
                camera_data=camera_data,
            )
        
        fall_status = self.fall_detector.analyze_frame(camera_data, pose_data)
        
        # Log fall status
        if fall_status == FallStatus.FALL_DETECTED:
            self.logger.critical(f"FALL DETECTED! Status: {fall_status.value}")
        elif fall_status == FallStatus.SUSPICIOUS:
            self.logger.warning(f"Suspicious activity detected: {fall_status.value}")
        else:
            self.logger.debug(f"Fall detection status: {fall_status.value}")
        
        # Handle alerts if fall detected
        if fall_status == FallStatus.FALL_DETECTED:
            self._handle_fall_alert()
        
        return {
            'fall_status': fall_status.value,
            'detector_status': self.fall_detector.get_status(),
        }
    
    def _handle_fall_alert(self):
        """Handle fall detection alert."""
        detector_status = self.fall_detector.get_status()
        fall_time = detector_status.get('fall_detected_time')
        
        alert = self.alert_manager.create_alert(
            AlertLevel.CRITICAL,
            "FALL DETECTED: Person may have fallen and needs immediate assistance",
            {
                'type': 'fall_detection',
                'fall_detected_time': fall_time,
                'detector_status': detector_status,
            }
        )
        
        # Send alert immediately (no escalation delay for falls)
        all_channels = list(self.alert_channels.keys())
        self.alert_manager.send_alert(alert, all_channels)
    
    def _print_status(self, result):
        """Print status with fall detection specific info."""
        from datetime import datetime
        status = result.get('fall_status', 'unknown')
        detector_status = result.get('detector_status', {})
        position = detector_status.get('last_position', 'unknown')
        
        print(f"[{datetime.now().strftime('%H:%M:%S')}] "
              f"Status: {status}, "
              f"Position: {position}")
    
    def shutdown_project(self):
        """Project-specific cleanup."""
        # Save any fall detection data if needed
        pass


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Fall Detection System'
    )
    parser.add_argument(
        '--config',
        type=str,
        default='config.yaml',
        help='Path to configuration file (default: config.yaml)'
    )
    parser.add_argument(
        '--mock',
        action='store_true',
        help='Force use of mock sensors (overrides config)'
    )
    
    args = parser.parse_args()
    
    # Create and run system
    system = FallDetectionSystem(args.config)
    
    # Override mock setting if requested
    if args.mock:
        system.use_mock = True
        # Reinitialize sensors with mock
        system.sensors.clear()
        system._initialize_sensors()
    
    # Initialize and run
    system.initialize()
    system.run()


if __name__ == '__main__':
    main()
