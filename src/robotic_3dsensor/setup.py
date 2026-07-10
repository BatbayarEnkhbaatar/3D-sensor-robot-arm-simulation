#!/home/ubuntu/Documents/my_work_1/mesh_matcher/python/myenv/bin/python

from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'robotic_3dsensor'
submodules = "algorithms/"
submodules1= "robot"
submodules2= "tesseravue/"
submodules_files = glob("src/robotic_3dsensor/algorithms/*", recursive=True)
submodules_files1 = glob("src/robotic_3dsensor/robot/*", recursive=True)
submodules_files2 = glob("src/robotic_3dsensor/tesseravue/*", recursive=True)
setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name, submodules, submodules1, submodules2],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob(os.path.join('launch', '*launch.[pxy][yma]*')))
    ],
    package_data={

        'algorithms': submodules_files, 
        'robot': submodules_files1,
        'tesseravue':  submodules_files2
        
    },
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Batbayar.E',
    maintainer_email='baggi@haanvision.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'ftp_client_node_ActionClient = robotic_3dsensor.ftp_node_ActionClient:main',
            'get_user_target_points_node = robotic_3dsensor.get_target_pose:main',
            'calibraion_eye2hand_node = robotic_3dsensor.calibration_eye_to_hand_node:main',
            # 'calibraion_eye2hand_node2 = robotic_3dsensor.calibration_eye_to_hand_node2:main',
            # 'calibraion_eye2hand_with2matrix_node = robotic_3dsensor.hand2eye_calib_node_with2matrix:main',
            'joint_states_listener = robotic_3dsensor.joint_states_listener:main',
            'tesseravuCleint_ActionClient_node = robotic_3dsensor.tesseravuCleint_ActionClient_node:main',
            'tesseravuCleint_trigger = robotic_3dsensor.tesseravuCleint_ActionClient_trigger:main',
            'tesseravueAPI_node = robotic_3dsensor.tesseravueAPI_node:main',
        ],
    },
)
