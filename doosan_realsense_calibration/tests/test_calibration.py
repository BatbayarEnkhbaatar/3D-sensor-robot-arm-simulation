"""
Unit tests for the eye-in-hand calibration validation module.

Run with:
    cd doosan_realsense_calibration
    python -m pytest tests/ -v

or from the repo root:
    python -m pytest doosan_realsense_calibration/tests/ -v
"""

import json
import math
import os
import sys
import tempfile
import unittest

import numpy as np

# Make the calibration package importable from the test file
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from calibration.eye_in_hand_calibration import (
    apply_calibration_matrix,
    euler_to_rotation_matrix,
    homogeneous_from_pose,
    load_pose_pairs,
    pose_from_homogeneous,
    quaternion_to_rotation_matrix,
    rotation_error,
    rotation_matrix_to_euler,
    rotation_matrix_to_quaternion,
    translation_error,
    validate_calibration,
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _identity() -> np.ndarray:
    return np.eye(4, dtype=np.float64)


def _make_pose(x=0.0, y=0.0, z=0.0, rx=0.0, ry=0.0, rz=0.0) -> np.ndarray:
    return homogeneous_from_pose(
        np.array([x, y, z]),
        euler_to_rotation_matrix(rx, ry, rz),
    )


# ---------------------------------------------------------------------------
# Test: homogeneous_from_pose / pose_from_homogeneous
# ---------------------------------------------------------------------------

class TestHomogeneousConversions(unittest.TestCase):

    def test_identity_round_trip(self):
        """Building and decomposing an identity matrix returns zeros."""
        T = homogeneous_from_pose(np.zeros(3), np.eye(3))
        np.testing.assert_array_almost_equal(T, np.eye(4))
        t, R = pose_from_homogeneous(T)
        np.testing.assert_array_almost_equal(t, np.zeros(3))
        np.testing.assert_array_almost_equal(R, np.eye(3))

    def test_translation_stored_correctly(self):
        t_in = np.array([0.1, -0.2, 0.3])
        T = homogeneous_from_pose(t_in, np.eye(3))
        t_out, _ = pose_from_homogeneous(T)
        np.testing.assert_array_almost_equal(t_in, t_out)

    def test_rotation_stored_correctly(self):
        R_in = euler_to_rotation_matrix(10.0, 20.0, 30.0)
        T = homogeneous_from_pose(np.zeros(3), R_in)
        _, R_out = pose_from_homogeneous(T)
        np.testing.assert_array_almost_equal(R_in, R_out)

    def test_bottom_row_is_0001(self):
        T = homogeneous_from_pose(np.array([1.0, 2.0, 3.0]), np.eye(3))
        np.testing.assert_array_equal(T[3, :], [0, 0, 0, 1])


# ---------------------------------------------------------------------------
# Test: quaternion_to_rotation_matrix / rotation_matrix_to_quaternion
# ---------------------------------------------------------------------------

class TestQuaternionConversions(unittest.TestCase):

    def test_identity_quaternion(self):
        """[0, 0, 0, 1] → identity rotation matrix."""
        R = quaternion_to_rotation_matrix([0, 0, 0, 1])
        np.testing.assert_array_almost_equal(R, np.eye(3))

    def test_90_deg_z(self):
        """90° about Z: q = [0, 0, sin45, cos45]."""
        angle = math.pi / 2
        q = [0, 0, math.sin(angle / 2), math.cos(angle / 2)]
        R = quaternion_to_rotation_matrix(q)
        expected = euler_to_rotation_matrix(0, 0, 90)
        np.testing.assert_array_almost_equal(R, expected, decimal=6)

    def test_round_trip(self):
        """R → q → R is idempotent."""
        R_in = euler_to_rotation_matrix(15.0, -25.0, 40.0)
        q = rotation_matrix_to_quaternion(R_in)
        R_out = quaternion_to_rotation_matrix(q)
        np.testing.assert_array_almost_equal(R_in, R_out, decimal=10)

    def test_unit_norm(self):
        """Output quaternion is always unit norm."""
        R = euler_to_rotation_matrix(30.0, 60.0, 90.0)
        q = rotation_matrix_to_quaternion(R)
        self.assertAlmostEqual(np.linalg.norm(q), 1.0, places=12)

    def test_zero_norm_raises(self):
        with self.assertRaises(ValueError):
            quaternion_to_rotation_matrix([0, 0, 0, 0])


# ---------------------------------------------------------------------------
# Test: euler_to_rotation_matrix / rotation_matrix_to_euler
# ---------------------------------------------------------------------------

class TestEulerConversions(unittest.TestCase):

    def test_zero_angles(self):
        R = euler_to_rotation_matrix(0, 0, 0)
        np.testing.assert_array_almost_equal(R, np.eye(3))

    def test_90_deg_x(self):
        R = euler_to_rotation_matrix(90, 0, 0)
        expected = np.array([[1, 0, 0],
                              [0, 0, -1],
                              [0, 1,  0]], dtype=np.float64)
        np.testing.assert_array_almost_equal(R, expected, decimal=10)

    def test_round_trip(self):
        """Euler → R → Euler is idempotent (avoiding gimbal-lock angles)."""
        for angles in [(10, 20, 30), (-15, 5, -45), (5, -10, 60)]:
            R = euler_to_rotation_matrix(*angles)
            rx, ry, rz = rotation_matrix_to_euler(R)
            R_back = euler_to_rotation_matrix(rx, ry, rz)
            np.testing.assert_array_almost_equal(R, R_back, decimal=10,
                                                  err_msg=f"Failed for angles {angles}")

    def test_orthogonality(self):
        """Output rotation matrix must be orthogonal with det=+1."""
        R = euler_to_rotation_matrix(12.3, -34.5, 56.7)
        np.testing.assert_array_almost_equal(R @ R.T, np.eye(3), decimal=12)
        self.assertAlmostEqual(float(np.linalg.det(R)), 1.0, places=12)


# ---------------------------------------------------------------------------
# Test: apply_calibration_matrix
# ---------------------------------------------------------------------------

class TestApplyCalibrationMatrix(unittest.TestCase):

    def test_all_identity(self):
        """Identity matrices → identity result."""
        T = apply_calibration_matrix(_identity(), _identity(), _identity())
        np.testing.assert_array_almost_equal(T, _identity())

    def test_translation_chain(self):
        """Pure translation: T_base_target = T_base_ee + T_ee_cam + T_cam_target."""
        T_base_ee    = _make_pose(x=0.5)
        T_ee_cam     = _make_pose(y=0.1)
        T_cam_target = _make_pose(z=0.2)
        T_result = apply_calibration_matrix(T_base_ee, T_ee_cam, T_cam_target)
        expected = _make_pose(x=0.5, y=0.1, z=0.2)
        np.testing.assert_array_almost_equal(T_result, expected)

    def test_inverse_undoes_transform(self):
        """Applying then inverting the calibration matrix recovers the original pose."""
        T_base_ee    = _make_pose(x=0.4, y=-0.1, z=0.3, rz=15.0)
        T_ee_cam     = _make_pose(x=0.0, y=0.05, z=0.1, rx=-15.0)
        T_cam_target = _make_pose(x=0.05, z=-0.3, ry=5.0)

        T_pred = apply_calibration_matrix(T_base_ee, T_ee_cam, T_cam_target)

        # Recover T_cam_target from T_pred
        T_cam_target_recovered = (
            np.linalg.inv(T_ee_cam) @ np.linalg.inv(T_base_ee) @ T_pred
        )
        np.testing.assert_array_almost_equal(T_cam_target, T_cam_target_recovered,
                                             decimal=10)

    def test_representative_sample(self):
        """Representative sample: Doosan pose + D405 offset + target seen at 50 cm."""
        # End-effector at (0.4, 0.0, 0.5) with 30° yaw
        T_base_ee = _make_pose(x=0.4, z=0.5, rz=30.0)
        # Camera 10 cm forward of EE, 15° pitched down
        T_ee_cam  = _make_pose(z=0.10, rx=-15.0)
        # Target 40 cm in front of camera
        T_cam_target = _make_pose(z=0.40)

        T_result = apply_calibration_matrix(T_base_ee, T_ee_cam, T_cam_target)

        # Result must be a valid homogeneous matrix
        np.testing.assert_array_almost_equal(T_result[3, :], [0, 0, 0, 1])
        self.assertAlmostEqual(float(np.linalg.det(T_result[:3, :3])), 1.0, places=10)


# ---------------------------------------------------------------------------
# Test: translation_error / rotation_error
# ---------------------------------------------------------------------------

class TestErrorMetrics(unittest.TestCase):

    def test_zero_error_same_matrix(self):
        T = _make_pose(x=0.5, y=0.1, rx=10.0)
        self.assertAlmostEqual(translation_error(T, T), 0.0, places=12)
        self.assertAlmostEqual(rotation_error(T, T),     0.0, places=10)

    def test_translation_error_known_value(self):
        T1 = _make_pose(x=0.0)
        T2 = _make_pose(x=0.3)
        self.assertAlmostEqual(translation_error(T1, T2), 0.3, places=10)

    def test_rotation_error_90_degrees(self):
        T1 = _make_pose(rz=0.0)
        T2 = _make_pose(rz=90.0)
        self.assertAlmostEqual(rotation_error(T1, T2), 90.0, places=8)

    def test_rotation_error_180_degrees(self):
        T1 = _make_pose(rz=0.0)
        T2 = _make_pose(rz=180.0)
        self.assertAlmostEqual(rotation_error(T1, T2), 180.0, places=6)

    def test_symmetry(self):
        """error(A, B) == error(B, A)."""
        T1 = _make_pose(x=0.1, rx=10.0)
        T2 = _make_pose(x=0.3, rx=-5.0)
        self.assertAlmostEqual(translation_error(T1, T2), translation_error(T2, T1))
        self.assertAlmostEqual(rotation_error(T1, T2),    rotation_error(T2, T1), places=10)


# ---------------------------------------------------------------------------
# Test: validate_calibration
# ---------------------------------------------------------------------------

class TestValidateCalibration(unittest.TestCase):

    def _make_pairs(self, n=5, noise_sigma_t=0.0, noise_sigma_r=0.0):
        """Create n synthetic pose pairs with optional noise."""
        T_ee_cam = _make_pose(z=0.10, rx=-15.0)
        T_base_target = _make_pose(x=0.55, y=0.05, z=0.25)

        rng = np.random.default_rng(0)
        pairs = []
        for _ in range(n):
            x  = rng.uniform(0.3, 0.7)
            y  = rng.uniform(-0.3, 0.3)
            z  = rng.uniform(0.3, 0.65)
            rx = rng.uniform(-20, 20)
            ry = rng.uniform(-20, 20)
            rz = rng.uniform(-30, 30)
            T_base_ee = _make_pose(x=x, y=y, z=z, rx=rx, ry=ry, rz=rz)
            T_cam_target = (
                np.linalg.inv(T_ee_cam) @ np.linalg.inv(T_base_ee) @ T_base_target
            )
            if noise_sigma_t > 0:
                T_cam_target[:3, 3] += rng.normal(0, noise_sigma_t, 3)
            pairs.append({"id": _ + 1, "T_base_ee": T_base_ee,
                          "T_cam_target": T_cam_target})
        return pairs, T_ee_cam, T_base_target

    def test_perfect_calibration_zero_error(self):
        """With exact T_ee_cam and no noise, all errors should be ~0."""
        pairs, T_ee_cam, T_base_target = self._make_pairs(n=10, noise_sigma_t=0.0)
        result = validate_calibration(pairs, T_ee_cam, T_base_target_gt=T_base_target)
        self.assertAlmostEqual(result["mean_translation_error_m"], 0.0, places=10)
        self.assertAlmostEqual(result["mean_rotation_error_deg"],  0.0, places=8)
        self.assertEqual(result["num_pairs"], 10)

    def test_wrong_matrix_produces_nonzero_error(self):
        """Using a wrong T_ee_cam must yield non-trivial errors."""
        pairs, T_ee_cam, T_base_target = self._make_pairs(n=10)
        T_wrong = _make_pose(z=0.15, rx=-10.0)   # deliberately wrong
        result = validate_calibration(pairs, T_wrong, T_base_target_gt=T_base_target)
        self.assertGreater(result["mean_translation_error_m"], 0.01)

    def test_with_noise_consensus_mode(self):
        """With small noise, consensus-mode mean translation error stays low."""
        pairs, T_ee_cam, _ = self._make_pairs(n=40, noise_sigma_t=0.002)
        result = validate_calibration(pairs, T_ee_cam)   # no GT → consensus mode
        # 2 mm noise per measurement → mean error should be well below 10 mm
        self.assertLess(result["mean_translation_error_m"], 0.010)

    def test_per_pair_errors_count(self):
        """per_pair_errors must have the same length as input pose_pairs."""
        pairs, T_ee_cam, _ = self._make_pairs(n=7)
        result = validate_calibration(pairs, T_ee_cam)
        self.assertEqual(len(result["per_pair_errors"]), 7)

    def test_summary_statistics_consistent(self):
        """max error must be >= mean error and >= std."""
        pairs, T_ee_cam, _ = self._make_pairs(n=40, noise_sigma_t=0.003)
        result = validate_calibration(pairs, T_ee_cam)
        self.assertGreaterEqual(result["max_translation_error_m"],
                                result["mean_translation_error_m"])
        self.assertGreaterEqual(result["max_rotation_error_deg"],
                                result["mean_rotation_error_deg"])


# ---------------------------------------------------------------------------
# Test: load_pose_pairs
# ---------------------------------------------------------------------------

class TestLoadPosePairs(unittest.TestCase):

    def _write_tmp_json(self, n=3) -> str:
        """Write a minimal valid pose-pairs JSON to a temp file, return path."""
        T = np.eye(4).tolist()
        data = {
            "description": "unit test",
            "T_ee_cam": T,
            "pose_pairs": [{"id": i, "T_base_ee": T, "T_cam_target": T}
                           for i in range(n)],
        }
        fd, path = tempfile.mkstemp(suffix=".json")
        with os.fdopen(fd, "w") as fh:
            json.dump(data, fh)
        return path

    def test_loads_successfully(self):
        path = self._write_tmp_json(n=3)
        result = load_pose_pairs(path)
        self.assertEqual(len(result["pose_pairs"]), 3)
        self.assertEqual(result["T_ee_cam"].shape, (4, 4))
        os.unlink(path)

    def test_matrices_are_numpy(self):
        path = self._write_tmp_json(n=2)
        result = load_pose_pairs(path)
        for pair in result["pose_pairs"]:
            self.assertIsInstance(pair["T_base_ee"],    np.ndarray)
            self.assertIsInstance(pair["T_cam_target"], np.ndarray)
        os.unlink(path)

    def test_missing_file_raises(self):
        with self.assertRaises(FileNotFoundError):
            load_pose_pairs("/tmp/nonexistent_does_not_exist_xyz.json")

    def test_load_sample_poses_json(self):
        """The shipped sample_poses.json must load without errors."""
        sample_path = os.path.join(
            os.path.dirname(__file__), "..", "data", "sample_poses.json"
        )
        if not os.path.exists(sample_path):
            self.skipTest("sample_poses.json not found — run generate_sample_poses.py first")
        result = load_pose_pairs(sample_path)
        self.assertEqual(result["T_ee_cam"].shape, (4, 4))
        self.assertEqual(len(result["pose_pairs"]), 40)


# ---------------------------------------------------------------------------
# Integration scenario: full workflow
# ---------------------------------------------------------------------------

class TestFullCalibrationWorkflow(unittest.TestCase):
    """End-to-end integration test using representative Doosan + D405 geometry."""

    def test_representative_doosan_d405_scenario(self):
        """
        Simulate a realistic 40-pair collection:
        - Doosan arm in various poses looking at a fixed ArUco board
        - RealSense D405 mounted 10 cm forward, 5 cm side, 15° pitch down
        - Target board at (0.55, 0.05, 0.25) m from Doosan base
        - 2 mm / 0.3° Gaussian noise on camera measurements
        """
        # Ground-truth calibration
        T_ee_cam_gt = _make_pose(y=0.05, z=0.10, rx=-15.0)
        T_base_target_gt = _make_pose(x=0.55, y=0.05, z=0.25)

        rng = np.random.default_rng(99)
        pairs = []
        for i in range(40):
            x  = rng.uniform(0.30, 0.70)
            y  = rng.uniform(-0.30, 0.30)
            z  = rng.uniform(0.30, 0.65)
            rx = rng.uniform(-20, 20)
            ry = rng.uniform(-20, 20)
            rz = rng.uniform(-30, 30)
            T_base_ee = _make_pose(x=x, y=y, z=z, rx=rx, ry=ry, rz=rz)
            T_cam_target_exact = (
                np.linalg.inv(T_ee_cam_gt)
                @ np.linalg.inv(T_base_ee)
                @ T_base_target_gt
            )
            # Add sensor noise
            T_cam_target = T_cam_target_exact.copy()
            T_cam_target[:3, 3] += rng.normal(0, 0.002, 3)
            pairs.append({"id": i + 1, "T_base_ee": T_base_ee,
                          "T_cam_target": T_cam_target})

        result = validate_calibration(pairs, T_ee_cam_gt,
                                      T_base_target_gt=T_base_target_gt)

        # With 2 mm measurement noise, the mean error must be small
        self.assertLess(result["mean_translation_error_m"], 0.005,
                        "Mean translation error exceeds 5 mm — calibration looks bad")
        self.assertLess(result["mean_rotation_error_deg"], 1.0,
                        "Mean rotation error exceeds 1° — calibration looks bad")
        self.assertEqual(result["num_pairs"], 40)

        # Reference translation should be close to the ground truth
        ref_t = np.array(result["reference_translation"])
        gt_t  = T_base_target_gt[:3, 3]
        self.assertLess(float(np.linalg.norm(ref_t - gt_t)), 0.005)


if __name__ == "__main__":
    unittest.main(verbosity=2)
