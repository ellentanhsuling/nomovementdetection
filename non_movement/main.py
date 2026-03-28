#!/usr/bin/env python3
"""
Non-Movement Detection System
Main application entry point

Detects extended periods of inactivity (30+ minutes) that may indicate
a medical emergency or need for assistance.
"""

import sys
from pathlib import Path

# Add shared and project paths
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / 'shared'))

from shared.base.monitoring_base import BaseMonitoringSystem
from shared.data.thingspeak_logger import ThingSpeakLogger
from non_movement.detection.alert_manager import AlertManager, AlertLevel
from non_movement.detection.movement_detector import MovementDetector, MovementStatus
from non_movement.detection.pattern_learner import PatternLearner


class NonMovementSystem(BaseMonitoringSystem):
    """
    Non-movement detection monitoring system.
    
    Detects extended periods of inactivity using time-based thresholds.
    """
    
    def __init__(self, config_path: str = 'config.yaml'):
        super().__init__(config_path, "Non-Movement Detection System")
        
        self.movement_detector: MovementDetector = None
        self.pattern_learner: PatternLearner = None
        self.alert_manager: AlertManager = None
        self.thingspeak_logger: ThingSpeakLogger = None
    
    def initialize_project(self):
        """Initialize project-specific components."""
        # Initialize movement detector
        self.movement_detector = MovementDetector(self.config)
        
        # Initialize pattern learner
        self.pattern_learner = PatternLearner(self.config)
        
        # Initialize alert manager
        self.alert_manager = AlertManager(
            self.config.get('alerts', {}),
            self.alert_channels
        )
        
        # Initialize ThingSpeak logger (if enabled)
        thingspeak_config = self.config.get('data_logging', {}).get('thingspeak', {})
        if thingspeak_config.get('enabled', False):
            try:
                self.thingspeak_logger = ThingSpeakLogger(thingspeak_config, self.logger)
                if self.thingspeak_logger.is_enabled():
                    self.logger.info("ThingSpeak data logger enabled")
            except Exception as e:
                self.logger.warning(f"ThingSpeak logger not available: {e}")
        
        self.logger.info("Non-movement detection components initialized")
    
    def run_cycle(self):
        """Run one monitoring cycle."""
        from datetime import datetime
        
        # Read camera sensor
        sensor_readings = {}
        for sensor_name, sensor in self.sensors.items():
            try:
                value = sensor.read()
                sensor_readings[sensor_name] = value
                
                # Log sensor reading
                self.logger.log_sensor_reading(sensor_name, value)
                
                # Record for pattern learning
                if value is not None:
                    if isinstance(value, dict):
                        # Camera returns dict
                        self.pattern_learner.record_movement_event(
                            datetime.now(),
                            sensor_name,
                            value
                        )
            except Exception as e:
                self.logger.error(f"Error reading {sensor_name} sensor: {e}")
                sensor_readings[sensor_name] = None
        
        # Check movement status
        movement_status = self.movement_detector.check_movement_status(sensor_readings)
        
        # Get time since last movement
        time_since = self.movement_detector.get_time_since_last_movement()
        
        # Debug: log status and threshold info
        if time_since is not None and time_since >= 0.1:  # Only log if we have meaningful time
            self.logger.debug(f"Movement status: {movement_status.value}, Time since: {time_since:.3f} min")
        
        # Log movement status
        self.logger.log_movement_event(
            movement_status == MovementStatus.ACTIVE,
            time_since
        )
        
        # Handle alerts if concerning
        if movement_status == MovementStatus.CONCERNING:
            self.logger.info(f"CONCERNING status detected - time since movement: {time_since} min, triggering alert...")
            self.alert_manager.handle_movement_alert(
                movement_status.value,
                time_since,
                {
                    'sensor_readings': sensor_readings,
                    'detector_status': self.movement_detector.get_status(),
                }
            )
        elif movement_status == MovementStatus.INACTIVE:
            # Debug: log when we're inactive but not yet concerning
            self.logger.debug(f"INACTIVE status - time since movement: {time_since} min (threshold: 0.167 min)")
        
        # Send data to ThingSpeak (if enabled)
        if self.thingspeak_logger and self.thingspeak_logger.is_enabled():
            try:
                # Extract camera data from sensor readings
                camera_data = sensor_readings.get('Camera', {})
                if isinstance(camera_data, dict):
                    motion_detected = camera_data.get('motion_detected', False)
                    motion_level = camera_data.get('motion_level', 0.0)
                    person_detected = camera_data.get('person_detected', False)
                    person_confidence = camera_data.get('person_confidence', 0.0)
                    
                    self.thingspeak_logger.send_data(
                        motion_detected=motion_detected,
                        motion_level=motion_level,
                        person_detected=person_detected,
                        person_confidence=person_confidence,
                        time_since_movement=time_since
                    )
            except Exception as e:
                self.logger.warning(f"Failed to send data to ThingSpeak: {e}")
        
        return {
            'movement_status': movement_status.value,
            'time_since_movement': time_since,
            'sensor_readings': sensor_readings,
        }
    
    def _print_status(self, result):
        """Print status with non-movement specific info."""
        from datetime import datetime
        status = result.get('movement_status', 'unknown')
        time_since = result.get('time_since_movement')
        
        time_str = f"{time_since:.1f} min" if time_since else "N/A"
        print(f"[{datetime.now().strftime('%H:%M:%S')}] "
              f"Status: {status}, "
              f"Time since movement: {time_str}")
    
    def shutdown_project(self):
        """Project-specific cleanup."""
        # Save patterns
        try:
            self.pattern_learner.save_patterns()
            self.logger.info("Pattern data saved")
        except Exception as e:
            self.logger.error(f"Error saving patterns: {e}")


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Non-Movement Detection System'
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
    system = NonMovementSystem(args.config)
    
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
