"""
Logging system for alerts and system events
"""

import logging
import os
from logging.handlers import RotatingFileHandler
from typing import Dict, Any, Optional
from datetime import datetime


class AlertLogger:
    """
    Centralized logging system for the monitoring application.
    
    Handles both file and console logging with rotation.
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize logger.
        
        Args:
            config: Logging configuration from config.yaml
        """
        self.config = config
        
        # Get configuration values
        log_level = getattr(logging, config.get('level', 'INFO').upper())
        log_file = config.get('file', 'logs/monitoring.log')
        max_file_size = config.get('max_file_size_mb', 10) * 1024 * 1024  # Convert to bytes
        backup_count = config.get('backup_count', 5)
        console_output = config.get('console_output', True)
        
        # Create logs directory if needed
        log_dir = os.path.dirname(log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir, exist_ok=True)
        
        # Create logger
        self.logger = logging.getLogger('elderly_monitoring')
        self.logger.setLevel(log_level)
        
        # Clear existing handlers
        self.logger.handlers = []
        
        # File handler with rotation
        if log_file:
            file_handler = RotatingFileHandler(
                log_file,
                maxBytes=max_file_size,
                backupCount=backup_count
            )
            file_handler.setLevel(log_level)
            file_formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            file_handler.setFormatter(file_formatter)
            self.logger.addHandler(file_handler)
        
        # Console handler
        if console_output:
            console_handler = logging.StreamHandler()
            console_handler.setLevel(log_level)
            console_formatter = logging.Formatter(
                '%(asctime)s - %(levelname)s - %(message)s',
                datefmt='%H:%M:%S'
            )
            console_handler.setFormatter(console_formatter)
            self.logger.addHandler(console_handler)
    
    def debug(self, message: str, **kwargs):
        """Log debug message."""
        self.logger.debug(self._format_message(message, **kwargs))
    
    def info(self, message: str, **kwargs):
        """Log info message."""
        self.logger.info(self._format_message(message, **kwargs))
    
    def warning(self, message: str, **kwargs):
        """Log warning message."""
        self.logger.warning(self._format_message(message, **kwargs))
    
    def error(self, message: str, **kwargs):
        """Log error message."""
        self.logger.error(self._format_message(message, **kwargs))
    
    def critical(self, message: str, **kwargs):
        """Log critical message."""
        self.logger.critical(self._format_message(message, **kwargs))
    
    def log_alert(self, alert_level: str, message: str, details: Dict[str, Any] = None):
        """
        Log an alert event.
        
        Args:
            alert_level: Alert level (info, warning, critical)
            message: Alert message
            details: Additional details
        """
        log_message = f"ALERT [{alert_level.upper()}]: {message}"
        if details:
            log_message += f" | Details: {details}"
        
        if alert_level.lower() == 'critical':
            self.critical(log_message)
        elif alert_level.lower() == 'warning':
            self.warning(log_message)
        else:
            self.info(log_message)
    
    def log_sensor_reading(self, sensor_name: str, value: Any):
        """Log a sensor reading."""
        self.debug(f"Sensor {sensor_name}: {value}")
    
    def log_movement_event(self, has_movement: bool, time_since: Optional[float] = None):
        """Log a movement detection event."""
        if has_movement:
            self.info(f"Movement detected")
        else:
            time_str = f"{time_since:.1f} min" if time_since else "unknown"
            self.info(f"No movement - {time_str} since last movement")
    
    def _format_message(self, message: str, **kwargs) -> str:
        """Format message with additional context."""
        if kwargs:
            context = ", ".join(f"{k}={v}" for k, v in kwargs.items())
            return f"{message} | {context}"
        return message
    
    def get_logger(self) -> logging.Logger:
        """Get the underlying logger instance."""
        return self.logger
