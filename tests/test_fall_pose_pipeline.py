"""
Tests for pose inference backends and FallDetector integration (no Pi required).
"""

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from fall_detection.detection.fall_detector import FallDetector, FallStatus
from fall_detection.detection.pose_analyzer import PoseAnalyzer
from shared.inference.mock_pose import MockPoseBackend


def _camera_person():
    return {
        'person_detected': True,
        'motion_detected': True,
        'motion_level': 0.4,
        'person_confidence': 0.9,
    }


class TestMockPoseBackend(unittest.TestCase):
    def test_none_scenario(self):
        b = MockPoseBackend({'scenario': 'none'})
        r = b.infer()
        self.assertFalse(r['pose_detected'])

    def test_fall_sequence(self):
        b = MockPoseBackend({'scenario': 'fall_sequence', 'fall_sequence_standing_frames': 2})
        b.reset_sequence()
        self.assertEqual(b.infer()['position'], 'standing')
        self.assertEqual(b.infer()['position'], 'standing')
        self.assertEqual(b.infer()['position'], 'lying')


class TestFallDetectorPose(unittest.TestCase):
    def setUp(self):
        self.base_config = {
            'detection': {
                'fall_confirmation_time': 0,
                'prefer_pose_when_available': True,
                'pose_estimation_enabled': False,
            },
        }

    def test_pose_overrides_motion_when_enabled(self):
        cfg = {
            'detection': {
                **self.base_config['detection'],
                'fall_confirmation_time': 10,
                'prefer_pose_when_available': True,
            },
            'inference': {'backend': 'mock', 'mock': {'scenario': 'standing'}},
        }
        cfg_pose_on = {**cfg, 'detection': {**cfg['detection'], 'pose_estimation_enabled': True}}
        pa = PoseAnalyzer(cfg_pose_on)
        fd = FallDetector(cfg)
        cam = _camera_person()
        cam['motion_level'] = 0.9
        pose_standing = pa.analyze_pose(camera_data=cam)
        self.assertEqual(pose_standing['position'], 'standing')
        fd.analyze_frame(cam, pose_standing)
        cfg_lying = {**cfg_pose_on, 'inference': {'backend': 'mock', 'mock': {'scenario': 'lying'}}}
        pa_ly = PoseAnalyzer(cfg_lying)
        pose_lying = pa_ly.analyze_pose(camera_data=cam)
        self.assertEqual(pose_lying['position'], 'lying')
        st = fd.analyze_frame(cam, pose_lying)
        self.assertEqual(st, FallStatus.SUSPICIOUS)

    def test_sitting_to_lying_triggers_suspicious(self):
        cfg = {
            'detection': {
                **self.base_config['detection'],
                'fall_confirmation_time': 60,
                'prefer_pose_when_available': True,
            },
        }
        fd = FallDetector(cfg)
        cam = _camera_person()
        pose_sit = {'pose_detected': True, 'position': 'sitting', 'confidence': 0.9}
        fd.analyze_frame(cam, pose_sit)
        pose_ly = {'pose_detected': True, 'position': 'lying', 'confidence': 0.9}
        st = fd.analyze_frame(cam, pose_ly)
        self.assertEqual(st, FallStatus.SUSPICIOUS)


class TestPoseAnalyzerMockMirror(unittest.TestCase):
    def test_mirror_follows_motion(self):
        cfg = {
            'detection': {'pose_estimation_enabled': True},
            'inference': {'backend': 'mock', 'mock': {'scenario': 'mirror'}},
        }
        pa = PoseAnalyzer(cfg)
        cam = {
            'person_detected': True,
            'motion_level': 0.05,
            'person_confidence': 0.8,
        }
        pose = pa.analyze_pose(camera_data=cam)
        self.assertEqual(pose['position'], 'lying')


if __name__ == '__main__':
    unittest.main()
