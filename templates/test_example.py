"""
Example Test File Structure
Use this as a reference for writing your own tests

This shows the STRUCTURE, not the complete implementation.
You need to write the actual test logic.
"""

import unittest
import sys
import os

# Add project to path (adjust path as needed)
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Import what you're testing
# from shared.sensors.mock_camera import MockCameraSensor
# from non_movement.detection.movement_detector import MovementDetector


class TestExample(unittest.TestCase):
    """
    Example test class structure
    
    Each test method should:
    1. Set up what you need
    2. Run the code
    3. Check the result
    """
    
    def setUp(self):
        """
        This runs BEFORE each test
        Use it to set up test data
        """
        # Example: Create test configuration
        self.config = {
            'enabled': True,
            'check_interval': 30,
        }
        # Example: Create object to test
        # self.sensor = MockCameraSensor(self.config)
    
    def tearDown(self):
        """
        This runs AFTER each test
        Use it to clean up
        """
        pass
    
    def test_example(self):
        """
        Example test method
        
        Test names should start with 'test_'
        """
        # Arrange: Set up test
        # Act: Run the code you're testing
        # Assert: Check the result
        
        # Example:
        # result = self.sensor.read()
        # self.assertIsNotNone(result)
        # self.assertIn('person_detected', result)
        pass
    
    def test_another_example(self):
        """
        You can have multiple test methods
        Each tests a different aspect
        """
        pass


class TestAnotherClass(unittest.TestCase):
    """
    You can have multiple test classes
    One per class you're testing
    """
    pass


# Run tests if file is executed directly
if __name__ == '__main__':
    unittest.main()

# To run from command line:
# python -m pytest tests/test_example.py
# or
# python tests/test_example.py
