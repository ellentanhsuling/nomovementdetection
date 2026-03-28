# Student Build Guide - Step 5: Fall Detection Project

## What You're Building

**Project 2**: Detects immediate falls (person goes from standing to lying down).

**Use case**: Emergency situation - person needs immediate help.

---

## Understanding the Algorithm

**How it works:**
1. Camera analyzes frames in real-time (every second)
2. Detects person's position (standing, sitting, lying)
3. Detects sudden position change (standing → lying = fall)
4. If person on floor for X seconds → Alert immediately!

**Key differences from non-movement:**
- **Real-time**: Checks every second, not every 30 seconds
- **Position-based**: Looks at WHERE person is, not just movement
- **Immediate alerts**: No delay, sends alert right away

---

## Part 1: Fall Detector

**File**: `fall_detection/detection/fall_detector.py`

**What it does**: Core algorithm that detects falls.

**Key concepts:**
- **FallStatus enum**: NORMAL, SUSPICIOUS, FALL_DETECTED, UNKNOWN
- **Position tracking**: standing, sitting, lying
- **Sudden change**: Standing → Lying = potential fall
- **Confirmation time**: Person must be on floor for X seconds

**Simplified approach (for now):**
- Use motion level to guess position
- Low motion + high confidence = lying
- High motion = standing
- (Later: Use pose estimation for accuracy)

---

### 🎯 Your Turn: Build the Fall Detector

**Step 1: Create the file and imports**

1. Open/create `fall_detection/detection/fall_detector.py`
2. **Write the imports** - You'll need:
   - `Enum` from `enum` module
   - `datetime`, `timedelta` from `datetime` module
   - `Dict`, `Any`, `Optional` from `typing`

   **Prompt**: Write all the import statements.

**Step 2: Create the FallStatus enum**

3. **Create the enum**:
   - **Prompt**: Create an enum called `FallStatus` with values:
     - `NORMAL` - Person is in normal position
     - `SUSPICIOUS` - Something unusual detected
     - `FALL_DETECTED` - Fall confirmed!
     - `UNKNOWN` - Can't determine status
   
   - **Write it**:
     ```python
     from enum import Enum
     
     class FallStatus(Enum):
         NORMAL = "normal"
         SUSPICIOUS = "suspicious"
         FALL_DETECTED = "fall_detected"
         UNKNOWN = "unknown"
     ```

**Step 3: Create the FallDetector class**

4. **Create the class**:
   ```python
   class FallDetector:
   ```

5. **Add `__init__` method**:
   - **Prompt**: Write `__init__` that takes `config: Dict[str, Any]`
   - **What should it store?**
     - Fall confirmation time (from config)
     - Current status (starts as UNKNOWN)
     - Last position (standing, sitting, lying)
     - Time when person went to floor
     - Last frame analysis time
   
   - **Write it**:
     ```python
     def __init__(self, config: Dict[str, Any]):
         detection = config.get('detection', {})
         self.fall_confirmation_time = detection.get('fall_confirmation_time', 10)
         
         self.status = FallStatus.UNKNOWN
         self.last_position: Optional[str] = None
         self.time_on_floor: Optional[datetime] = None
         self.last_analysis_time: Optional[datetime] = None
     ```

**Step 4: Implement `_determine_position` method**

6. **Implement `_determine_position()`** - This guesses position from sensor data:
   - **Prompt**: Write a method that takes `sensor_data: Dict[str, Any]` and returns position string
   - **Logic**:
     - If no person detected → return None
     - If motion_level > 0.5 → "standing" (person moving)
     - If motion_level < 0.2 and confidence > 0.7 → "lying" (person still, high confidence)
     - Otherwise → "sitting" or "unknown"
   
   - **Write it**:
     ```python
     def _determine_position(self, sensor_data: Dict[str, Any]) -> Optional[str]:
         person_detected = sensor_data.get('person_detected', False)
         if not person_detected:
             return None
         
         motion_level = sensor_data.get('motion_level', 0.0)
         confidence = sensor_data.get('person_confidence', 0.0)
         
         if motion_level > 0.5:
             return "standing"
         elif motion_level < 0.2 and confidence > 0.7:
             return "lying"
         else:
             return "sitting"
     ```

**Step 5: Implement `analyze_frame` method** - Core detection logic!

7. **Implement `analyze_frame()`** - This analyzes one camera frame:
   - **Prompt**: Write a method that:
     1. Determines current position from sensor data
     2. Checks if position changed suddenly (standing → lying = fall!)
     3. Tracks how long person has been on floor
     4. Updates status based on time on floor
   
   - **Logic**:
     - If position is "lying" and last position was "standing" → SUSPICIOUS (sudden change!)
     - If person on floor for X seconds → FALL_DETECTED
     - If person standing/sitting → NORMAL
   
   - **Write it**:
     ```python
     def analyze_frame(self, sensor_data: Dict[str, Any]) -> FallStatus:
         current_position = self._determine_position(sensor_data)
         now = datetime.now()
         
         # No person detected
         if current_position is None:
             self.status = FallStatus.UNKNOWN
             self.last_position = None
             self.time_on_floor = None
             return self.status
         
         # Check for sudden position change (standing → lying)
         if current_position == "lying" and self.last_position == "standing":
             # Sudden change! Potential fall
             self.time_on_floor = now
             self.status = FallStatus.SUSPICIOUS
         elif current_position == "lying":
             # Person still on floor
             if self.time_on_floor is None:
                 self.time_on_floor = now
            
             # Check if on floor long enough to confirm fall
             time_on_floor = (now - self.time_on_floor).total_seconds()
             if time_on_floor >= self.fall_confirmation_time:
                 self.status = FallStatus.FALL_DETECTED
             else:
                 self.status = FallStatus.SUSPICIOUS
         else:
             # Person is standing or sitting - normal
             self.status = FallStatus.NORMAL
             self.time_on_floor = None
         
         self.last_position = current_position
         self.last_analysis_time = now
         
         return self.status
     ```

**Step 6: Implement `get_status` method**

8. **Implement `get_status()`**:
   - **Prompt**: Write a method that returns the current status
   - **Write it**:
     ```python
     def get_status(self) -> FallStatus:
         return self.status
     ```

**Step 7: Test your code**

9. **Checkpoint**: Test the fall detector:
    ```python
    from fall_detection.detection.fall_detector import FallDetector, FallStatus
    
    config = {
        'detection': {
            'fall_confirmation_time': 10
        }
    }
    
    detector = FallDetector(config)
    
    # Simulate standing
    result1 = detector.analyze_frame({
        'person_detected': True,
        'motion_level': 0.8,
        'person_confidence': 0.9
    })
    print(f"Standing: {result1}")
    
    # Simulate sudden fall (standing → lying)
    result2 = detector.analyze_frame({
        'person_detected': True,
        'motion_level': 0.1,
        'person_confidence': 0.9
    })
    print(f"Fall: {result2}")
    assert result2 == FallStatus.SUSPICIOUS
    
    print("✅ Fall detector works!")
    ```

**✅ Checkpoint Questions:**
- [ ] Does your enum have all four status values?
- [ ] Does `_determine_position()` correctly guess position from motion?
- [ ] Does `analyze_frame()` detect sudden position changes?
- [ ] Does it track time on floor correctly?
- [ ] Does it return FALL_DETECTED after confirmation time?

---

## Part 2: Pose Analyzer + inference backends

**File**: `fall_detection/detection/pose_analyzer.py`

**What it does**: Runs pose-style estimation through **`shared/inference/`** so `FallDetector` can prefer real posture over motion-only heuristics when enabled.

**How it fits together:**
- **`PoseAnalyzer`** turns `detection.pose_estimation_enabled` on/off and picks a backend from **`inference.backend`**: `none`, **`mock`**, or **`hailo`**.
- **`shared/inference/mock_pose.py`**: deterministic scenarios for your laptop (`standing`, `lying`, `fall_sequence`, `mirror`, etc.) — see `tests/test_fall_pose_pipeline.py`.
- **`shared/inference/hailo_pose.py`**: stub for **Raspberry Pi 5 + Raspberry Pi AI HAT+ (Hailo-8L / Hailo-8)**. On the Pi you install **HailoRT** and wire **YOLOv8-pose** (or similar) compiled to a **`.hef`** file; then implement `infer()` to return the same dict shape as the mock backend.
- **`fall_detection/main.py`** passes `camera_data` (and optional `frame` if `sensors.camera.include_frame_for_pose: true`) into `analyze_pose()`, then passes the result into **`FallDetector.analyze_frame(..., pose_data)`**.

**Config (see `fall_detection/config.yaml` and `templates/config_fall_detection.yaml`):**
```yaml
detection:
  pose_estimation_enabled: false   # set true to use a backend
  prefer_pose_when_available: true

inference:
  backend: none    # none | mock | hailo
  mock:
    scenario: standing
    fall_sequence_standing_frames: 3
  hailo:
    hef_path: ""   # path to .hef on the Pi when you implement Hailo
```

**Other options (not in-repo defaults):** You could still integrate **MediaPipe** or **CPU YOLO** behind the same `PoseInferenceBackend` interface if you add another backend module.

**Hailo / Pi references (official):**
- Raspberry Pi AI HAT+ product info: https://www.raspberrypi.com/products/ai-hat/
- Hailo developer resources: https://hailo.ai/ — use the **Raspberry Pi 5** + Hailo install flow and model zoo / compiler docs when you are on hardware.

---

## Part 3: Alert Manager

**File**: `fall_detection/detection/alert_manager.py`

**What it does**: Same as non-movement, but alerts immediately (no escalation delay).

**Key difference**: Falls are CRITICAL - send to ALL channels immediately!

**What to build:**
- Copy alert manager from non-movement
- Modify `handle_fall_alert()` to send immediately
- No escalation delay for falls

---

## Part 4: Configuration File

**File**: `fall_detection/config.yaml`

**What it does**: Settings specific to fall detection.

**Key settings:**
```yaml
detection:
  position_change_threshold: 0.5
  floor_detection_enabled: true
  fall_confirmation_time: 10  # seconds
  frame_analysis_interval: 1  # seconds (real-time)
  pose_estimation_enabled: false  # true when using mock or Hailo
  prefer_pose_when_available: true

inference:
  backend: none   # mock | hailo on Pi + AI HAT+

sensors:
  camera:
    check_interval: 1  # Check every second!
    include_frame_for_pose: false  # true when Hailo pipeline needs raw frames
```

**What to include:**
- Fall detection parameters
- Real-time processing settings
- Camera settings (faster than non-movement)
- Alert settings (immediate alerts)

---

## Part 5: Main Application

**File**: `fall_detection/main.py`

**What it does**: Entry point for fall detection.

**Key differences from non-movement:**
- Faster check interval (1 second vs 30 seconds)
- Different detection algorithm
- Immediate alerts

---

### 🎯 Your Turn: Build the Main Application

**Step 1: Create the file and imports**

1. Open/create `fall_detection/main.py`
2. **Write the imports** - You'll need:
   - `sys` module
   - `BaseMonitoringSystem` from `shared.base.monitoring_base`
   - `FallDetector` from `fall_detection.detection.fall_detector`
   - `FallStatus` from `fall_detection.detection.fall_detector`
   - `AlertManager` from `fall_detection.detection.alert_manager`
   - `load_config` from `shared.utils.config_loader`

   **Prompt**: Write all the import statements.

**Step 2: Create the FallDetectionSystem class**

3. **Create the class**:
   ```python
   class FallDetectionSystem(BaseMonitoringSystem):
   ```

4. **Add `__init__` method**:
   - **Prompt**: Write `__init__` that calls `super().__init__(config_path)`
   - **What else should it store?**
     - Fall detector (will create in initialize_project)
     - Alert manager (will create in initialize_project)
   - **Write it**:
     ```python
     def __init__(self, config_path: str = 'config.yaml'):
         super().__init__(config_path)
         self.fall_detector: Optional[FallDetector] = None
         self.alert_manager: Optional[AlertManager] = None
     ```

**Step 3: Implement `initialize_project` method**

5. **Implement `initialize_project()`**:
   - **Prompt**: This method should:
     - Create a `FallDetector` instance with the config
     - Create an `AlertManager` instance
     - Store them in instance variables
   
   - **Write it**:
     ```python
     def initialize_project(self) -> None:
         # Create fall detector
         self.fall_detector = FallDetector(self.config)
         
         # Create alert manager
         self.alert_manager = AlertManager(self.config, self.logger)
         
         self.logger.info("Fall detection system initialized")
     ```

**Step 4: Implement `run_cycle` method** - Real-time fall detection!

6. **Implement `run_cycle()`** - This runs every second (faster than non-movement):
   - **Prompt**: Write a method that:
     1. Reads from the camera sensor
     2. Analyzes the frame for falls
     3. If fall detected, send immediate alert to ALL channels
     4. Logs status changes
   
   - **Key difference**: Falls are CRITICAL - send immediately, no delay!
   
   - **Write it**:
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
         
         # Analyze frame for falls
         status = self.fall_detector.analyze_frame(sensor_data)
         
         # Log status changes
         if status != self.fall_detector.status:
             self.logger.info(f"Status changed to: {status.value}")
         
         # If fall detected, send immediate alert!
         if status == FallStatus.FALL_DETECTED:
             self.logger.critical("FALL DETECTED! Sending immediate alert!")
             
             # Create critical alert
             alert = self.alert_manager.create_alert(
                 level='CRITICAL',
                 message="FALL DETECTED! Person may need immediate assistance!",
                 details={'status': status.value, 'position': self.fall_detector.last_position}
             )
             
             # Send to ALL channels immediately (no escalation delay)
             self.alert_manager.send_alert(alert, immediate=True)
     ```

**Step 5: Implement `shutdown_project` method**

7. **Implement `shutdown_project()`**:
   - **Prompt**: Write a method that cleans up
   - **Write it**:
     ```python
     def shutdown_project(self) -> None:
         self.logger.info("Shutting down fall detection system")
     ```

**Step 6: Create the `main` function**

8. **Create `main()` function**:
   - **Prompt**: Write a function similar to non-movement, but for fall detection
   - **Write it**:
     ```python
     def main():
         config_path = sys.argv[1] if len(sys.argv) > 1 else 'config.yaml'
         
         system = FallDetectionSystem(config_path)
         
         try:
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

9. **Checkpoint**: Test the fall detection application:
    ```bash
    cd fall_detection
    python main.py
    ```
    
    **What should happen:**
    - System initializes
    - Camera reads every second (faster than non-movement)
    - When fall detected, immediate alert sent
    - Press Ctrl+C to stop

**✅ Checkpoint Questions:**
- [ ] Does your class inherit from `BaseMonitoringSystem`?
- [ ] Does `initialize_project()` create the fall detector?
- [ ] Does `run_cycle()` analyze frames every second?
- [ ] Does it send immediate alerts when fall detected?
- [ ] Does `main()` handle Ctrl+C gracefully?
- [ ] Can you run the application without errors?

---

## Part 6: Requirements File

**File**: `fall_detection/requirements.txt`

**What it does**: Lists packages needed.

**Same as non-movement, plus (optional for future):**
```
# Optional: For advanced pose estimation
# mediapipe>=0.10.0
# tensorflow>=2.13.0
```

---

## Testing Your Project

**Test with mock camera:**

```bash
cd fall_detection
python main.py --mock
```

**Test fall scenario:**
```python
# In your code or test:
sensor.set_simulation_mode('fall')
# Should detect fall and send alert
```

**What you should see:**
- System initializes
- Camera reads every second
- Status shows position
- Alert sent immediately when fall detected

---

## Understanding the Flow

1. **Start**: `main.py` runs
2. **Initialize**: Load config, setup sensors, setup fall detector
3. **Loop**: Every 1 second:
   - Read camera frame
   - Analyze position
   - Check for fall
   - Send immediate alert if fall detected
4. **Shutdown**: Cleanup

---

## Key Differences: Fall vs Non-Movement

| Aspect | Non-Movement | Fall Detection |
|--------|--------------|----------------|
| Check interval | 30 seconds | 1 second |
| Algorithm | Time-based | Position-based |
| Alert speed | Escalation (delayed) | Immediate |
| CPU usage | Low | Higher (lower if pose runs on Hailo NPU) |
| Use case | Long inactivity | Emergency |

---

## ✅ Checklist

- [ ] Fall detector created and working
- [ ] Pose analyzer + inference config understood (`mock` / `hailo` path)
- [ ] Alert manager created (immediate alerts)
- [ ] Config file created
- [ ] Main application created
- [ ] Requirements file created
- [ ] Tests with mock camera pass
- [ ] Can detect "fall" scenario
- [ ] Immediate alerts work

---

## Common Issues

### "Too slow"
- **Solution**: Reduce resolution or increase check_interval slightly
- Fall detection is CPU-intensive

### "False positives"
- **Solution**: Adjust `fall_confirmation_time` (longer = fewer false alarms)
- Improve position detection algorithm

### "Can't detect position"
- **Solution**: Keep `pose_estimation_enabled: false` to use motion heuristics, or enable **`mock`** inference to test the pose path without hardware
- On Pi with **AI HAT+**: set **`inference.backend: hailo`**, implement `shared/inference/hailo_pose.py`, and tune `fall_confirmation_time`

---

## Next Step

Once both projects work, go to **STUDENT_GUIDE_06_TESTING.md**

---

*Fall detection is more complex. Take time to understand position detection!*
