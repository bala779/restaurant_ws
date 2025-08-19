from launch import LaunchDescription
from launch.actions import ExecuteProcess
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
from pathlib import Path
import os

world_package_path = get_package_share_directory('restaurant')
butler_package_path = get_package_share_directory('butler_bot')

def generate_launch_description():

    world_path = '/home/balaji/restaurant_ws/src/restaurant/models/restaurant.world'

    urdf_path = Path(butler_package_path)/'urdf'/'butler.urdf'
    urdf_text = urdf_path.read_text()
    
    return LaunchDescription([

        # Launch Gazebo with your world
        ExecuteProcess(
            cmd=["gazebo", "--verbose", "-s", "libgazebo_ros_factory.so","-s", "libgazebo_ros_init.so", world_path],
            output="screen"
        ),

        # Spawn robot
        Node(
            package="gazebo_ros",
            executable="spawn_entity.py",
            arguments=[
                "-file", str(urdf_path),
                "-entity", "butler_bot",
                "-x", "0", "-y", "0", "-z", "0.1"
            ],
            output="screen"
        ),

        # Robot state publisher
        Node(
            package="robot_state_publisher",
            executable="robot_state_publisher",
            name="robot_state_publisher",
            output="screen",
            parameters=[{
                "use_sim_time": True,
                "robot_description": urdf_text
            }]
        ),

        # Joint state publisher
        Node(
            package="joint_state_publisher",
            executable="joint_state_publisher",
            name="joint_state_publisher",
            output="screen"
        ),

        Node(
            package='butler_bot',
            executable='bot_node',
            name='butler_bot_node',
            output='screen'
        ),

        # map server
        Node(
            package='nav2_map_server',
            executable='map_server',
            name='map_server',
            output='screen',
            parameters=[{
                'yaml_filename': '/home/balaji/restaurant_ws/src/restaurant/config/maps/map.yaml' 
            }]
        ),
        Node(
            package='slam_toolbox',
            executable='async_slam_toolbox_node',
            name='slam_toolbox',
            output='screen',
            parameters=[{
                'use_sim_time': True,         
                'scan_topic': '/scan',        
                'map_frame': 'map',
                'odom_frame': 'odom',
                'base_frame': 'base_link',
                'update_map': True
            }]
        )
    ])

