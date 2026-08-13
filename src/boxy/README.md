# Should definitely be in a package
ros2 pkg create --build-type ament_cmake boxy \
        --dependencies rclcpp rclpy \
        --license Apache-2.0 \
        --maintainer-name "Amy Kibara" \
        --maintainer-email "amy.kibara@gmail.com" \
        --description "Just a box"

# create folders for your files
launch -> launch files go here
config -> rviz configs go here
worlds -> gazebo worlds go here
description -> urdfs go here

# edit cmakelists to include new folders at the end before ament_package()
install(
  DIRECTORY launch description config worlds
  DESTINATION share/${PROJECT_NAME}
)

# edit package.xml to include dependencies within <package> tags
<exec_depend>robot_state_publisher</exec_depend>
<exec_depend>joint_state_publisher_gui</exec_depend>
<exec_depend>rviz2</exec_depend>

# URDFs
Just a box with wheels

# Install dependencies
sudo apt install ros-$ROS_DISTRO-joint-state-publisher-gui ros-$ROS_DISTRO-xacro

# Build 
colcon build --symlink-install --packages-select boxy && source install/setup.bash

# Launch file
ros2 launch boxy display.launch.py

# Visualise within rviz
Fixed Frame: In the left "Global Options" panel, change map to base_link.
Add Robot Model: Click the Add button (bottom left), select RobotModel, and click OK. In the RobotModel properties, set Description Topic to /robot_description. To see axes, click Add and select TF. The axes can be moved using the jsp gui.
Add TF (Optional): Click Add and select TF to see the coordinate axes of each part.

# Save and launch config file
On rviz, click file->save config as->save to configs folder. 

# Gazebo edits
Ensure urdf has inertial and collision defined, and add gazebo plugins to urdf
Add Gazebo ROS and plugins to package.xml
<exec_depend>gazebo_ros</exec_depend>
<exec_depend>gazebo_plugins</exec_depend>

# Install dependencies and build 
sudo apt update && sudo apt install ros-jazzy-ros-gz ros-jazzy-gz-ros2-control ros-jazzy-ros-gz-sim
colcon build --symlink-install --packages-select boxy && source install/setup.bash

# Launch
ros2 launch boxy gazebo.launch.py

# Drive it in a new terminal using teleop
ros2 run teleop_twist_keyboard teleop_twist_keyboard
When you press i, the node sends a "speed = 0.5" command. The robot will keep that speed forever until you press k to stop it or send a different command.

# Creating a world that spawns instead of the empty world
Ensure worlds folder added in cmakelists
Instead of empty.sdf it launches in my_room.sdf and add plugins to handle entities and ohysics
Build and run as before. With the collision tags, it shouldn't go past the walls 


