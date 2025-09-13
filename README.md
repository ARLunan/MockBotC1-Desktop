# MockBOTc1-Desktop

## MockBot Create1 Base Project Robot Desktop

### MockBOT Project - iRobot© Create1/Roomba 500 Base

### At this time, this repository is "Work in Progress" so expect errors to be displayed after launching many of the scripts and packages.

The purpose of this document is to document the development and post the release of ROS 2 Packages that migrate the original "Willow Garage" / Open Robotics Turtlebot (tm) where the last released repository was ROS Indigo, to ROS 2 Jazzy/Navigation 2 autonomous navigation'. The new repositories are called "MockBOTc1-Robot and "MockBOTc1-Desktop" uses this orgiginal iRobot Create (™) 1 Base. It should be mentioned that while this repository is written to use with a iRobot Create 1, the installed base drive package (Autonomy Labs ™) includes support for the Roomba Model 500 or 600) and Create 2 base. To enable these drivers, a manual revison must be made to the mockbotc1\_bringup launch file that is installed in the ros2\_ws workspace, and "\$ colcon build" recompiled and sourced from the workspace root,  
\$ ros2_ws: . install/setup.bash". 

To run the MockBOT, the Desktop Machine and Robot Raspberry Pi, Logitech Gamepad Joystick and other devices must be powered up and connected by WiFi over the same network

From the **Desktop** Machine, open a Terminal and connect by ssh to the Robot:  
**\$ sudo ssh unbuntu@rp5-ub24j-mb.local** , using the password you assigned when installing installing Ubuntu 24.04 on the RAspberry Pi Robot. 

Launch the **Robot** by typing into a new ssh conection Terminal window to startup various packages that provide common operational functions, such as :

 **\$ ros2 launch mockbotc1_bringup bringup.launch.py**  
  This will start up the ROS 2 packages for the Base, RPLidar Lidar, MPU9250 IMU, F710 Joystick (by default) and OAK-D_Lite Camera. A log of the many actions will scroll by on the terminal.

Open a Terminal on the Desktop and type the following to startup common ROS publishing and Subscription functions, such as "description Robot State Publisher, Joint Publisher, Robot Localization, Madgwick IMU and Odometry Sensor Fusion.

**\$ ros2 launch mockbotc1_desktop_bringup bringup.launch.py.**

This will start up the ROS 2 packages for the Robot Description (joint_state_publisher & robot_state_publisher), Common packages for Slam ToolBox, Navigation 2 (ekt filter, tf), F710 Joystick (optionally). A log of the many actions will scroll by on the terminal.

The **Robot** can now be driven with the Keyboard Teleop  
**\$ ros2 run teleop_twist_keyboard teleop_twist_keyboard** , or with the GamePad Joystick (default Logitech F710).

This will visualize the published robot URDF image with an open RVIZ2 Window.  

Create a **Map** by typing into another window on the Desktop Terminal:  
**\$ ros2 launch mockbotc1_navigation slam.launch.py**

**Mapping**

From another Desktop Terminal Window,  

\$ cd Desktop  
\$ mkdir maps  
\$ cd maps

Move the **Robot** around the area of navigation until suitably covered, then save the **MAP** onto a Desktop Folder, /home/ubuntu/Desktop/maps.  

Use <map_name> = "~/Desktop/maps/mapname"  
**\$ ros2 run nav2\_map\_server map\_saver\_cli \-f <map_name> --ros-args -p save\_map\_timeout:=10000**  
  
**Autonomous Navigatio**

Load the map you created:
**\$ ros2 launch mockbotc1_navigation navigation.launch.py map:='~/Desktop/maps/mapname.yaml**

Run Nav2 package:  
**\$ ros2 launch mockbot_navigation navigation.launch.py**

The Map will Vizualize (by Default) in **RViz2** on the Desktop Host Machine  
 **\$ ros2 launch linorobot2_viz navigation.launch.py  rviz:=true**
  
 Check out Nav2 Tutorial [NAV2](https://docs.nav2.org/tutorials/docs/navigation2_on_real_turtlebot3.html#initialize-the-location-of-turtlebot-3) for more details on how to initialize and send goal pose.

## Installation of ROS 2 on Robot (Raspberry Pi Single Board Computer - SBC) and Remote Desktop Computer**

**Installation of ROS 2 Packages and Dependancies on the Robot (Raspberry Pi Single Board Computer-SBC) and Desktop Computer.** This Repository material references the ROS 2 and dependencies installation documented in the linorobot2 repository *https://github.com/linorobot/linorobot2/blob/jazzy/ROBOT* , and adds instructions specfically for this MockBOTc1 robot model.

This "install" script on the ros2me repository script below will install  
**ROS 2 jazzy distro** and a number of python3 libraries and dependancies for the Ubuntu 24.04 Jammy Release meta-package:

ros-jazzy-desktop on a "x86_64" machine,  or
jazzyhumble-base (barebones) on a "aarch64", i.e Raspberry Pi or MAC M1.

Note that if your Remote Desktop Machine is an "aarch64" such as a MAC M1, as it installs the base, you must manually run an additional script  
**"~/sudo apt install ros-jazzy-desktop** to add the necessary packages to upgrade the install to a "Desktop" (e.g. rviz, teleop, joy, rqt)  

While not essential the following Ubuntu packages can be helpful in running and trouble-shotting your Robot & Desktop computers. Install these ubuntu packages with with  
**"~/sudo apt install" openssh-server, avahi-daemon, htop, nload** .

From the Ubuntu home directory,  
**~/git clone https://github.com/linorobot/ros2me** , then run **~/ .install**

**Manual installation of MockTurtleBotC1**, which is a Roomba 500/Create 1 varient of the MockTurtleBot robot package on ***robot*** **(RasPi)** computer.

1. Install dependencies

1.1 Source your ROS 2 distro, which is **jazzy** in this documentation and workspace
source /opt/ros/jazzy/setup.bash
cd ros2_ws
colcon build
source install/setup.bash

add this script to the ~/.bashrc in your home directory to make this designation persistant for any terminal instance  

**\$ export "source /opt/ros/jazzy/setup.bash"**

The <your_ws> workspace is designated as **ros2_ws/src**, or whatever you desire to use.

$ sudo apt-get install build-essential cmake libboost-system-dev libboost-thread-dev

1.2 Configure .gitignore in root directory of Remote Desktop and Robot SBC (Single Board Computer)
Suggest use the sample file ROS.gitignore file from [https://github.com/github/gitignore]() . Suggest using the ROS.gitignore file and add these several additional lines if VSCode is deployed on the Desktop and Robot machines and you use Git.

\# VSCode
/.vscode/  
**/.vscode/  
log/  
build/  
install/

\# .gitignore  
/.gitignore

\# .DS_Store  
.DS_Store