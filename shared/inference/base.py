"""
Abstract pose inference interface.

Implementations: MockPoseBackend (dev/CI), HailoPoseBackend (Pi + HAT).
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

import numpy as np


def empty_pose_result() -> Dict[str, Any]:
    """Default when pose is unavailable or backend is idle."""
    return {
        'pose_detected': False,
        'position': 'unknown',
        'confidence': 0.0,
        'keypoints': [],
        'angles': {},
        'backend': 'none',
    }


class PoseInferenceBackend(ABC):
    """Runs pose estimation on a frame (or metadata) and returns a normalized dict."""

    name: str = 'base'

    @abstractmethod
    def infer(
        self,
        frame: Optional[np.ndarray] = None,
        camera_data: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Returns a dict compatible with FallDetector / PoseAnalyzer:

        - pose_detected: bool
        - position: 'standing' | 'sitting' | 'lying' | 'unknown'
        - confidence: float 0..1
        - keypoints: optional list
        - angles: optional dict
        - backend: str (identifier)
        """
        pass
