"""
Hailo NPU pose backend — stub until HailoRT is integrated on the Pi.

On Raspberry Pi 5 + AI HAT+, replace infer() with a real pipeline
(e.g. HEF + HailoRT Python API or GStreamer post-process).
"""

from __future__ import annotations

import logging
from typing import Any, Dict, Optional

import numpy as np

from shared.inference.base import PoseInferenceBackend, empty_pose_result

logger = logging.getLogger(__name__)


class HailoPoseBackend(PoseInferenceBackend):
    """
    Placeholder backend. Configure on Pi with inference.hailo.hef_path, etc.

    Until implemented, infer() returns pose_detected=False so FallDetector
    falls back to motion heuristics.
    """

    name = 'hailo'

    def __init__(self, config: Dict[str, Any]):
        self.config = config or {}
        self.hef_path = self.config.get('hef_path') or ''
        self._warned = False

    def infer(
        self,
        frame: Optional[np.ndarray] = None,
        camera_data: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        if not self._warned:
            logger.warning(
                'HailoPoseBackend is not yet wired to HailoRT — returning no pose. '
                'Implement infer() on the Pi and load your .hef model (hef_path=%s).',
                self.hef_path or '(unset)',
            )
            self._warned = True
        out = empty_pose_result()
        out['backend'] = self.name
        return out
