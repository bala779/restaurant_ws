from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='nav2_amcl',
            executable='amcl',
            name='amcl',
            output='screen',
            parameters=[{
                'use_sim_time': False,
                'yaml_filename': '/home/balaji/restaurant_ws/src/restaurant/config/maps/map.yaml'
            }]
        )
    ])
