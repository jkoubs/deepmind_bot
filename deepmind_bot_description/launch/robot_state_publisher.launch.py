import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node
import xacro

from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch.actions import OpaqueFunction


def launch_setup(context, *args, **kwargs):
    ####### DATA INPUT ##########
    # This is to access the argument variables. Otherwise we cant access the values
    robot_name = LaunchConfiguration('robot_name').perform(context)
    robot_file = LaunchConfiguration('robot_file').perform(context)
    robot_description_topic_name = "/" + robot_name + "_robot_description"
    #robot_state_publisher_name = robot_name +  "_robot_state_publisher"
    robot_state_publisher_name = "robot_state_publisher"
    #joint_state_topic_name = "/" + robot_name + "/joint_states"
    joint_state_topic_name = "/joint_states"


    ####### DATA INPUT END ##########

    package_description = "deepmind_bot_description"    

    
    extension = robot_file.split(".")[1]

    if extension == "urdf":
        robot_desc_path = os.path.join(get_package_share_directory(
        package_description), "urdf", robot_file)
        robot_desc = xacro.process_file(robot_desc_path)
    elif extension == "xacro":
        robot_desc_path = os.path.join(get_package_share_directory(
        package_description), "robot", robot_file)
        # We load the XACRO file with ARGUMENTS
        robot_desc = xacro.process_file(robot_desc_path, mappings={'robot_name' : robot_name})
    else:
        assert False, "Extension of robot file not suppored = "+str(extension)
  
 
    xml = robot_desc.toxml()

    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name=robot_state_publisher_name,
        emulate_tty=True,
        parameters=[{'use_sim_time': True, 'robot_description': xml}],
        remappings=[("/robot_description", robot_description_topic_name),
                    ("/joint_states", joint_state_topic_name)
                    ],
        output="screen"
    )


    return [robot_state_publisher_node]

def generate_launch_description(): 

    robot_name_arg = DeclareLaunchArgument('robot_name', default_value='deepmind_bot1')
    robot_file_arg = DeclareLaunchArgument('robot_file', default_value='deepmind_bot.xacro')

    return LaunchDescription([
        robot_name_arg,
        robot_file_arg,
        OpaqueFunction(function = launch_setup)
        ])