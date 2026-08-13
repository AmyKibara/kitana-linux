# package creation -- within ros2_ws/src
ros2 pkg create --build-type ament_cmake auracle \
        --dependencies rclcpp rclpy \
        --license Apache-2.0 \
        --maintainer-name "Amy Kibara" \
        --maintainer-email "amy.kibara@gmail.com" \
        --description "Auracle robot"

# include directories in cmakelists
install(
  DIRECTORY launch description config worlds
  DESTINATION share/${PROJECT_NAME}
)

# Build
cd ~/Documents/ros2_ws
colcon build --symlink-install --packages-select auracle && source install/setup.bash

# Launch rsp - linked to robot.urdf.xacro
ros2 launch auracle rsp.launch.py use_sim_time:=false use_ros2_control:=false

# Publish joint states
source ~/Documents/ros2_ws/install/setup.bash && ros2 run joint_state_publisher_gui joint_state_publisher_gui

# Launch rviz2
rviz2

# Within rviz
Set Fixed Frame (top left, Global Options) to base_link (or base_footprint if your urdf uses one).
Click Add → RobotModel, and set its Description Topic to /robot_description.
Optionally Add → TF to see the frames.

# Save configuration in config files and launch from config (launch->jsp->default_rviz)
ros2 run rviz2 rviz2 -d ~/Documents/ros2_ws/src/auracle/config/default_rviz.rviz

# Create similar folder structure to one in auracle github and copy worlds and models



