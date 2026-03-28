"""
HTTP API alert channel

Sends alerts to a remote API endpoint (e.g., dashboard server).
"""

import requests
from typing import Dict, Any, Optional
from datetime import datetime

from shared.alerts.logger import AlertLogger


class APIAlert:
    """
    HTTP API alert channel.
    
    Sends alerts to a remote API endpoint via HTTP POST.
    """
    
    def __init__(self, config: Dict[str, Any], logger: Optional[AlertLogger] = None):
        """
        Initialize API alert channel.
        
        Args:
            config: API configuration from config.yaml
            logger: Optional logger instance
        """
        self.config = config
        self.logger = logger
        
        self.enabled = config.get('enabled', False)
        self.endpoint = config.get('endpoint', '')
        self.timeout = config.get('timeout', 5)
        self.retry_attempts = config.get('retry_attempts', 3)
        self.retry_delay = config.get('retry_delay', 2)
    
    def is_enabled(self) -> bool:
        """Check if API alerts are enabled."""
        return self.enabled and bool(self.endpoint)
    
    def send(self, alert: Any) -> bool:
        """
        Send alert via HTTP API.
        
        Args:
            alert: Alert object with message and details
        
        Returns:
            True if sent successfully, False otherwise
        """
        if not self.is_enabled():
            return False
        
        # Prepare payload
        payload = {
            'level': alert.level.value,
            'message': alert.message,
            'details': alert.details,
            'timestamp': alert.timestamp.isoformat(),
        }
        
        # Retry logic
        for attempt in range(self.retry_attempts):
            try:
                response = requests.post(
                    self.endpoint,
                    json=payload,
                    timeout=self.timeout,
                    headers={'Content-Type': 'application/json'}
                )
                
                # Check if request was successful
                if response.status_code in [200, 201, 202]:
                    if self.logger:
                        self.logger.info(f"API alert sent successfully to {self.endpoint}")
                    return True
                else:
                    if self.logger:
                        self.logger.warning(
                            f"API alert returned status {response.status_code}: {response.text}"
                        )
                    
                    # Don't retry on client errors (4xx)
                    if 400 <= response.status_code < 500:
                        return False
                    
            except requests.exceptions.Timeout:
                if self.logger:
                    self.logger.warning(f"API alert timeout (attempt {attempt + 1}/{self.retry_attempts})")
            except requests.exceptions.ConnectionError:
                if self.logger:
                    self.logger.warning(f"API alert connection error (attempt {attempt + 1}/{self.retry_attempts})")
            except Exception as e:
                if self.logger:
                    self.logger.error(f"API alert error: {e}")
                return False
            
            # Wait before retry (except on last attempt)
            if attempt < self.retry_attempts - 1:
                import time
                time.sleep(self.retry_delay)
        
        if self.logger:
            self.logger.error(f"Failed to send API alert after {self.retry_attempts} attempts")
        return False
