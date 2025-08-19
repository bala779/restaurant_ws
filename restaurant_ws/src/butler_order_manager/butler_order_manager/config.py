import os

PACKAGE_PATH = os.path.dirname(__file__)

ORDERS_FILE = os.path.join(PACKAGE_PATH, 'orders.json')
STATUS_FILE = os.path.join(PACKAGE_PATH, 'status.json')
CURRENT_FILE = os.path.join(PACKAGE_PATH, 'current_order.json')

TABLES = ["table_1", "table_2", "table_3", "kitchen", "home"]

MOVE_DELAY = 2
WAIT_LOAD_DELAY = 10
WAIT_UNLOAD_DELAY = 10

LOAD_TOPIC = '/load_machine'
