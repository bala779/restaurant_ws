import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from butler_bot_interfaces.srv import Order
from butler_bot_interfaces.action import OrderExecutor
from butler_order_manager.utils import *
from std_srvs.srv import Trigger

class OrderServer(Node):
    def __init__(self):
        super().__init__('order_server')
        clear_all_caches()
        self.order_queue = get_order_list()
        
        # Service for receiving orders
        self.srv = self.create_service(Order, 'order', self.order_callback)
        self.cancel_client = self.create_client(Trigger, 'cancel_current_order')

        log_print(f"OrderServer: Ready to receive orders.")
        self.get_logger().info("OrderServer ready!")

    def order_callback(self, request, response):
        action = request.action.strip().lower()
        table_id = request.table.strip()

        if action == "book":
            return self.book_order(table_id, request.items, response)
        elif action == "cancel":
            return self.cancel_order(table_id, response)
        else:
            log_print(f"OrderServer: Invalid action '{request.action}'")
            response.success = False
            return response

    def book_order(self, table_id, items, response):

        # Add new order
        new_order = {"table": table_id, "items": items}
        add_order(new_order)
        log_print(f"OrderServer: Added order for table {table_id}: {items}")

        response.success = True
        orders = get_order_list()
        log_print(f"OrderServer: {table_id} order Added in the stack- {len(orders)} is Pending. Orders list - {orders}")

        return response

    def cancel_order(self, table_id, response):
        """
        Cancel an order for a given table.
        Handles both currently executing orders and queued orders.
        """
        try:
            current_table = get_current_order_table()
            if current_table == table_id:
                log_print(f"OrderServer: Cancelling active order for table {table_id}")

                if not self.cancel_client.wait_for_service(timeout_sec=5.0):
                    log_print("OrderExecutor cancel service not ready")
                    response.success = False
                    return response

                future = self.cancel_client.call_async(Trigger.Request())
                rclpy.spin_until_future_complete(self, future, timeout_sec=3)

                if future.result() and future.result().success:
                    log_print(f"OrderServer: Active order cancelled successfully")
                    response.success = True
                else:
                    log_print(f"OrderServer: Failed to cancel active order")
                    response.success = False

            else:
                # Cancel queued orders safely
                if remove_order(table_id):
                    log_print(f"OrderServer: Order for table {table_id} removed from queue")
                    response.success = True
                else:
                    log_print(f"OrderServer: No order found for table {table_id} in queue")
                    response.success = False

        except Exception as e:
            log_print(f"OrderServer: Exception while cancelling order: {e}")
            response.success = False

        return response

def main(args=None):
    rclpy.init(args=args)
    node = OrderServer()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()
