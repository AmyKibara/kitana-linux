import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, SetEnvironmentVariable, RegisterEventHandler
from launch.event_handlers import OnProcessStart
from launch.launch_description_sources import PythonLaunchDescriptionSource

from launch_ros.actions import Node

def generate_launch_description():

    package_name = 'auracle'

    world_path = os.path.join(get_package_share_directory(package_name), 'worlds', 'gamefield.world')
    models_path = os.path.join(get_package_share_directory(package_name), 'models')

    set_gz_resource_path = SetEnvironmentVariable(
        name='GZ_SIM_RESOURCE_PATH',
        value=models_path
    )

    rsp = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory(package_name),'launch','rsp.launch.py'
        )]), launch_arguments={'use_sim_time': 'true', 'use_ros2_control': 'true'}.items()
    )

    joystick = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory(package_name),'launch','joystick.launch.py'
        )]), launch_arguments={'use_sim_time': 'true'}.items()
    )

    twist_mux_params = os.path.join(get_package_share_directory(package_name),'config','twist_mux.yaml')
    twist_mux = Node(
        package="twist_mux",
        executable="twist_mux",
        parameters=[twist_mux_params, {'use_sim_time': True}],
        remappings=[('/cmd_vel_out','/diff_cont/cmd_vel_unstamped')]
    )

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('ros_gz_sim'), 'launch', 'gz_sim.launch.py')]),
            launch_arguments={'gz_args': ['-r ', world_path]}.items()
    )

    # Spawn position lowered slightly so wheels sit closer to ground level
    spawn_entity = Node(
        package='ros_gz_sim', 
        executable='create',
        arguments=[
            '-topic', 'robot_description',
            '-name', 'my_bot', 
            '-x', '-2.6',
            '-y', '-1.3',
            '-z', '0.15',  # <--- Lowered from 0.25 so it settles immediately
            '-R', '0.0',
            '-P', '0.0',
            '-Y', '1.57'
        ],
        output='screen'
    )

    # Clock bridge
    gz_bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=['/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock'],
        output='screen'
    )

    # Controller spawners
    diff_drive_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["diff_cont"],
    )

    joint_broad_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joint_broad"],
    )

    # DELAY CONTROLLER SPAWNERS UNTIL ROBOT IS CREATED IN GAZEBO
    delayed_diff_drive_spawner = RegisterEventHandler(
        event_handler=OnProcessStart(
            target_action=spawn_entity,
            on_start=[diff_drive_spawner],
        )
    )

    delayed_joint_broad_spawner = RegisterEventHandler(
        event_handler=OnProcessStart(
            target_action=spawn_entity,
            on_start=[joint_broad_spawner],
        )
    )

    return LaunchDescription([
        set_gz_resource_path,
        rsp,
        joystick,
        twist_mux,
        gazebo,
        gz_bridge,
        spawn_entity,
        delayed_diff_drive_spawner,
        delayed_joint_broad_spawner
    ])