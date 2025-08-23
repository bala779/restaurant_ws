# Butler Bot - Restaurant Automation (ROS 2)

Butler Bot is a ROS 2 based restaurant automation simulation that manages customer orders and executes robot navigation in a Gazebo environment.  
It demonstrates order handling, task execution, and robot movement services

---

## Features
- **Order Management**: Handle new and canceled orders using services and actions.  
- **Order Dispatcher**: Publishes active orders to the robot executor.  
- **Order Executor**: Executes tasks, monitors tray status, and controls robot navigation.  
- **Custom Robot**: Mobile robot URDF with LiDAR and differential drive.  
- **Simulation**: Restaurant environment with map and robot movement using SLAM & Nav2  

---

## Package Structure
- `butler_bot` → Robot description, controllers, navigation setup  
- `butler_order_manager` → Order stack handling, services, and action servers  
- `butler_bot_interfaces` → Custom `.srv` and `.action` definitions (planned / pending setup)  
- `my_robot_description` → URDF model for the robot  
- `my_robot_bringup` → Launch files for simulation and testing     

---

## How to Build
```bash
# Build packages
colcon build --symlink-install
source install/setup.bash

# Launch simulation
ros2 launch my_robot_bringup restaurant_sim.launch.py

# Send order
ros2 service call /order_server butler_bot_interfaces/srv/Order "{order_id: 1}"

export GAZEBO_MODEL_PATH={your_ws_path}/restaurant_ws/src/restaurant/models

## 7. How to Run
# Launch Restaurant + Bot
ros2 launch butler_bot butler_restaurant_env.launch.py

# Start Order Manager
ros2 launch butler_order_manager butler_order_manager.launch.py

# Order/Cancel:
ros2 run butler_order_manager order_client

# Load Machine Sensor Simulation
ros2 run butler_bot load_machine_sim

