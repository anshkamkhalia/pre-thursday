from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'mini_thursday'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'),
            glob('launch/*.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='ansh',
    maintainer_email='anshkamkhalia@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'robot_state_publisher_and_server = mini_thursday.robot_state.robot_node:main',
            'robot_state_monitor = mini_thursday.robot_state.monitor_node:main',
            'robot_state_client = mini_thursday.robot_state.get_status_node:main',
            'robot_charging_action_server = mini_thursday.robot_state.charging_action_node:main',
            'robot_charging_action_client = mini_thursday.robot_state.charging_action_client_node:main',
            'movement_action_server = mini_thursday.movement.movement_action_server:main',
            'movement_action_client = mini_thursday.movement.movement_action_client:main',
        ],
    },
)
