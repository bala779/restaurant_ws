#!/usr/bin/env python3
import time, sys
import rclpy
from rclpy.node import Node
from rclpy.action import ActionServer, GoalResponse, CancelResponse
from rclpy.callback_groups import ReentrantCallbackGroup
from std_msgs.msg import Int32
from std_srvs.srv import Trigger

from butler_bot_interfaces.srv import MoveHome, MovePose
from butler_bot_interfaces.action import OrderExecutor
from butler_order_manager.utils import log_print

YELLOW, GREEN, RED, CYAN, RESET = "\033[93m", "\033[92m", "\033[91m", "\033[96m", "\033[0m"

class OrderExecutorServer(Node):
    def __init__(self):
        super().__init__("order_executor_server")
        self.cb_group = ReentrantCallbackGroup()
        self._action_server = ActionServer(self, OrderExecutor, "execute_order",
                                           execute_callback=self.execute_cb,
                                           cancel_callback=self.cancel_cb,
                                           goal_callback=self.goal_cb,
                                           callback_group=self.cb_group)
        self._load_status = 0
        self.sub = self.create_subscription(Int32, "/load_machine_status", self.load_status_cb, 10)
        self.food_delivered = False
        self.order_cancelled = False
        self.move_home_client = self.create_client(MoveHome, "/move_to_home", callback_group=self.cb_group)
        self.move_pose_client = self.create_client(MovePose, "/move_to_pose", callback_group=self.cb_group)
        self.cancel_service = self.create_service(Trigger, 'cancel_current_order', self.cancel_current_order_cb)
        
        while not self.move_home_client.wait_for_service(timeout_sec=1.0):
            log_print("Waiting for /move_to_home service...")
        while not self.move_pose_client.wait_for_service(timeout_sec=1.0):
            log_print("Waiting for /move_to_pose service...")
        log_print("OrderExecutor: Server ready.")
        self.move_to("Home")

    def load_status_cb(self, msg: Int32):
        self._load_status = msg.data

    def goal_cb(self, goal_request):
        log_print(f"Received goal [{goal_request.table_name}, {goal_request.items}]")
        return GoalResponse.ACCEPT

    def cancel_cb(self, goal_handle):
        log_print("Cancel request received!")
        return CancelResponse.ACCEPT

    def execute_cb(self, goal_handle):
        table, items = goal_handle.request.table_name, goal_handle.request.items
        self.print_header(table, items)
        feedback = OrderExecutor.Feedback()

        try:
            # BT Sequence
            steps = [
                ("Kitchen", "Moving to Kitchen", "move"),
                ("WaitLoad", "Waiting for load at Kitchen", "wait", 1),
                (table, f"Delivering to {table}", "move"),
                ("WaitUnload", f"Waiting for unload at {table}", "wait", 0),
                ("Home", "Returning Home", "move")
            ]

            for step in steps:
                dest, msg, action_type, *expected = step
                if self.order_cancelled:
                    return self.handle_cancel(goal_handle, msg)
                feedback.status = msg
                goal_handle.publish_feedback(feedback)

                if action_type == "move":
                    if not self.move_to(dest):
                        return self.handle_cancel(goal_handle)
                elif action_type == "wait":
                    if not self.wait_for_state(expected[0], msg):
                        return self.handle_cancel(goal_handle)

            goal_handle.succeed()
            return OrderExecutor.Result(success=True, message="Delivery completed")

        except Exception as e:
            log_print(f"Exception: {e}")
            return self.handle_cancel(goal_handle, "Exception raised")

    def wait_for_state(self, expected: int, msg: str, timeout=20) -> bool:
        start = time.time()
        while time.time() - start < timeout:
            rclpy.spin_once(self, timeout_sec=0.1)
            if self._load_status == expected:
                print(f"{msg} SUCCESS")
                return True
        print(f"{msg} TIMEOUT")
        return False

    def handle_cancel(self, goal_handle, step):
        try:
            log_print(f"Order canceled at step {step}, moving to safe state")
            if self._load_status == 1:
                self.move_to("Kitchen")
                for _ in range(10):
                    if self._load_status == 0: break
                    time.sleep(1)           
                else:
                    self._load_status = 0
            self.move_to("Home")
        except Exception as s:
            log_print(f"Exception raised in handel_cancel! {s}")
        finally:
            self.order_cancelled = False
            goal_handle.abort()
            return OrderExecutor.Result(success=False, message="Order canceled safely")

    def move_to(self, dest: str) -> bool:
        try:
            req = MoveHome.Request() if dest=="Home" else MovePose.Request()
            if dest != "Home": req.destination = dest
            future = self.move_home_client.call_async(req) if dest=="Home" else self.move_pose_client.call_async(req)
            rclpy.spin_until_future_complete(self, future)
            result = future.result()
            log_print(f"Reached {dest} [{result.status}]") if result.success else log_print(f"Failed {dest} [{result.status}]")
            return result.success
        except Exception as e:
            log_print(f"Move service failed: {e}")
            return False

    def cancel_current_order_cb(self, request, response):
        # if self.food_delivered:
        #     response.message = "Already in delivery"
        #     log_print(f"Order couldn't already in delivery!")
        # else:
        self.order_cancelled = True
        response.message = "Order canceled"
        log_print(f"Cancel Requset intiated.")

        response.success = True
        return response

    def print_header(self, table, items):
        w = 78
        print(f"\n{YELLOW}{'='*w}{RESET}")
        print(f"{GREEN}Executing Order{RESET}".center(w))
        print(f"{CYAN}Table : {table}{RESET}".center(w))
        print(f"{CYAN}Items : {items}{RESET}".center(w))
        print(f"{YELLOW}{'='*w}{RESET}\n")


def main(args=None):
    rclpy.init(args=args)
    node = OrderExecutorServer()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()
