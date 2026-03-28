"""
ThingSpeak Data Logger

Sends sensor readings and movement data to ThingSpeak (free IoT platform).
Free tier: 3 messages per 15 seconds, 8,200 messages/day

Setup:
1. Create free account at https://thingspeak.com
2. Create a new Channel
3. Get your Write API Key
4. Add to config.yaml or .env file
"""

import requests
import urllib3
from typing import Dict, Any, Optional
from datetime import datetime
import time

from shared.alerts.logger import AlertLogger

# Suppress SSL warnings (Pi has expired certificates)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class ThingSpeakLogger:
    """
    ThingSpeak data logger for sending sensor readings.
    
    Free tier limits:
    - 3 messages per 15 seconds
    - 8,200 messages per day
    - 4 million messages per year
    """
    
    def __init__(self, config: Dict[str, Any], logger: Optional[AlertLogger] = None):
        """
        Initialize ThingSpeak logger.
        
        Args:
            config: ThingSpeak configuration from config.yaml
            logger: Optional logger instance
        """
        self.config = config
        self.logger = logger
        
        self.enabled = config.get('enabled', False)
        self.write_api_key = config.get('write_api_key', '')
        self.channel_id = config.get('channel_id', '')
        self.base_url = f"https://api.thingspeak.com/update"
        
        # Rate limiting (3 messages per 15 seconds)
        self.last_send_time = 0
        self.min_interval = 5  # seconds between sends (conservative)
        
        if not self.write_api_key:
            if self.logger:
                self.logger.warning("ThingSpeak write API key not configured. ThingSpeak logging disabled.")
            self.enabled = False
    
    def is_enabled(self) -> bool:
        """Check if ThingSpeak logging is enabled."""
        return self.enabled and bool(self.write_api_key)
    
    def send_data(self, 
                  motion_detected: bool,
                  motion_level: float = 0.0,
                  person_detected: bool = False,
                  person_confidence: float = 0.0,
                  time_since_movement: Optional[float] = None) -> bool:
        """
        Send sensor data to ThingSpeak.
        
        ThingSpeak field mapping:
        - Field 1: motion_detected (0 or 1)
        - Field 2: motion_level (0.0 to 1.0)
        - Field 3: person_detected (0 or 1)
        - Field 4: person_confidence (0.0 to 1.0)
        - Field 5: time_since_movement (minutes, or -1 if unknown)
        
        Args:
            motion_detected: Whether motion was detected
            motion_level: Motion intensity (0.0 to 1.0)
            person_detected: Whether person was detected
            person_confidence: Person detection confidence (0.0 to 1.0)
            time_since_movement: Minutes since last movement (None if unknown)
        
        Returns:
            True if sent successfully, False otherwise
        """
        if not self.is_enabled():
            return False
        
        # Rate limiting
        current_time = time.time()
        if current_time - self.last_send_time < self.min_interval:
            if self.logger:
                self.logger.debug("ThingSpeak rate limit: skipping send")
            return False
        
        try:
            # Prepare data payload
            params = {
                'api_key': self.write_api_key,
                'field1': 1 if motion_detected else 0,
                'field2': round(motion_level, 3),
                'field3': 1 if person_detected else 0,
                'field4': round(person_confidence, 3),
                'field5': round(time_since_movement, 2) if time_since_movement is not None else -1,
            }
            
            # Send to ThingSpeak
            # Note: verify=False is used due to Pi's expired SSL certificates
            # For production, update system certificates: sudo apt update && sudo apt install ca-certificates
            response = requests.get(self.base_url, params=params, timeout=5, verify=False)
            
            if response.status_code == 200:
                entry_id = response.text.strip()
                if entry_id.isdigit():
                    self.last_send_time = current_time
                    if self.logger:
                        self.logger.debug(f"ThingSpeak data sent successfully (entry ID: {entry_id})")
                    return True
                else:
                    if self.logger:
                        self.logger.warning(f"ThingSpeak returned invalid entry ID: {entry_id}")
                    return False
            else:
                if self.logger:
                    self.logger.warning(f"ThingSpeak request failed with status {response.status_code}: {response.text}")
                return False
                
        except requests.exceptions.Timeout:
            if self.logger:
                self.logger.warning("ThingSpeak request timeout")
            return False
        except requests.exceptions.ConnectionError:
            if self.logger:
                self.logger.warning("ThingSpeak connection error")
            return False
        except Exception as e:
            if self.logger:
                self.logger.error(f"ThingSpeak error: {e}")
            return False
