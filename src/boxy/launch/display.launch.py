import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    package_name = 'boxy' # Your package name

    pkg_share = get_package_share_directory(package_name)

    urdf_path = os.path.join(pkg_share, 'description', 'my_robot.urdf')

    with open(urdf_path, 'r') as infp:
        robot_description_config = infp.read()

    return LaunchDescription([
        # Publishes the robot model
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            output='screen',
            parameters=[{'robot_description': robot_description_config}]
        ),
        # Opens a GUI slider to move the wheels
        Node(
            package='joint_state_publisher_gui',
            executable='joint_state_publisher_gui',
            name='joint_state_publisher_gui'
        ),
        # Opens RViz
        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            output='screen'
        )
    ])