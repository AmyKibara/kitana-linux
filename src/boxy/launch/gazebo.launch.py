import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node

def generate_launch_description():
    # Start Gazebo Sim with an empty world
    # pkg_boxy = get_package_share_directory('boxy')
    # gz_sim = IncludeLaunchDescription(
    #     PythonLaunchDescriptionSource(
    #         os.path.join(get_package_share_directory('ros_gz_sim'), 'launch', 'gz_sim.launch.py')
    #     ),
    #     launch_arguments={'gz_args': '-r empty.sdf'}.items(),
    # )

    pkg_share = get_package_share_directory('boxy')
    # 1. Path to your custom world file
    world_path = os.path.join(pkg_share, 'worlds', 'my_room.sdf')

    # 2. Start Gazebo Sim with YOUR WORLD
    gz_sim = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory('ros_gz_sim'), 'launch', 'gz_sim.launch.py')
        ),
        # Here we pass the path to our custom world file
        launch_arguments={'gz_args': f'-r {world_path}'}.items(),
    )

    # 3. Robot State Publisher
    urdf_path = os.path.join(pkg_share, 'description', 'my_robot.urdf')
    with open(urdf_path, 'r') as infp:
        robot_desc = infp.read()

    node_robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{'robot_description': robot_desc, 'use_sim_time': True}]
    )

    # 4. Spawn the robot (In Jazzy, use 'create' from ros_gz_sim). Add 0.2m lift for wheel radius of 0.1m
    gz_spawn_entity = Node(
        package='ros_gz_sim',
        executable='create',
        #arguments=['-topic', 'robot_description', '-name', 'boxy', '-allow_renaming', 'true', '-z', '0.2'],
        arguments=[
        '-file', urdf_path,  # Use the file path instead of -topic
        '-name', 'boxy',
        '-allow_renaming', 'true',
        '-z', '0.3'          # Lift it a bit higher
        ],
        output='screen',
    )

    # 5. Bridge ROS and Gazebo topics (IMPORTANT for Jazzy)
    # This bridges cmd_vel and odom so you can drive the robot
    bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=[
            '/cmd_vel@geometry_msgs/msg/Twist@gz.msgs.Twist',
            '/odom@nav_msgs/msg/Odometry@gz.msgs.Odometry',
            '/tf@tf2_msgs/msg/TFMessage@gz.msgs.Pose_V',
            '/joint_states@sensor_msgs/msg/JointState@gz.msgs.Model',
        ],
        output='screen'
    )

    return LaunchDescription([
        gz_sim,
        node_robot_state_publisher,
        gz_spawn_entity,
        bridge
    ])