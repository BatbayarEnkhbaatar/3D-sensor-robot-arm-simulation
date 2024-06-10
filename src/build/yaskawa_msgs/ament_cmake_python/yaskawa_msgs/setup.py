from setuptools import find_packages
from setuptools import setup

setup(
    name='yaskawa_msgs',
    version='0.0.0',
    packages=find_packages(
        include=('yaskawa_msgs', 'yaskawa_msgs.*')),
)
