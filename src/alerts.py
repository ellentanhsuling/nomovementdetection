"""
Alert handlers: console (Windows/dev), GPIO/Pi HAT (Raspberry Pi).
"""
import platform
import sys


def alert_console(duration_seconds: float, message: str = "Long period of non-movement") -> None:
    """Print alert to console. Used on Windows and for development."""
    print(f"\n[{message}] No motion detected for {duration_seconds:.1f} seconds.", file=sys.stderr, flush=True)


def alert_gpio_buzzer(duration_seconds: float, gpio_pin: int = 17) -> None:
    """Trigger buzzer/LED on Pi via GPIO (e.g. Pi HAT). Only on Raspberry Pi."""
    if platform.system() != "Linux":
        alert_console(duration_seconds, "GPIO not available (not on Pi); alert")
        return
    try:
        import RPi.GPIO as GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(gpio_pin, GPIO.OUT)
        GPIO.output(gpio_pin, GPIO.HIGH)
        # Beep for 2 seconds then turn off
        import time
        time.sleep(2.0)
        GPIO.output(gpio_pin, GPIO.LOW)
        GPIO.cleanup(gpio_pin)
    except ImportError:
        alert_console(duration_seconds, "RPi.GPIO not installed; alert")
    except Exception as e:
        alert_console(duration_seconds, f"GPIO error: {e}")


def get_alert_callback(use_gpio: bool, gpio_pin: int = 17):
    """Return a callback suitable for run_detection_loop's on_stillness_alert."""
    def callback(duration: float) -> None:
        alert_console(duration)
        if use_gpio and platform.system() == "Linux":
            alert_gpio_buzzer(duration, gpio_pin)
    return callback
