from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'robotic_api'
submodules = "algorithms/"
submodules2= "tesseravue/"
submodules_files = glob("src/robotic_3dsensor/algorithms/*", recursive=True)
submodules_files2 = glob("src/robotic_3dsensor/tesseravue/*", recursive=True)
setup(
    name=package_name,
    version='0.0.0',
    # packages=find_packages(exclude=['test']),
    packages=[package_name, submodules, submodules2],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
         (os.path.join('share', package_name, 'launch'), glob(os.path.join('launch', '*launch.[pxy][yma]*')))
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='ubuntu',
    maintainer_email='baggi@haanvision.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'tesseraVue_Urrobot = robotic_api.tesseraVue_Urrobot_api:main',
            'ftp_client_node = robotic_api.ftp_node:main',
            'get_target_node = robotic_api.get_target_pose:main',
            'hand_eye_calib_node = robotic_api.calibration_eye_to_hand_node:main',
            'tesseravue_ActionClient_api =robotic_api.tesseravue_ActionClient_api:main'

        ],
    },
)
