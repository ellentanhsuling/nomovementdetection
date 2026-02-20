# Student Build Guide - Step 6: Testing Everything

## What You're Doing

Testing both projects to make sure they work correctly before deploying to Raspberry Pi.

---

## Testing Strategy

**Three levels of testing:**
1. **Unit tests** - Test individual components
2. **Integration tests** - Test components working together
3. **End-to-end tests** - Test complete projects

---

## Part 1: Test Shared Library

**File**: `tests/test_shared.py`

**What to test:**
- Mock camera sensor works
- Logger writes to file
- Config loader reads YAML
- Time utilities work

**Example test:**
```python
import unittest
from shared.sensors.mock_camera import MockCameraSensor
from shared.alerts.logger import AlertLogger

class TestShared(unittest.TestCase):
    def test_mock_camera(self):
        sensor = MockCameraSensor({'enabled': True})
        self.assertTrue(sensor.initialize())
        result = sensor.read()
        self.assertIsNotNone(result)
        self.assertIn('person_detected', result)

if __name__ == '__main__':
    unittest.main()
```

**Run**: `python -m pytest tests/test_shared.py`

**Python testing**: https://docs.python.org/3/library/unittest.html

---

## Part 2: Test Non-Movement Project

**Test scenarios:**

1. **Normal activity** (person moving)
   - Should show ACTIVE status
   - No alerts

2. **No movement for 20 minutes** (during active hours)
   - Should show INACTIVE (below threshold)
   - No alerts yet

3. **No movement for 35 minutes** (during active hours)
   - Should show CONCERNING
   - Should send alert

4. **No movement during sleep hours**
   - Should use sleep threshold (longer)
   - Different behavior

**How to test:**
```python
# Create test script: test_non_movement.py
from non_movement.detection.movement_detector import MovementDetector

detector = MovementDetector(config)
detector.record_movement('Camera', {'person_detected': True, 'motion_detected': True})
# Wait or simulate time passing
status = detector.check_movement_status(...)
assert status == MovementStatus.CONCERNING
```

---

## Part 3: Test Fall Detection Project

**Test scenarios:**

1. **Normal standing**
   - Should show NORMAL status
   - No alerts

2. **Person lies down slowly** (going to bed)
   - Should show SUSPICIOUS
   - But not FALL_DETECTED (not sudden)

3. **Sudden fall** (standing → lying quickly)
   - Should show FALL_DETECTED
   - Should send immediate alert

4. **Person on floor for 10+ seconds**
   - Should confirm fall
   - Should send alert

**How to test:**
```python
# Create test script: test_fall_detection.py
from fall_detection.detection.fall_detector import FallDetector

detector = FallDetector(config)
# Simulate standing
result1 = detector.analyze_frame({'person_detected': True, 'motion_level': 0.8})
# Simulate sudden fall
result2 = detector.analyze_frame({'person_detected': True, 'motion_level': 0.0})
assert result2 == FallStatus.FALL_DETECTED
```

---

## Part 4: Test Alert System

**Test each alert channel:**

1. **Email alerts**
   - Configure SMTP settings
   - Send test email
   - Verify received

2. **SMS alerts** (if using Twilio)
   - Configure Twilio
   - Send test SMS
   - Verify received

3. **API alerts**
   - Set up test endpoint
   - Send test alert
   - Verify received

4. **Logging**
   - Check log file created
   - Verify messages written
   - Check log rotation works

---

## Part 5: Integration Testing

**Test complete workflows:**

**Non-Movement:**
```bash
cd non_movement
python main.py --mock
# Let it run for a few minutes
# Change mock camera mode to simulate no movement
# Verify alerts are sent
```

**Fall Detection:**
```bash
cd fall_detection
python main.py --mock
# Change mock camera mode to 'fall'
# Verify immediate alert
```

---

## Part 6: Performance Testing

**Check resource usage:**

```bash
# Monitor CPU and memory
# On Mac/Linux:
top -p $(pgrep -f "python.*main.py")

# On Windows:
# Task Manager
```

**What to check:**
- CPU usage (should be reasonable)
- Memory usage (shouldn't grow forever)
- Response time (alerts sent quickly)

---

## Part 7: Error Handling Tests

**Test error scenarios:**

1. **Camera fails**
   - Should handle gracefully
   - Should log error
   - Should continue running

2. **Config file missing**
   - Should show clear error
   - Should not crash

3. **Network failure** (for API alerts)
   - Should retry
   - Should log error
   - Should continue running

4. **Invalid sensor data**
   - Should handle None values
   - Should not crash

---

## Part 8: Test Project Switching

**Test the switcher script:**

```bash
# Start non-movement
cd non_movement
python main.py --mock &
# Note the process ID

# Switch to fall detection
./switch_project.sh fall_detection
# Verify non-movement stopped
# Verify fall detection started
```

---

## Testing Checklist

### Shared Library
- [ ] Mock camera works
- [ ] Logger works
- [ ] Config loader works
- [ ] All alert channels work
- [ ] Time utilities work

### Non-Movement Project
- [ ] Detects normal activity
- [ ] Detects inactivity
- [ ] Sends alerts at correct thresholds
- [ ] Pattern learning works
- [ ] Handles errors gracefully

### Fall Detection Project
- [ ] Detects normal position
- [ ] Detects falls
- [ ] Sends immediate alerts
- [ ] Handles errors gracefully

### Integration
- [ ] Both projects can run (separately)
- [ ] Switching works
- [ ] Alerts work end-to-end
- [ ] Performance is acceptable

---

## Common Testing Issues

### "Tests fail with import errors"
- **Solution**: Make sure you're in project root
- Add paths: `sys.path.insert(0, '..')`

### "Mock camera always returns same values"
- **Solution**: That's normal - it's random but consistent
- Use `set_simulation_mode()` to test different scenarios

### "Alerts not sending"
- **Solution**: Check configuration
- Check credentials (email/SMS)
- Check network connection (API)

---

## Next Step

Once everything tests successfully, go to **STUDENT_GUIDE_07_RASPBERRY_PI.md**

---

*Testing is crucial. Don't skip it! Find and fix bugs now, not later.*
