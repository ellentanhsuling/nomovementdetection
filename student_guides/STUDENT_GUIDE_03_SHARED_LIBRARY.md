# Student Build Guide - Step 3: Build Shared Library

## What You're Doing

Building code that **both projects will use**. This avoids writing the same code twice!

---

## Understanding the Shared Library

**Think of it like a toolbox**: Both projects use the same tools (camera, alerts, etc.)

**Structure:**
```
shared/
├── sensors/     # Camera code (mock for testing, real for Pi)
├── alerts/      # Email, SMS, API alerts
├── utils/       # Helper functions
└── base/        # Base class for projects
```

---

## Part 1: Base Sensor Class

**File**: `shared/sensors/base_sensor.py`

**What it does**: Defines what ALL sensors must have (like a template).

**Key concepts:**
- **Abstract class**: Can't use it directly, other classes inherit from it
- **Methods**: `initialize()`, `read()`, `cleanup()`

**Python reference**: https://docs.python.org/3/library/abc.html (Abstract Base Classes)

**What to build:**
- A class called `BaseSensor`
- Methods that child classes will override
- Status tracking (enabled, initialized, etc.)

---

## Part 2: Mock Camera Sensor

**File**: `shared/sensors/mock_camera.py`

**What it does**: Simulates a camera for testing (works without hardware).

**Key concepts:**
- **Simulation**: Pretends to be a real camera
- **Random values**: Generates fake detection data
- **Different modes**: Normal, fall, no person, etc.

**What to build:**
- Class `MockCameraSensor` that inherits from `BaseSensor`
- Methods to simulate person detection
- Methods to simulate motion detection
- Ability to change simulation mode

**Helpful packages:**
- `random` - Built into Python (no install needed)
- `numpy` - For arrays (already installed)

---

## Part 3: Real Camera Sensor (Placeholder)

**File**: `shared/sensors/real_camera.py`

**What it does**: Will use real Raspberry Pi camera (for later).

**For now**: Just create the structure, leave implementation empty.

**What to build:**
- Class `RealCameraSensor` that inherits from `BaseSensor`
- Placeholder methods (will implement when you have Pi)
- Comments explaining what each method will do

**Future reference**: https://datasheets.raspberrypi.com/camera/picamera2-manual.pdf

---

## Part 4: Logger

**File**: `shared/alerts/logger.py`

**What it does**: Writes messages to files and console.

**Key concepts:**
- **Logging levels**: DEBUG, INFO, WARNING, ERROR, CRITICAL
- **File rotation**: Prevents log files from getting too big
- **Formatters**: How messages look

**Python reference**: https://docs.python.org/3/library/logging.html

**What to build:**
- Class `AlertLogger`
- Methods: `debug()`, `info()`, `warning()`, `error()`, `critical()`
- File and console output
- Log rotation

---

## Part 5: Email Alert

**File**: `shared/alerts/email_alert.py`

**What it does**: Sends emails when alerts happen.

**Key concepts:**
- **SMTP**: Protocol for sending emails
- **TLS/SSL**: Secure connection
- **Environment variables**: Store passwords safely

**Python reference**: https://docs.python.org/3/library/smtplib.html

**What to build:**
- Class `EmailAlert`
- Method `send()` that sends email
- Configuration from config file
- Error handling

**Package needed**: `smtplib` (built into Python)

---

## Part 6: SMS Alert (Optional)

**File**: `shared/alerts/sms_alert.py`

**What it does**: Sends SMS messages via Twilio.

**Key concepts:**
- **API**: Using external service (Twilio)
- **API keys**: Authentication
- **Optional dependency**: Code works even if Twilio not installed

**Twilio docs**: https://www.twilio.com/docs/sms/quickstart/python

**What to build:**
- Class `SMSAlert`
- Try/except for missing Twilio library
- Method `send()` that uses Twilio API
- Error handling

**Package needed**: `twilio` (optional - `pip install twilio`)

---

## Part 7: API Alert

**File**: `shared/alerts/api_alert.py`

**What it does**: Sends alerts to a web API endpoint.

**Key concepts:**
- **HTTP POST**: Sending data to a server
- **JSON**: Data format
- **Retry logic**: Try again if it fails

**Python reference**: https://requests.readthedocs.io/ (you installed `requests`)

**What to build:**
- Class `APIAlert`
- Method `send()` that posts to API
- Retry logic (try 3 times if it fails)
- Error handling

---

## Part 8: Configuration Loader

**File**: `shared/utils/config_loader.py`

**What it does**: Reads YAML configuration files.

**Key concepts:**
- **YAML**: Human-readable config format
- **File reading**: Opening and reading files
- **Validation**: Checking config is correct

**PyYAML docs**: https://pyyaml.org/wiki/PyYAMLDocumentation

**What to build:**
- Function `load_config()` - reads YAML file
- Function `validate_config()` - checks it's valid
- Error handling for missing/invalid files

---

## Part 9: Time Utilities

**File**: `shared/utils/time_utils.py`

**What it does**: Helper functions for working with time.

**Key concepts:**
- **datetime**: Python's time handling
- **timedelta**: Time differences
- **Formatting**: Making time readable

**Python reference**: https://docs.python.org/3/library/datetime.html

**What to build:**
- Function `get_current_time()` - returns now
- Function `format_timedelta()` - makes time readable
- Function `is_time_between()` - checks if time is in range

---

## Part 10: Base Monitoring Class

**File**: `shared/base/monitoring_base.py`

**What it does**: Base class that both projects will inherit from.

**Key concepts:**
- **Inheritance**: Projects extend this class
- **Common functionality**: Setup, sensor init, alerts, main loop
- **Abstract methods**: Projects must implement `run_cycle()`

**What to build:**
- Class `BaseMonitoringSystem`
- Methods: `initialize()`, `run()`, `shutdown()`
- Sensor initialization
- Alert channel setup
- Main loop framework

---

## Testing Your Shared Library

Create a simple test:

**File**: `tests/test_shared.py`

```python
from shared.sensors.mock_camera import MockCameraSensor

# Test mock camera
sensor = MockCameraSensor({'enabled': True})
sensor.initialize()
result = sensor.read()
print(f"Camera result: {result}")
```

Run it:
```bash
python tests/test_shared.py
```

---

## ✅ Checklist

- [ ] Base sensor class created
- [ ] Mock camera sensor working
- [ ] Real camera sensor placeholder created
- [ ] Logger working
- [ ] Email alert working
- [ ] SMS alert working (optional)
- [ ] API alert working
- [ ] Config loader working
- [ ] Time utilities working
- [ ] Base monitoring class created
- [ ] Tests pass

---

## Common Issues

### "Module not found"
- **Solution**: Make sure you're in the project root
- Check `__init__.py` files exist

### "Can't import"
- **Solution**: Add project root to Python path:
  ```python
  import sys
  sys.path.insert(0, '/path/to/raspberry')
  ```

---

## Next Step

Once shared library is complete, go to **STUDENT_GUIDE_04_NON_MOVEMENT.md**

---

*The shared library is the foundation. Take time to understand each part!*
