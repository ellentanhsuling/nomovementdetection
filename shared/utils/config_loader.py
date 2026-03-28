"""
Configuration loader

Loads and validates configuration from YAML file.
"""

import yaml
import os
from typing import Dict, Any
from pathlib import Path


def load_config(config_path: str = 'config.yaml') -> Dict[str, Any]:
    """
    Load configuration from YAML file.
    
    Args:
        config_path: Path to config file
    
    Returns:
        Configuration dictionary
    
    Raises:
        FileNotFoundError: If config file doesn't exist
        yaml.YAMLError: If config file is invalid
    """
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Configuration file not found: {config_path}")
    
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    
    if config is None:
        config = {}
    
    return config


def validate_config(config: Dict[str, Any]) -> tuple:
    """
    Validate configuration structure.
    
    Args:
        config: Configuration dictionary
    
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    
    # Check required sections
    required_sections = ['sensors', 'monitoring', 'alerts', 'logging', 'system']
    for section in required_sections:
        if section not in config:
            errors.append(f"Missing required section: {section}")
    
    # Validate sensor configuration
    if 'sensors' in config:
        sensors = config['sensors']
        # Allow camera-only, PIR, Ultrasonic, or any combination
        if 'camera' not in sensors and 'pir' not in sensors and 'ultrasonic' not in sensors:
            errors.append("At least one sensor (Camera, PIR, or Ultrasonic) must be configured")
        # If camera is configured, check it's enabled
        if 'camera' in sensors:
            camera_config = sensors.get('camera', {})
            if camera_config.get('enabled', False) is False:
                errors.append("Camera sensor is configured but not enabled")
    
    # Validate monitoring thresholds
    if 'monitoring' in config:
        monitoring = config['monitoring']
        thresholds = [
            'no_movement_threshold_active',
            'no_movement_threshold_sleep',
            'no_movement_threshold_anytime',
        ]
        for threshold in thresholds:
            if threshold in monitoring:
                value = monitoring[threshold]
                if not isinstance(value, (int, float)) or value <= 0:
                    errors.append(f"Invalid threshold value for {threshold}: {value}")
    
    return len(errors) == 0, errors
