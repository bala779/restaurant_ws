from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    pkg_share = get_package_share_directory('butler_bot')
    nav2_bringup_share = get_package_share_directory('nav2_bringup')

    # Paths
    nav2_config = os.path.join(pkg_share, 'config', 'nav2_params.yaml')
    bringup_launch_file = os.path.join(nav2_bringup_share, 'launch', 'bringup_launch.py')
    amcl_launch_file = os.path.join(pkg_share, 'launch', 'amcl.launch.py')
    default_map = '/home/balaji/restaurant_ws/src/restaurant/config/maps/map.yaml'

    return LaunchDescription([

        DeclareLaunchArgument(
            'use_sim_time',
            default_value='true',
            description='Use simulation (Gazebo) clock'),

        DeclareLaunchArgument(
            'map',
            default_value=default_map,
            description='Full path to map yaml file to load'),

        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(pkg_share, 'launch', 'map_server.launch.py')
            ),
            launch_arguments={
                'use_sim_time': LaunchConfiguration('use_sim_time'),
                'map': LaunchConfiguration('map')
            }.items()
        ),

        TimerAction(
            period=1.0,
            actions=[
                IncludeLaunchDescription(
                    PythonLaunchDescriptionSource(amcl_launch_file),
                    launch_arguments={
                        'use_sim_time': LaunchConfiguration('use_sim_time'),
                        'map': LaunchConfiguration('map')
                    }.items()
                )
            ]
        ),

        TimerAction(
            period=2.0,
            actions=[
                IncludeLaunchDescription(
                    PythonLaunchDescriptionSource(bringup_launch_file),
                    launch_arguments={
                        'params_file': nav2_config,
                        'use_sim_time': LaunchConfiguration('use_sim_time'),
                        'map': LaunchConfiguration('map')
                    }.items()
                )
            ]
        ),
    ])
