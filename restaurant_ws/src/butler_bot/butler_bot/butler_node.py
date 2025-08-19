#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from butler_bot_interfaces.srv import MoveHome, MovePose
import math
import time

class ButlerBot(Node):
    def __init__(self):
        super().__init__('butler_bot_node')
        print("ButlerBot ready to receive service calls")

        # Publisher for velocity commands
        self.cmd_pub = self.create_publisher(Twist, '/cmd_vel', 10)

        # Create services
        self.srv_home = self.create_service(MoveHome, '/move_to_home', self.move_to_home_callback)
        self.srv_pose = self.create_service(MovePose, '/move_to_pose', self.move_pose_callback)

    # --- Movement functions ---
    def move_forward(self, distance, speed=0.2):
        duration = distance / speed
        end_time = self.get_clock().now().nanoseconds / 1e9 + duration
        twist = Twist()
        twist.linear.x = speed
        while self.get_clock().now().nanoseconds / 1e9 < end_time:
            self.cmd_pub.publish(twist)
            rclpy.spin_once(self, timeout_sec=0.1)
        twist.linear.x = 0.0
        self.cmd_pub.publish(twist)

    def rotate(self, angle_deg, angular_speed=0.5):
        angle_rad = math.radians(angle_deg)
        duration = abs(angle_rad) / angular_speed
        end_time = self.get_clock().now().nanoseconds / 1e9 + duration
        twist = Twist()
        twist.angular.z = angular_speed if angle_rad > 0 else -angular_speed
        while self.get_clock().now().nanoseconds / 1e9 < end_time:
            self.cmd_pub.publish(twist)
            rclpy.spin_once(self, timeout_sec=0.1)
        twist.angular.z = 0.0
        self.cmd_pub.publish(twist)

    # --- Service callbacks ---
    def move_to_home_callback(self, request, response):
        print("Service call: Moving to Home position")
        # Example: move backward a bit and rotate to home orientation
        self.rotate(-90)
        self.move_forward(2.0)
        response.status = "Moved to Home"
        response.success = True
        return response

    def move_pose_callback(self, request, response):
        valid_destinations = {
            "Kitchen": (2.5, 0.0, 0),
            "table_1": (2.5, 1.0, 90),
            "table_2": (2.5, -1.0, -90),
            "table_3": (3.5, 0.0, 0)
        }

        dest = request.destination
        if dest in valid_destinations:
            x, y, yaw = valid_destinations[dest]
            print(f"Service call: Moving to {dest}")
            # For simplicity, move forward by x (tune for your Gazebo world)
            self.move_forward(x)
            self.rotate(yaw)
            self.move_forward(y)
            response.status = f"Moved to {dest}"
            response.success = True
        else:
            print(f"Invalid destination: {dest}")
            response.status = "Invalid destination!"
            response.success = False

        return response


def main(args=None):
    rclpy.init(args=args)
    node = ButlerBot()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
