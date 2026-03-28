"""
Email alert channel

Sends alerts via SMTP email.
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, Any, List, Optional
import os
from dotenv import load_dotenv

from shared.alerts.logger import AlertLogger

# Load environment variables
load_dotenv()


class EmailAlert:
    """
    Email alert channel using SMTP.
    
    Supports Gmail and other SMTP servers.
    """
    
    def __init__(self, config: Dict[str, Any], logger: Optional[AlertLogger] = None):
        """
        Initialize email alert channel.
        
        Args:
            config: Email configuration from config.yaml
            logger: Optional logger instance
        """
        self.config = config
        self.logger = logger
        
        self.enabled = config.get('enabled', False)
        self.smtp_server = config.get('smtp_server', 'smtp.gmail.com')
        self.smtp_port = config.get('smtp_port', 587)
        self.use_tls = config.get('use_tls', True)
        
        # Get credentials from environment
        self.from_email = config.get('from_email') or os.getenv('EMAIL_FROM', '')
        self.email_password = os.getenv('EMAIL_PASSWORD', '')
        
        # Get recipient list
        to_emails_config = config.get('to_emails', [])
        to_emails_env = os.getenv('EMAIL_TO', '')
        
        if to_emails_env:
            # Parse comma-separated list from env
            self.to_emails = [e.strip() for e in to_emails_env.split(',')]
        else:
            self.to_emails = to_emails_config
        
        if not self.from_email or not self.email_password:
            if self.logger:
                self.logger.warning("Email credentials not configured. Email alerts disabled.")
            self.enabled = False
    
    def is_enabled(self) -> bool:
        """Check if email alerts are enabled."""
        return self.enabled and bool(self.from_email and self.email_password and self.to_emails)
    
    def send(self, alert: Any) -> bool:
        """
        Send alert via email.
        
        Args:
            alert: Alert object with message and details
        
        Returns:
            True if sent successfully, False otherwise
        """
        if not self.is_enabled():
            return False
        
        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = self.from_email
            msg['To'] = ', '.join(self.to_emails)
            msg['Subject'] = f"[Elderly Monitoring] {alert.level.value.upper()}: {alert.message}"
            
            # Create email body
            body = f"""
Elderly Non-Movement Monitoring System Alert

Level: {alert.level.value.upper()}
Time: {alert.timestamp.strftime('%Y-%m-%d %H:%M:%S')}
Message: {alert.message}
"""
            
            if alert.details:
                body += "\nDetails:\n"
                for key, value in alert.details.items():
                    body += f"  {key}: {value}\n"
            
            msg.attach(MIMEText(body, 'plain'))
            
            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                if self.use_tls:
                    server.starttls()
                server.login(self.from_email, self.email_password)
                server.send_message(msg)
            
            if self.logger:
                self.logger.info(f"Email alert sent to {len(self.to_emails)} recipient(s)")
            
            return True
            
        except Exception as e:
            if self.logger:
                self.logger.error(f"Failed to send email alert: {e}")
            return False
