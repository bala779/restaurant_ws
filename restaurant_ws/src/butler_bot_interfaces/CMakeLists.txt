cmake_minimum_required(VERSION 3.5)
project(butler_bot_interfaces)

find_package(ament_cmake REQUIRED)
find_package(rosidl_default_generators REQUIRED)
find_package(std_msgs REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(action_msgs REQUIRED)
find_package(rclcpp REQUIRED)
find_package(rclpy REQUIRED)

# Generate services and actions
rosidl_generate_interfaces(${PROJECT_NAME}
  "srv/MoveHome.srv"
  "srv/MovePose.srv"
  "srv/Order.srv"
  "action/OrderExecutor.action"
  DEPENDENCIES std_msgs geometry_msgs action_msgs
)

ament_package()
