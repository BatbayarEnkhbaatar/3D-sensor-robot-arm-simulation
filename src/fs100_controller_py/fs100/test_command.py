
import os
import sys
import unittest

# Include the test module directory
test_dir = os.path.dirname(os.path.realpath(__file__))
module_dir = os.path.dirname(test_dir)
sys.path.append(module_dir)

from fs100_controller_py.fs100 import FS100

print(FS100('192.168.10.2'))
robot_controller = FS100(ip="10.0.0.2")
# Define target position in micrometers and ten-thousandths of a degree


def move_to_position(fs100, move_type, coordinate, speed_class, speed, position):

    # Call the mov method to send the position command
    result = fs100.mov(
        move_type=move_type,
        coordinate=coordinate,
        speed_class=speed_class,
        speed=speed,
        pos=position
    )
    print(f"command result:  {fs100.errno}")
    # Check if the move was successful
    if result == fs100.ERROR_SUCCESS:
        print("The command is succeeded, RESULT: ", result)
    else:
        print(f"Failed to move. Error code: {fs100.errno}, {position}")
    return result 
initial_pose = (570000, 2665, 435800, -900000, 0, -900000, 0, 0)
pickup = (736090, 3501, -47096, 1310118, -66151, 848797, 0, 0) 
place = (378560, 617966, -129851, 1436337, 0, -315067, 0,0)

target_position4 = (896365, 55026, -52453, 1785430, -28774, 43004, 0)  



command1 = move_to_position(
    fs100=robot_controller,
    move_type=FS100.MOVE_TYPE_LINEAR_ABSOLUTE_POS,
    coordinate=FS100.MOVE_COORDINATE_SYSTEM_ROBOT,
    speed_class=FS100.MOVE_SPEED_CLASS_MILLIMETER,
    speed=1000,   
    # position=target_position
    position=initial_pose
    
)


