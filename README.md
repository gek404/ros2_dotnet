ROS2 for .NET
=============

[![CircleCI](https://circleci.com/gh/samiamlabs/ros2_dotnet/tree/dashing.svg?style=svg)](https://circleci.com/gh/samiamlabs/ros2_dotnet/tree/master)

ROS2 C# client library implementation. To my knowledge the most advanced ros2 C# project.

Notice
------

This fork from https://github.com/samiamlabs/ros2_dotnet which include implementation of rclcs with and integrated improvements from https://github.com/DynoRobotics/unity_ros2. For this fork repository added support for ROS2 Foxy version.
Linux
-----

Make sure to source your ROS2 Foxy environment. For using cyclone dds implementation set RMW_IMPLEMENTATION:

```
export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp
ros2 doctor --report
```

Build ROS2 for .NET:

```
mkdir -p ~/ros2_dotnet_ws/src
cd ~/ros2_dotnet_ws
wget https://raw.githubusercontent.com/gek404/ros2_dotnet/foxy/ros2_dotnet_foxy.repos
vcs import ~/ros2_dotnet_ws/src < ros2_dotnet_foxy.repos
colcon build
source ~/ros2_dotnet_ws/install/local_setup.bash
```
For testing rclcs realisation.

Talker in first terminal:

```
source ~/ros2_dotnet_ws/install/local_setup.bash
ros2 run rcldotnet_examples rcldotnet_talker
```
Listener in second terminal console:
```
source ~/ros2_dotnet_ws/install/local_setup.bash
ros2 run rcldotnet_examples rcldotnet_listener
```

Windows
-----

Make sure to source your ROS2 Foxy environment. For using cyclone dds implementation set RMW_IMPLEMENTATION:

```
set RMW_IMPLEMENTATION=rmw_cyclonedds_cpp
ros2 dotor --report
```

Build ROS2 for .NET:

```
md C:\dev\ros2_dotnet_ws\src
cd C:\dev\ros2_dotnet_ws\src
curl -o ros2_dotnet_foxy.repos https://raw.githubusercontent.com/gek404/ros2_dotnet/foxy/ros2_dotnet_foxy.repos
vcs import C:\dev\ros2_dotnet_ws\src < ros2_dotnet_foxy.repos
call "C:\Program Files (x86)\Microsoft Visual Studio\2019\Community\VC\Auxiliary\Build\vcvarsall.bat" x86_amd64
colcon build
call C:\dev\ros2_dotnet_ws\install\local_setup.bat
```

**Note:** If you getting error about MAX_PATH in Windows, you need make this recommendations: https://knowledge.autodesk.com/support/autocad/troubleshooting/caas/sfdcarticles/sfdcarticles/The-Windows-10-default-path-length-limitation-MAX-PATH-is-256-characters.html      

For testing rclcs realisation.

Talker in first cmd console:

```
call C:\dev\ros2_dotnet_ws\install\local_setup.bat
ros2 run rcldotnet_examples rcldotnet_talker
```

Listener in second cmd console:

```
call C:\dev\ros2_dotnet_ws\install\local_setup.bat
ros2 run rcldotnet_examples rcldotnet_listener
```

Build custom messages
-----

If you want to generate custom messages for rclcs ROS2 realisation you need add your message packages to ros2_dotnet_ws/src and build workspace.

Generate Plugins for Unity3d
-----

If you want to generate Unity3d plugins you need added your message packages to script create_unity_plugin.py from package rcldotnet_utils:

```
class UnityROS2LibCopier:
    def __init__(self, output_path):
        self.ament_dependencies = [
            'rcl',
            'rcl_interfaces',
            'rmw',
            'rmw_implementation',
            'rmw_cyclonedds_cpp',
            'rosidl_generator_c',
            'rosidl_typesupport_c',
            'rosidl_typesupport_cpp',
            'rcl_logging_noop',
            'rosidl_typesupport_introspection_c',
            'rosidl_typesupport_introspection_cpp',
            'builtin_interfaces',
            'rcutils',
            'rcldotnet',
            'std_msgs',
            'geometry_msgs',
            'sensor_msgs',
            'nav_msgs',
            'test_msgs',
            'action_msgs',
            'unique_identifier_msgs',
            'tf2_msgs',
            'YOUR_CUSTOM_MESSAGE_PACKAGE_NAME'
        ]
```

After that build workspace and run script. 

For Linux:

```
cd ~/ros2_dotnet_ws
colcon build
source install/local_setup.bash
ros2 run rcldotnet_utils create_unity_plugin
```

For Windows:

```
cd C:\dev\ros2_dotnet_ws
colcon build
call install\local_setup.bat
ros2 run rcldotnet_utils create_unity_plugin
```

Result directory Plugins will created in current path. Plugins contain all dynamic libraries for work with rclcs in Unity3d projects. You can found examples for Unity3d in this repository: https://github.com/DynoRobotics/unity_ros2.

Contribution
------

See Projects page for what tasks and contributions are needed.
