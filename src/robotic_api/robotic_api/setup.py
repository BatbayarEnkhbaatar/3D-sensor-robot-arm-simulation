#!~/Documents/work/venv/bin/activate
from setuptools import find_packages, setup
import os
import glob
package_name = 'robotic_3dsensor'
submod = 'tesseravue/'
submod1= 'algorithms/'
submod_files = glob.glob('src/robotic_3dsensor/algorithms/', recursive=True)
submod1_files = glob.glob("src/robotic_3dsensor/robot/*", recursive=True)
setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    # packages=[package_name, submod, submod1],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob.glob(os.path.join('launch', '*launch.[pxy][yma]*')))
    ],
    package_data={
        'algorithms': submod_files, 
        'tesseravue':  submod1_files
    },
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='BAggi',
    maintainer_email='baggi@haanvision.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'ftp_client_node = robotic_3dsensor.ftp_node:main',
            'get_target_node = robotic_3dsensor.get_target_pose:main',
            'hand_eye_calib_node = robotic_3dsensor.calibration_eye_to_hand_node:main',
            'tesseravueAPI_node = robotic_3dsensor.tesseravueAPI_node:main'
        ],
    },
)
