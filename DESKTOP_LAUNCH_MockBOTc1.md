Created by Claude AI Sonnet 4.6

### Nav2 with simultaineus localization on existing map (Localize and navigate - not SLAM). Standard "load map > localize with AMCL > navigate workflow" 
### Architecture Overview 
Since your robot already has:  
✅ Robot base (hardware drivers, robot_state_publisher, etc.)  
✅ ekf_node running (robot_localization)

**Map Server** – serves map.yaml  
**AMCL** – localizes the robot on the existing map  
**Nav2 stack** – planner, controller, BT navigator, etc.  
**RViz** (optional) – for visualization and goal setting

## You need to launch:

### Launch Commands (using nav2_bringup directly)

#### Terminal 1 — already running: robot base + ekf_node

#### Terminal 2 — Nav2 + map server + AMCL
ros2 launch your_robot_bringup navigation.launch.py \
    map:=/path/to/your/map.yaml \
    params_file:=/path/to/nav2_params.yaml

#### Terminal 3 — RViz (optional)
ros2 launch your_robot_bringup rviz_nav2.launch.py

#### Terminal 4 — Set initial pose (if not set in params)
ros2 topic pub /initialpose geometry_msgs/PoseWithCovarianceStamped \
  "{ header: {frame_id: map}, pose: { pose: { position: {x: 0.0, y: 0.0}, orientation: {w: 1.0} } } }" --once

## Critical TF/Frame Notes

| Frame pair                           | Published by             |
| ------------------------------------ | ------------------------ |
| map > odom                           | AMCL (tf_broadcast: true |
| odom > base_footprint                | **ekf_node**             |
| base_footprint → base_link → sensors | robot_state_publisher    |



###  Key Things to Verify
#### Confirm TF tree is complete  
ros2 run tf2_tools view_frames

#### Check map is being served  
ros2 topic echo /map --once

#### Check AMCL is publishing the map→odom transform
ros2 run tf2_ros tf2_echo map odom

#### Check Nav2 nodes are active
ros2 lifecycle list

Once AMCL converges (use 2D Pose Estimate in RViz to set initial pose), you can send navigation goals via Nav2 Goal in RViz or programmatically via the NavigateToPose action server.

## Streamlined version using Nav2's built-in launch files directly from the nav2_bringup package:

### Launch Commands (using nav2_bringup directly)
#### Terminal 1 — Map Server + AMCL (localization)
ros2 launch nav2_bringup localization_launch.py \\
  map:=/path/to/your/map.yaml \\
  use_sim_time:=false \\
  params_file:=/path/to/nav2_params.yaml
#### Terminal 2 — Nav2 Navigation Stack
ros2 launch nav2_bringup navigation_launch.py \\
  use_sim_time:=false \\
  params_file:=/path/to/nav2_params.yaml \\
  map_subscribe_transient_local:=true
#### Terminal 3 — RViz (optional, nav2_bringup includes it)
ros2 launch nav2_bringup rviz_launch.py \\
  use_sim_time:=false \\
  rviz_config_file:=$(ros2 pkg prefix nav2_bringup)/share/nav2_bringup/rviz/nav2_default_view.rviz

## Single combined Launch (bringup_launch.py)

**nav2_bringup** ships a single **bringup_launch.py** that handles map server + AMCL + nav stack together:

ros2 launch nav2_bringup bringup_launch.py \
  map:=/path/to/your/map.yaml \
  use_sim_time:=false \
  params_file:=/path/to/nav2_params.yaml \
  slam:=false \
  use_composition:=true \
  use_respawn:=false \
  autostart:=true \
  rviz_config_file:=$(ros2 pkg prefix nav2_bringup)/share/nav2_bringup/rviz/nav2_default_view.rviz

Setting slam:=false tells it to use AMCL + the provided map instead of SLAM Toolbox.
### Set Initial Pose After Launch
In RViz use **2D Pose Estimate**, or via CLI:  
 
ros2 topic pub /initialpose geometry_msgs/PoseWithCovarianceStamped \
  "{header: {frame_id: map}, pose: {pose: {position: {x: 0.0, y: 0.0, z: 0.0}, \
  orientation: {x: 0.0, y: 0.0, z: 0.0, w: 1.0}}}}" --once

### OR: Quick Reference: All bringup_launch.py Parameters

| Parameter        | Default                   | Notes                             |
| ---------------- | ------------------------- | --------------------------------  |
| map              | ""                        | Full path to map.yaml             |
| use_sim_time     | false                     | true for Gazebo/sim               |
| params_file      | nav2_params.yaml from pkg | your custom params C              |
| slam             | false                     | true=SLAM Toolbox instead of AMCL |
| use_composition  | true                      | Composable nodes (more efficient)  |
| use_respawn      | false                     | Restart crashed                   |
| rviz_config_file | defaults nav2 rviz        | Path to custom .rviz file         |
| log_level        | info                      | debug, info, warn, error          |

### Verify the nav2_bringup launch files exist on your system
#### List all available nav2_bringup launch files
ros2 pkg prefix nav2_bringup  
ls $(ros2 pkg prefix nav2_bringup)/share/nav2_bringup/launch/

#### Should show:
\# bringup_launch.py  
\# localization_launch.py  
\# navigation_launch.py  
\# rviz_launch.py  
\# slam_launch.py  
\# tb3_simulation_launch.py  (turtlebot3 sim example)

The key insight is **slam:=false + map:=** is the flag combination that switches the entire stack from SLAM-mapping mode to AMCL localization-on-existing-map mode — no custom launch file needed.
