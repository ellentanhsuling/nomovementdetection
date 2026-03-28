"""
Pose Analyzer

Delegates to shared inference backends (mock for dev, Hailo stub on Pi).
"""

from typing import Any, Dict, Optional

import numpy as np

from shared.inference import create_pose_backend
from shared.inference.base import PoseInferenceBackend, empty_pose_result


class PoseAnalyzer:
    """
    Analyzes person pose/position using a pluggable backend.
    """

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        detection = config.get('detection', {})
        self.enabled = bool(detection.get('pose_estimation_enabled', False))
        self._backend: Optional[PoseInferenceBackend] = None
        if self.enabled:
            self._backend = create_pose_backend(config)

    def is_active(self) -> bool:
        return self.enabled and self._backend is not None

    def analyze_pose(
        self,
        frame: Optional[np.ndarray] = None,
        camera_data: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Run pose estimation. Pass camera_data so mock 'mirror' scenario can align with motion heuristics.
        """
        if not self.enabled or self._backend is None:
            return empty_pose_result()

        return self._backend.infer(frame=frame, camera_data=camera_data)

    def reset_mock_sequence(self) -> None:
        """If using mock fall_sequence, reset frame counter (tests)."""
        if self._backend is not None and hasattr(self._backend, 'reset_sequence'):
            self._backend.reset_sequence()

    def is_person_standing(self, pose_data: Dict[str, Any]) -> bool:
        """Check if person is standing based on pose."""
        position = pose_data.get('position', 'unknown')
        return position == 'standing'

    def is_person_lying(self, pose_data: Dict[str, Any]) -> bool:
        """Check if person is lying down based on pose."""
        position = pose_data.get('position', 'unknown')
        return position == 'lying'

    def detect_sudden_change(
        self,
        current_pose: Dict[str, Any],
        previous_pose: Dict[str, Any],
    ) -> bool:
        """Detect sudden position change (potential fall)."""
        if not previous_pose.get('pose_detected', False):
            return False

        current_pos = current_pose.get('position', 'unknown')
        previous_pos = previous_pose.get('position', 'unknown')

        if previous_pos == 'standing' and current_pos == 'lying':
            return True
        if previous_pos == 'sitting' and current_pos == 'lying':
            return True

        return False
