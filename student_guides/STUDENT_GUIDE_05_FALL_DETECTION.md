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

**What to build:**
- Class `FallDetector`
- Method `analyze_frame()` - checks one camera frame
- Method `_determine_position()` - figures out person's position
- Method `get_status()` - current detector status
- State tracking (last position, time on floor)

**Simplified approach (for now):**
- Use motion level to guess position
- Low motion + high confidence = lying
- High motion = standing
- (Later: Use pose estimation for accuracy)

---

## Part 2: Pose Analyzer (Placeholder)

**File**: `fall_detection/detection/pose_analyzer.py`

**What it does**: Will analyze person's pose/position (for future enhancement).

**For now**: Create structure, leave implementation simple.

**Future options:**
- **MediaPipe**: Google's pose estimation
- **OpenPose**: Open-source pose detection
- **YOLO**: Object detection with pose

**What to build:**
- Class `PoseAnalyzer`
- Method `analyze_pose()` - placeholder for now
- Methods: `is_person_standing()`, `is_person_lying()`
- Method `detect_sudden_change()` - detects position change

**MediaPipe reference** (for later): https://google.github.io/mediapipe/solutions/pose

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

sensors:
  camera:
    check_interval: 1  # Check every second!
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

**What to build:**
- Class `FallDetectionSystem` extends `BaseMonitoringSystem`
- Method `initialize_project()` - sets up fall detector
- Method `run_cycle()` - analyzes frame for falls
- Method `_handle_fall_alert()` - sends immediate alert
- `main()` function

**Structure:**
```python
class FallDetectionSystem(BaseMonitoringSystem):
    def initialize_project(self):
        # Create fall detector, pose analyzer
        
    def run_cycle(self):
        # Read camera
        # Analyze for falls
        # Send immediate alert if fall detected
        
    def _handle_fall_alert(self):
        # Send to ALL channels immediately
```

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
| CPU usage | Low | High |
| Use case | Long inactivity | Emergency |

---

## ✅ Checklist

- [ ] Fall detector created and working
- [ ] Pose analyzer placeholder created
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
- **Solution**: For now, use simplified motion-based detection
- Later: Add pose estimation (MediaPipe, etc.)

---

## Next Step

Once both projects work, go to **STUDENT_GUIDE_06_TESTING.md**

---

*Fall detection is more complex. Take time to understand position detection!*
