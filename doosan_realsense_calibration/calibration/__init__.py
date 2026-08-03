"""
Eye-in-hand calibration validation package for Doosan robot arm + RealSense D405 camera.
"""
from .eye_in_hand_calibration import (
    load_pose_pairs,
    homogeneous_from_pose,
    pose_from_homogeneous,
    quaternion_to_rotation_matrix,
    rotation_matrix_to_quaternion,
    euler_to_rotation_matrix,
    rotation_matrix_to_euler,
    apply_calibration_matrix,
    translation_error,
    rotation_error,
    validate_calibration,
)

__all__ = [
    "load_pose_pairs",
    "homogeneous_from_pose",
    "pose_from_homogeneous",
    "quaternion_to_rotation_matrix",
    "rotation_matrix_to_quaternion",
    "euler_to_rotation_matrix",
    "rotation_matrix_to_euler",
    "apply_calibration_matrix",
    "translation_error",
    "rotation_error",
    "validate_calibration",
]
