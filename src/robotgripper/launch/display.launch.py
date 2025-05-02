#!/usr/bin/env python3
import os
from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    # Get the share directory of your package
    pkg_share = get_package_share_directory('robotgripper')
    # Build absolute paths to your URDF file and RViz config file
    urdf_file = os.path.join(pkg_share, 'urdf', 'urtene_parsed.urdf')
    rviz_config_file = os.path.join(pkg_share, 'config', 'my_robot.rviz')
    
    # Open and read the URDF file so that its contents are stored in the parameter
    with open(urdf_file, 'r') as inf:
        robot_description_content = inf.read()

    return LaunchDescription([
        # Joint State Publisher GUI (if available; else use joint_state_publisher)
        Node(
            package='joint_state_publisher_gui',
            executable='joint_state_publisher_gui',
            name='joint_state_publisher_gui'
        ),
        # Robot State Publisher with the full URDF (including 3D mesh references)
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            parameters=[{'robot_description': robot_description_content}],
        ),
        # RViz2 to visualize the robot model using the loaded robot_description
        Node(
            package='rviz2',
            executable='rviz2',
            arguments=['-d', rviz_config_file],
            output='screen',
        )
    ])

