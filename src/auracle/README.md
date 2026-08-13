# package creation -- within ros2_ws/src
ros2 pkg create --build-type ament_cmake auracle \
        --dependencies rclcpp rclpy \
        --license Apache-2.0 \
        --maintainer-name "Amy Kibara" \
        --maintainer-email "amy.kibara@gmail.com" \
        --description "Auracle robot"

# include directories in cmakelists
install(
  DIRECTORY launch description config worlds models
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
Add worlds and models folders

# Install dependencies
sudo apt update && sudo apt install ros-jazzy-ros-gz ros-jazzy-ros2-control ros-jazzy-ros2-controllers ros-jazzy-gz-ros2-control ros-jazzy-twist-mux

# Swap gazebo classic plugins for gazebo harmonic plugins in ros2_control.xacro and launch_sim.launch.py


# Build and launch
cd ~/Documents/ros2_ws
colcon build --packages-select auracle --symlink-install && source install/setup.bash
ros2 launch auracle launch_sim.launch.py

# Drive around using keyboard (oystick.launch.py is already included in launch_sim.launch.py, remapping teleop output to /cmd_vel_joy. However twist_mux.yaml and joystick.yaml don't exixt, so rerouting wont happen)
ros2 run teleop_twist_keyboard teleop_twist_keyboard --ros-args -r /cmd_vel:=/cmd_vel_joy



