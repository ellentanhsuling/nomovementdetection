"""
IVAD: Long period of non-movement detection.
Run on Windows (webcam) for development, or on Raspberry Pi 5 with camera module + Pi HAT.
"""
import argparse
import sys
import time

from .detector import DetectorConfig, run_detection_loop
from .alerts import get_alert_callback


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Detect long periods of non-movement (e.g. person down, no activity)."
    )
    parser.add_argument(
        "--stillness-seconds",
        type=float,
        default=60.0,
        help="Seconds without motion before alerting (default: 60)",
    )
    parser.add_argument(
        "--check-interval",
        type=float,
        default=1.0,
        help="How often to check for motion in seconds (default: 1)",
    )
    parser.add_argument(
        "--min-contour-area",
        type=int,
        default=500,
        help="Minimum contour area to count as motion in pixels² (default: 500)",
    )
    parser.add_argument(
        "--gpio",
        action="store_true",
        help="On Raspberry Pi: trigger GPIO (e.g. Pi HAT buzzer/LED) on alert",
    )
    parser.add_argument(
        "--gpio-pin",
        type=int,
        default=17,
        help="BCM GPIO pin for alert output (default: 17)",
    )
    parser.add_argument(
        "--test-camera",
        action="store_true",
        help="Use second camera index (e.g. 1) on Windows if you have multiple webcams",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Print status every 5s and when motion is detected (so you see the app is working)",
    )
    args = parser.parse_args()

    config = DetectorConfig(
        stillness_threshold_seconds=args.stillness_seconds,
        check_interval_seconds=args.check_interval,
        min_contour_area=args.min_contour_area,
    )
    on_alert = get_alert_callback(use_gpio=args.gpio, gpio_pin=args.gpio_pin)

    # Optional verbose status (every 5s) and motion messages
    last_status_time = [0.0]  # list so inner function can mutate

    def on_status(stillness_seconds: float) -> None:
        if not args.verbose:
            return
        now = time.monotonic()
        if now - last_status_time[0] >= 5.0:
            print(f"  No motion for {stillness_seconds:.1f}s (alert at {args.stillness_seconds}s)", flush=True)
            last_status_time[0] = time.monotonic()

    def on_motion() -> None:
        if args.verbose:
            print("  Motion detected.", flush=True)

    print(
        f"IVAD running. Camera on. Alert after {args.stillness_seconds}s of no motion. Ctrl+C to stop.",
        flush=True,
    )
    if args.verbose:
        print("Verbose: status every 5s and motion events.", flush=True)

    try:
        run_detection_loop(
            config,
            on_stillness_alert=on_alert,
            on_motion_seen=on_motion if args.verbose else None,
            on_status=on_status,
            use_test_camera=args.test_camera,
        )
    except KeyboardInterrupt:
        print("\nStopped by user.", file=sys.stderr)
        return 0
    except RuntimeError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
