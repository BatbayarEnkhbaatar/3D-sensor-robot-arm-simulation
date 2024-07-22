#!/usr/bin/env python3

from setuptools import find_packages, setup
# from absl import app
package_name = 'robotic_ai_model'
submodules = "robotic_ai_model/rt1_jax/"
submodules2 = "robotic_ai_model/rt1_jax/models/"
submodules3 = "robotic_ai_model/rt1_jax/rt_1_x_jax/b321733791_75882326_000900000"
setup(
    name=package_name,
    version='0.0.0',
    # packages=find_packages(exclude=['test']),
    packages = [package_name, submodules, submodules2, submodules3],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools', 
                      'absl-py>=0.1.0',
                      'flax'],
    zip_safe=True,
    maintainer='ubuntu',
    maintainer_email='ubuntu@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'task_client = robotic_ai_model.task_client:main'
        ],
    },
)
