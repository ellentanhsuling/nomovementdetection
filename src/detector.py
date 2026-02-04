"""
Non-movement (stillness) detector for Raspberry Pi 5 + camera.
Detects long periods without motion and triggers an alert (e.g. person down, no activity).
"""
from __future__ import annotations

import time
import platform
from dataclasses import dataclass
from typing import Callable

# Optional: picamera2 only on Raspberry Pi; opencv for Windows dev / fallback
_CAMERA_BACKEND = None
if platform.system() == "Linux":
    try:
        from picamera2 import Picamera2
        _CAMERA_BACKEND = "picamera2"
    except ImportError:
        pass

if _CAMERA_BACKEND is None:
    try:
        import cv2
        _CAMERA_BACKEND = "opencv"
    except ImportError:
        pass


@dataclass
class DetectorConfig:
    """Configuration for non-movement detection."""
    # Seconds without motion before alerting
    stillness_threshold_seconds: float = 60.0
    # Motion detection sensitivity (0–1, higher = more sensitive)
    motion_threshold: float = 0.02
    # How often to check for motion (seconds)
    check_interval_seconds: float = 1.0
    # Minimum contour area to count as motion (pixels²)
    min_contour_area: int = 500


def _motion_detected_opencv(frame_prev, frame_curr, config: DetectorConfig) -> bool:
    """Detect motion between two frames using OpenCV (works on Windows and Pi)."""
    import cv2
    gray_prev = cv2.cvtColor(frame_prev, cv2.COLOR_BGR2GRAY)
    gray_curr = cv2.cvtColor(frame_curr, cv2.COLOR_BGR2GRAY)
    gray_prev = cv2.GaussianBlur(gray_prev, (21, 21), 0)
    gray_curr = cv2.GaussianBlur(gray_curr, (21, 21), 0)
    delta = cv2.absdiff(gray_prev, gray_curr)
    _, thresh = cv2.threshold(delta, 25, 255, cv2.THRESH_BINARY)
    thresh = cv2.dilate(thresh, None, iterations=2)
    contours, _ = cv2.findContours(
        thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )
    for c in contours:
        if cv2.contourArea(c) >= config.min_contour_area:
            return True
    return False


def _motion_detected_picamera2(prev_array, curr_array, config: DetectorConfig) -> bool:
    """Detect motion using raw arrays (picamera2 gives numpy arrays in various formats)."""
    import cv2
    import numpy as np
    if prev_array is None or curr_array is None:
        return False
    # picamera2 can give RGB or BGR; normalize to 2D gray
    if len(prev_array.shape) == 3:
        gray_prev = cv2.cvtColor(prev_array, cv2.COLOR_RGB2GRAY)
        gray_curr = cv2.cvtColor(curr_array, cv2.COLOR_RGB2GRAY)
    else:
        gray_prev = prev_array
        gray_curr = curr_array
    gray_prev = cv2.GaussianBlur(gray_prev.astype(np.uint8), (21, 21), 0)
    gray_curr = cv2.GaussianBlur(gray_curr.astype(np.uint8), (21, 21), 0)
    delta = cv2.absdiff(gray_prev, gray_curr)
    _, thresh = cv2.threshold(delta, 25, 255, cv2.THRESH_BINARY)
    thresh = cv2.dilate(thresh, None, iterations=2)
    contours, _ = cv2.findContours(
        thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )
    for c in contours:
        if cv2.contourArea(c) >= config.min_contour_area:
            return True
    return False


def run_detection_loop(
    config: DetectorConfig,
    on_stillness_alert: Callable[[float], None],
    on_motion_seen: Callable[[], None] | None = None,
    on_status: Callable[[float], None] | None = None,
    use_test_camera: bool = False,
) -> None:
    """
    Main loop: capture frames, detect motion, and call on_stillness_alert
    when there has been no motion for stillness_threshold_seconds.
    on_status(stillness_duration_seconds) is called each loop if set (e.g. for verbose output).
    """
    if _CAMERA_BACKEND is None:
        raise RuntimeError(
            "No camera backend available. On Raspberry Pi install picamera2; "
            "on Windows install opencv-python for webcam testing."
        )

    motion_detected = _motion_detected_opencv  # same logic for opencv frames
    prev_frame = None
    last_motion_time = time.monotonic()

    if _CAMERA_BACKEND == "picamera2":
        cam = Picamera2()
        cam.configure(cam.create_preview_configuration(main={"size": (640, 480)}))
        cam.start()

        def get_frame():
            return cam.capture_array()

        motion_detected = _motion_detected_picamera2
    else:
        import cv2
        cam = cv2.VideoCapture(0 if not use_test_camera else 1)
        if not cam.isOpened():
            raise RuntimeError("Could not open webcam. Plug in a camera or use --test.")

        def get_frame():
            ok, frame = cam.read()
            return frame if ok else None

    try:
        while True:
            frame = get_frame()
            if frame is None:
                time.sleep(config.check_interval_seconds)
                continue

            if prev_frame is not None:
                if motion_detected(prev_frame, frame, config):
                    last_motion_time = time.monotonic()
                    if on_motion_seen:
                        on_motion_seen()

            prev_frame = frame
            now = time.monotonic()
            stillness_duration = now - last_motion_time

            if stillness_duration >= config.stillness_threshold_seconds:
                on_stillness_alert(stillness_duration)
                # Reset so we don't alert every second
                last_motion_time = time.monotonic()

            if on_status is not None:
                on_status(stillness_duration)

            time.sleep(config.check_interval_seconds)
    finally:
        if _CAMERA_BACKEND == "picamera2":
            cam.stop()
        else:
            cam.release()
