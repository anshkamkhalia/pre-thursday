import rclpy
from interfaces.srv import RobotStateSrv
from rclpy.node import Node

class RobotStateClient(Node):

    def __init__(self):
        super().__init__('robot_state_client')

        self.client = self.create_client(RobotStateSrv, 'get_robot_state')

        while not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info(f"service not available yet, waiting")

        self.request = RobotStateSrv.Request()

    def send_request(self):
        self.future = self.client.call_async(self.request)
        rclpy.spin_until_future_complete(self, self.future)

        return self.future.result()

def main():
    rclpy.init()
    client = RobotStateClient()

    response = client.send_request()
    client.get_logger().info(f"battery_pct: {response.battery_pct}\nposition: {response.position}\nstatus: {response.status}\n")

    client.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()