import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
import xacro

def generate_launch_description():
    # Declare launch arguments
    use_sim_time = LaunchConfiguration('use_sim_time')
    declare_use_sim_time_cmd = DeclareLaunchArgument(
        'use_sim_time',
        default_value='false',
        description='Use simulation (Gazebo) clock if true'
    )

    # Get the path to the robot description file
    pkg_path = os.path.join(get_package_share_directory('articubot'))
    xacro_file = os.path.join(pkg_path, 'description', 'bot.urdf.xacro')

    # Process xacro file into plain URDF XML string
    robot_description_config = xacro.process_file(xacro_file).toxml()

    # Create a robot_state_publisher node
    node_robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[{
            'robot_description': robot_description_config,
            'use_sim_time': use_sim_time
            }]
    )

    # Launch!
    return LaunchDescription([
        declare_use_sim_time_cmd,
        node_robot_state_publisher
    ])