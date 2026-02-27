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

---

### 🎯 Your Turn: Build the Base Sensor Class

**Step 1: Create the file and imports**

1. Open/create `shared/sensors/base_sensor.py`
2. **Write the imports** - You'll need:
   - `ABC` and `abstractmethod` from `abc` module
   - `Optional` from `typing` module
   - `Dict` and `Any` from `typing` module

   **Prompt**: Write the import statements. Think: What do you need to create an abstract class in Python?

   **Hint**: `from abc import ABC, abstractmethod`

**Step 2: Create the class structure**

3. **Create the class** - Write:
   ```python
   class BaseSensor(ABC):
   ```
   Why does it inherit from `ABC`? (Think: Abstract Base Class)

4. **Add `__init__` method** - This initializes the sensor with configuration:
   - **Prompt**: Write an `__init__` method that takes `config: Dict[str, Any]` as a parameter
   - **What should it store?** Think about what a sensor needs:
     - Is it enabled? (from config)
     - Is it initialized? (starts as False)
     - The config itself (for later use)
   - **Write it**: Create instance variables like `self.enabled`, `self.initialized`, `self.config`

   **Hint**: 
   ```python
   def __init__(self, config: Dict[str, Any]):
       self.config = config
       self.enabled = config.get('enabled', False)
       self.initialized = False
   ```

**Step 3: Add abstract methods**

5. **Add `initialize` method** - This will be overridden by child classes:
   - **Prompt**: Write an abstract method called `initialize()` that returns `bool`
   - **What makes it abstract?** Use the `@abstractmethod` decorator
   - **Write it**: 
     ```python
     @abstractmethod
     def initialize(self) -> bool:
         pass
     ```
   - **Question**: Why do we use `pass`? (Because child classes will implement it)

6. **Add `read` method** - This reads sensor data:
   - **Prompt**: Write an abstract method `read()` that returns `Optional[Dict[str, Any]]`
   - **Why Optional?** (Sometimes sensors might return None if there's an error)
   - **Write it**: Use `@abstractmethod` decorator

7. **Add `cleanup` method** - This cleans up resources:
   - **Prompt**: Write an abstract method `cleanup()` that returns `None`
   - **Write it**: Use `@abstractmethod` decorator

**Step 4: Add helper methods**

8. **Add `is_enabled` method** - Check if sensor is enabled:
   - **Prompt**: Write a method that returns `True` if the sensor is enabled
   - **Write it**: Should return `self.enabled`

9. **Add `is_initialized` method** - Check if sensor is initialized:
   - **Prompt**: Write a method that returns `True` if the sensor is initialized
   - **Write it**: Should return `self.initialized`

**Step 5: Test your code**

10. **Checkpoint**: Try to create an instance (it should fail because it's abstract):
    ```python
    # This should give an error - that's good!
    from shared.sensors.base_sensor import BaseSensor
    sensor = BaseSensor({'enabled': True})  # Should fail!
    ```
    **Why does it fail?** (Because you can't instantiate an abstract class)

**✅ Checkpoint Questions:**
- [ ] Does your class inherit from `ABC`?
- [ ] Do you have `@abstractmethod` decorators on `initialize()`, `read()`, and `cleanup()`?
- [ ] Does `__init__` store `enabled`, `initialized`, and `config`?
- [ ] Can you import the class without errors?

---

## Part 2: Mock Camera Sensor

**File**: `shared/sensors/mock_camera.py`

**What it does**: Simulates a camera for testing (works without hardware).

**Key concepts:**
- **Simulation**: Pretends to be a real camera
- **Random values**: Generates fake detection data
- **Different modes**: Normal, fall, no person, etc.

**Helpful packages:**
- `random` - Built into Python (no install needed)
- `numpy` - For arrays (already installed)

---

### 🎯 Your Turn: Build the Mock Camera Sensor

**Step 1: Create the file and imports**

1. Open/create `shared/sensors/mock_camera.py`
2. **Write the imports** - You'll need:
   - `BaseSensor` from `shared.sensors.base_sensor`
   - `Dict`, `Any`, `Optional` from `typing`
   - `random` module (built-in)
   - `time` module (built-in)

   **Prompt**: Write all the import statements. Think: What do you need to import?

**Step 2: Create the class**

3. **Create the class** - Write:
   ```python
   class MockCameraSensor(BaseSensor):
   ```
   **Question**: Why does it inherit from `BaseSensor`? (So it follows the same interface)

4. **Add `__init__` method**:
   - **Prompt**: Write `__init__` that calls `super().__init__(config)`
   - **What else should it store?** Think about simulation:
     - Current simulation mode (e.g., 'normal', 'fall', 'no_person')
     - Maybe a counter for tracking reads?
   - **Write it**: 
     ```python
     def __init__(self, config: Dict[str, Any]):
         super().__init__(config)
         self.simulation_mode = config.get('simulation_mode', 'normal')
         self.read_count = 0
     ```

**Step 3: Implement `initialize` method**

5. **Implement `initialize()`**:
   - **Prompt**: This method should:
     - Set `self.initialized = True`
     - Return `True` if successful
   - **Write it**: 
     ```python
     def initialize(self) -> bool:
         self.initialized = True
         return True
     ```
   - **Question**: Why is this simple? (Mock sensor doesn't need real hardware setup)

**Step 4: Implement `read` method**

6. **Implement `read()`** - This is the fun part! You'll generate fake camera data:
   - **Prompt**: Write a method that returns a dictionary with:
     - `person_detected`: bool (is a person visible?)
     - `person_confidence`: float (0.0 to 1.0, how confident?)
     - `motion_detected`: bool (is there movement?)
     - `motion_level`: float (0.0 to 1.0, how much movement?)

   - **Think about different modes**:
     - `'normal'`: Person detected, some motion
     - `'fall'`: Person detected, no motion (lying down)
     - `'no_person'`: No person detected
     - `'active'`: Person detected, lots of motion

   - **Write it step by step**:
     ```python
     def read(self) -> Optional[Dict[str, Any]]:
         if not self.initialized:
             return None
         
         self.read_count += 1
         
         # Based on simulation_mode, return different data
         if self.simulation_mode == 'normal':
             return {
                 'person_detected': True,
                 'person_confidence': random.uniform(0.7, 0.95),
                 'motion_detected': True,
                 'motion_level': random.uniform(0.3, 0.7)
             }
         # TODO: Add other modes!
     ```

7. **Add other simulation modes**:
   - **Prompt**: Add `elif` statements for:
     - `'fall'`: Person detected, but no motion (person lying down)
     - `'no_person'`: No person detected
     - `'active'`: Person detected, high motion
   - **Write it**: Use `random.uniform()` for confidence and motion levels

**Step 5: Implement `cleanup` method**

8. **Implement `cleanup()`**:
   - **Prompt**: This should reset the sensor state
   - **Write it**: Set `self.initialized = False`

**Step 6: Add helper method for changing mode**

9. **Add `set_simulation_mode` method**:
   - **Prompt**: Write a method that takes a mode string and updates `self.simulation_mode`
   - **Write it**: 
     ```python
     def set_simulation_mode(self, mode: str) -> None:
         self.simulation_mode = mode
     ```

**Step 7: Test your code**

10. **Checkpoint**: Test the mock camera:
    ```python
    from shared.sensors.mock_camera import MockCameraSensor
    
    # Create sensor
    sensor = MockCameraSensor({'enabled': True, 'simulation_mode': 'normal'})
    
    # Initialize
    sensor.initialize()
    
    # Read data
    result = sensor.read()
    print(f"Result: {result}")
    
    # Check it has the right keys
    assert 'person_detected' in result
    assert 'motion_detected' in result
    print("✅ Mock camera works!")
    ```

**✅ Checkpoint Questions:**
- [ ] Does your class inherit from `BaseSensor`?
- [ ] Does `initialize()` set `self.initialized = True`?
- [ ] Does `read()` return a dictionary with all required keys?
- [ ] Can you test different simulation modes?
- [ ] Does `cleanup()` reset the initialized state?

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

---

### 🎯 Your Turn: Build the Logger

**Step 1: Create the file and imports**

1. Open/create `shared/alerts/logger.py`
2. **Write the imports** - You'll need:
   - `logging` module (built-in)
   - `RotatingFileHandler` from `logging.handlers`
   - `Optional` from `typing`
   - `os` module (for file paths)

   **Prompt**: Write all the import statements.

**Step 2: Create the class**

3. **Create the class**:
   ```python
   class AlertLogger:
   ```

4. **Add `__init__` method**:
   - **Prompt**: Write `__init__` that takes:
     - `log_file`: str (path to log file)
     - `log_level`: str (default 'INFO')
     - `max_bytes`: int (default 10485760, which is 10MB)
     - `backup_count`: int (default 5, how many backup files)
   
   - **What should it do?**
     - Create the logger
     - Set up file handler with rotation
     - Set up console handler
     - Set the log level
   
   - **Write it step by step**:
     ```python
     def __init__(self, log_file: str = 'monitoring.log', 
                  log_level: str = 'INFO',
                  max_bytes: int = 10485760,
                  backup_count: int = 5):
         # Create logger
         self.logger = logging.getLogger('AlertLogger')
         self.logger.setLevel(getattr(logging, log_level.upper()))
         
         # Prevent duplicate handlers
         if self.logger.handlers:
             self.logger.handlers.clear()
         
         # Create formatter
         formatter = logging.Formatter(
             '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
         )
         
         # File handler with rotation
         file_handler = RotatingFileHandler(
             log_file, maxBytes=max_bytes, backupCount=backup_count
         )
         file_handler.setFormatter(formatter)
         self.logger.addHandler(file_handler)
         
         # Console handler
         console_handler = logging.StreamHandler()
         console_handler.setFormatter(formatter)
         self.logger.addHandler(console_handler)
     ```

**Step 3: Implement logging methods**

5. **Implement `debug()` method**:
   - **Prompt**: Write a method that logs a DEBUG message
   - **Write it**: 
     ```python
     def debug(self, message: str) -> None:
         self.logger.debug(message)
     ```

6. **Implement other logging methods**:
   - **Prompt**: Write `info()`, `warning()`, `error()`, and `critical()` methods
   - **Write it**: Each should call the corresponding logger method
   - **Example**:
     ```python
     def info(self, message: str) -> None:
         self.logger.info(message)
     ```

**Step 4: Test your code**

7. **Checkpoint**: Test the logger:
    ```python
    from shared.alerts.logger import AlertLogger
    
    logger = AlertLogger('test.log')
    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning")
    logger.error("This is an error")
    
    # Check if file was created
    import os
    assert os.path.exists('test.log')
    print("✅ Logger works!")
    ```

**✅ Checkpoint Questions:**
- [ ] Does your logger create a file handler?
- [ ] Does it create a console handler?
- [ ] Do all logging methods (debug, info, warning, error, critical) work?
- [ ] Does log rotation work? (Try writing many messages)

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

---

### 🎯 Your Turn: Build the Configuration Loader

**Step 1: Create the file and imports**

1. Open/create `shared/utils/config_loader.py`
2. **Write the imports** - You'll need:
   - `yaml` module (you installed PyYAML)
   - `os` module (for file paths)
   - `Dict`, `Any` from `typing`
   - `Optional` from `typing`

   **Prompt**: Write all the import statements.

**Step 2: Implement `load_config` function**

3. **Write `load_config()` function**:
   - **Prompt**: Write a function that:
     - Takes `file_path: str` as parameter
     - Opens and reads the YAML file
     - Parses it using `yaml.safe_load()`
     - Returns the config as a dictionary
     - Handles errors (file not found, invalid YAML)
   
   - **Write it step by step**:
     ```python
     def load_config(file_path: str) -> Optional[Dict[str, Any]]:
         # Check if file exists
         if not os.path.exists(file_path):
             raise FileNotFoundError(f"Config file not found: {file_path}")
         
         # Open and read file
         try:
             with open(file_path, 'r') as f:
                 config = yaml.safe_load(f)
             return config
         except yaml.YAMLError as e:
             raise ValueError(f"Invalid YAML in config file: {e}")
     ```

   - **Question**: Why use `yaml.safe_load()` instead of `yaml.load()`? (Security - safe_load prevents code execution)

**Step 3: Implement `validate_config` function**

4. **Write `validate_config()` function**:
   - **Prompt**: Write a function that checks if config has required sections:
     - `sensors` section (required)
     - At least one sensor enabled
     - `monitoring` or `detection` section (depending on project)
   
   - **Think about**: What should happen if validation fails?
     - Raise an exception? Return False?
   
   - **Write it**:
     ```python
     def validate_config(config: Dict[str, Any]) -> bool:
         # Check required sections
         if 'sensors' not in config:
             raise ValueError("Config missing 'sensors' section")
         
         # Check at least one sensor is enabled
         sensors = config.get('sensors', {})
         has_enabled = False
         for sensor_name, sensor_config in sensors.items():
             if sensor_config.get('enabled', False):
                 has_enabled = True
                 break
         
         if not has_enabled:
             raise ValueError("At least one sensor must be enabled")
         
         return True
     ```

**Step 4: Test your code**

5. **Checkpoint**: Create a test config file and test loading:
    ```yaml
    # test_config.yaml
    sensors:
      camera:
        enabled: true
    monitoring:
      check_interval: 30
    ```
    
    ```python
    from shared.utils.config_loader import load_config, validate_config
    
    config = load_config('test_config.yaml')
    print(f"Config loaded: {config}")
    
    validate_config(config)
    print("✅ Config is valid!")
    ```

**✅ Checkpoint Questions:**
- [ ] Does `load_config()` read YAML files correctly?
- [ ] Does it handle file not found errors?
- [ ] Does it handle invalid YAML errors?
- [ ] Does `validate_config()` check for required sections?
- [ ] Does it check that at least one sensor is enabled?

---

## Part 9: Time Utilities

**File**: `shared/utils/time_utils.py`

**What it does**: Helper functions for working with time.

**Key concepts:**
- **datetime**: Python's time handling
- **timedelta**: Time differences
- **Formatting**: Making time readable

**Python reference**: https://docs.python.org/3/library/datetime.html

---

### 🎯 Your Turn: Build Time Utilities

**Step 1: Create the file and imports**

1. Open/create `shared/utils/time_utils.py`
2. **Write the imports** - You'll need:
   - `datetime` from `datetime` module
   - `timedelta` from `datetime` module

   **Prompt**: Write the import statements.

**Step 2: Implement `get_current_time` function**

3. **Write `get_current_time()` function**:
   - **Prompt**: Write a function that returns the current date and time
   - **Write it**:
     ```python
     def get_current_time() -> datetime:
         return datetime.now()
     ```
   - **Question**: Why use `datetime.now()`? (Gets current time with timezone)

**Step 3: Implement `format_timedelta` function**

4. **Write `format_timedelta()` function**:
   - **Prompt**: Write a function that takes a `timedelta` and returns a readable string
   - **Example**: `timedelta(hours=2, minutes=30)` → `"2 hours 30 minutes"`
   - **Think about**: How to extract hours, minutes, seconds from a timedelta?
   
   - **Write it**:
     ```python
     def format_timedelta(td: timedelta) -> str:
         total_seconds = int(td.total_seconds())
         hours = total_seconds // 3600
         minutes = (total_seconds % 3600) // 60
         seconds = total_seconds % 60
         
         parts = []
         if hours > 0:
             parts.append(f"{hours} hour{'s' if hours != 1 else ''}")
         if minutes > 0:
             parts.append(f"{minutes} minute{'s' if minutes != 1 else ''}")
         if seconds > 0 or not parts:
             parts.append(f"{seconds} second{'s' if seconds != 1 else ''}")
         
         return " ".join(parts)
     ```

**Step 4: Implement `is_time_between` function**

5. **Write `is_time_between()` function**:
   - **Prompt**: Write a function that checks if current time is between two times
   - **Parameters**: `start_hour: int`, `end_hour: int`, `current_time: Optional[datetime] = None`
   - **Example**: `is_time_between(7, 22)` returns True if current time is between 7am and 10pm
   
   - **Write it**:
     ```python
     def is_time_between(start_hour: int, end_hour: int, 
                        current_time: Optional[datetime] = None) -> bool:
         if current_time is None:
             current_time = datetime.now()
         
         current_hour = current_time.hour
         
         if start_hour <= end_hour:
             return start_hour <= current_hour < end_hour
         else:
             # Handles overnight ranges (e.g., 22 to 7)
             return current_hour >= start_hour or current_hour < end_hour
     ```

**Step 5: Test your code**

6. **Checkpoint**: Test the time utilities:
    ```python
    from shared.utils.time_utils import get_current_time, format_timedelta, is_time_between
    from datetime import timedelta
    
    # Test get_current_time
    now = get_current_time()
    print(f"Current time: {now}")
    
    # Test format_timedelta
    td = timedelta(hours=2, minutes=30, seconds=45)
    formatted = format_timedelta(td)
    print(f"Formatted: {formatted}")
    
    # Test is_time_between
    is_active = is_time_between(7, 22)
    print(f"Is active hours? {is_active}")
    
    print("✅ Time utilities work!")
    ```

**✅ Checkpoint Questions:**
- [ ] Does `get_current_time()` return current datetime?
- [ ] Does `format_timedelta()` format time nicely?
- [ ] Does `is_time_between()` correctly check time ranges?
- [ ] Does it handle overnight ranges (e.g., 22 to 7)?

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
