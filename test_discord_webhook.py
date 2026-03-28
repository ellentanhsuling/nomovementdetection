#!/usr/bin/env python3
"""
Quick test script to verify a Discord webhook (no secrets in repo).

Usage:
  export DISCORD_WEBHOOK_URL='https://discord.com/api/webhooks/...'
  python3 test_discord_webhook.py

Or one-shot:
  DISCORD_WEBHOOK_URL='...' python3 test_discord_webhook.py
"""

import os
import sys
import json
from datetime import datetime

import requests

webhook_url = os.environ.get("DISCORD_WEBHOOK_URL", "").strip()
if not webhook_url:
    print(
        "Set DISCORD_WEBHOOK_URL to your full Discord webhook URL, then run again.\n"
        "Example: export DISCORD_WEBHOOK_URL='https://discord.com/api/webhooks/...'",
        file=sys.stderr,
    )
    sys.exit(1)

embed = {
    "title": "✅ Test Alert: Monitoring System",
    "description": "This is a test message from your Raspberry Pi monitoring system!",
    "color": 0x00FF00,
    "timestamp": datetime.now().isoformat(),
    "fields": [
        {
            "name": "Status",
            "value": "Webhook is working correctly!",
            "inline": True,
        },
        {
            "name": "Time",
            "value": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "inline": True,
        },
    ],
}

payload = {"embeds": [embed]}

print("Testing Discord webhook...")
print(f"URL prefix: {webhook_url[:48]}...")

try:
    response = requests.post(
        webhook_url,
        json=payload,
        timeout=5,
        headers={"Content-Type": "application/json"},
    )

    if response.status_code == 204:
        print("✅ SUCCESS! Check your Discord channel for the test message.")
    else:
        print(f"❌ Error: Status code {response.status_code}")
        print(f"Response: {response.text}")
except Exception as e:
    print(f"❌ Error: {e}")
