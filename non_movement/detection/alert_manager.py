"""
Alert management system

Manages alert escalation and coordinates different alert channels.
"""

from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from enum import Enum


class AlertLevel(Enum):
    """Alert severity levels"""
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"


class Alert:
    """Represents a single alert"""
    
    def __init__(self, level: AlertLevel, message: str, details: Optional[Dict[str, Any]] = None):
        self.level = level
        self.message = message
        self.details = details or {}
        self.timestamp = datetime.now()
        self.sent_channels: List[str] = []
        self.acknowledged = False
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert alert to dictionary for storage/transmission."""
        return {
            'level': self.level.value,
            'message': self.message,
            'details': self.details,
            'timestamp': self.timestamp.isoformat(),
            'sent_channels': self.sent_channels,
            'acknowledged': self.acknowledged,
        }


class AlertManager:
    """
    Manages alert generation, escalation, and delivery.
    
    Coordinates between different alert channels (email, SMS, API)
    and implements escalation logic.
    """
    
    def __init__(self, config: Dict[str, Any], alert_channels: Dict[str, Any]):
        """
        Initialize alert manager.
        
        Args:
            config: Alert configuration from config.yaml
            alert_channels: Dictionary of channel_name -> channel_instance
        """
        self.config = config
        self.alert_channels = alert_channels
        
        # Escalation configuration
        escalation_config = config.get('escalation', {})
        self.escalation_enabled = escalation_config.get('enabled', True)
        self.escalation_levels = escalation_config.get('levels', [])
        
        # Alert history
        self.alert_history: List[Alert] = []
        self.active_alerts: List[Alert] = []
        
        # Track last alert time to prevent spam
        self.last_alert_time: Optional[datetime] = None
        self.min_alert_interval = timedelta(minutes=5)  # Don't spam alerts
    
    def create_alert(self, level: AlertLevel, message: str, details: Optional[Dict[str, Any]] = None) -> Alert:
        """
        Create a new alert.
        
        Args:
            level: Alert severity level
            message: Alert message
            details: Additional details
        
        Returns:
            Created Alert object
        """
        alert = Alert(level, message, details)
        self.alert_history.append(alert)
        
        # Keep only last 1000 alerts
        if len(self.alert_history) > 1000:
            self.alert_history.pop(0)
        
        return alert
    
    def send_alert(self, alert: Alert, channels: Optional[List[str]] = None) -> Dict[str, bool]:
        """
        Send alert through specified channels.
        
        Args:
            alert: Alert to send
            channels: List of channel names to use (None = all enabled channels)
        
        Returns:
            Dictionary of channel_name -> success status
        """
        if channels is None:
            # Use all enabled channels
            channels = [name for name, channel in self.alert_channels.items() 
                       if channel.is_enabled()]
        
        results = {}
        
        for channel_name in channels:
            if channel_name not in self.alert_channels:
                results[channel_name] = False
                continue
            
            channel = self.alert_channels[channel_name]
            
            try:
                success = channel.send(alert)
                results[channel_name] = success
                
                if success:
                    alert.sent_channels.append(channel_name)
            except Exception as e:
                print(f"Error sending alert via {channel_name}: {e}")
                results[channel_name] = False
        
        return results
    
    def handle_movement_alert(self, movement_status: str, time_since_movement: Optional[float], 
                             details: Optional[Dict[str, Any]] = None):
        """
        Handle a movement-related alert.
        
        Args:
            movement_status: Status from MovementDetector
            time_since_movement: Minutes since last movement
            details: Additional context
        """
        # Check if we should send alert (prevent spam)
        if self.last_alert_time:
            time_since_last_alert = datetime.now() - self.last_alert_time
            if time_since_last_alert < self.min_alert_interval:
                return  # Too soon since last alert
        
        if movement_status == "concerning":
            # Determine alert level based on time
            if time_since_movement and time_since_movement > 60:
                level = AlertLevel.CRITICAL
                message = f"CRITICAL: No movement detected for {time_since_movement:.1f} minutes"
            elif time_since_movement and time_since_movement > 30:
                level = AlertLevel.WARNING
                message = f"WARNING: No movement detected for {time_since_movement:.1f} minutes"
            else:
                level = AlertLevel.WARNING
                message = f"WARNING: No movement detected for {time_since_movement:.1f} minutes"
            
            alert = self.create_alert(level, message, {
                'type': 'no_movement',
                'time_since_movement_minutes': time_since_movement,
                **(details or {}),
            })
            
            # Send alert with escalation
            self._send_with_escalation(alert)
            
            self.last_alert_time = datetime.now()
            self.active_alerts.append(alert)
    
    def _send_with_escalation(self, alert: Alert):
        """
        Send alert with escalation logic.
        
        Escalation means sending to more channels as time passes.
        """
        if not self.escalation_enabled or not self.escalation_levels:
            # No escalation - send to all channels immediately
            all_channels = [name for name, channel in self.alert_channels.items() 
                          if channel.is_enabled()]
            self.send_alert(alert, all_channels)
            return
        
        # For now, send to first escalation level immediately
        # In a full implementation, we'd use a background task to handle delays
        first_level = self.escalation_levels[0] if self.escalation_levels else {}
        channels = first_level.get('channels', [])
        
        if channels:
            self.send_alert(alert, channels)
    
    def acknowledge_alert(self, alert: Alert):
        """Mark an alert as acknowledged."""
        alert.acknowledged = True
        if alert in self.active_alerts:
            self.active_alerts.remove(alert)
    
    def get_active_alerts(self) -> List[Alert]:
        """Get all active (unacknowledged) alerts."""
        return [a for a in self.active_alerts if not a.acknowledged]
    
    def get_recent_alerts(self, limit: int = 10) -> List[Alert]:
        """Get most recent alerts."""
        return self.alert_history[-limit:]
    
    def get_status(self) -> Dict[str, Any]:
        """Get current status of alert manager."""
        return {
            'escalation_enabled': self.escalation_enabled,
            'active_alerts_count': len(self.get_active_alerts()),
            'total_alerts_sent': len(self.alert_history),
            'last_alert_time': self.last_alert_time.isoformat() if self.last_alert_time else None,
        }
