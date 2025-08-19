import rclpy
from rclpy.node import Node
from butler_bot_interfaces.srv import Order

class OrderClient(Node):
    def __init__(self):
        super().__init__('order_client')
        self.cli = self.create_client(Order, 'order')

        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Waiting for order service...')
        
    def send_order(self, table, action, items=None):
        try:
            req = Order.Request()
            req.table = table
            req.action = action
            req.items = items if items else []

            future = self.cli.call_async(req)
            rclpy.spin_until_future_complete(self, future)

            if future.result() is not None:
                self.get_logger().info(f"Order response: {future.result().success}")
            else:
                self.get_logger().error("Service call returned None")
        except Exception as e:
            self.get_logger().error(f"Service call failed: {e}")

def main(args=None):
    rclpy.init(args=args)
    client = OrderClient()

    # Define 10 sample orders
    sample_orders = [
        ("table_1", "book", ["pizza", "coke"]),
        ("table_2", "book", ["burger"]),
        ("table_3", "book", ["pasta"]),
        ("table_1", "cancel", []),
        ("table_2", "cancel", []),
        ("table_3", "book", ["salad", "juice"]),
        ("table_1", "book", ["sandwich"]),
        ("table_2", "book", ["biryani", "lassi"]),
        ("table_3", "book", ["coffee", "cake"]),
        ("table_1", "book", ["noodles"]),
    ]

    print("\n📋 Sample Orders Menu:")
    for i, (table, action, items) in enumerate(sample_orders, start=1):
        print(f"{i}. Table: {table}, Action: {action}, Items: {items}")

    try:
        while rclpy.ok():
            choice = int(input("\n👉 Enter your choice (1-10): "))
            if 1 <= choice <= len(sample_orders):
                table, action, items = sample_orders[choice - 1]
                print(f"\n✅ Sending Order: Table={table}, Action={action}, Items={items}")
                client.send_order(table, action, items)
            else:
                print("❌ Invalid choice")
    except ValueError:
        print("❌ Please enter a number between 1 and 10")

    client.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
