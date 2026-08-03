#!/usr/bin/env python3
"""
Interactive calibration validation UI for Doosan robot arm + RealSense D405.

Provides a web interface (Flask) that lets you:
  1. View the loaded EE→camera calibration matrix (T_ee_cam).
  2. Enter a camera-frame target pose (XYZ + RPY Euler angles).
  3. See the transformed robot base-frame target pose instantly.
  4. Run full validation over all collected pose pairs and view per-pair
     translation / rotation error metrics.

Usage
-----
    cd doosan_realsense_calibration
    python ui/calibration_ui.py [--data PATH_TO_POSES_JSON] [--host 0.0.0.0] [--port 5001]

Then open http://localhost:5001 in your browser.

The server also exposes a small REST API so the UI can call it with AJAX:

    POST /api/transform
        Body (JSON): {"x": 0.1, "y": 0.0, "z": 0.4,
                      "rx": 0.0, "ry": 5.0, "rz": 0.0}
        Returns: {"predicted_translation": [...], "predicted_euler_deg": [...],
                  "T_base_target": [[...], ...]}

    GET  /api/validate
        Returns: full validate_calibration() result as JSON.

    GET  /api/calibration_matrix
        Returns: {"T_ee_cam": [[...], ...]} as JSON.
"""

import argparse
import json
import os
import sys

from flask import Flask, jsonify, render_template, request

# Make the calibration package importable from the ui/ directory
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from calibration.eye_in_hand_calibration import (
    apply_calibration_matrix,
    euler_to_rotation_matrix,
    homogeneous_from_pose,
    load_pose_pairs,
    pose_from_homogeneous,
    rotation_matrix_to_euler,
    validate_calibration,
)
import numpy as np

# ---------------------------------------------------------------------------
# App setup
# ---------------------------------------------------------------------------

app = Flask(__name__, template_folder="templates")

# Default data path (relative to this file)
DEFAULT_DATA_PATH = os.path.join(
    os.path.dirname(__file__), "..", "data", "sample_poses.json"
)

# Populated at startup by _load_data()
_calibration_data: dict = {}


def _load_data(data_path: str) -> None:
    """Load pose pairs and calibration matrix from JSON into module-level state."""
    global _calibration_data
    _calibration_data = load_pose_pairs(data_path)
    print(f"[calibration_ui] Loaded {len(_calibration_data['pose_pairs'])} pose pairs "
          f"from {data_path}")
    t = _calibration_data["T_ee_cam"][:3, 3]
    print(f"[calibration_ui] T_ee_cam translation: {t.tolist()}")


# ---------------------------------------------------------------------------
# Helper: convert pose params to 4×4 matrix
# ---------------------------------------------------------------------------

def _pose_params_to_matrix(x, y, z, rx, ry, rz):
    """Build a 4×4 homogeneous matrix from XYZ (metres) + RPY Euler (degrees)."""
    R = euler_to_rotation_matrix(float(rx), float(ry), float(rz))
    t = np.array([float(x), float(y), float(z)])
    return homogeneous_from_pose(t, R)


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.route("/")
def index():
    """Render the main calibration dashboard."""
    T_ee_cam = _calibration_data.get("T_ee_cam", np.eye(4))
    t, R = pose_from_homogeneous(T_ee_cam)
    rx, ry, rz = rotation_matrix_to_euler(R)
    num_pairs = len(_calibration_data.get("pose_pairs", []))

    return render_template(
        "index.html",
        ee_cam_matrix=[[round(v, 6) for v in row] for row in T_ee_cam.tolist()],
        ee_cam_translation=[round(v, 6) for v in t.tolist()],
        ee_cam_euler=[round(rx, 4), round(ry, 4), round(rz, 4)],
        num_pairs=num_pairs,
    )


@app.route("/api/transform", methods=["POST"])
def api_transform():
    """Transform a camera-frame target pose into the robot base frame.

    Expected JSON body:
        { "x": float, "y": float, "z": float,
          "rx": float, "ry": float, "rz": float }
    All lengths in metres; angles in degrees (intrinsic ZYX Euler).
    """
    body = request.get_json(force=True, silent=True) or {}
    try:
        x  = float(body.get("x",  0.0))
        y  = float(body.get("y",  0.0))
        z  = float(body.get("z",  0.0))
        rx = float(body.get("rx", 0.0))
        ry = float(body.get("ry", 0.0))
        rz = float(body.get("rz", 0.0))
    except (TypeError, ValueError):
        return jsonify({"error": "Invalid input: all fields must be numeric values."}), 400

    T_cam_target = _pose_params_to_matrix(x, y, z, rx, ry, rz)

    # We need a T_base_ee to apply the full transform.
    # Without a live robot connection we use the identity (camera pose IS the
    # base-frame pose) so users can test the transform math interactively.
    # Real integration would inject the live Doosan EE pose here.
    T_base_ee = np.eye(4)
    T_ee_cam  = _calibration_data.get("T_ee_cam", np.eye(4))

    T_result = apply_calibration_matrix(T_base_ee, T_ee_cam, T_cam_target)
    t_res, R_res = pose_from_homogeneous(T_result)
    rx_r, ry_r, rz_r = rotation_matrix_to_euler(R_res)

    return jsonify({
        "predicted_translation": [round(v, 6) for v in t_res.tolist()],
        "predicted_euler_deg":   [round(rx_r, 4), round(ry_r, 4), round(rz_r, 4)],
        "T_base_target":         [[round(v, 6) for v in row]
                                  for row in T_result.tolist()],
    })


@app.route("/api/validate", methods=["GET"])
def api_validate():
    """Run full calibration validation over all loaded pose pairs.

    Returns summary statistics and per-pair errors as JSON.
    """
    pose_pairs = _calibration_data.get("pose_pairs", [])
    T_ee_cam   = _calibration_data.get("T_ee_cam", np.eye(4))

    if not pose_pairs:
        return jsonify({"error": "No pose pairs loaded."}), 400

    # Use ground-truth if present in the file, else consensus mode
    T_gt = _calibration_data.get("T_base_target_gt", None)

    result = validate_calibration(pose_pairs, T_ee_cam, T_base_target_gt=T_gt)
    return jsonify(result)


@app.route("/api/calibration_matrix", methods=["GET"])
def api_calibration_matrix():
    """Return the loaded T_ee_cam calibration matrix as JSON."""
    T_ee_cam = _calibration_data.get("T_ee_cam", np.eye(4))
    return jsonify({
        "T_ee_cam": [[round(v, 8) for v in row] for row in T_ee_cam.tolist()]
    })


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Eye-in-hand calibration validation UI for Doosan + RealSense D405"
    )
    parser.add_argument(
        "--data", default=DEFAULT_DATA_PATH,
        help="Path to pose-pairs JSON file (default: data/sample_poses.json)"
    )
    parser.add_argument("--host", default="127.0.0.1",
                        help="Host to bind the Flask server (default: 127.0.0.1)")
    parser.add_argument("--port", type=int, default=5001,
                        help="Port to listen on (default: 5001)")
    parser.add_argument("--debug", action="store_true",
                        help="Enable Flask debug mode")
    args = parser.parse_args()

    _load_data(args.data)
    app.run(host=args.host, port=args.port, debug=args.debug)


if __name__ == "__main__":
    main()
