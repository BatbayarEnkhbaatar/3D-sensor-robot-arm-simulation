#!/usr/bin/env python3
"""
trigger_choose_job_loop.py

Continuously prompts the user to enter “1” or “2” on the console to run the corresponding JBI job once
in ONE_CYCLE mode. The script stays running until the user types “q” to quit.

Usage:
    python3 trigger_choose_job_loop.py
"""

import sys

# ─── EDIT THESE TWO LINES ──────────────────────────────────────────────────────────→
ROBOT_IP = "10.0.0.2"  # ←– Change to your FS100 controller’s IP
JOB_1    = "OPEN"      # ←– Job name to run if user types “1” (no “.JBI” extension)
JOB_2    = "CLOSE"      # ←– Job name to run if user types “2”
# ────────────────────────────────────────────────────────────────────────────────←
from  fs100_gripper_controller.fs100 import FS100, FS100 as FS
# try:
#     from fs100 import FS100, FS100 as FS
# except ImportError:
#     print("ERROR: Cannot find fs100.py.  Make sure it’s in the same folder.", file=sys.stderr)
#     sys.exit(1)



def send_job(job_name: str) -> bool:
    """
    Selects and plays the given JBI job once (ONE_CYCLE).
    Returns True if all FS100 calls succeed (status 0), False otherwise.
    """
    fs = FS100(ROBOT_IP)

    # 1) Select the job
    if fs.select_job(job_name) != FS.ERROR_SUCCESS:
        print(f"ERROR: select_job('{job_name}') failed (err=0x{fs.errno:X})", file=sys.stderr)
        return False

    # 2) Set cycle to ONE_CYCLE
    if fs.select_cycle(FS.CYCLE_TYPE_ONE_CYCLE) != FS.ERROR_SUCCESS:
        print(f"ERROR: select_cycle(ONE_CYCLE) for '{job_name}' failed (err=0x{fs.errno:X})", file=sys.stderr)
        return False

    # 3) Play the job
    if fs.play_job() != FS.ERROR_SUCCESS:
        print(f"ERROR: play_job() for '{job_name}' failed (err=0x{fs.errno:X})", file=sys.stderr)
        return False

    return True


def main():
    print("FS100 Job Trigger Loop (type 'q' to quit)\n")
    try:
        while True:
            print(f"Enter '1' to run job: {JOB_1}")
            print(f"Enter '2' to run job: {JOB_2}")
            print("Enter 'q' to exit")
            choice = input("Your choice (1, 2, or q): ").strip().lower()

            if choice == "q":
                print("Exiting.")
                break
            elif choice == "1":
                job_to_run = JOB_1
            elif choice == "2":
                job_to_run = JOB_2
            else:
                print("Invalid input. Please type 1, 2, or q.\n")
                continue

            if send_job(job_to_run):
                print(f"Job '{job_to_run}' triggered successfully.\n")
            else:
                print(f"Failed to trigger '{job_to_run}'.\n")

    except KeyboardInterrupt:
        print("\nInterrupted by user. Exiting.")
    sys.exit(0)


if __name__ == "__main__":
    main()
