"""
Eye-in-hand calibration validation module for Doosan robot arm + RealSense D405.

Eye-in-hand setup: the RealSense D405 camera is rigidly mounted on the Doosan
robot's end-effector (flange). Calibration solves for T_ee_cam — the fixed
homogeneous transformation from the end-effector (EE) frame to the camera frame.

Calibration equation:
    T_base_target = T_base_ee  @  T_ee_cam  @  T_cam_target

where:
    T_base_ee     — end-effector pose in robot base frame  (measured by Doosan)
    T_ee_cam      — EE-to-camera transform  (the calibration result)
    T_cam_target  — target pose in camera frame  (measured by RealSense D405)
    T_base_target — target pose in robot base frame  (the prediction)

Validation approach:
    A calibration target (e.g. ArUco board) is placed at a fixed location.
    For each of the 40 collected pose pairs, we predict where the target is in
    the base frame and compare the predictions to their consensus, reporting
    translation (mm) and rotation (degrees) residuals.

Unit-testable public API
------------------------
load_pose_pairs             – load pose pairs from a JSON file
homogeneous_from_pose       – build 4×4 matrix from translation + rotation matrix
pose_from_homogeneous       – extract translation + rotation matrix from 4×4 matrix
quaternion_to_rotation_matrix
rotation_matrix_to_quaternion
euler_to_rotation_matrix    – ZYX Euler angles (rx, ry, rz) → 3×3 R
rotation_matrix_to_euler    – 3×3 R → ZYX Euler angles (rx, ry, rz) in degrees
apply_calibration_matrix    – T_base_target = T_base_ee @ T_ee_cam @ T_cam_target
translation_error           – Euclidean distance between two poses (metres)
rotation_error              – angular difference between two poses (degrees)
validate_calibration        – full validation over a list of pose pairs
"""

import json
import math
from typing import Dict, List, Optional, Tuple

import numpy as np


# ---------------------------------------------------------------------------
# Pose representation helpers
# ---------------------------------------------------------------------------

def homogeneous_from_pose(
    translation: np.ndarray,
    rotation_matrix: np.ndarray,
) -> np.ndarray:
    """Return a 4×4 homogeneous transformation matrix.

    Args:
        translation: (3,) array — [x, y, z] in metres.
        rotation_matrix: (3, 3) rotation matrix.

    Returns:
        (4, 4) numpy float64 array.
    """
    T = np.eye(4, dtype=np.float64)
    T[:3, :3] = np.asarray(rotation_matrix, dtype=np.float64)
    T[:3, 3] = np.asarray(translation, dtype=np.float64)
    return T


def pose_from_homogeneous(
    T: np.ndarray,
) -> Tuple[np.ndarray, np.ndarray]:
    """Extract translation and rotation matrix from a 4×4 homogeneous matrix.

    Args:
        T: (4, 4) homogeneous transformation matrix.

    Returns:
        (translation, rotation_matrix) — shapes (3,) and (3, 3).
    """
    T = np.asarray(T, dtype=np.float64)
    return T[:3, 3].copy(), T[:3, :3].copy()


def quaternion_to_rotation_matrix(q: np.ndarray) -> np.ndarray:
    """Convert a unit quaternion [qx, qy, qz, qw] to a 3×3 rotation matrix.

    Args:
        q: (4,) array [qx, qy, qz, qw].

    Returns:
        (3, 3) rotation matrix.
    """
    q = np.asarray(q, dtype=np.float64)
    norm = np.linalg.norm(q)
    if norm < 1e-10:
        raise ValueError("Quaternion norm is zero — cannot normalise.")
    q = q / norm
    qx, qy, qz, qw = q
    R = np.array([
        [1 - 2 * (qy**2 + qz**2),     2 * (qx * qy - qz * qw), 2 * (qx * qz + qy * qw)],
        [    2 * (qx * qy + qz * qw), 1 - 2 * (qx**2 + qz**2), 2 * (qy * qz - qx * qw)],
        [    2 * (qx * qz - qy * qw),     2 * (qy * qz + qx * qw), 1 - 2 * (qx**2 + qy**2)],
    ], dtype=np.float64)
    return R


def rotation_matrix_to_quaternion(R: np.ndarray) -> np.ndarray:
    """Convert a 3×3 rotation matrix to a unit quaternion [qx, qy, qz, qw].

    Uses the numerically stable Shepperd method.

    Args:
        R: (3, 3) rotation matrix.

    Returns:
        (4,) array [qx, qy, qz, qw] — unit quaternion.
    """
    R = np.asarray(R, dtype=np.float64)
    trace = R[0, 0] + R[1, 1] + R[2, 2]
    if trace > 0:
        s = 0.5 / math.sqrt(trace + 1.0)
        qw = 0.25 / s
        qx = (R[2, 1] - R[1, 2]) * s
        qy = (R[0, 2] - R[2, 0]) * s
        qz = (R[1, 0] - R[0, 1]) * s
    elif R[0, 0] > R[1, 1] and R[0, 0] > R[2, 2]:
        s = 2.0 * math.sqrt(1.0 + R[0, 0] - R[1, 1] - R[2, 2])
        qw = (R[2, 1] - R[1, 2]) / s
        qx = 0.25 * s
        qy = (R[0, 1] + R[1, 0]) / s
        qz = (R[0, 2] + R[2, 0]) / s
    elif R[1, 1] > R[2, 2]:
        s = 2.0 * math.sqrt(1.0 + R[1, 1] - R[0, 0] - R[2, 2])
        qw = (R[0, 2] - R[2, 0]) / s
        qx = (R[0, 1] + R[1, 0]) / s
        qy = 0.25 * s
        qz = (R[1, 2] + R[2, 1]) / s
    else:
        s = 2.0 * math.sqrt(1.0 + R[2, 2] - R[0, 0] - R[1, 1])
        qw = (R[1, 0] - R[0, 1]) / s
        qx = (R[0, 2] + R[2, 0]) / s
        qy = (R[1, 2] + R[2, 1]) / s
        qz = 0.25 * s
    q = np.array([qx, qy, qz, qw], dtype=np.float64)
    return q / np.linalg.norm(q)


def euler_to_rotation_matrix(rx_deg: float, ry_deg: float, rz_deg: float) -> np.ndarray:
    """Convert intrinsic ZYX Euler angles (roll=rx, pitch=ry, yaw=rz) to a 3×3 matrix.

    Convention matches ROS / Doosan API: the rotation is applied as Rz @ Ry @ Rx.

    Args:
        rx_deg: Roll  (rotation about X) in degrees.
        ry_deg: Pitch (rotation about Y) in degrees.
        rz_deg: Yaw   (rotation about Z) in degrees.

    Returns:
        (3, 3) rotation matrix.
    """
    rx = math.radians(rx_deg)
    ry = math.radians(ry_deg)
    rz = math.radians(rz_deg)

    Rx = np.array([
        [1,          0,           0],
        [0,  math.cos(rx), -math.sin(rx)],
        [0,  math.sin(rx),  math.cos(rx)],
    ], dtype=np.float64)
    Ry = np.array([
        [ math.cos(ry), 0, math.sin(ry)],
        [0,             1,            0],
        [-math.sin(ry), 0, math.cos(ry)],
    ], dtype=np.float64)
    Rz = np.array([
        [math.cos(rz), -math.sin(rz), 0],
        [math.sin(rz),  math.cos(rz), 0],
        [0,             0,            1],
    ], dtype=np.float64)
    return Rz @ Ry @ Rx


def rotation_matrix_to_euler(R: np.ndarray) -> Tuple[float, float, float]:
    """Convert a 3×3 rotation matrix to intrinsic ZYX Euler angles in degrees.

    Returns:
        (rx_deg, ry_deg, rz_deg) — roll, pitch, yaw in degrees.
    """
    R = np.asarray(R, dtype=np.float64)
    # Clamp for numerical safety
    sy = math.sqrt(R[0, 0] ** 2 + R[1, 0] ** 2)
    singular = sy < 1e-6
    if not singular:
        rx = math.atan2( R[2, 1], R[2, 2])
        ry = math.atan2(-R[2, 0], sy)
        rz = math.atan2( R[1, 0], R[0, 0])
    else:
        rx = math.atan2(-R[1, 2], R[1, 1])
        ry = math.atan2(-R[2, 0], sy)
        rz = 0.0
    return math.degrees(rx), math.degrees(ry), math.degrees(rz)


# ---------------------------------------------------------------------------
# Data I/O
# ---------------------------------------------------------------------------

def load_pose_pairs(filepath: str) -> Dict:
    """Load collected calibration pose pairs from a JSON file.

    Expected JSON structure::

        {
          "description": "...",
          "T_ee_cam": [[...], ...],       // 4×4 list-of-lists
          "pose_pairs": [
            {
              "id": 1,
              "T_base_ee":    [[...], ...],   // 4×4
              "T_cam_target": [[...], ...]    // 4×4
            },
            ...
          ]
        }

    The matrices can also be stored as flat 16-element lists; they will be
    reshaped to (4, 4) automatically.

    Args:
        filepath: Path to the JSON file.

    Returns:
        Dict with keys ``T_ee_cam`` (numpy 4×4) and ``pose_pairs`` (list of
        dicts, each containing ``T_base_ee`` and ``T_cam_target`` as numpy 4×4
        arrays).

    Raises:
        FileNotFoundError: if the file does not exist.
        KeyError: if required keys are missing from the JSON.
    """
    with open(filepath, "r", encoding="utf-8") as fh:
        raw = json.load(fh)

    def _to_mat(data):
        arr = np.asarray(data, dtype=np.float64)
        if arr.shape == (16,):
            arr = arr.reshape(4, 4)
        if arr.shape != (4, 4):
            raise ValueError(f"Expected a 4×4 matrix, got shape {arr.shape}.")
        return arr

    T_ee_cam = _to_mat(raw["T_ee_cam"])

    pose_pairs = []
    for entry in raw["pose_pairs"]:
        pose_pairs.append({
            "id": entry.get("id", None),
            "T_base_ee":    _to_mat(entry["T_base_ee"]),
            "T_cam_target": _to_mat(entry["T_cam_target"]),
        })

    return {
        "description": raw.get("description", ""),
        "T_ee_cam": T_ee_cam,
        "pose_pairs": pose_pairs,
    }


# ---------------------------------------------------------------------------
# Core calibration operations
# ---------------------------------------------------------------------------

def apply_calibration_matrix(
    T_base_ee: np.ndarray,
    T_ee_cam: np.ndarray,
    T_cam_target: np.ndarray,
) -> np.ndarray:
    """Transform a camera-frame target pose into the robot base frame.

    Applies the eye-in-hand calibration equation:
        T_base_target = T_base_ee  @  T_ee_cam  @  T_cam_target

    Args:
        T_base_ee:    (4, 4) end-effector pose in robot base frame.
        T_ee_cam:     (4, 4) calibration result — EE-to-camera transform.
        T_cam_target: (4, 4) target pose in camera frame.

    Returns:
        (4, 4) predicted target pose in robot base frame.
    """
    T_base_ee    = np.asarray(T_base_ee,    dtype=np.float64)
    T_ee_cam     = np.asarray(T_ee_cam,     dtype=np.float64)
    T_cam_target = np.asarray(T_cam_target, dtype=np.float64)
    return T_base_ee @ T_ee_cam @ T_cam_target


def translation_error(T_pred: np.ndarray, T_expected: np.ndarray) -> float:
    """Compute the Euclidean translation error between two poses in metres.

    Args:
        T_pred:     (4, 4) predicted pose.
        T_expected: (4, 4) reference / expected pose.

    Returns:
        Euclidean distance in metres (float).
    """
    t_pred     = np.asarray(T_pred,     dtype=np.float64)[:3, 3]
    t_expected = np.asarray(T_expected, dtype=np.float64)[:3, 3]
    return float(np.linalg.norm(t_pred - t_expected))


def rotation_error(T_pred: np.ndarray, T_expected: np.ndarray) -> float:
    """Compute the angular rotation error between two poses in degrees.

    Uses the geodesic distance on SO(3):
        angle = arccos( (trace(R_rel) − 1) / 2 )  where R_rel = R_expected^T @ R_pred

    Args:
        T_pred:     (4, 4) predicted pose.
        T_expected: (4, 4) reference / expected pose.

    Returns:
        Rotation error in degrees (float, range [0, 180]).
    """
    R_pred     = np.asarray(T_pred,     dtype=np.float64)[:3, :3]
    R_expected = np.asarray(T_expected, dtype=np.float64)[:3, :3]
    R_rel = R_expected.T @ R_pred
    # Clamp to [-1, 1] to guard against floating-point rounding
    cos_angle = np.clip((np.trace(R_rel) - 1.0) / 2.0, -1.0, 1.0)
    return float(math.degrees(math.acos(cos_angle)))


# ---------------------------------------------------------------------------
# Full validation workflow
# ---------------------------------------------------------------------------

def validate_calibration(
    pose_pairs: List[Dict],
    T_ee_cam: np.ndarray,
    T_base_target_gt: Optional[np.ndarray] = None,
) -> Dict:
    """Validate the eye-in-hand calibration using the collected pose pairs.

    For each pair ``(T_base_ee_i, T_cam_target_i)``, predicts the target pose
    in the robot base frame:
        T_pred_i = T_base_ee_i @ T_ee_cam @ T_cam_target_i

    If ``T_base_target_gt`` (ground-truth target pose) is provided, errors are
    computed relative to it.  Otherwise, the *consensus* (mean predicted
    translation + mean quaternion rotation) is used as the reference, which
    measures the *consistency* of the calibration.

    Args:
        pose_pairs: List of dicts, each with keys ``T_base_ee`` and
                    ``T_cam_target`` as (4, 4) numpy arrays.
        T_ee_cam:   (4, 4) calibration matrix.
        T_base_target_gt: Optional (4, 4) ground-truth target pose.

    Returns:
        Dict with keys:
            num_pairs (int)
            reference_translation ([x, y, z])
            mean_translation_error_m (float)
            std_translation_error_m (float)
            max_translation_error_m (float)
            mean_rotation_error_deg (float)
            std_rotation_error_deg (float)
            max_rotation_error_deg (float)
            per_pair_errors (list of dicts)
    """
    T_ee_cam = np.asarray(T_ee_cam, dtype=np.float64)

    # --- Compute all predicted poses ---
    predicted = []
    for pair in pose_pairs:
        T_pred = apply_calibration_matrix(
            pair["T_base_ee"], T_ee_cam, pair["T_cam_target"]
        )
        predicted.append(T_pred)

    # --- Determine reference pose ---
    if T_base_target_gt is not None:
        T_ref = np.asarray(T_base_target_gt, dtype=np.float64)
    else:
        # Consensus: mean translation + average quaternion rotation
        translations = np.stack([T[:3, 3] for T in predicted], axis=0)
        mean_translation = translations.mean(axis=0)

        # Average quaternions (simple linear average + normalise)
        quats = np.stack(
            [rotation_matrix_to_quaternion(T[:3, :3]) for T in predicted], axis=0
        )
        # Ensure all quaternions are in the same hemisphere before averaging
        ref_quat = quats[0]
        for i in range(1, len(quats)):
            if np.dot(quats[i], ref_quat) < 0:
                quats[i] = -quats[i]
        mean_quat = quats.mean(axis=0)
        norm = np.linalg.norm(mean_quat)
        if norm < 1e-10:
            mean_quat = np.array([0, 0, 0, 1], dtype=np.float64)
        else:
            mean_quat = mean_quat / norm
        mean_rotation = quaternion_to_rotation_matrix(mean_quat)

        T_ref = homogeneous_from_pose(mean_translation, mean_rotation)

    # --- Compute per-pair errors ---
    per_pair_errors = []
    for i, T_pred in enumerate(predicted):
        t_err = translation_error(T_pred, T_ref)
        r_err = rotation_error(T_pred, T_ref)
        t_pred, R_pred = pose_from_homogeneous(T_pred)
        rx, ry, rz = rotation_matrix_to_euler(R_pred)
        per_pair_errors.append({
            "pair_index": i,
            "pair_id": pose_pairs[i].get("id", i),
            "translation_error_m": round(t_err, 6),
            "rotation_error_deg": round(r_err, 4),
            "predicted_translation": [round(v, 6) for v in t_pred.tolist()],
            "predicted_euler_deg": [round(rx, 4), round(ry, 4), round(rz, 4)],
        })

    t_errors = np.array([e["translation_error_m"] for e in per_pair_errors])
    r_errors = np.array([e["rotation_error_deg"]   for e in per_pair_errors])

    ref_t, ref_R = pose_from_homogeneous(T_ref)
    ref_rx, ref_ry, ref_rz = rotation_matrix_to_euler(ref_R)

    return {
        "num_pairs": len(pose_pairs),
        "reference_translation": [round(v, 6) for v in ref_t.tolist()],
        "reference_euler_deg": [round(ref_rx, 4), round(ref_ry, 4), round(ref_rz, 4)],
        "mean_translation_error_m":  round(float(t_errors.mean()), 6),
        "std_translation_error_m":   round(float(t_errors.std()),  6),
        "max_translation_error_m":   round(float(t_errors.max()),  6),
        "mean_rotation_error_deg":   round(float(r_errors.mean()), 4),
        "std_rotation_error_deg":    round(float(r_errors.std()),  4),
        "max_rotation_error_deg":    round(float(r_errors.max()),  4),
        "per_pair_errors": per_pair_errors,
    }
