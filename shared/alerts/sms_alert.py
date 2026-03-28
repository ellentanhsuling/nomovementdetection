"""
SMS alert channel using Twilio

Sends alerts via SMS using Twilio API.
"""

from typing import Dict, Any, List, Optional
import os
from dotenv import load_dotenv

from shared.alerts.logger import AlertLogger

# Load environment variables
load_dotenv()

# Try to import Twilio (optional dependency)
try:
    from twilio.rest import Client
    TWILIO_AVAILABLE = True
except ImportError:
    TWILIO_AVAILABLE = False
    Client = None


class SMSAlert:
    """
    SMS alert channel using Twilio.
    
    Requires Twilio account and credentials.
    """
    
    def __init__(self, config: Dict[str, Any], logger: Optional[AlertLogger] = None):
        """
        Initialize SMS alert channel.
        
        Args:
            config: SMS configuration from config.yaml
            logger: Optional logger instance
        """
        self.config = config
        self.logger = logger
        
        self.enabled = config.get('enabled', False)
        
        if not TWILIO_AVAILABLE:
            if self.logger:
                self.logger.warning("Twilio library not installed. SMS alerts disabled.")
            self.enabled = False
            return
        
        # Get credentials from environment
        self.account_sid = config.get('twilio_account_sid') or os.getenv('TWILIO_ACCOUNT_SID', '')
        self.auth_token = config.get('twilio_auth_token') or os.getenv('TWILIO_AUTH_TOKEN', '')
        self.from_number = config.get('twilio_from_number') or os.getenv('TWILIO_FROM_NUMBER', '')
        
        # Get recipient list
        to_numbers_config = config.get('to_numbers', [])
        to_numbers_env = os.getenv('TWILIO_TO_NUMBERS', '')
        
        if to_numbers_env:
            # Parse comma-separated list from env
            self.to_numbers = [n.strip() for n in to_numbers_env.split(',')]
        else:
            self.to_numbers = to_numbers_config
        
        # Initialize Twilio client if credentials available
        if self.account_sid and self.auth_token:
            try:
                self.client = Client(self.account_sid, self.auth_token)
            except Exception as e:
                if self.logger:
                    self.logger.error(f"Failed to initialize Twilio client: {e}")
                self.enabled = False
        else:
            if self.logger:
                self.logger.warning("Twilio credentials not configured. SMS alerts disabled.")
            self.enabled = False
            self.client = None
    
    def is_enabled(self) -> bool:
        """Check if SMS alerts are enabled."""
        return (self.enabled and 
                TWILIO_AVAILABLE and 
                self.client is not None and
                bool(self.from_number and self.to_numbers))
    
    def send(self, alert: Any) -> bool:
        """
        Send alert via SMS.
        
        Args:
            alert: Alert object with message and details
        
        Returns:
            True if sent successfully, False otherwise
        """
        if not self.is_enabled():
            return False
        
        try:
            # Format SMS message
            message = f"[Elderly Monitoring] {alert.level.value.upper()}: {alert.message}"
            if alert.details:
                # Add key details (SMS has character limit)
                time_since = alert.details.get('time_since_movement_minutes')
                if time_since:
                    message += f" ({time_since:.0f} min)"
            
            # Send to all recipients
            success_count = 0
            for to_number in self.to_numbers:
                try:
                    self.client.messages.create(
                        body=message,
                        from_=self.from_number,
                        to=to_number
                    )
                    success_count += 1
                except Exception as e:
                    if self.logger:
                        self.logger.error(f"Failed to send SMS to {to_number}: {e}")
            
            if success_count > 0:
                if self.logger:
                    self.logger.info(f"SMS alert sent to {success_count}/{len(self.to_numbers)} recipient(s)")
                return True
            else:
                return False
                
        except Exception as e:
            if self.logger:
                self.logger.error(f"Failed to send SMS alert: {e}")
            return False
