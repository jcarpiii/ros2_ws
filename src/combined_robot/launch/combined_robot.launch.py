from launch import LaunchDescription
from launch_ros.actions import Node
from launch.substitutions import Command, PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare
from launch_ros.parameter_descriptions import ParameterValue

def generate_launch_description():
    xacro_file = PathJoinSubstitution(
        [FindPackageShare('combined_robot'), 'urdf', 'combined_robot.xacro'])

    robot_description = {
        'robot_description': ParameterValue(
            Command(['xacro ', xacro_file]), value_type=str)
    }

    rsp = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[robot_description])

    jsp = Node(                        #‑‑ use GUI **or** non‑GUI publisher
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui')

    rviz = Node(                       #‑‑ add RViz back
        package='rviz2',
        executable='rviz2',
        arguments=[
            '-d',
            PathJoinSubstitution(
                [FindPackageShare('combined_robot'), 'config', 'view.rviz'])
        ])

    return LaunchDescription([jsp, rsp, rviz])