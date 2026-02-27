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

**Python reference**: 
- Enums: https://docs.python.org/3/library/enum.html
- datetime: https://docs.python.org/3/library/datetime.html

---

### 🎯 Your Turn: Build the Movement Detector

**Step 1: Create the file and imports**

1. Open/create `non_movement/detection/movement_detector.py`
2. **Write the imports** - You'll need:
   - `Enum` from `enum` module
   - `datetime`, `timedelta` from `datetime` module
   - `Dict`, `Any`, `Optional` from `typing`
   - `is_time_between` from `shared.utils.time_utils`

   **Prompt**: Write all the import statements.

**Step 2: Create the MovementStatus enum**

3. **Create the enum**:
   - **Prompt**: Create an enum called `MovementStatus` with values:
     - `ACTIVE` - Person is moving normally
     - `INACTIVE` - No movement, but not concerning yet
     - `CONCERNING` - No movement for too long - alert needed!
     - `UNKNOWN` - Can't determine status
   
   - **Write it**:
     ```python
     from enum import Enum
     
     class MovementStatus(Enum):
         ACTIVE = "active"
         INACTIVE = "inactive"
         CONCERNING = "concerning"
         UNKNOWN = "unknown"
     ```

**Step 3: Create the MovementDetector class**

4. **Create the class**:
   ```python
   class MovementDetector:
   ```

5. **Add `__init__` method**:
   - **Prompt**: Write `__init__` that takes `config: Dict[str, Any]`
   - **What should it store?**
     - Thresholds from config (active, sleep, anytime)
     - Active hours (start, end)
     - Last movement time (starts as None)
     - Last sensor that detected movement
   
   - **Write it**:
     ```python
     def __init__(self, config: Dict[str, Any]):
         monitoring = config.get('monitoring', {})
         self.threshold_active = monitoring.get('no_movement_threshold_active', 30)
         self.threshold_sleep = monitoring.get('no_movement_threshold_sleep', 120)
         self.threshold_anytime = monitoring.get('no_movement_threshold_anytime', 60)
         
         active_hours = monitoring.get('active_hours', {})
         self.active_start = active_hours.get('start', 7)
         self.active_end = active_hours.get('end', 22)
         
         self.last_movement_time: Optional[datetime] = None
         self.last_movement_sensor: Optional[str] = None
     ```

**Step 4: Implement `record_movement` method**

6. **Implement `record_movement()`**:
   - **Prompt**: Write a method that:
     - Takes `sensor_name: str` and `sensor_data: Dict[str, Any]`
     - Checks if movement was detected (from sensor_data)
     - If movement detected, update `last_movement_time` to now
     - Store which sensor detected it
   
   - **Write it**:
     ```python
     def record_movement(self, sensor_name: str, sensor_data: Dict[str, Any]) -> None:
         # Check if movement was detected
         motion_detected = sensor_data.get('motion_detected', False)
         person_detected = sensor_data.get('person_detected', False)
         
         if motion_detected and person_detected:
             self.last_movement_time = datetime.now()
             self.last_movement_sensor = sensor_name
     ```

**Step 5: Implement `get_time_since_last_movement` method**

7. **Implement `get_time_since_last_movement()`**:
   - **Prompt**: Write a method that returns the time (in minutes) since last movement
   - **What if there's no last movement?** Return None
   - **Write it**:
     ```python
     def get_time_since_last_movement(self) -> Optional[float]:
         if self.last_movement_time is None:
             return None
         
         time_diff = datetime.now() - self.last_movement_time
         return time_diff.total_seconds() / 60.0  # Convert to minutes
     ```

**Step 6: Implement `is_active_hours` method**

8. **Implement `is_active_hours()`**:
   - **Prompt**: Write a method that checks if current time is in active hours
   - **Hint**: Use `is_time_between()` from time_utils
   - **Write it**:
     ```python
     def is_active_hours(self) -> bool:
         return is_time_between(self.active_start, self.active_end)
     ```

**Step 7: Implement `check_movement_status` method**

9. **Implement `check_movement_status()`** - This is the core logic!
   - **Prompt**: Write a method that returns the current `MovementStatus`
   - **Logic**:
     - If no last movement time → return `UNKNOWN`
     - Get time since last movement
     - If in active hours: compare to `threshold_active`
     - If in sleep hours: compare to `threshold_sleep`
     - If time exceeds threshold → return `CONCERNING`
     - If time is significant but not over threshold → return `INACTIVE`
     - Otherwise → return `ACTIVE`
   
   - **Write it**:
     ```python
     def check_movement_status(self) -> MovementStatus:
         if self.last_movement_time is None:
             return MovementStatus.UNKNOWN
         
         time_since = self.get_time_since_last_movement()
         if time_since is None:
             return MovementStatus.UNKNOWN
         
         # Determine which threshold to use
         if self.is_active_hours():
             threshold = self.threshold_active
         else:
             threshold = self.threshold_sleep
         
         # Check status
         if time_since >= threshold:
             return MovementStatus.CONCERNING
         elif time_since >= threshold * 0.7:  # 70% of threshold
             return MovementStatus.INACTIVE
         else:
             return MovementStatus.ACTIVE
     ```

**Step 8: Test your code**

10. **Checkpoint**: Test the movement detector:
    ```python
    from non_movement.detection.movement_detector import MovementDetector, MovementStatus
    
    config = {
        'monitoring': {
            'no_movement_threshold_active': 30,
            'no_movement_threshold_sleep': 120,
            'active_hours': {'start': 7, 'end': 22}
        }
    }
    
    detector = MovementDetector(config)
    
    # Record movement
    detector.record_movement('camera', {'motion_detected': True, 'person_detected': True})
    
    # Check status (should be ACTIVE)
    status = detector.check_movement_status()
    print(f"Status: {status}")
    assert status == MovementStatus.ACTIVE
    
    print("✅ Movement detector works!")
    ```

**✅ Checkpoint Questions:**
- [ ] Does your enum have all four status values?
- [ ] Does `record_movement()` update `last_movement_time`?
- [ ] Does `get_time_since_last_movement()` return minutes?
- [ ] Does `is_active_hours()` use the time utility?
- [ ] Does `check_movement_status()` return the correct status based on thresholds?

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

---

### 🎯 Your Turn: Build the Main Application

**Step 1: Create the file and imports**

1. Open/create `non_movement/main.py`
2. **Write the imports** - You'll need:
   - `sys`, `os` modules
   - `signal` module (for Ctrl+C handling)
   - `BaseMonitoringSystem` from `shared.base.monitoring_base`
   - `MovementDetector` from `non_movement.detection.movement_detector`
   - `AlertManager` from `non_movement.detection.alert_manager`
   - `load_config` from `shared.utils.config_loader`

   **Prompt**: Write all the import statements. Think: What do you need to import?

**Step 2: Create the NonMovementSystem class**

3. **Create the class**:
   ```python
   class NonMovementSystem(BaseMonitoringSystem):
   ```

4. **Add `__init__` method**:
   - **Prompt**: Write `__init__` that calls `super().__init__(config_path)`
   - **What else should it store?**
     - Movement detector (will create in initialize_project)
     - Alert manager (will create in initialize_project)
   - **Write it**:
     ```python
     def __init__(self, config_path: str = 'config.yaml'):
         super().__init__(config_path)
         self.movement_detector: Optional[MovementDetector] = None
         self.alert_manager: Optional[AlertManager] = None
     ```

**Step 3: Implement `initialize_project` method**

5. **Implement `initialize_project()`**:
   - **Prompt**: This method should:
     - Create a `MovementDetector` instance with the config
     - Create an `AlertManager` instance
     - Store them in instance variables
   
   - **Write it**:
     ```python
     def initialize_project(self) -> None:
         # Create movement detector
         self.movement_detector = MovementDetector(self.config)
         
         # Create alert manager
         self.alert_manager = AlertManager(self.config, self.logger)
         
         self.logger.info("Non-movement detection system initialized")
     ```

**Step 4: Implement `run_cycle` method** - This is the main logic!

6. **Implement `run_cycle()`** - This runs every check interval:
   - **Prompt**: Write a method that:
     1. Reads from the camera sensor
     2. Records movement in the movement detector
     3. Checks the movement status
     4. If status is CONCERNING, send an alert
     5. Logs the status periodically
   
   - **Think about**: 
     - How do you read from the camera? (Use `self.sensors['camera'].read()`)
     - What if the camera returns None? (Handle errors gracefully)
     - How often should you log? (Maybe every 10 cycles to avoid spam)
   
   - **Write it step by step**:
     ```python
     def run_cycle(self) -> None:
         # Read camera
         camera = self.sensors.get('camera')
         if not camera:
             self.logger.warning("Camera sensor not available")
             return
         
         sensor_data = camera.read()
         if sensor_data is None:
             self.logger.warning("Camera read returned None")
             return
         
         # Record movement
         self.movement_detector.record_movement('camera', sensor_data)
         
         # Check movement status
         status = self.movement_detector.check_movement_status()
         
         # Log status periodically (every 10 cycles)
         if not hasattr(self, '_cycle_count'):
             self._cycle_count = 0
         self._cycle_count += 1
         
         if self._cycle_count % 10 == 0:
             time_since = self.movement_detector.get_time_since_last_movement()
             self.logger.info(
                 f"Status: {status.value}, "
                 f"Time since movement: {time_since:.1f} minutes"
             )
         
         # Send alert if concerning
         if status == MovementStatus.CONCERNING:
             time_since = self.movement_detector.get_time_since_last_movement()
             self.logger.warning(
                 f"CONCERNING status detected! "
                 f"No movement for {time_since:.1f} minutes"
             )
             
             # Create and send alert
             alert = self.alert_manager.create_alert(
                 level='CRITICAL',
                 message=f"No movement detected for {time_since:.1f} minutes",
                 details={'status': status.value, 'time_since': time_since}
             )
             self.alert_manager.send_alert(alert)
     ```

**Step 5: Implement `shutdown_project` method**

7. **Implement `shutdown_project()`**:
   - **Prompt**: Write a method that saves any data and cleans up
   - **Write it**:
     ```python
     def shutdown_project(self) -> None:
         self.logger.info("Shutting down non-movement detection system")
         # Add any cleanup code here (save patterns, etc.)
     ```

**Step 6: Create the `main` function**

8. **Create `main()` function**:
   - **Prompt**: Write a function that:
     - Creates a `NonMovementSystem` instance
     - Calls `initialize()` (from base class)
     - Calls `run()` (from base class - this starts the main loop)
     - Handles KeyboardInterrupt (Ctrl+C) gracefully
   
   - **Write it**:
     ```python
     def main():
         # Get config path from command line or use default
         config_path = sys.argv[1] if len(sys.argv) > 1 else 'config.yaml'
         
         # Create system
         system = NonMovementSystem(config_path)
         
         try:
             # Initialize and run
             system.initialize()
             system.run()
         except KeyboardInterrupt:
             print("\nShutting down...")
             system.shutdown()
         except Exception as e:
             print(f"Error: {e}")
             system.shutdown()
             raise
     
     if __name__ == '__main__':
         main()
     ```

**Step 7: Test your code**

9. **Checkpoint**: Test the main application:
    ```bash
    cd non_movement
    python main.py
    ```
    
    **What should happen:**
    - System initializes
    - Camera reads (mock data if using mock camera)
    - Status updates every 10 cycles
    - Press Ctrl+C to stop gracefully

**✅ Checkpoint Questions:**
- [ ] Does your class inherit from `BaseMonitoringSystem`?
- [ ] Does `initialize_project()` create the detector and manager?
- [ ] Does `run_cycle()` read from camera and check status?
- [ ] Does it send alerts when status is CONCERNING?
- [ ] Does `main()` handle Ctrl+C gracefully?
- [ ] Can you run the application without errors?

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
