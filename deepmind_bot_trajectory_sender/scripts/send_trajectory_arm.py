#! /usr/bin/env python3

import rclpy
from rclpy.action import ActionClient
from control_msgs.action import FollowJointTrajectory
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
import random

def rand_sign():
    # Generate a random number between -1 and 1
    random_number = random.uniform(-1, 1)

    # Determine the sign of the random number
    if random_number < 0:
        sign = -1  # Negative
    elif random_number > 0:
        sign = 1  # Positive
    else:
        sign = 0  # Zero

    return sign

def main(args=None):
    rclpy.init(args=args)

    # Create a ROS 2 node
    node = rclpy.create_node('trajectory_sender_node')

    # Create an Action Client for the FollowJointTrajectory action
    action_client = ActionClient(node, FollowJointTrajectory, '/deepmind_bot_arm_controller/follow_joint_trajectory')

    # Wait for the action server to be available
    if not action_client.wait_for_server(timeout_sec=5.0):
        node.get_logger().error('Action server not available. Exiting...')
        return

    # Create a FollowJointTrajectory goal
    goal_msg = FollowJointTrajectory.Goal()
    goal_msg.trajectory = JointTrajectory()
    goal_msg.trajectory.joint_names = ['deepmind_robot1_middle_base_joint',
                                        'deepmind_robot1_arm1_joint',
                                        'deepmind_robot1_arm2_joint',
                                        'deepmind_robot1_arm3_joint',
                                        'deepmind_robot1_arm4_joint',
                                        'deepmind_robot1_arm5_joint',
                                        'deepmind_robot1_arm6_joint',]  
    # Create a trajectory point
    point = JointTrajectoryPoint()
    random_v = random.random()*3.1416

    point.positions = [ random_v*rand_sign(),
                        random_v*rand_sign(),
                        random_v*rand_sign(),
                        random_v*rand_sign(),
                        random_v*rand_sign(),
                        random_v*rand_sign(),
                        random_v*rand_sign(),]
    
    print(point.positions)

    point.time_from_start.sec = 2  # Time to reach the desired position in seconds

    # Add the trajectory point to the goal
    goal_msg.trajectory.points.append(point)

    # Send the goal to the action server
    future = action_client.send_goal_async(goal_msg)

    rclpy.spin_until_future_complete(node, future)

    if future.result() is not None:
        node.get_logger().info('Goal successfully completed.')
    else:
        node.get_logger().error('Goal failed to complete')

    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
