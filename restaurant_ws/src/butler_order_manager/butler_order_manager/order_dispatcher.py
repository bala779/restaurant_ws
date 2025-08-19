import rclpy, time
from rclpy.node import Node
from rclpy.action import ActionClient
from butler_order_manager.utils import *
from butler_bot_interfaces.action import OrderExecutor


class Dispatcher(Node):
    def __init__(self):
        super().__init__("order_dispatcher")
        try:
            self.client = ActionClient(self, OrderExecutor, "execute_order")
            self.timer = self.create_timer(3.0, self.check_orders)
            self.active = False
        except Exception as e:
            log_print(f"Dispatcher: Error initializing node: {e}")

    def check_orders(self):
        try:
            if self.active:
                return
            orders = get_order_list()
            if not orders:
                return
            self.send_goal(orders[0])
        except Exception as e:
            log_print(f"Dispatcher: Error checking orders: {e}")

    def send_goal(self, order):
        try:
            goal_msg = OrderExecutor.Goal()
            goal_msg.table_name = order.get("table", "unknown")
            goal_msg.items = ', '.join(order.get("items", []))

            set_current_order_table(goal_msg.table_name)
            log_print(f"Orders List: {get_order_list}")
            remove_order(goal_msg.table_name)

            if not self.client.wait_for_server(timeout_sec=5.0):
                log_print("Dispatcher: Action server not available")
                self.active = False
                return

            self.active = True
            self.future = self.client.send_goal_async(goal_msg, feedback_callback=self.feedback_cb)
            self.future.add_done_callback(self.goal_response_cb)

        except Exception as e:
            log_print(f"Dispatcher: Error sending goal: {e}")
            self.active = False

    def goal_response_cb(self, future):
        try:
            goal_handle = future.result()
            if not goal_handle.accepted:
                log_print("Dispatcher: Goal rejected")
                self.active = False
                return

            self.result_future = goal_handle.get_result_async()
            self.result_future.add_done_callback(self.result_cb)

        except Exception as e:
            log_print(f"Dispatcher: Error in goal response: {e}")
            self.active = False

    def feedback_cb(self, feedback):
        try:
            log_print(f"Dispatcher: Feedback: {feedback.feedback.status}")
        except Exception as e:
            log_print(f"Dispatcher: Error in feedback callback: {e}")

    def result_cb(self, future):
        try:
            result = future.result().result
            log_print(f"Dispatcher: Result: {result.success}, {result.message}")
        except Exception as e:
            log_print(f"Dispatcher: Error in result callback: {e}")
        finally:
            self.active = False


def main():
    try:
        rclpy.init()
        node = Dispatcher()
        rclpy.spin(node)
    except Exception as e:
        log_print(f"Dispatcher: Node exception: {e}")
    finally:
        try:
            node.destroy_node()
        except:
            pass
        rclpy.shutdown()


if __name__ == "__main__":
    main()
