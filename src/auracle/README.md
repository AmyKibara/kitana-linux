# package creation
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
colcon build --packages-select auracle
source install/setup.bash


