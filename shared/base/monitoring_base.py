"""
Base monitoring system class

Provides common functionality for both non-movement and fall detection projects.
"""

import sys
import signal
import time
from datetime import datetime
from typing import Dict, Any, Optional
from pathlib import Path

# Add shared to path
shared_path = Path(__file__).parent.parent
sys.path.insert(0, str(shared_path.parent))

from shared.utils.config_loader import load_config, validate_config
from shared.alerts.logger import AlertLogger
from shared.alerts.email_alert import EmailAlert
from shared.alerts.sms_alert import SMSAlert
from shared.alerts.api_alert import APIAlert
from shared.alerts.webhook_alert import WebhookAlert
from shared.sensors.mock_camera import MockCameraSensor
from shared.sensors.real_camera import RealCameraSensor


class BaseMonitoringSystem:
    """
    Base class for monitoring systems.
    
    Provides common functionality:
    - Configuration loading
    - Logger initialization
    - Sensor initialization (camera)
    - Alert channel setup
    - Signal handling
    - Main loop framework
    """
    
    def __init__(self, config_path: str, project_name: str):
        """
        Initialize the base monitoring system.
        
        Args:
            config_path: Path to configuration file
            project_name: Name of the project (for display)
        """
        self.project_name = project_name
        self.config_path = config_path
        self.config: Optional[Dict[str, Any]] = None
        self.logger: Optional[AlertLogger] = None
        self.sensors: Dict[str, Any] = {}
        self.alert_channels: Dict[str, Any] = {}
        self.running = False
        self.use_mock = True
        
        # Setup signal handlers
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
    
    def initialize(self):
        """Initialize all components. Override in subclasses for project-specific init."""
        print("=" * 60)
        print(f"{self.project_name}")
        print("=" * 60)
        
        # Load configuration
        print(f"\n[1/5] Loading configuration from {self.config_path}...")
        try:
            self.config = load_config(self.config_path)
            is_valid, errors = validate_config(self.config)
            if not is_valid:
                print("Configuration errors:")
                for error in errors:
                    print(f"  - {error}")
                sys.exit(1)
            print("✓ Configuration loaded")
        except Exception as e:
            print(f"✗ Failed to load configuration: {e}")
            sys.exit(1)
        
        # Initialize logger
        print("\n[2/5] Initializing logger...")
        try:
            self.logger = AlertLogger(self.config.get('logging', {}))
            self.logger.info(f"{self.project_name} starting up")
            print("✓ Logger initialized")
        except Exception as e:
            print(f"✗ Failed to initialize logger: {e}")
            sys.exit(1)
        
        # Initialize sensors
        print("\n[3/5] Initializing sensors...")
        try:
            self._initialize_sensors()
            print(f"✓ Sensors initialized ({len(self.sensors)} sensor(s))")
        except Exception as e:
            self.logger.error(f"Failed to initialize sensors: {e}")
            print(f"✗ Failed to initialize sensors: {e}")
            sys.exit(1)
        
        # Initialize alert channels
        print("\n[4/5] Initializing alert channels...")
        try:
            self._initialize_alert_channels()
            print(f"✓ Alert system initialized ({len(self.alert_channels)} channel(s))")
        except Exception as e:
            self.logger.error(f"Failed to initialize alerts: {e}")
            print(f"✗ Failed to initialize alerts: {e}")
            sys.exit(1)
        
        # Project-specific initialization
        print("\n[5/5] Project-specific initialization...")
        try:
            self.initialize_project()
            print("✓ Project initialized")
        except Exception as e:
            self.logger.error(f"Failed project initialization: {e}")
            print(f"✗ Failed project initialization: {e}")
            sys.exit(1)
        
        print("\n" + "=" * 60)
        print("System initialized successfully!")
        print(f"Mode: {'MOCK SENSORS' if self.use_mock else 'REAL SENSORS'}")
        print("=" * 60 + "\n")
    
    def _initialize_sensors(self):
        """Initialize camera sensor."""
        sensors_config = self.config.get('sensors', {})
        self.use_mock = self.config.get('system', {}).get('use_mock_sensors', True)
        
        if self.use_mock:
            # Use mock camera
            if sensors_config.get('camera', {}).get('enabled', True):
                camera_config = sensors_config.get('camera', {})
                camera_config['simulation_mode'] = 'normal'
                self.sensors['Camera'] = MockCameraSensor(camera_config)
                if self.sensors['Camera'].initialize():
                    self.logger.info("Mock Camera sensor initialized")
        else:
            # Use real camera
            if sensors_config.get('camera', {}).get('enabled', True):
                self.sensors['Camera'] = RealCameraSensor(sensors_config.get('camera', {}))
                if self.sensors['Camera'].initialize():
                    self.logger.info("Real Camera sensor initialized")
        
        if not self.sensors:
            raise ValueError("No sensors enabled or initialized")
    
    def _initialize_alert_channels(self):
        """Initialize alert channels."""
        alerts_config = self.config.get('alerts', {})
        
        # Email alerts
        if alerts_config.get('email', {}).get('enabled', False):
            try:
                email_alert = EmailAlert(alerts_config.get('email', {}), self.logger)
                if email_alert.is_enabled():
                    self.alert_channels['email'] = email_alert
                    self.logger.info("Email alert channel enabled")
            except Exception as e:
                self.logger.warning(f"Email alerts not available: {e}")
        
        # SMS alerts
        if alerts_config.get('sms', {}).get('enabled', False):
            try:
                sms_alert = SMSAlert(alerts_config.get('sms', {}), self.logger)
                if sms_alert.is_enabled():
                    self.alert_channels['sms'] = sms_alert
                    self.logger.info("SMS alert channel enabled")
            except Exception as e:
                self.logger.warning(f"SMS alerts not available: {e}")
        
        # API alerts
        if alerts_config.get('api', {}).get('enabled', False):
            try:
                api_alert = APIAlert(alerts_config.get('api', {}), self.logger)
                if api_alert.is_enabled():
                    self.alert_channels['api'] = api_alert
                    self.logger.info("API alert channel enabled")
            except Exception as e:
                self.logger.warning(f"API alerts not available: {e}")
        
        # Webhook alerts (Discord, Telegram, Slack, custom)
        if alerts_config.get('webhook', {}).get('enabled', False):
            try:
                webhook_alert = WebhookAlert(alerts_config.get('webhook', {}), self.logger)
                if webhook_alert.is_enabled():
                    self.alert_channels['webhook'] = webhook_alert
                    self.logger.info("Webhook alert channel enabled")
            except Exception as e:
                self.logger.warning(f"Webhook alerts not available: {e}")
    
    def initialize_project(self):
        """
        Project-specific initialization.
        Override in subclasses.
        """
        pass
    
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals."""
        self.logger.info(f"Received signal {signum}, shutting down gracefully...")
        self.running = False
    
    def run_cycle(self):
        """
        Run one monitoring cycle.
        Override in subclasses with project-specific logic.
        """
        raise NotImplementedError("Subclasses must implement run_cycle()")
    
    def run(self):
        """Main monitoring loop."""
        self.running = True
        self.logger.info("Starting monitoring loop")
        
        # Get check interval
        check_interval = min(
            sensor.check_interval 
            for sensor in self.sensors.values() 
            if sensor.enabled
        )
        
        print(f"\nMonitoring started (check interval: {check_interval} seconds)")
        print("Press Ctrl+C to stop\n")
        
        cycle_count = 0
        
        try:
            while self.running:
                cycle_start = time.time()
                cycle_count += 1
                
                # Run monitoring cycle
                result = self.run_cycle()
                
                # Print status periodically (override in subclass for custom display)
                if cycle_count % 10 == 0:
                    self._print_status(result)
                
                # Calculate sleep time
                cycle_duration = time.time() - cycle_start
                sleep_time = max(0, check_interval - cycle_duration)
                
                if sleep_time > 0:
                    time.sleep(sleep_time)
                else:
                    self.logger.warning(f"Cycle took {cycle_duration:.2f}s, longer than interval {check_interval}s")
        
        except KeyboardInterrupt:
            self.logger.info("Interrupted by user")
        finally:
            self.shutdown()
    
    def _print_status(self, result: Dict[str, Any]):
        """Print status. Override in subclasses for custom display."""
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Status: {result}")
    
    def shutdown(self):
        """Gracefully shutdown the system."""
        self.logger.info("Shutting down monitoring system...")
        
        # Cleanup sensors
        for sensor_name, sensor in self.sensors.items():
            try:
                sensor.cleanup()
                self.logger.info(f"{sensor_name} sensor cleaned up")
            except Exception as e:
                self.logger.error(f"Error cleaning up {sensor_name}: {e}")
        
        # Project-specific cleanup
        self.shutdown_project()
        
        self.logger.info("Shutdown complete")
    
    def shutdown_project(self):
        """
        Project-specific cleanup.
        Override in subclasses.
        """
        pass
