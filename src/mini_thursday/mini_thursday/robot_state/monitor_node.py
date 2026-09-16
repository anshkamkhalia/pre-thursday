import rclpy
from rclpy.node import Node
from interfaces.msg import RobotStateMsg

class RobotStateMonitorNode(Node):

    def __init__(self):
        super().__init__("robot_state_monitor")
        self.battery_pct = None
        self.status = None
        self.position = None

        self.subscription = self.create_subscription(RobotStateMsg, 'robot_state', self.monitor_callback, 10)

    def monitor_callback(self, msg):
        self.battery_pct = msg.battery_pct
        self.status = msg.status
        self.position = msg.position

        self.get_logger().info(f"battery_pct: {self.battery_pct * 100}%\nstatus: {self.status}\nposition: {self.position}")

def main(args=None):

    rclpy.init()
    robot_state_monitor = RobotStateMonitorNode()
    rclpy.spin(robot_state_monitor)
    robot_state_monitor.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()