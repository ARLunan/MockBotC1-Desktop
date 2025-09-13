# Manual installation of MockBOTc1-Desktop packages on Desktop computer

## Refer to separate Manual Installation of MockBOTc1-Robot on Remote Desktop computer

    This Repository is a varient of the Linorobot2 and slgrobitics Repositories with hardwire specific revisions to URDF applicable to the AutonomyLab Create1 Base (https://github.com/AutonomyLab/create_robot), SlamTec RPLidar, Luxonis Oak-D-Lite Camera & IMU
    Note: This Procedure installs Desktop Joystick and  Navigation packages on the Remote Desktop Computer (Ubuntu) that does has a connected monitor for Robot, SLAM & Nav Visualization functions

## Manual installation of MockTurtleBOTc1-Desktop packages on Desktop computer

### Refer to separate Manual Installation of MockBOTc1-Robot on Remote Desktop computer

Note: This Procedure installs navigation packages on the Remote Desktop Computer (Ubuntu) that does has a connected monitor for robot, SLAM & Nav Visualization functions .

1. Install Specfic Functional Packages from ROS 2 and MockTurtleBotC1-Desktop Github Repository

1.1 Source your ROS2 distro and workspace
If it's your first time using ROS2 and haven't created your ROS2 workspace yet, you can check out 
[ROS2 Creating a Workspace](https://docs.ros.org/en/galactic/Tutorials/Workspace/Creating-A-Workspace.html) tutorial. 
The MockTurtleBotC1 code supports your_ros_distro = **jazzy** currently.

    source /opt/ros/humble/setup.bash
    cd <your_ws>
    colcon build
    source install/setup.bash

### 2. Download MockBotC1-Desktop and dependencies:

=======

### 2. Download MockBOTc1-Desktop and dependencies:

2.1.2 Install MockBOTc1-Desktop package:

    cd ros2_ws
    git clone *https://github.com/ARLunan/MockBOTc1-Desktop.git
    rosdep update && rosdep install --from-path src --ignore-src -y 
    colcon build 
    source install/setup.bash

## Miscellaneous

A reminder that , as described in this repository's README.me, configure the **.gitignore** file if using Git and VSCode applications to develop code.
