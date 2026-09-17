from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='mini_thursday',
            executable='robot_state_publisher_and_server',
        ),
        Node(
            package='mini_thursday',
            executable='robot_state_monitor',
        ),
        Node(
            package='mini_thursday',
            executable='movement_action_server',
        ),
        Node(
            package='mini_thursday',
            executable='movement_action_client',
            arguments=['3', '3']
        ),
    ])