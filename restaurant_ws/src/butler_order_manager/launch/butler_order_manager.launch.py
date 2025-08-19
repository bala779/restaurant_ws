from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package="butler_order_manager",
            executable="order_server",
            name="order_server",
            output="screen",
        ),
        Node(
            package="butler_order_manager",
            executable="order_dispatcher",
            name="order_dispatcher",
            output="screen"
        ),
        Node(
            package="butler_order_manager",
            executable="order_executor",
            name="order_executor",
            output="screen"
        )
    ])
