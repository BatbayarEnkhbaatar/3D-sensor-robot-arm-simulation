
import os
import sys
import unittest

# Include the test module directory
test_dir = os.path.dirname(os.path.realpath(__file__))
module_dir = os.path.dirname(test_dir)
sys.path.append(module_dir)

from fs100_controller_py.fs100 import FS100

print(FS100('10.0.0.2'))
robot_controller = FS100(ip="10.0.0.2")
# Define target position in micrometers and ten-thousandths of a degree



def main ():
   
    result = robot_controller.reset_alarm(FS100.RESET_ALARM_TYPE_ALARM)
    
    if result == FS100.ERROR_SUCCESS:
        print("Alarm reset successfully.")
    else:
        print(f"Failed to reset alarm. Error code: {robot_controller.errno}")

    # Similarly, to reset an error, you could use:
    result = robot_controller.reset_alarm(FS100.RESET_ALARM_TYPE_ERROR)
    
    if result == FS100.ERROR_SUCCESS:
        print("Error reset successfully.")
    else:
        print(f"Failed to reset error. Error code: {robot_controller.errno}")

if __name__ == "__main__":
    main()