# Eye-in-Hand Calibration Validator
### Doosan Robot Arm + Intel RealSense D405

This package validates an **eye-in-hand** camera–robot calibration and provides
an interactive web interface for inspecting calibration quality.

---

## Background

In the **eye-in-hand** configuration the RealSense D405 camera is rigidly
mounted on the Doosan robot's end-effector (flange).  Calibration determines
the fixed transform **T\_ee\_cam** — from the end-effector frame to the camera
frame — by solving:

```
T_base_target = T_base_ee  @  T_ee_cam  @  T_cam_target
```

| Symbol | Description |
|--------|-------------|
| `T_base_ee` | End-effector pose in the Doosan base frame (from robot kinematics) |
| `T_ee_cam` | **Calibration result** — rigid EE→camera offset |
| `T_cam_target` | Target pose as detected by the RealSense D405 |
| `T_base_target` | Predicted target pose in the Doosan base frame |

---

## Package Structure

```
doosan_realsense_calibration/
├── calibration/
│   ├── __init__.py
│   └── eye_in_hand_calibration.py   # Core math + validation logic
├── data/
│   ├── generate_sample_poses.py     # Regenerate sample_poses.json
│   └── sample_poses.json            # 40 synthetic pose pairs (Doosan + D405)
├── tests/
│   ├── __init__.py
│   └── test_calibration.py          # 32 unit tests
├── ui/
│   ├── __init__.py
│   ├── calibration_ui.py            # Flask web server
│   └── templates/
│       └── index.html               # Dashboard UI
├── requirements.txt
└── README.md
```

---

## Installation

```bash
# From the repo root:
pip install -r doosan_realsense_calibration/requirements.txt
```

Python ≥ 3.9 and NumPy are required.  No ROS installation needed for
validation or the UI.

---

## Quick Start

### 1 — Run the unit tests

```bash
# From the repo root:
python -m pytest doosan_realsense_calibration/tests/ -v
```

Expected: **32 tests passed**.

### 2 — Launch the interactive UI

```bash
python doosan_realsense_calibration/ui/calibration_ui.py
```

Open **http://localhost:5001** in your browser.

Optional arguments:
```
--data PATH    Path to pose-pairs JSON (default: data/sample_poses.json)
--host HOST    Bind address (default: 127.0.0.1)
--port PORT    Port (default: 5001)
--debug        Enable Flask debug/reload mode
```

### 3 — Use your own calibration data

Replace `data/sample_poses.json` with a file in the same format:

```json
{
  "description": "My Doosan + D405 calibration",
  "T_ee_cam": [
    [ r00, r01, r02, tx ],
    [ r10, r11, r12, ty ],
    [ r20, r21, r22, tz ],
    [ 0,   0,   0,   1  ]
  ],
  "T_base_target_gt": [ ... ],   // optional ground-truth (4×4)
  "pose_pairs": [
    {
      "id": 1,
      "T_base_ee":    [ [...], [...], [...], [...] ],
      "T_cam_target": [ [...], [...], [...], [...] ]
    },
    ...
  ]
}
```

Then start the UI pointing at your file:

```bash
python doosan_realsense_calibration/ui/calibration_ui.py \
  --data /path/to/my_poses.json
```

---

## REST API

The Flask server also exposes a small JSON API:

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/transform` | Transform a camera-frame pose to robot base frame |
| `GET`  | `/api/validate`  | Run full validation, return summary + per-pair errors |
| `GET`  | `/api/calibration_matrix` | Return the loaded T\_ee\_cam matrix |

### POST `/api/transform`

**Request body** (JSON):
```json
{ "x": 0.05, "y": 0.0, "z": 0.40, "rx": 0.0, "ry": 5.0, "rz": 0.0 }
```
All lengths in **metres**; angles in **degrees** (intrinsic ZYX / ROS RPY convention).

**Response**:
```json
{
  "predicted_translation": [0.055, 0.048, 0.387],
  "predicted_euler_deg":   [-15.0, 5.0, 0.0],
  "T_base_target": [[...], [...], [...], [...]]
}
```

---

## Calibration API Reference

All functions are importable from `calibration.eye_in_hand_calibration`:

```python
from doosan_realsense_calibration.calibration.eye_in_hand_calibration import (
    load_pose_pairs,
    homogeneous_from_pose,
    pose_from_homogeneous,
    euler_to_rotation_matrix,
    rotation_matrix_to_euler,
    quaternion_to_rotation_matrix,
    rotation_matrix_to_quaternion,
    apply_calibration_matrix,
    translation_error,
    rotation_error,
    validate_calibration,
)
```

### Key functions

| Function | Description |
|----------|-------------|
| `load_pose_pairs(filepath)` | Load pose pairs JSON → dict with numpy arrays |
| `homogeneous_from_pose(t, R)` | Build 4×4 matrix from translation + rotation |
| `pose_from_homogeneous(T)` | Extract translation + rotation from 4×4 |
| `apply_calibration_matrix(T_base_ee, T_ee_cam, T_cam_target)` | Core transform |
| `translation_error(T_pred, T_ref)` | Euclidean distance in metres |
| `rotation_error(T_pred, T_ref)` | Geodesic angle in degrees |
| `validate_calibration(pose_pairs, T_ee_cam, T_base_target_gt=None)` | Full validation |

### Validation thresholds (guidelines)

| Quality | Mean Trans. Error | Mean Rot. Error |
|---------|-------------------|-----------------|
| ✅ Good | ≤ 3 mm | ≤ 0.5° |
| ⚠️ Acceptable | 3–10 mm | 0.5–2° |
| ❌ Poor | > 10 mm | > 2° |

---

## Regenerating Sample Data

```bash
python doosan_realsense_calibration/data/generate_sample_poses.py
```

This script creates 40 synthetic pose pairs with 2 mm / 0.3° Gaussian noise,
matching a realistic Doosan + D405 setup.
