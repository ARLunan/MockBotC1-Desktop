### Launch Commands (using nav2_bringup directly)

# Terminal 1 — already running: robot base + ekf_node

# Terminal 2 — Nav2 + map server + AMCL
ros2 launch your_robot_bringup navigation.launch.py \
    map:=/path/to/your/map.yaml \
    params_file:=/path/to/nav2_params.yaml

# Terminal 3 — RViz (optional)
ros2 launch your_robot_bringup rviz_nav2.launch.py

# Terminal 4 — Set initial pose (if not set in params)
ros2 topic pub /initialpose geometry_msgs/PoseWithCovarianceStamped \
  "{ header: {frame_id: map}, pose: { pose: { position: {x: 0.0, y: 0.0}, orientation: {w: 1.0} } } }" --once

#  Key Things to Verify
# Confirm TF tree is complete
ros2 run tf2_tools view_frames

# Check map is being served
ros2 topic echo /map --once

# Check AMCL is publishing the map→odom transform
ros2 run tf2_ros tf2_echo map odom

# Check Nav2 nodes are active
ros2 lifecycle list
Once AMCL converges (use 2D Pose Estimate in RViz to set initial pose), you can send navigation goals via Nav2 Goal in RViz or programmatically via the NavigateToPose action server.

# Launch Commands (using nav2_bringup directly)
# Terminal 1 — Map Server + AMCL (localization)
ros2 launch nav2_bringup localization_launch.py \
  map:=/path/to/your/map.yaml \
  use_sim_time:=false \
  params_file:=/path/to/nav2_params.yaml
# Terminal 2 — Nav2 Navigation Stack
ros2 launch nav2_bringup navigation_launch.py \
  use_sim_time:=false \
  params_file:=/path/to/nav2_params.yaml \
  map_subscribe_transient_local:=true
# Terminal 3 — RViz (optional, nav2_bringup includes it)
ros2 launch nav2_bringup rviz_launch.py \
  use_sim_time:=false \
  rviz_config_file:=$(ros2 pkg prefix nav2_bringup)/share/nav2_bringup/rviz/nav2_default_view.rviz


# Quick Reference: All bringup_launch.py Parameters
Parameter Default Notes
map""Full path to map.yaml
use_sim_time false true for Gazebo/sim
params_file nav2_params.yaml from pkg Your custom params
slam false true = SLAM Toolbox instead of AMCL
autostart true Auto-activate lifecycle nodes
use_compositiontrueComposable nodes (more efficient)
use_respawn false Restart crashed nodes 
rviz_config_file default nav2 rviz Path to custom .rviz file
log_level info debug, info, warn, error

# Verify the nav2_bringup launch files exist on your system
# List all available nav2_bringup launch files
ros2 pkg prefix nav2_bringup
ls $(ros2 pkg prefix nav2_bringup)/share/nav2_bringup/launch/

# Should show:
# bringup_launch.py
# localization_launch.py
# navigation_launch.py
# rviz_launch.py
# slam_launch.py
# tb3_simulation_launch.py  (turtlebot3 sim example)

The key insight is slam:=false + map:= is the flag combination that switches the entire stack from SLAM-mapping mode to AMCL localization-on-existing-map mode — no custom launch file needed.
