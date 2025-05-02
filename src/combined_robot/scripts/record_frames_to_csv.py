#!/usr/bin/env python3
"""
ROS 2 node that logs every /joint_states message to CSV,
with one column per joint.

Usage:
  ros2 run combined_robot record_frames_to_csv.py --csv ~/ros2_ws/joint_states.csv
"""

import csv, rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from argparse import ArgumentParser


class JointStateLogger(Node):
    def __init__(self, csv_path):
        super().__init__('joint_state_logger')
        self.csv_file = open(csv_path, 'w', newline='')
        self.writer = None
        self.subscription = self.create_subscription(
            JointState,
            '/joint_states',
            self.joint_cb,
            10
        )
        self.get_logger().info(f"Subscribed to /joint_states, logging to {csv_path}")

    def joint_cb(self, msg: JointState):
        # On first message, write header with joint names
        if self.writer is None:
            header = ['time'] + list(msg.name)
            self.writer = csv.writer(self.csv_file)
            self.writer.writerow(header)

        # Then write timestamp + positions
        t = self.get_clock().now().nanoseconds / 1e9
        row = [f"{t:.9f}"] + [f"{p:.6f}" for p in msg.position]
        self.writer.writerow(row)
        self.csv_file.flush()


def main():
    parser = ArgumentParser()
    parser.add_argument(
        '--csv',
        default='/tmp/joint_states.csv',
        help='Path to output CSV file'
    )
    args = parser.parse_args()

    rclpy.init()
    node = JointStateLogger(args.csv)
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.csv_file.close()
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
