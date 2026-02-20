# Student Build Guide - Step 4: Non-Movement Detection Project

## What You're Building

**Project 1**: Detects when someone hasn't moved for a long time (30+ minutes).

**Use case**: Elderly person might have fallen or had medical emergency.

---

## Understanding the Algorithm

**How it works:**
1. Camera checks for movement every 30 seconds
2. Tracks "time since last movement"
3. If no movement for X minutes → Alert!
4. Different thresholds for day vs night

**Key concepts:**
- **Time-based detection**: Not real-time, checks periodically
- **Thresholds**: How long is "too long"?
- **Pattern learning**: Learns normal activity patterns

---

## Part 1: Movement Detector

**File**: `non_movement/detection/movement_detector.py`

**What it does**: Core algorithm that decides if there's a problem.

**Key concepts:**
- **MovementStatus enum**: ACTIVE, INACTIVE, CONCERNING, UNKNOWN
- **Time tracking**: When was last movement?
- **Thresholds**: Active hours vs sleep hours

**What to build:**
- Class `MovementDetector`
- Method `record_movement()` - saves when movement happened
- Method `check_movement_status()` - decides current status
- Method `is_active_hours()` - checks time of day
- Method `get_time_since_last_movement()` - calculates time

**Python reference**: 
- Enums: https://docs.python.org/3/library/enum.html
- datetime: https://docs.python.org/3/library/datetime.html

---

## Part 2: Pattern Learner

**File**: `non_movement/detection/pattern_learner.py`

**What it does**: Learns normal activity patterns to reduce false alarms.

**Key concepts:**
- **Baseline**: What's "normal" for this person?
- **Hourly patterns**: More active at 10am, less at 2am
- **Learning period**: Takes 7 days to learn patterns

**What to build:**
- Class `PatternLearner`
- Method `record_movement_event()` - saves movement data
- Method `analyze_patterns()` - finds patterns
- Method `get_expected_activity_level()` - what's normal for this hour?
- Save/load patterns to file (JSON)

**Python reference**:
- JSON: https://docs.python.org/3/library/json.html
- File I/O: https://docs.python.org/3/tutorial/inputoutput.html

---

## Part 3: Alert Manager

**File**: `non_movement/detection/alert_manager.py`

**What it does**: Manages alerts and sends them through channels.

**Key concepts:**
- **Alert levels**: INFO, WARNING, CRITICAL
- **Escalation**: Send to more channels as time passes
- **Spam prevention**: Don't send too many alerts

**What to build:**
- Class `Alert` - represents one alert
- Class `AlertManager`
- Method `create_alert()` - makes new alert
- Method `send_alert()` - sends through channels
- Method `handle_movement_alert()` - specific to movement detection

---

## Part 4: Configuration File

**File**: `non_movement/config.yaml`

**What it does**: Settings for the project.

**YAML format:**
```yaml
sensors:
  camera:
    enabled: true
    check_interval: 30

monitoring:
  no_movement_threshold_active: 30  # minutes
  no_movement_threshold_sleep: 120  # minutes
  active_hours:
    start: 7
    end: 22
```

**What to include:**
- Camera settings
- Time thresholds
- Active/sleep hours
- Alert settings
- Logging settings

**YAML reference**: https://yaml.org/spec/1.2.2/

---

## Part 5: Main Application

**File**: `non_movement/main.py`

**What it does**: Entry point - starts the monitoring system.

**Key concepts:**
- **Inheritance**: Extends `BaseMonitoringSystem`
- **Main loop**: Runs forever until stopped
- **Signal handling**: Graceful shutdown (Ctrl+C)

**What to build:**
- Class `NonMovementSystem` extends `BaseMonitoringSystem`
- Method `initialize_project()` - sets up detectors
- Method `run_cycle()` - one check cycle
- Method `shutdown_project()` - cleanup
- `main()` function to start everything

**Structure:**
```python
class NonMovementSystem(BaseMonitoringSystem):
    def initialize_project(self):
        # Create detectors, managers
        
    def run_cycle(self):
        # Read camera
        # Check movement status
        # Send alerts if needed
        
    def shutdown_project(self):
        # Save data
```

---

## Part 5.5: Integrate Data Logging and Alerts

**What you're adding:** Connect to external services for data logging (ThingSpeak) and alerts (Discord).

### Step 1: Set Up ThingSpeak (Data Logging)

**What is ThingSpeak?** Free IoT data logging service - perfect for prototypes!

**Setup:**
1. Go to https://thingspeak.com
2. Sign up (free account)
3. Create a new channel:
   - Name: "Elderly Monitoring"
   - Enable Field 1-5 (for different data types)
   - Save channel
4. Go to "API Keys" tab
5. Copy your **Write API Key** (keep it secret!)

**Add to config.yaml:**
```yaml
data_logging:
  thingspeak:
    enabled: true
    write_api_key: "YOUR_WRITE_API_KEY_HERE"
    channel_id: "YOUR_CHANNEL_ID"  # Optional, for reference
```

**Reference:** See `references/FREE_SERVICES_SETUP.md` for detailed ThingSpeak setup.

### Step 2: Set Up Discord Webhook (Alerts)

**What is Discord Webhook?** Free way to send alerts to Discord - perfect for prototypes!

**Setup:**
1. Open Discord
2. Create a server (or use existing)
3. Go to Server Settings → Integrations → Webhooks
4. Click "New Webhook"
5. Name it "Monitoring Alerts"
6. Choose a channel
7. Click "Copy Webhook URL"
8. Save changes

**Add to config.yaml:**
```yaml
alerts:
  webhook:
    enabled: true
    type: "discord"
    webhook_urls:
      - "https://discord.com/api/webhooks/YOUR_WEBHOOK_URL"
    timeout: 5
    retry_attempts: 2
  
  # For simple alerts, disable escalation:
  escalation:
    enabled: false
    # If you enable escalation, include webhook:
    levels:
      - channels: ["webhook"]
        delay_minutes: 0
```

**Reference:** See `references/FREE_SERVICES_SETUP.md` for detailed Discord setup.

### Step 3: Update Your Code

**The shared library already includes:**
- `ThingSpeakLogger` in `shared/data/thingspeak_logger.py`
- `WebhookAlert` in `shared/alerts/webhook_alert.py`

**These are already integrated into `BaseMonitoringSystem`!**

**You just need to:**
1. Make sure `config.yaml` has the settings above
2. The system will automatically use them when enabled

**For prototype testing, set short thresholds:**
```yaml
detection:
  no_movement_threshold_active: 0.167  # 10 seconds (for testing)
  no_movement_threshold_sleep: 0.167
  no_movement_threshold_anytime: 0.167
```

**Reference:** See `FAQ_TROUBLESHOOTING.md` for troubleshooting ThingSpeak and Discord issues.

---

## Part 6: Requirements File

**File**: `non_movement/requirements.txt`

**What it does**: Lists all packages needed.

**Format:**
```
pyyaml>=6.0.1
python-dotenv>=1.0.0
requests>=2.31.0
numpy>=1.24.0
opencv-python>=4.8.0
Pillow>=10.0.0
python-dateutil>=2.8.2
```

**Install**: `pip install -r requirements.txt`

---

## Testing Your Project

**Test with mock camera:**

```bash
cd non_movement
python main.py --mock
```

**What you should see:**
- System initializes
- Camera reads (mock data)
- Status updates every 10 cycles
- Can stop with Ctrl+C

**Test different scenarios:**
- Change mock camera mode to 'fall' (no movement)
- Change mock camera mode to 'normal' (regular movement)
- Watch how thresholds work

---

## Understanding the Flow

1. **Start**: `main.py` runs
2. **Initialize**: Load config, setup sensors, setup alerts
3. **Loop**: Every 30 seconds:
   - Read camera
   - Check movement status
   - Update pattern learner
   - Send alert if needed
4. **Shutdown**: Save data, cleanup

---

## ✅ Checklist

- [ ] Movement detector created and working
- [ ] Pattern learner created and working
- [ ] Alert manager created and working
- [ ] Config file created
- [ ] Main application created
- [ ] Requirements file created
- [ ] Tests with mock camera pass
- [ ] Can detect "no movement" scenario
- [ ] Alerts work (at least logging)

---

## Common Issues

### "No module named 'shared'"
- **Solution**: Make sure you're in project root
- Add to path: `sys.path.insert(0, '..')`

### "Config file not found"
- **Solution**: Make sure `config.yaml` is in `non_movement/` folder

### "Mock camera not working"
- **Solution**: Check you imported from `shared.sensors.mock_camera`

---

## Next Step

Once non-movement project works, go to **STUDENT_GUIDE_05_FALL_DETECTION.md**

---

*This is the first complete project. Make sure it works before moving on!*
