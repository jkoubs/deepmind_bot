#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_prefix
from launch.substitutions import LaunchConfiguration, Command
from launch.conditions import IfCondition, UnlessCondition


def generate_launch_description():
    # Get the package directories
    pkg_gazebo_ros = get_package_share_directory('gazebo_ros')
    pkg_deepmind_bot_gazebo = get_package_share_directory('deepmind_bot_gazebo')

    # Determine paths for robot descriptions and plugins
    description_package_name = "deepmind_bot_description"
    install_dir = get_package_prefix(description_package_name)
    gazebo_models_path = os.path.join(pkg_deepmind_bot_gazebo, 'models')

    gazebo_plugins_name = "gazebo_plugins"
    gazebo_plugins_name_path_install_dir = get_package_prefix(gazebo_plugins_name)

    # Update the GAZEBO_MODEL_PATH and GAZEBO_PLUGIN_PATH environment variables
    os.environ['GAZEBO_MODEL_PATH'] = os.pathsep.join([
        os.environ.get('GAZEBO_MODEL_PATH', ''),
        os.path.join(install_dir, 'share'),
        gazebo_models_path
    ]).strip(':')

    os.environ['GAZEBO_PLUGIN_PATH'] = os.pathsep.join([
        os.environ.get('GAZEBO_PLUGIN_PATH', ''),
        os.path.join(install_dir, 'lib'),
        os.path.join(gazebo_plugins_name_path_install_dir, 'lib')
    ]).strip(':')

    # Print paths for debugging
    print("GAZEBO MODELS PATH=="+str(os.environ["GAZEBO_MODEL_PATH"]))
    print("GAZEBO PLUGINS PATH=="+str(os.environ["GAZEBO_PLUGIN_PATH"]))

    # Define launch arguments
    world_file_arg = LaunchConfiguration('world')
    verbose_arg = LaunchConfiguration('verbose')
    gzweb_arg = LaunchConfiguration('gzweb')

    # Define launch actions for Gazebo server and client, using the world file specified by the launch argument
    gzserver = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(pkg_gazebo_ros, 'launch', 'gzserver.launch.py')),
        launch_arguments={
            'world': world_file_arg,
            'verbose': verbose_arg  # Pass the verbose argument
        }.items(),
        condition=IfCondition(gzweb_arg)
    )
    
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(pkg_gazebo_ros, 'launch', 'gazebo.launch.py')),
        condition=UnlessCondition(gzweb_arg)
    )

    # Return the launch description, including the declaration of the 'world' argument
    return LaunchDescription([
        DeclareLaunchArgument(
            'world',
            default_value=os.path.join(pkg_deepmind_bot_gazebo, 'worlds', 'room.world'),
            description='Path to the SDF world file'),
        DeclareLaunchArgument(
            'verbose', default_value='true',
            description='Set "true" to increase messages written to the terminal.'
        ),
        DeclareLaunchArgument(
            'gzweb',
            default_value='false',  # Adjust based on preference
            description='Launch Gazebo with gzweb'
        ),
        gzserver,
        gazebo
    ])
