"""
Mock pose backend for development without a Raspberry Pi or Hailo NPU.

Scenarios are deterministic so tests and demos can reproduce fall sequences.
"""

from __future__ import annotations

from typing import Any, Dict, Optional

import numpy as np

from shared.inference.base import PoseInferenceBackend, empty_pose_result


class MockPoseBackend(PoseInferenceBackend):
    """
    Simulated pose output.

    Config keys (under inference.mock):
      scenario: none | standing | sitting | lying | fall_sequence | mirror
      fall_sequence_standing_frames: int (default 3) — then switches to lying
    """

    name = 'mock'

    def __init__(self, config: Dict[str, Any]):
        self.config = config or {}
        self.scenario = (self.config.get('scenario') or 'none').lower()
        self._fall_standing_frames = int(self.config.get('fall_sequence_standing_frames', 3))
        self._frame_index = 0

    def infer(
        self,
        frame: Optional[np.ndarray] = None,
        camera_data: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        if self.scenario == 'none':
            return empty_pose_result()

        if self.scenario == 'mirror' and camera_data is not None:
            return self._mirror_from_camera(camera_data)

        if self.scenario == 'fall_sequence':
            self._frame_index += 1
            if self._frame_index <= self._fall_standing_frames:
                pos = 'standing'
            else:
                pos = 'lying'
            return {
                'pose_detected': True,
                'position': pos,
                'confidence': 0.95,
                'keypoints': [],
                'angles': {},
                'backend': self.name,
                'scenario': self.scenario,
            }

        position_map = {
            'standing': 'standing',
            'sitting': 'sitting',
            'lying': 'lying',
        }
        pos = position_map.get(self.scenario)
        if pos is None:
            return empty_pose_result()

        return {
            'pose_detected': True,
            'position': pos,
            'confidence': 0.9,
            'keypoints': [],
            'angles': {},
            'backend': self.name,
            'scenario': self.scenario,
        }

    def _mirror_from_camera(self, camera_data: Dict[str, Any]) -> Dict[str, Any]:
        """Approximate pose labels from existing motion heuristics (integration testing)."""
        if not camera_data.get('person_detected', False):
            return empty_pose_result()

        motion_level = float(camera_data.get('motion_level', 0.0))
        person_confidence = float(camera_data.get('person_confidence', 0.0))

        if person_confidence < 0.5:
            return {
                'pose_detected': True,
                'position': 'unknown',
                'confidence': person_confidence,
                'keypoints': [],
                'angles': {},
                'backend': self.name,
                'scenario': 'mirror',
            }

        if motion_level < 0.1 and person_confidence > 0.7:
            position = 'lying'
        elif motion_level < 0.35:
            position = 'sitting'
        else:
            position = 'standing'

        return {
            'pose_detected': True,
            'position': position,
            'confidence': max(person_confidence, 0.75),
            'keypoints': [],
            'angles': {},
            'backend': self.name,
            'scenario': 'mirror',
        }

    def reset_sequence(self) -> None:
        """Reset fall_sequence counter (e.g. between tests)."""
        self._frame_index = 0
