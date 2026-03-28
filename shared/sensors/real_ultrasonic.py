"""
Real Ultrasonic Distance Sensor (HC-SR04) for Raspberry Pi

This will be implemented when the Raspberry Pi arrives.
It will use GPIO pins to trigger and read echo from the actual HC-SR04 sensor.

For now, this is a placeholder that shows the structure.
"""

from typing import Optional
from .base_sensor import BaseSensor


class RealUltrasonicSensor(BaseSensor):
    """
    Real ultrasonic sensor implementation using Raspberry Pi GPIO.
    
    This class will be implemented when hardware is available.
    It will use gpiozero or RPi.GPIO to control trigger and echo pins.
    """
    
    def __init__(self, config: dict):
        super().__init__("Real Ultrasonic Sensor", config)
        self.trigger_pin = config.get('trigger_pin', 23)
        self.echo_pin = config.get('echo_pin', 24)
        self.min_distance = config.get('min_distance', 2)
        self.max_distance = config.get('max_distance', 400)
        self.presence_threshold = config.get('presence_threshold', 200)
        
        # GPIO objects (will be initialized when Pi arrives)
        self.trigger = None
        self.echo = None
    
    def _initialize(self) -> bool:
        """
        Initialize GPIO pins for trigger and echo.
        
        TODO: When Pi arrives, implement:
        from gpiozero import OutputDevice, InputDevice
        import time
        
        self.trigger = OutputDevice(self.trigger_pin)
        self.echo = InputDevice(self.echo_pin)
        """
        print("[Real Ultrasonic] WARNING: Real sensor not yet implemented. Use mock sensor for now.")
        return False
    
    def _read(self) -> Optional[float]:
        """
        Read distance from real ultrasonic sensor.
        
        TODO: When Pi arrives, implement:
        1. Send trigger pulse
        2. Measure echo pulse duration
        3. Calculate distance: distance = (duration * speed_of_sound) / 2
        4. Return distance in cm
        """
        return None
    
    def is_person_present(self) -> bool:
        """Check if person is present based on distance threshold."""
        distance = self.read()
        if distance is None:
            return False
        return distance < self.presence_threshold
    
    def _cleanup(self):
        """Clean up GPIO resources."""
        if self.trigger:
            self.trigger.close()
        if self.echo:
            self.echo.close()
