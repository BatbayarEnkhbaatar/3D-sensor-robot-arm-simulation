#!/usr/bin/env python3
"""
trigger_gripper_job.py

A minimal script that simply selects and runs an existing JBI job once,
then exits with code 0 on success or 1 on failure. All “extra” steps (servo on/off,
status polling, verbose prints) have been removed.

Usage:
    python3 trigger_gripper_job.py
"""

import sys

# ─── EDIT THESE TWO LINES ─────────────────────────────────────────────────────────→
# ROBOT_IP = "10.0.0.2"   # ←– Change to your FS100 controller’s IP
# JOB_NAME  = "DEM2"        # ←– Change to the exact job name (no “.JBI” extension)
# ────────────────────────────────────────────────────────────────────────────────←

# try:
# import fs100_gripper_controller.fs100 as FS100
from  fs100_gripper_controller.fs100 import FS100, FS100 as FS


def gripper_comma(ROBOT_IP, COMMAND):
    fs = FS100(ROBOT_IP)

    JOB_1 = "OPEN"
    JOB_2 = "CLOSE"

    if COMMAND == 1:
        COMMAND = JOB_1
    elif COMMAND == 2:
        COMMAND = JOB_2
    elif isinstance(COMMAND, str):
        pass  # user passed in "DEM1" or "DEM2" directly
    else:
        print("ERROR: Invalid COMMAND argument", file=sys.stderr)
        return "fail"

    # 1) Select the job
    if fs.select_job(COMMAND) != FS100.ERROR_SUCCESS:
        print(f"ERROR: select_job('{COMMAND}') failed (err=0x{fs.errno:X})", file=sys.stderr)
        return "fail"

    # 2) Set cycle mode to ONE_CYCLE
    if fs.select_cycle(FS.CYCLE_TYPE_ONE_CYCLE) != FS100.ERROR_SUCCESS:
        print(f"ERROR: select_cycle(ONE_CYCLE) failed (err=0x{fs.errno:X})", file=sys.stderr)
        return "fail"

    # 3) Play the job
    if fs.play_job() != FS.ERROR_SUCCESS:
        print(f"ERROR: play_job() failed (err=0x{fs.errno:X})", file=sys.stderr)
        return "fail"

    return "success"
