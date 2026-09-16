import rclpy
from rclpy.node import Node
from interfaces.msg import RobotStateMsg, BatteryPct, Position
from interfaces.srv import RobotStateSrv

class RobotStateNode(Node):

    def __init__(self):
        super().__init__("robot_state_publisher_and_server")

        self.position = (0,0)
        self.battery_pct = 0.85
        self.status = "idle"

        self._publisher = self.create_publisher(RobotStateMsg, 'robot_state', 10)
        self.timer = self.create_timer(0.5, self.timer_callback)

        self.publish_idx = 0

        self.get_state_service = self.create_service(RobotStateSrv, 'get_robot_state', self.service_callback)
        self.battery_pct_subscriber = self.create_subscription(BatteryPct, 'charging_battery_pct', self.charging_callback, 10)

        self.position_subscriber = self.create_subscription(Position, 'position_updater', self.position_callback, 10)
        self.prev_position = None

        self.last_position_update = self.get_clock().now()

        self.movement_timer = self.create_timer(
            0.1,
            self.check_movement
        )

    def timer_callback(self):

        msg = RobotStateMsg()

        msg.position = self.position
        msg.battery_pct = self.battery_pct
        msg.status = self.status

        self._publisher.publish(msg)

        self.get_logger().info(f"published robot status: {self.publish_idx}")
        self.publish_idx += 1

    def service_callback(self, request, response):
        response.position = self.position
        response.status = self.status
        response.battery_pct = self.battery_pct

        self.get_logger().info(f"received request from client")
        return response

    def charging_callback(self, msg):
        new_battery_pct = msg.battery_pct
        self.battery_pct = new_battery_pct

    def position_callback(self, msg):
        new_position = msg.position
        self.position = new_position
        self.status = "moving"
        self.last_position_update = self.get_clock().now()

    def check_movement(self):
        now = self.get_clock().now()

        elapsed = (now - self.last_position_update).nanoseconds / 1e9

        if self.status == "moving" and elapsed > 1.0:
            self.status = "idle"
            self.get_logger().info("movement finished")

def main(args=None):

    rclpy.init()
    robot_state = RobotStateNode()
    rclpy.spin(robot_state)
    robot_state.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()