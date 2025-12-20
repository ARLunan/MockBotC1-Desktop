# Revised and adopted for the MockBOT Project by AR Lunan Dec 2025
# Removed simulation elements for MockBOTc1-Desktop navigation launch file.
# Sigyn by Wimble Robotics https://github.com/wimblerobotics/Sigyn.git
# Options:
# bt_xml = Full path to behavior tree overriding default_nav_to_pose_bt_xml in the navigation yaml file.
# do_joint_state_gui (false) - Flag to enable joint_state_publisher_gui.
# do_rviz (true) - Launch RViz if true.
# make_map (false) - Make a map vs navigate.
# urdf_file_name (sigyn.urdf.xacro) - URDF file name.
# use_sim_time (true) - Use simulation vs a real robot.
# world (home.world) - World to load if simulating.

import os
import platform
import tempfile
import xacro
import yaml

import launch_ros.actions
from launch import LaunchDescription
from launch.actions import (
    DeclareLaunchArgument,
    ExecuteProcess,
    IncludeLaunchDescription,
    LogInfo,
    OpaqueFunction,
    RegisterEventHandler,
    SetEnvironmentVariable,
    TimerAction,
)
from launch.conditions import IfCondition, UnlessCondition
from launch.event_handlers import OnProcessStart
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import (
    AndSubstitution,
    Command,
    LaunchConfiguration,
    NotSubstitution,
    PathJoinSubstitution,
    # PythonExpression,
)
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    ld = LaunchDescription()
    base_pgk = get_package_share_directory("mockbotc1_navigation")
    rviz_config_path = os.path.join(base_pgk, "rviz", "config.rviz")

    bt_xml = LaunchConfiguration("bt_xml")
    bt_xml_arg = DeclareLaunchArgument(
        "bt_xml",
        default_value="/opt/ros/jazzy/share/nav2_bt_navigator/behavior_trees/navigate_to_pose_w_replanning_and_recovery.xml",
        description="XML to use for nav_to_pose",
    )
    ld.add_action(bt_xml_arg)

    do_rviz = LaunchConfiguration("do_rviz")
    ld.add_action(
        DeclareLaunchArgument(
            name="do_rviz", default_value="true", description="Launch RViz if true"
        )
    )

    make_map = LaunchConfiguration("make_map")
    make_map_arg = DeclareLaunchArgument(
        "make_map", default_value="False", description="Make a map vs navigate"
    )
    ld.add_action(make_map_arg)

    use_sim_time = LaunchConfiguration("use_sim_time")
    use_sim_time_arg = DeclareLaunchArgument(
        "use_sim_time",
        default_value="false",
        description="Simulation mode vs real robot",
    )
    ld.add_action(use_sim_time_arg)

    log_info_action = LogInfo(
        msg=[
            "do_rviz: [",
            do_rviz,
            "], make_map: [",
            make_map,
            "]"
        ]           
    )
    ld.add_action(log_info_action)
   
    # Include the SLAM Toolbox launch file for mapping
    slam_toolbox = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [
                os.path.join(
                    get_package_share_directory("slam_toolbox"),
                    "launch",
                    "online_async_launch.py",
                )
            ],
        ),
        condition=IfCondition(make_map),
        launch_arguments={
            "use_lifecycle_manager": "False",
            "use_sim_time": use_sim_time,
            "slam_params_file": os.path.join(
                base_pgk, "config", "mapper_params_online_async.yaml"
            ),
            # "params_file": "/opt/ros/jazzy/share/slam_toolbox/config/mapper_params_online_async.yaml",
        }.items(),
    )
    ld.add_action(slam_toolbox)

    # Bring up the navigation stack.
    navigation_launch_path = PathJoinSubstitution(
        [base_pgk, "launch", "nav2_bringup.launch.py"]
    )
 
    # map_path_sim = os.path.join(base_pgk, "maps", "map2.yaml")
    map_path_sim = os.path.join(base_pgk, "maps", "my_map.yaml")
    map_path_real = os.path.join(base_pgk, "maps", "my_map.yaml") # "basement_20251220.yaml")
    
    nav2_config_path = os.path.join(
        base_pgk, "config", "navigation_sim.yaml"
        # "/opt/ros/jazzy/share/nav2_bringup/params/nav2_params.yaml"
    )         

    nav2_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(navigation_launch_path),
        launch_arguments={
            "autostart": "True",
            "map": map_path_real,
            "params_file": nav2_config_path,  # Use original config file
            "slam": "False",
            "use_composition": "True",
            "use_respawn": "True",
            "use_sim_time": use_sim_time,
            "use_localization": "True",
            "container_name": "nav2_container",
        }.items(),
    )
    ld.add_action(nav2_launch)
    
    echo_action = ExecuteProcess(
        cmd=["echo", "[sim] Rviz config file path: " + rviz_config_path],
        output="screen",
    )
    ld.add_action(echo_action)
        
    rviz_node = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        condition=IfCondition(LaunchConfiguration("do_rviz")),
        arguments=["-d", rviz_config_path],
    )
    ld.add_action(rviz_node)

    return ld
