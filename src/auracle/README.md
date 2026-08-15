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
sudo apt update && sudo apt install ros-jazzy-ros-gz ros-jazzy-ros2-control ros-jazzy-ros2-controllers ros-jazzy-gz-ros2-control ros-jazzy-twist-mux ros-jazzy-twist-stamper

# Swap gazebo classic plugins for gazebo harmonic plugins in ros2_control.xacro and launch_sim.launch.py, and create yaml files within config folder
my_controllers.yaml — wheel geometry (separation: 0.297, radius: 0.033) is pulled straight from your gazebo_control.xacro. If your real robot's actual wheel measurements differ, update these — wrong values mean the robot drives but odometry will be off.
joystick.yaml — button/axis numbers assume a standard Xbox-layout gamepad (axis 1 = left stick vertical, axis 0 = left stick horizontal, button 4 = LB as the dead-man switch). If you're on keyboard-only or a different controller, this needs adjusting — let me know which and I'll fix the mapping.
twist_mux.yaml — routes both /cmd_vel_joy (your joystick) and /cmd_vel_tracker (from ball_tracker.launch.py) into the single output, joystick taking priority. No lock/e-stop topic configured — fine for now, just flagging it's empty.
gaz_ros2_ctl_use_sim.yaml -- for launching i think idk

# Build and launch
cd ~/Documents/ros2_ws
colcon build --packages-select auracle --symlink-install && source install/setup.bash
ros2 launch auracle launch_sim.launch.py

# Drive around using keyboard (oystick.launch.py is already included in launch_sim.launch.py, remapping teleop output to /cmd_vel_joy)
source install/setup.bash && ros2 run teleop_twist_keyboard teleop_twist_keyboard --ros-args -r /cmd_vel:=/cmd_vel_joy

# Confirm publishing
ros2 topic echo /cmd_vel_joy 
ros2 topic echo /diff_cont/cmd_vel_unstamped

# Install mapping dependencies
sudo apt update && sudo apt install ros-jazzy-slam-toolbox ros-jazzy-navigation2 ros-jazzy-nav2-bringup 

# Launch SLAM_toolbox alongside simulation
ros2 launch auracle online_async_launch.py use_sim_time:=true

# Open rviz 
rviz2

Set Fixed Frame (top left, Global Options) to map
Click Add → By topic → find /map → add the Map display
Optionally add LaserScan on /scan and TF to watch it build live

# Drive around robot with teleop and fill map on rviz
source install/setup.bash && ros2 run teleop_twist_keyboard teleop_twist_keyboard --ros-args -r /cmd_vel:=/cmd_vel_joy

# Save the map via CLI
ros2 run nav2_map_server map_saver_cli -f ~/my_map
