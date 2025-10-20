from setuptools import find_packages, setup
from  glob import glob
import os
package_name = 'fs100_controller_py'
submodules = "fs100/"
submodules_gripper = "fs100_gripper_controller/"

setup(
    name=package_name,
    version='0.0.0',
    packages= [package_name, submodules, submodules_gripper],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        # ('share/' + package_name + '/fs100', glob('src/fs100_controller_py/fs100/*'))
        (os.path.join('share', package_name, 'launch'), glob(os.path.join('launch', '*launch.[pxy][yma]*')))
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='ubuntu',
    maintainer_email='baggi@haanivision.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    # tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'real_robot_pose = fs100.read_robot_pose:main',
            'sim_robot_pose = fs100.sim_robot_pose:main',
            'task_server = fs100.task_server:main',
            'task_server_demo = fs100.task_server_demo:main',
            'task_client_demo = fs100.task_client_demo:main',
            'task_server_robot = fs100.task_server_robot:main',
            'task_server_gripper = fs100.task_server_gripper:main'
        ],
    },
)
