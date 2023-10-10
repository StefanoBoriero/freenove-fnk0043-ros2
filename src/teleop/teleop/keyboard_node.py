#!/bin/python3

import rclpy
import threading
from rclpy.node import Node
from pynput import keyboard


class KeyboardNode(Node):

    def __init__(self, node_name: str) -> None:
        super().__init__(node_name, parameter_overrides=[])
        self.counter = 0
        self.get_logger().info("Hello from keyobard_node")
        self.listener: threading.Thread = keyboard.Listener(
            on_press=self.on_press, on_release=self.on_release)
        self.listener.start()

    def timer_callback(self):
        self.counter += 1
        self.get_logger().info(f"Scheduled salute number {self.counter}")

    def on_release(self, key):
        try:
            char = getattr(key, 'char', None)
            if isinstance(char, str):
                # TODO send out message that a key was pressed
                self.get_logger().info("Released char " + char)
        except Exception as e:
            self.get_logger().error(str(e))
            raise

    def on_press(self, key):
        try:
            char = getattr(key, 'char', None)
            if isinstance(char, str):
                self.get_logger().info('pressed ' + char)
        except Exception as e:
            self.get_logger().error(str(e))
            raise

        if key == keyboard.Key.esc and self.exit_on_esc:
            self.get_logger().info('stopping listener')
            raise keyboard.Listener.StopException

    def destroy_node(self):
        self.get_logger().info("Shutting node down...")
        super().destroy_node()


def main(args=None):
    rclpy.init(args=args)
    node: Node = KeyboardNode("keyboard_node")
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()
