#!/usr/bin/env python3
"""Test Discord alert using local non_movement config (not committed — see .gitignore)."""

import sys
from pathlib import Path

repo_root = Path(__file__).resolve().parent
sys.path.insert(0, str(repo_root))

import yaml
from shared.alerts.webhook_alert import WebhookAlert
from shared.alerts.logger import AlertLogger
from non_movement.detection.alert_manager import Alert, AlertLevel

config_path = repo_root / "non_movement" / "config.yaml"
if not config_path.is_file():
    print(
        f"Missing {config_path}\n"
        "Copy templates/config_non_movement.yaml and add your webhook (never commit secrets).",
        file=sys.stderr,
    )
    sys.exit(1)

with open(config_path, "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)

logger = AlertLogger(config.get("logging", {}))
webhook_config = config.get("alerts", {}).get("webhook", {})
webhook = WebhookAlert(webhook_config, logger)

test_alert = Alert(
    AlertLevel.WARNING,
    "TEST: No movement detected for 0.5 minutes",
    {"type": "no_movement", "time_since_movement_minutes": 0.5},
)

print("Sending test alert to Discord...")
result = webhook.send(test_alert)
print(f"Result: {result}")
