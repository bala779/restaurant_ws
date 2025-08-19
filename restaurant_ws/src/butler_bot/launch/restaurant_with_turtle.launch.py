# restaurant_launch.py
from launch import LaunchDescription
from launch.actions import ExecuteProcess
from launch_ros.actions import Node
from pathlib import Path

def generate_launch_description():

    # Paths
    world_path = '/home/balaji/restaurant_ws/src/restaurant/models/restaurant.world'
    urdf_path = Path('/home/balaji/restaurant_ws/src/butler_bot/urdf/butler.urdf')
    urdf_text = urdf_path.read_text()

    return LaunchDescription([

        # Launch Gazebo
        ExecuteProcess(
            cmd=["gazebo", "--verbose",
                 "-s", "libgazebo_ros_factory.so",
                 "-s", "libgazebo_ros_init.so",
                 world_path],
            output="screen"
        ),

        # Spawn Robot
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

        # Robot State Publisher
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

        # Joint State Publisher
        Node(
            package="joint_state_publisher",
            executable="joint_state_publisher",
            name="joint_state_publisher",
            output="screen"
        ),

        # MoveBot Node (simple move sequence)
        Node(
            package="butler_bot",
            executable="turtle_bot",
            name="move_bot",
            output="screen"
        )

    ])
