#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32
from butler_order_manager.utils import log_print
import time
import random

class LoadMachineSim(Node):
    """
    Simulates the load/unload sensor.
    Publishes:
        /load_machine_status : Int32 (1 = loaded, 0 = unloaded)
    """

    def __init__(self):
        super().__init__('load_machine_sim')
        self.publisher_ = self.create_publisher(Int32, '/load_machine_status', 10)
        log_print("LoadMachineSim: Load Machine Publisher started")

    def publish_value(self, value: int, duration: float = 2.0, hz: float = 10.0):
        """Publish `value` continuously for given duration."""
        msg = Int32()
        msg.data = value
        end_time = time.time() + duration
        rate = 1.0 / hz

        while time.time() < end_time:
            self.publisher_.publish(msg)
            log_print(f'LoadMachineSim: Publishing: {msg.data}')
            time.sleep(rate)

    def publish_random(self, delay: float = 2.0):
        """Continuously publish random values every `delay` seconds."""
        try:
            while rclpy.ok():
                msg = Int32()
                msg.data = random.choice([0, 1])
                self.publisher_.publish(msg)
                log_print(f'LoadMachineSim: Auto Random Publishing: {msg.data}')
                time.sleep(delay)
        except KeyboardInterrupt:
            pass


def main():
    rclpy.init()
    node = LoadMachineSim()

    log_print("Choose mode:")
    log_print("1. Manual Mode (type values 0/1)")
    log_print("2. Auto Mode (random publish every 2s)")

    mode = input("Enter option (1 or 2): ")

    if mode.strip() == "2":
        node.publish_random(delay=2.0)
    else:
        try:
            while rclpy.ok():
                user_in = input("Enter sensor value (1=loaded, 0=unloaded, q=quit): ")
                if user_in.lower() == 'q':
                    break
                elif user_in in ['0', '1']:
                    node.publish_value(int(user_in))
                else:
                    log_print("LoadMachineSim: Invalid input. Please enter 1, 0, or q.")
        except KeyboardInterrupt:
            pass

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
