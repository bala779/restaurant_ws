import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource


def generate_launch_description():
    # Paths to individual launch files
    butler_bot_launch = os.path.join(
        get_package_share_directory('butler_bot'),
        'launch',
        'butler_restaurant_env.launch.py'
    )

    butler_order_manager_launch = os.path.join(
        get_package_share_directory('butler_order_manager'),
        'launch',
        'butler_order_manager.launch.py'
    )

    # Include both
    return LaunchDescription([
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(butler_bot_launch)
        ),
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(butler_order_manager_launch)
        )
    ])
