import numpy as np
from scipy.spatial.transform import Rotation as Rot


# =========================
# Conversions (mm/deg, ZYX)
# =========================

def rxyz_deg_to_rotm_xyz(rx_deg: float, ry_deg: float, rz_deg: float) -> np.ndarray:
    """
    Convert (Rx, Ry, Rz) in degrees to rotation matrix using XYZ composition:
        R = Rx * Ry * Rz
    """
    return Rot.from_euler('ZYX', [rz_deg, ry_deg, rx_deg], degrees=True).as_matrix()


def rotm_to_rxyz_deg_xyz(Rm: np.ndarray) -> tuple[float, float, float]:
    """
    Convert rotation matrix to (Rx, Ry, Rz) degrees using XYZ composition.
    SciPy returns angles for 'xyz' as [rx, ry, rz].
    """
    rz_deg, ry_deg, rx_deg = Rot.from_matrix(Rm).as_euler('ZYX', degrees=True)
    return float(rx_deg), float(ry_deg), float(rz_deg)


def pose_xyz_rxyz_to_T_mm_deg(pose6: np.ndarray) -> np.ndarray:
    """
    [X,Y,Z,Rx,Ry,Rz] (mm,deg) -> 4x4 homogeneous transform [R t; 0 1]
    """
    x, y, z, rx, ry, rz = [float(v) for v in pose6]
    Rm = rxyz_deg_to_rotm_xyz(rx, ry, rz)
    T = np.eye(4, dtype=float)
    T[0:3, 0:3] = Rm
    T[0:3, 3] = np.array([x, y, z], dtype=float)
    return T


def T_to_pose_xyz_rxyz_mm_deg(T: np.ndarray) -> np.ndarray:
    """
    4x4 homogeneous transform [R t; 0 1] -> [X,Y,Z,Rx,Ry,Rz] (mm,deg)
    """
    Rm = T[0:3, 0:3]
    t = T[0:3, 3]
    rx, ry, rz = rotm_to_rxyz_deg_xyz(Rm)
    return np.array([t[0], t[1], t[2], rx, ry, rz], dtype=float)


def orthonormalize_R(Rm: np.ndarray) -> np.ndarray:
    """
    Enforce R in SO(3) using SVD (helps with tiny numeric drift).
    """
    U, _, Vt = np.linalg.svd(Rm)
    Rn = U @ Vt
    if np.linalg.det(Rn) < 0:
        U[:, 2] *= -1
        Rn = U @ Vt
    return Rn


def normalize_rotation_in_T(T: np.ndarray) -> np.ndarray:
    Tn = T.copy()
    Tn[0:3, 0:3] = orthonormalize_R(Tn[0:3, 0:3])
    return Tn


# ==========================================
# Core computation (stand-alone, no files)
# ==========================================

def compute_target_pose_base_mm_deg(
    target_pose_cam_xyz_rxyz: np.ndarray,   # ^C T_T
    gripper_pose_base_xyz_rxyz: np.ndarray, # ^B T_G
    T_GC: np.ndarray                         # ^G T_C (4x4)
) -> np.ndarray:
    """
    Returns target pose in base as [X,Y,Z,Rx,Ry,Rz] (mm, deg).

    ^B T_T = (^B T_G) * (^G T_C) * (^C T_T)
    """
    T_CT = pose_xyz_rxyz_to_T_mm_deg(target_pose_cam_xyz_rxyz)
    T_BG = pose_xyz_rxyz_to_T_mm_deg(gripper_pose_base_xyz_rxyz)



    T_BT = T_BG @ T_GC @ T_CT

    T_BT = normalize_rotation_in_T(T_BT)
    
    return T_to_pose_xyz_rxyz_mm_deg(T_BT)


def pose6_to_T(pose6: np.ndarray) -> np.ndarray:
    x, y, z, rx, ry, rz = np.asarray(pose6, float).reshape(6)
    T = np.eye(4)
    T[:3, :3] = Rot.from_euler('ZYX', [rz, ry, rx], degrees=True).as_matrix()
    T[:3,  3] = [x, y, z]
    return T

def T_to_pose6(T: np.ndarray) -> np.ndarray:
    T = np.asarray(T, float)
    rz, ry, rx = Rot.from_matrix(T[:3, :3]).as_euler('ZYX', degrees=True)
    x, y, z = T[:3, 3]
    return np.array([x, y, z, rx, ry, rz], float)

def wrist_to_tool_pose6(wrist_pose6: np.ndarray, L=205.0, sX=-30.0, sY=-10.0) -> np.ndarray:
    T = pose6_to_T(wrist_pose6)
    T[:3, 3] += T[:3, :3] @ np.array([sX, sY, -L], float)  # -L confirmed
    return T_to_pose6(T)
