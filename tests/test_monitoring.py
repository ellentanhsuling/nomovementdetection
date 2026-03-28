"""
Tests for monitoring logic
"""

import unittest
from datetime import datetime, timedelta
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.monitoring.movement_detector import MovementDetector, MovementStatus


class TestMovementDetector(unittest.TestCase):
    """Test movement detection logic"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.config = {
            'monitoring': {
                'no_movement_threshold_active': 30,  # 30 minutes
                'no_movement_threshold_sleep': 120,  # 2 hours
                'no_movement_threshold_anytime': 60,  # 1 hour
                'active_hours': {'start': 7, 'end': 22},
                'sleep_hours': {'start': 22, 'end': 7},
                'require_multiple_sensors': False,
            },
            'sensors': {
                'ultrasonic': {
                    'presence_threshold': 200,
                },
            },
        }
        self.detector = MovementDetector(self.config)
    
    def test_movement_detection_active(self):
        """Test detection when movement is active"""
        sensor_readings = {
            'PIR': True,
            'Ultrasonic': 150,  # Person present
        }
        
        status = self.detector.check_movement_status(sensor_readings)
        self.assertEqual(status, MovementStatus.ACTIVE)
    
    def test_movement_detection_inactive(self):
        """Test detection when no movement but within threshold"""
        # Record some movement first
        self.detector.record_movement('PIR', True, datetime.now() - timedelta(minutes=10))
        
        sensor_readings = {
            'PIR': False,
            'Ultrasonic': 350,  # Person absent
        }
        
        status = self.detector.check_movement_status(sensor_readings)
        self.assertEqual(status, MovementStatus.INACTIVE)
    
    def test_movement_detection_concerning(self):
        """Test detection when threshold exceeded"""
        # Record movement long ago
        self.detector.record_movement('PIR', True, datetime.now() - timedelta(minutes=45))
        
        sensor_readings = {
            'PIR': False,
            'Ultrasonic': 350,  # Person absent
        }
        
        status = self.detector.check_movement_status(sensor_readings)
        self.assertEqual(status, MovementStatus.CONCERNING)
    
    def test_active_hours_detection(self):
        """Test active hours detection"""
        # Test during active hours (e.g., 10 AM)
        test_time = datetime.now().replace(hour=10, minute=0)
        self.assertTrue(self.detector.is_active_hours(test_time))
        
        # Test during sleep hours (e.g., 2 AM)
        test_time = datetime.now().replace(hour=2, minute=0)
        self.assertTrue(self.detector.is_sleep_hours(test_time))
    
    def test_time_since_movement(self):
        """Test time since last movement calculation"""
        # Record movement
        movement_time = datetime.now() - timedelta(minutes=15)
        self.detector.record_movement('PIR', True, movement_time)
        
        time_since = self.detector.get_time_since_last_movement()
        self.assertIsNotNone(time_since)
        self.assertAlmostEqual(time_since, 15.0, delta=1.0)  # Allow 1 minute tolerance
    
    def test_reset(self):
        """Test detector reset"""
        self.detector.record_movement('PIR', True)
        self.assertIsNotNone(self.detector.last_movement_time)
        
        self.detector.reset()
        self.assertIsNone(self.detector.last_movement_time)


if __name__ == '__main__':
    unittest.main()
