#!/bin/python3

import rclpy
from rclpy.node import Node

class MyNode(Node):

    def __init__(self, node_name: str) -> None:
        super().__init__(node_name, parameter_overrides=[])
        self.counter = 0
        self.get_logger().info("Hello from keyobard_node")
        self.create_timer(0.5, self.timer_callback)
    
    def timer_callback(self):
        self.counter += 1
        self.get_logger().info(f"Scheduled salute number {self.counter}")

def main(args=None):
    rclpy.init(args=args)
    node: Node = MyNode("keyboard_node")
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == "__main__":
    main()
