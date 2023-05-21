#!/usr/bin/env python3
# Author: Sarifou DIALLO
# Date : May 21, 2023

import os
from launch import LaunchDescription
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch.substitutions import Command, LaunchConfiguration
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition, UnlessCondition
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    # Find the path of shared folder of this package.
    pkg_path = FindPackageShare(package='visualization').find('visualization')
    # Set the path of the rviz configuration settings
    rviz_config_path = os.path.join(pkg_path, 'config/basic.rviz')
    # Set the path of urdf file
    urdf_path =  os.path.join(pkg_path, 'models/primius.urdf')
    # Specific variable for urdf model
    gui = LaunchConfiguration('gui')
    urdf_model = LaunchConfiguration('urdf_model')
    rviz_config_file= LaunchConfiguration('rviz_config_file')
    use_robot_state_pub = LaunchConfiguration('use_robot_state_pub')
    use_rviz = LaunchConfiguration('use_rviz')
    use_sim_time = LaunchConfiguration('use_sim_time')
    # Declare urdf model for launch argument
    declare_urdf_model_path_cmd = DeclareLaunchArgument(
        name='urdf_model',
        default_value=urdf_path,
        description='Primius model'
    )
    declare_rviz_config_file_cmd = DeclareLaunchArgument(
        name='rviz_config_file',
        default_value=rviz_config_path,
        description='Path to rviz configuration'
    )
    declare_use_joint_state_publisher_cmd = DeclareLaunchArgument(
        name='gui',
        default_value='True',
        description='Flag to enable joint state publisher'
    )
    declare_use_robot_state_pub_cmd = DeclareLaunchArgument(
        name='use_robot_state_pub',
        default_value='True',
        description='Flag to enable robot state publisher'
    )
    declare_use_rviz_cmd = DeclareLaunchArgument(
        name='use_rviz',
        default_value='True',
        description='Flag to enable rviz'
    )
    declare_use_sim_time_cmd = DeclareLaunchArgument(
        name='use_sim_time',
        default_value='True',
        description='Use simulation clock (Gasebo)'
    )
    # Launch Joint State Publisher
    joint_state_pub_launch = Node(
        condition=UnlessCondition(gui),
        package='joint_state_publisher',
        executable='joint_state_publisher',
        name='joint_state_publisher'
    )
    # Launch Joint State Publisher Gui
    joint_state_gui_launch = Node(
        condition=IfCondition(gui),
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui',
        name='joint_state_publisher_gui'
    )
    # Launch Robot State Publisher
    robot_state_pub_launch = Node(
        condition=IfCondition(use_robot_state_pub),
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{'use_sim_time' : use_sim_time,
                     'robot_description' : Command(['xacro ', urdf_model])}],
        arguments=[urdf_path]
    )
    # Launch RVIZ
    rviz_launch = Node (
        condition=IfCondition(use_rviz),
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        arguments= ['-d', rviz_config_file]
    )
    # Create a launch description
    ld = LaunchDescription()
    # Delcare launch options
    ld.add_action(declare_urdf_model_path_cmd)
    ld.add_action(declare_rviz_config_file_cmd)
    ld.add_action(declare_use_joint_state_publisher_cmd)
    ld.add_action(declare_use_robot_state_pub_cmd)
    ld.add_action(declare_use_rviz_cmd)
    ld.add_action(declare_use_sim_time_cmd)
    # Add all actions
    ld.add_action(joint_state_pub_launch)
    ld.add_action(joint_state_gui_launch)
    ld.add_action(robot_state_pub_launch)
    ld.add_action(rviz_launch)
    return ld