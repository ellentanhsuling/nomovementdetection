"""
Tests for sensor implementations
"""

import unittest
from datetime import datetime
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.sensors.mock_pir import MockPIRSensor
from src.sensors.mock_ultrasonic import MockUltrasonicSensor


class TestMockPIRSensor(unittest.TestCase):
    """Test mock PIR sensor"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.config = {
            'enabled': True,
            'check_interval': 30,
            'sensitivity': 'medium',
            'simulation_mode': 'normal',
        }
        self.sensor = MockPIRSensor(self.config)
    
    def test_initialization(self):
        """Test sensor initialization"""
        self.assertTrue(self.sensor.initialize())
        self.assertTrue(self.sensor.is_initialized)
    
    def test_reading(self):
        """Test sensor reading"""
        self.sensor.initialize()
        value = self.sensor.read()
        self.assertIsNotNone(value)
        self.assertIsInstance(value, bool)
    
    def test_simulation_modes(self):
        """Test different simulation modes"""
        self.sensor.initialize()
        
        # Test active mode
        self.sensor.set_simulation_mode('active')
        active_readings = [self.sensor.read() for _ in range(10)]
        # Should have more True values in active mode
        self.assertGreater(sum(active_readings), 3)
        
        # Test inactive mode
        self.sensor.set_simulation_mode('inactive')
        inactive_readings = [self.sensor.read() for _ in range(10)]
        # Should have fewer True values in inactive mode
        self.assertLess(sum(inactive_readings), 5)
    
    def test_cleanup(self):
        """Test sensor cleanup"""
        self.sensor.initialize()
        self.sensor.cleanup()
        self.assertFalse(self.sensor.is_initialized)


class TestMockUltrasonicSensor(unittest.TestCase):
    """Test mock ultrasonic sensor"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.config = {
            'enabled': True,
            'check_interval': 30,
            'min_distance': 2,
            'max_distance': 400,
            'presence_threshold': 200,
            'simulation_mode': 'normal',
        }
        self.sensor = MockUltrasonicSensor(self.config)
    
    def test_initialization(self):
        """Test sensor initialization"""
        self.assertTrue(self.sensor.initialize())
        self.assertTrue(self.sensor.is_initialized)
    
    def test_reading(self):
        """Test sensor reading"""
        self.sensor.initialize()
        value = self.sensor.read()
        self.assertIsNotNone(value)
        self.assertIsInstance(value, (int, float))
        self.assertGreaterEqual(value, self.config['min_distance'])
        self.assertLessEqual(value, self.config['max_distance'])
    
    def test_presence_detection(self):
        """Test person presence detection"""
        self.sensor.initialize()
        
        # Set close distance (person present)
        self.sensor.set_distance(50)
        self.assertTrue(self.sensor.is_person_present())
        
        # Set far distance (person absent)
        self.sensor.set_distance(300)
        self.assertFalse(self.sensor.is_person_present())
    
    def test_simulation_modes(self):
        """Test different simulation modes"""
        self.sensor.initialize()
        
        # Test person_present mode
        self.sensor.set_simulation_mode('person_present')
        readings = [self.sensor.read() for _ in range(10)]
        avg_distance = sum(readings) / len(readings)
        self.assertLess(avg_distance, 150)  # Should be closer
        
        # Test person_absent mode
        self.sensor.set_simulation_mode('person_absent')
        readings = [self.sensor.read() for _ in range(10)]
        avg_distance = sum(readings) / len(readings)
        self.assertGreater(avg_distance, 200)  # Should be farther


if __name__ == '__main__':
    unittest.main()
