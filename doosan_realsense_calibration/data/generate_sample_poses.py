#!/usr/bin/env python3
"""
Generate sample_poses.json — 40 synthetic pose pairs for the Doosan + RealSense D405
eye-in-hand calibration example.

Usage:
    python generate_sample_poses.py

This overwrites data/sample_poses.json with fresh data.

Simulation setup
----------------
* A calibration target (e.g. ArUco / ChArUco board) is fixed in the robot workspace
  at approximately (0.55, 0.05, 0.25) m from the Doosan base frame.
* The RealSense D405 is mounted on the flange; the EE→camera offset is
  ~10 cm in Z (forward), ~5 cm in Y (side), with a slight downward tilt.
* For each of the 40 poses, we simulate a random EE pose inside the Doosan
  workspace, compute the exact camera→target transform from geometry, and
  add small Gaussian noise (σ=2 mm translation, σ=0.3° rotation) to
  represent real-world measurement uncertainty.
"""

import json
import math
import os
import sys

import numpy as np

# Ensure the calibration package is importable from this script's location
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from calibration.eye_in_hand_calibration import (
    euler_to_rotation_matrix,
    homogeneous_from_pose,
    rotation_matrix_to_quaternion,
)

SEED = 42
NUM_PAIRS = 40
OUTPUT_FILE = os.path.join(os.path.dirname(__file__), "sample_poses.json")

# ---------------------------------------------------------------------------
# Ground-truth calibration matrix  T_ee_cam
# (what the Doosan+D405 calibration procedure would produce)
# ---------------------------------------------------------------------------
# Camera is offset ~10 cm along the EE Z-axis (forward), 5 cm along Y,
# and pitched ~15° downward so the D405 can see objects on a table.
T_ee_cam = homogeneous_from_pose(
    translation=np.array([0.0, 0.05, 0.10]),
    rotation_matrix=euler_to_rotation_matrix(rx_deg=-15.0, ry_deg=0.0, rz_deg=0.0),
)

# ---------------------------------------------------------------------------
# Fixed calibration target pose in base frame
# ---------------------------------------------------------------------------
T_base_target_true = homogeneous_from_pose(
    translation=np.array([0.55, 0.05, 0.25]),
    rotation_matrix=euler_to_rotation_matrix(rx_deg=0.0, ry_deg=0.0, rz_deg=0.0),
)

# ---------------------------------------------------------------------------
# Generate pose pairs
# ---------------------------------------------------------------------------

def random_ee_pose(rng: np.random.Generator) -> np.ndarray:
    """Sample a plausible Doosan end-effector pose in the robot base frame."""
    # Doosan workspace (M-series): roughly 0.3–0.75 m in front, ±0.3 m sides
    x   = rng.uniform(0.30, 0.70)
    y   = rng.uniform(-0.30, 0.30)
    z   = rng.uniform(0.30, 0.65)
    rx  = rng.uniform(-20.0, 20.0)   # roll
    ry  = rng.uniform(-20.0, 20.0)   # pitch
    rz  = rng.uniform(-30.0, 30.0)   # yaw
    R = euler_to_rotation_matrix(rx, ry, rz)
    return homogeneous_from_pose(np.array([x, y, z]), R)


def add_noise(T: np.ndarray, rng: np.random.Generator,
              sigma_t: float = 0.002, sigma_r_deg: float = 0.3) -> np.ndarray:
    """Add small Gaussian noise to a homogeneous transform (simulates sensor noise)."""
    T_noisy = T.copy()
    T_noisy[:3, 3] += rng.normal(0, sigma_t, 3)
    noise_axis = rng.normal(0, 1, 3)
    norm = np.linalg.norm(noise_axis)
    if norm > 1e-10:
        noise_axis /= norm
    angle = math.radians(rng.normal(0, sigma_r_deg))
    K = np.array([
        [          0, -noise_axis[2],  noise_axis[1]],
        [ noise_axis[2],           0, -noise_axis[0]],
        [-noise_axis[1],  noise_axis[0],           0],
    ])
    # Rodrigues' rotation formula
    R_noise = np.eye(3) + math.sin(angle) * K + (1 - math.cos(angle)) * (K @ K)
    T_noisy[:3, :3] = R_noise @ T_noisy[:3, :3]
    return T_noisy


rng = np.random.default_rng(SEED)

pose_pairs = []
for i in range(NUM_PAIRS):
    T_base_ee = random_ee_pose(rng)

    # Exact T_cam_target derived from known geometry:
    #   T_base_target = T_base_ee @ T_ee_cam @ T_cam_target
    #   => T_cam_target = inv(T_ee_cam) @ inv(T_base_ee) @ T_base_target
    T_cam_target_exact = (
        np.linalg.inv(T_ee_cam)
        @ np.linalg.inv(T_base_ee)
        @ T_base_target_true
    )
    # Simulate RealSense measurement noise
    T_cam_target = add_noise(T_cam_target_exact, rng)

    pose_pairs.append({
        "id": i + 1,
        "T_base_ee":    T_base_ee.tolist(),
        "T_cam_target": T_cam_target.tolist(),
    })

# ---------------------------------------------------------------------------
# Serialise
# ---------------------------------------------------------------------------
output = {
    "description": (
        "40 synthetic eye-in-hand pose pairs for Doosan robot arm + RealSense D405. "
        "T_ee_cam is the ground-truth EE→camera calibration transform. "
        "T_base_ee entries contain Doosan end-effector poses in the robot base frame. "
        "T_cam_target entries contain the ArUco calibration board pose as seen by the D405 "
        "(with 2 mm / 0.3° Gaussian noise)."
    ),
    "T_ee_cam": T_ee_cam.tolist(),
    "T_base_target_gt": T_base_target_true.tolist(),
    "pose_pairs": pose_pairs,
}

with open(OUTPUT_FILE, "w", encoding="utf-8") as fh:
    json.dump(output, fh, indent=2)

print(f"Written {NUM_PAIRS} pose pairs → {OUTPUT_FILE}")
print(f"T_base_target (ground truth):  {T_base_target_true[:3, 3].tolist()}")
q = rotation_matrix_to_quaternion(T_ee_cam[:3, :3])
print(f"T_ee_cam quaternion [x,y,z,w]: {[round(v,4) for v in q.tolist()]}")
print(f"T_ee_cam translation:          {T_ee_cam[:3, 3].tolist()}")
