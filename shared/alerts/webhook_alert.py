"""
Webhook Alert Channel

Sends alerts to webhook URLs (Discord, Telegram, Slack, or any custom endpoint).
Free and perfect for prototypes!

Discord Setup:
1. Create a Discord server (or use existing)
2. Go to Server Settings > Integrations > Webhooks
3. Create New Webhook
4. Copy the webhook URL
5. Add to config.yaml

Telegram Setup:
1. Message @BotFather on Telegram
2. Create a bot with /newbot
3. Get your bot token
4. Create a group/channel
5. Add bot to group
6. Get chat ID (use @userinfobot)
7. Use: https://api.telegram.org/bot<TOKEN>/sendMessage?chat_id=<CHAT_ID>&text=<MESSAGE>
"""

import requests
import urllib3
from typing import Dict, Any, Optional, List
from datetime import datetime
import json

from shared.alerts.logger import AlertLogger

# Suppress SSL warnings (Pi has expired certificates)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class WebhookAlert:
    """
    Webhook alert channel for Discord, Telegram, Slack, or custom endpoints.
    
    Supports multiple webhook URLs for redundancy.
    """
    
    def __init__(self, config: Dict[str, Any], logger: Optional[AlertLogger] = None):
        """
        Initialize webhook alert channel.
        
        Args:
            config: Webhook configuration from config.yaml
            logger: Optional logger instance
        """
        self.config = config
        self.logger = logger
        
        self.enabled = config.get('enabled', False)
        
        # Support multiple webhook URLs
        webhook_urls = config.get('webhook_urls', [])
        if isinstance(webhook_urls, str):
            webhook_urls = [webhook_urls]
        self.webhook_urls = [url for url in webhook_urls if url]
        
        self.webhook_type = config.get('type', 'discord').lower()  # discord, telegram, slack, custom
        self.timeout = config.get('timeout', 5)
        self.retry_attempts = config.get('retry_attempts', 2)
        
        if not self.webhook_urls:
            if self.logger:
                self.logger.warning("No webhook URLs configured. Webhook alerts disabled.")
            self.enabled = False
    
    def is_enabled(self) -> bool:
        """Check if webhook alerts are enabled."""
        return self.enabled and bool(self.webhook_urls)
    
    def _format_discord_message(self, alert: Any) -> Dict[str, Any]:
        """Format alert as Discord webhook message."""
        # Discord color coding by alert level
        color_map = {
            'info': 0x3498db,      # Blue
            'warning': 0xf39c12,   # Orange
            'error': 0xe74c3c,      # Red
            'critical': 0x8b0000,   # Dark red
        }
        
        color = color_map.get(alert.level.value.lower(), 0x95a5a6)  # Gray default
        
        embed = {
            "title": f"🚨 {alert.level.value.upper()}: {alert.message}",
            "description": f"**Time:** {alert.timestamp.strftime('%Y-%m-%d %H:%M:%S')}",
            "color": color,
            "timestamp": alert.timestamp.isoformat(),
        }
        
        if alert.details:
            fields = []
            for key, value in alert.details.items():
                fields.append({
                    "name": str(key).replace('_', ' ').title(),
                    "value": str(value),
                    "inline": True
                })
            embed["fields"] = fields
        
        return {
            "embeds": [embed]
        }
    
    def _format_telegram_message(self, alert: Any) -> str:
        """Format alert as Telegram message."""
        message = f"🚨 *{alert.level.value.upper()}: {alert.message}*\n\n"
        message += f"Time: {alert.timestamp.strftime('%Y-%m-%d %H:%M:%S')}\n"
        
        if alert.details:
            message += "\n*Details:*\n"
            for key, value in alert.details.items():
                message += f"• {str(key).replace('_', ' ').title()}: {value}\n"
        
        return message
    
    def _format_slack_message(self, alert: Any) -> Dict[str, Any]:
        """Format alert as Slack webhook message."""
        color_map = {
            'info': 'good',      # Green
            'warning': 'warning', # Yellow
            'error': 'danger',   # Red
            'critical': 'danger', # Red
        }
        
        color = color_map.get(alert.level.value.lower(), '#808080')  # Gray default
        
        attachment = {
            "color": color,
            "title": f"{alert.level.value.upper()}: {alert.message}",
            "fields": [],
            "ts": int(alert.timestamp.timestamp())
        }
        
        if alert.details:
            for key, value in alert.details.items():
                attachment["fields"].append({
                    "title": str(key).replace('_', ' ').title(),
                    "value": str(value),
                    "short": True
                })
        
        return {
            "attachments": [attachment]
        }
    
    def _format_custom_message(self, alert: Any) -> Dict[str, Any]:
        """Format alert as generic JSON payload."""
        return {
            "level": alert.level.value,
            "message": alert.message,
            "timestamp": alert.timestamp.isoformat(),
            "details": alert.details or {}
        }
    
    def send(self, alert: Any) -> bool:
        """
        Send alert via webhook.
        
        Args:
            alert: Alert object with message and details
        
        Returns:
            True if sent successfully to at least one webhook, False otherwise
        """
        if not self.is_enabled():
            return False
        
        # Format message based on webhook type
        if self.webhook_type == 'discord':
            payload = self._format_discord_message(alert)
        elif self.webhook_type == 'telegram':
            # Telegram uses GET with query params, handled differently
            message = self._format_telegram_message(alert)
            payload = {"text": message, "parse_mode": "Markdown"}
        elif self.webhook_type == 'slack':
            payload = self._format_slack_message(alert)
        else:  # custom
            payload = self._format_custom_message(alert)
        
        success_count = 0
        
        # Try each webhook URL
        for webhook_url in self.webhook_urls:
            for attempt in range(self.retry_attempts):
                try:
                    if self.webhook_type == 'telegram':
                        # Telegram uses GET with query params
                        # Note: verify=False due to Pi's expired SSL certificates
                        response = requests.get(
                            webhook_url,
                            params=payload,
                            timeout=self.timeout,
                            verify=False
                        )
                    else:
                        # Discord, Slack, and custom use POST with JSON
                        # Note: verify=False due to Pi's expired SSL certificates
                        response = requests.post(
                            webhook_url,
                            json=payload,
                            timeout=self.timeout,
                            headers={'Content-Type': 'application/json'},
                            verify=False
                        )
                    
                    # Check if request was successful
                    if response.status_code in [200, 201, 204]:
                        success_count += 1
                        if self.logger:
                            self.logger.info(f"Webhook alert sent successfully to {webhook_url[:50]}...")
                        break  # Success, move to next webhook
                    else:
                        if attempt == self.retry_attempts - 1:  # Last attempt
                            if self.logger:
                                self.logger.warning(
                                    f"Webhook alert failed for {webhook_url[:50]}... "
                                    f"Status: {response.status_code}, Response: {response.text[:100]}"
                                )
                
                except requests.exceptions.Timeout:
                    if attempt == self.retry_attempts - 1:
                        if self.logger:
                            self.logger.warning(f"Webhook alert timeout for {webhook_url[:50]}...")
                except requests.exceptions.ConnectionError:
                    if attempt == self.retry_attempts - 1:
                        if self.logger:
                            self.logger.warning(f"Webhook alert connection error for {webhook_url[:50]}...")
                except Exception as e:
                    if attempt == self.retry_attempts - 1:
                        if self.logger:
                            self.logger.error(f"Webhook alert error for {webhook_url[:50]}...: {e}")
        
        return success_count > 0
