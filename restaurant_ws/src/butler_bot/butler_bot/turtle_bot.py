#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from geometry_msgs.msg import PoseStamped
from butler_bot_interfaces.srv import MoveHome, MovePose
from nav2_msgs.action import NavigateToPose

import math

# Predefined poses on your map
POSES = {
    "Home": {"x": 0.0, "y": 0.0, "yaw": 0.0},
    "Kitchen": {"x": 2.5, "y": 1.0, "yaw": 0.0},
    "table_1": {"x": 3.0, "y": 2.0, "yaw": math.pi/2},
    "table_2": {"x": 4.0, "y": 1.5, "yaw": math.pi/2},
    "table_3": {"x": 3.5, "y": 0.5, "yaw": math.pi/2},
}

def pose_to_pose_stamped(x, y, yaw):
    ps = PoseStamped()
    ps.header.frame_id = "map"
    ps.header.stamp = rclpy.time.Time().to_msg()
    ps.pose.position.x = x
    ps.pose.position.y = y
    ps.pose.position.z = 0.0

    # Convert yaw to quaternion
    import tf_transformations
    q = tf_transformations.quaternion_from_euler(0, 0, yaw)
    ps.pose.orientation.x = q[0]
    ps.pose.orientation.y = q[1]
    ps.pose.orientation.z = q[2]
    ps.pose.orientation.w = q[3]
    return ps

class ButlerBotSLAM(Node):
    def __init__(self):
        super().__init__('butler_bot_slam')
        self.get_logger().info("ButlerBot with SLAM ready")

        # Nav2 action client
        self.nav_action_client = ActionClient(self, NavigateToPose, 'navigate_to_pose')

        # Services
        self.srv_home = self.create_service(MoveHome, '/move_to_home', self.move_to_home_callback)
        self.srv_pose = self.create_service(MovePose, '/move_to_pose', self.move_pose_callback)

    def move_to_pose(self, pose_name):
        if pose_name not in POSES:
            self.get_logger().error(f"Unknown pose: {pose_name}")
            return False

        # Wait until action server is ready
        while not self.nav_action_client.wait_for_server(timeout_sec=1.0):
            self.get_logger().info('Waiting for Nav2 action server...')

        # Create goal
        goal_msg = NavigateToPose.Goal()
        goal_msg.pose = pose_to_pose_stamped(**POSES[pose_name])

        # Send goal and wait
        future = self.nav_action_client.send_goal_async(goal_msg)
        rclpy.spin_until_future_complete(self, future)
        goal_handle = future.result()

        if not goal_handle.accepted:
            self.get_logger().error(f"Goal to {pose_name} rejected")
            return False

        self.get_logger().info(f"Moving to {pose_name}...")
        result_future = goal_handle.get_result_async()
        rclpy.spin_until_future_complete(self, result_future)
        result = result_future.result().result
        self.get_logger().info(f"Arrived at {pose_name}")
        return True

    def move_to_home_callback(self, request, response):
        success = self.move_to_pose("Home")
        response.success = success
        response.status = "Moved to Home" if success else "Failed to move Home"
        return response

    def move_pose_callback(self, request, response):
        success = self.move_to_pose(request.destination)
        response.success = success
        response.status = f"Moved to {request.destination}" if success else f"Failed to move to {request.destination}"
        return response

def main(args=None):
    rclpy.init(args=args)
    node = ButlerBotSLAM()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()
