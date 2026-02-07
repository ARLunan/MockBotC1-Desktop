# MockBOT Project - TurtleTron MockBOTc1-Desktop

## MockBOT TurtleTron Roomba 400 Base/Create 1 Base Project

This repository for the **MockBOT** TurtleTron project defines the Jazzy branch for the **Desktop Compute** that complements the **Robot Compute** Roomba 400/Create 1 base, that is supported by several varients on the AutonomyLabs Packages repository. The **MockBOT** project is described in the book "MockBOT: Over-the-shoulder instructions on how to build your own personal robot". It can be purchased from amazon.com, amazon.ca, or in other locations, in Books dropdown, Search MockBOT, DIY robotics. Addendums to The TurtleTron specific text are also hosted in the **MockBOTc1-Docs** repository.

The purpose of this document is to document the development and post the release of ROS 2 Packages that migrate the original "Willow Garage" / Open Robotics Turtlebot (tm) where the last released repository was ROS Indigo, to ROS 2 Jazzy/Navigation 2 autonomous navigation'. The new repositories are called "MockBOTc1-Robot and "MockBOTc1-Desktop" uses this original iRobot Create (™) 1 Base. It should be mentioned that while this repository is written to use with a iRobot Create 1, the installed base drive package (Autonomy Labs ™) includes support for the Roomba Model 500 or 600) and Create 2 base. To enable these drivers, a manual revison must be made to the mockbotc1\_bringup launch file that is installed in the ros2\_ws workspace, and "\$ colcon build" recompiled and sourced from the workspace root,  
\$ ros2_ws: . install/setup.bash". 

### At this time, this repository is "Work in Progress" so expect errors to be displayed after launching many of the scripts and packages.

To run the MockBOT_c1, the Desktop Machine and Robot Raspberry Pi, Roomb/Create1 Base, Logitech Gamepad Joystick and other devices must be powered up and connected by WiFi over the same network

From the **Desktop** Machine, open a new **Terminal Window** and connect by ssh to the Robot:  
**\$ sudo ssh unbuntu@rp5\-ub24j\-mb.local** , using the password you assigned when installing installing Ubuntu 24.04 on the Raspberry Pi Robot. 

Launch the **Robot** by typing into a new ssh conection **Terminal window** window to startup various packages that provide common operational functions, such as :

 **\$ ros2 launch mockbotc1\_bringup bringup.launch.py**  
  This will start up the ROS 2 packages for the Base, RPLidar Lidar, F710 Joystick (by default), OAK-D-Lite Camera and IMU, twist_mux, description. A log of the many actions will scroll by on the terminal. 
  
You can drive the Robot with the Joystick or from the Desktop run the **keyboard teleop** and visualize the Robot URDF alone OR with a map in the RVIZ Display on the Desktop Compute. 

Open another **Terminal Window** on the Desktop
#### Keyboard Teleop
The **Robot** can now be driven with the Keyboard Teleop  
**\$ ros2 run teleop\_twist\_keyboard teleop\_twist\_keyboard --ros-args --remap cmd_vel:=cmd\_vel\_key** .

#### Then Launch just the Robot Visualization OR Localization slam\_toolbox
Open another **Terminal Window** Terminal on the Desktop 
**\$ ros2 launch mockbotc1\_viz robot\_model.launch.py**

This will visualize the published robot URDF image with an open RVIZ2 Window on the Desktop.  

####Localization, Visualization and manually Drive the Robot 

Open another **Terminal Window** Terminal on the Desktop and drive the Robot by Teleop.
**\$ ros2 launch mockbotc1\_navigation slam.launch.py**
 
Create a **Map** by typing into another window on the Desktop Terminal:  
**Mapping**

From another Desktop Terminal Window,  

\$ cd Desktop  
\$ mkdir maps  
\$ cd maps

Move the **Robot** around the area of navigation until suitably covered, then save the **MAP** onto a Desktop Folder, /home/ubuntu/Desktop/maps.  Be sure to use the specific your user name instead of "ubuntu"

Use <map_name> = "~/Desktop/maps/mapname"  
**\$ ros2 run nav2\_map\_server map\_saver\_cli \-f \<map_name> --ros-args -p save\_map\_timeout:=10000**  
  
**Autonomous Navigation**

Load the map you created and run the Navigation2 package:
**\$ ros2 launch mockbotc1\_navigation navigation.launch.py rviz:=True map:='~/Desktop/maps/mapname.yaml**

The Map will Vizualize (by Default) in **RViz2** on the Desktop Host Machine  
   
 Check out Nav2 Tutorial [NAV2](https://docs.nav2.org/tutorials/docs/navigation2\_on\_real\_turtlebot3.html#initialize-the\-location\-of\-turtlebot-3) for more details on how to initialize and send goal pose.

## Installation of ROS 2 on Robot Compute Remote Desktop Computer

### Refer to separate Manual Installation of MockBOTc1-Robot on the Raspberry Pi 5 Compute.

**Installation of ROS 2 Packages and Dependancies on the Robot Desktop Computer.** This Repository material references the ROS 2 and dependencies installation documented in the linorobot2 repository **https://github.com/linorobot/linorobot2/blob/jazzy/ROBOT** , SLGRepository **https://github.com/slgroboticshttps://github.com/slgrobotics**, and WimbleRobotics **https://github.com/wimblerobotics/Sigyn**, and adds instructions specfically for this MockBOTc1-Robot model.

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
