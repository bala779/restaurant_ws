#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from nav2_msgs.action import NavigateToPose
from rclpy.action import ActionClient
from geometry_msgs.msg import PoseStamped
import math
from butler_bot.poses import home_pose, table1, table2, table3, kitchen

class MoveRobot(rclpy.node.Node):
    def __init__(self):
        super().__init__('move_robot')
        self.client = ActionClient(self, NavigateToPose, 'navigate_to_pose')

    def move_to(self, pose_dict):
        goal_msg = NavigateToPose.Goal()
        goal_msg.pose.header.frame_id = 'map'
        goal_msg.pose.header.stamp = self.get_clock().now().to_msg()
        goal_msg.pose.pose.position.x = pose_dict['x']
        goal_msg.pose.pose.position.y = pose_dict['y']

        # Convert yaw to quaternion
        yaw = pose_dict['yaw']
        goal_msg.pose.pose.orientation.z = math.sin(yaw / 2.0)
        goal_msg.pose.pose.orientation.w = math.cos(yaw / 2.0)

        self.client.wait_for_server()

        # Send goal asynchronously
        send_goal_future = self.client.send_goal_async(goal_msg)
        rclpy.spin_until_future_complete(self, send_goal_future)
        goal_handle = send_goal_future.result()

        if not goal_handle.accepted:
            self.get_logger().info('Goal rejected :(')
            return None

        # Get result
        get_result_future = goal_handle.get_result_async()
        rclpy.spin_until_future_complete(self, get_result_future)
        result = get_result_future.result().result

        self.get_logger().info("Reached destination!")
        return result


def main(args=None):
    rclpy.init(args=args)
    mover = MoveRobot()
    
    # Example: move to table1, then home
    mover.move_to(table1)
    mover.move_to(home_pose)
    
    mover.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
