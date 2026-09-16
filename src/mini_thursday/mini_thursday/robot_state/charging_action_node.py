import rclpy
from rclpy.node import Node
from interfaces.action import Charge
from interfaces.msg import BatteryPct
from rclpy.action import ActionServer
import time

class RobotChargingActionServer(Node):

    def __init__(self):
        super().__init__("robot_charging_action_server")

        self.charging_action_server = ActionServer(self, Charge, 'charge_robot', self.charging_callback)
        self.robot_status_publisher = self.create_publisher(BatteryPct, 'charging_battery_pct', 10)

    def charging_callback(self, goal_handle):

        current_battery_pct = goal_handle.request.current_battery_pct
        feedback_msg = Charge.Feedback()

        while current_battery_pct <= 1.0:
            time.sleep(1)
            current_battery_pct += 0.01

            msg = BatteryPct()
            msg.battery_pct = current_battery_pct
            feedback_msg.ongoing_battery_pct = current_battery_pct

            goal_handle.publish_feedback(feedback_msg)
            self.robot_status_publisher.publish(msg)

        goal_handle.succeed()
        result = Charge.Result()
        result.success = True
        return result

def main():
    rclpy.init()
    action_server = RobotChargingActionServer()
    rclpy.spin(action_server)
    rclpy.shutdown()

if __name__ == "__main__":
    main()