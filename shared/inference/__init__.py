"""
Pose / NPU inference backends (mock, Hailo on Pi).

Fall detection and future modules can share the same interface without
importing Hailo on machines that do not have the hardware.
"""

from shared.inference.base import PoseInferenceBackend, empty_pose_result
from shared.inference.mock_pose import MockPoseBackend
from shared.inference.hailo_pose import HailoPoseBackend

__all__ = [
    'PoseInferenceBackend',
    'empty_pose_result',
    'MockPoseBackend',
    'HailoPoseBackend',
    'create_pose_backend',
]


def create_pose_backend(config: dict) -> PoseInferenceBackend:
    """
    Build a backend from the `inference` section of config.

    Args:
        config: Full application config dict.

    Returns:
        Backend instance (never None — use MockPoseBackend or a no-op).
    """
    inference = config.get('inference') or {}
    backend = (inference.get('backend') or 'none').lower()

    if backend in ('', 'none', 'off'):
        return MockPoseBackend({'scenario': 'none'})
    if backend == 'mock':
        return MockPoseBackend(inference.get('mock') or {})
    if backend == 'hailo':
        return HailoPoseBackend(inference.get('hailo') or {})
    return MockPoseBackend({'scenario': 'none'})
