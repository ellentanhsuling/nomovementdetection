"""
Base sensor class that all sensors inherit from
"""

from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
from datetime import datetime


class BaseSensor(ABC):
    """
    Abstract base class for all sensors.
    
    This defines the interface that all sensors (mock or real) must implement.
    When the Raspberry Pi arrives, real sensor classes will inherit from this
    and implement the actual GPIO reading methods.
    """
    
    def __init__(self, name: str, config: Dict[str, Any]):
        """
        Initialize the sensor.
        
        Args:
            name: Human-readable name of the sensor
            config: Configuration dictionary for this sensor
        """
        self.name = name
        self.config = config
        self.enabled = config.get('enabled', True)
        self.check_interval = config.get('check_interval', 30)
        self.last_reading_time: Optional[datetime] = None
        self.last_reading_value: Optional[Any] = None
        self.is_initialized = False
    
    def initialize(self) -> bool:
        """
        Initialize the sensor hardware/software.
        Returns True if successful, False otherwise.
        """
        if not self.enabled:
            return False
        
        try:
            result = self._initialize()
            self.is_initialized = result
            return result
        except Exception as e:
            print(f"Error initializing {self.name}: {e}")
            self.is_initialized = False
            return False
    
    @abstractmethod
    def _initialize(self) -> bool:
        """
        Sensor-specific initialization.
        Must be implemented by each sensor class.
        """
        pass
    
    def read(self) -> Optional[Any]:
        """
        Read the current sensor value.
        Returns the sensor reading or None if error.
        """
        if not self.enabled or not self.is_initialized:
            return None
        
        try:
            value = self._read()
            self.last_reading_time = datetime.now()
            self.last_reading_value = value
            return value
        except Exception as e:
            print(f"Error reading {self.name}: {e}")
            return None
    
    @abstractmethod
    def _read(self) -> Optional[Any]:
        """
        Sensor-specific reading implementation.
        Must be implemented by each sensor class.
        """
        pass
    
    def cleanup(self):
        """
        Clean up resources when shutting down.
        """
        if self.is_initialized:
            try:
                self._cleanup()
            except Exception as e:
                print(f"Error cleaning up {self.name}: {e}")
            finally:
                self.is_initialized = False
    
    def _cleanup(self):
        """
        Sensor-specific cleanup.
        Override if needed.
        """
        pass
    
    def get_status(self) -> Dict[str, Any]:
        """
        Get current status of the sensor.
        """
        return {
            'name': self.name,
            'enabled': self.enabled,
            'initialized': self.is_initialized,
            'last_reading_time': self.last_reading_time.isoformat() if self.last_reading_time else None,
            'last_reading_value': self.last_reading_value,
            'check_interval': self.check_interval,
        }
