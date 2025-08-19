#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from butler_bot_interfaces.srv import MoveHome, MovePose
import time


class ButlerBot(Node):
    """ButlerBot service node handling movement requests."""

    def __init__(self):
        super().__init__('butler_bot_node')

        # Create service servers
        self.srv_home = self.create_service(MoveHome, 'move_to_home', self.move_to_home_callback)
        self.srv_pose = self.create_service(MovePose, 'move_to_pose', self.move_pose_callback)

        self.valid_destinations = ["Kitchen", "table_1", "table_2", "table_3"]

        self.get_logger().info("ButlerBot is ready to receive service calls.")

    def move_to_home_callback(self, request, response):
        """Callback for moving robot to home position."""
        self.get_logger().info("Received request: Move to Home position")

        # Simulated execution
        time.sleep(5)

        response.status = "Moved to Home"
        response.success = True
        self.get_logger().info("Successfully moved to Home position")

        return response

    def move_pose_callback(self, request, response):
        """Callback for moving robot to a specific destination."""
        destination = request.destination

        if destination in self.valid_destinations:
            self.get_logger().info(f"Received request: Move to {destination}")

            # Simulated execution
            time.sleep(5)

            response.status = f"Moved to {destination}"
            response.success = True
            self.get_logger().info(f"Successfully moved to {destination}")
        else:
            self.get_logger().warn(f"Invalid destination requested: {destination}")
            response.status = "Invalid destination!"
            response.success = False

        return response

def main(args=None):
    rclpy.init(args=args)
    node = ButlerBot()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info("Shutting down ButlerBot service node...")
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
