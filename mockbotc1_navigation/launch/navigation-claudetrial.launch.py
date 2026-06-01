# Derived from ClaudeAI Sonnet 4.6: https://claude.ai/chat/9b1e5c8c-7a0d-4f1b-8e3c-9a2c6e5f8b2d
# June 1, 2026
# This launch file is for the Navigation stack of MockBotC1,
# which includes the map server and AMCL for localization.
# Need to ensure that the map yaml file and Nav2 params file are correctly specified.

import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():

    # ── Arguments ──────────────────────────────────────────────
    map_yaml_file = LaunchConfiguration('map')
    params_file   = LaunchConfiguration('params_file')
    use_sim_time  = LaunchConfiguration('use_sim_time', default='false')

    declare_map_cmd = DeclareLaunchArgument(
        'map',
        default_value=os.path.join(
            get_package_share_directory('mockbotc1_navigation'),
            'maps', 'map.yaml'),
        description='Full path to the map yaml file')

    declare_params_cmd = DeclareLaunchArgument(
        'params_file',
        default_value=os.path.join(
            get_package_share_directory('mockbotc1_navigation'),
            'config', 'nav2_params.yaml'),
        description='Full path to the Nav2 params file')

    # ── Map Server ──────────────────────────────────────────────
    map_server_node = Node(
        package='nav2_map_server',
        executable='map_server',
        name='map_server',
        output='screen',
        parameters=[{
            'use_sim_time': use_sim_time,
            'yaml_filename': map_yaml_file
        }])

    # ── AMCL (localization on existing map) ────────────────────
    amcl_node = Node(
        package='nav2_amcl',
        executable='amcl',
        name='amcl',
        output='screen',
        parameters=[params_file, {'use_sim_time': use_sim_time}])

    # ── Nav2 Stack ─────────────────────────────────────────────
    nav2_bringup_dir = get_package_share_directory('nav2_bringup')

    nav2_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(nav2_bringup_dir, 'launch', 'navigation_launch.py')),
        launch_arguments={
            'use_sim_time': use_sim_time,
            'params_file':  params_file,
        }.items())

    # ── Lifecycle Manager ──────────────────────────────────────
    # Manages map_server and amcl lifecycle (nav2_bringup handles the rest)
    lifecycle_manager = Node(
        package='nav2_lifecycle_manager',
        executable='lifecycle_manager',
        name='lifecycle_manager_localization',
        output='screen',
        parameters=[{
            'use_sim_time': use_sim_time,
            'autostart':    True,
            'node_names':   ['map_server', 'amcl']
        }])

    return LaunchDescription([
        declare_map_cmd,
        declare_params_cmd,
        map_server_node,
        amcl_node,
        nav2_launch,
        lifecycle_manager,
    ])