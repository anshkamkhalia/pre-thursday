import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from interfaces.action import Move
from interfaces.srv import RobotStateSrv
import sys

class MovementActionClient(Node):

    def __init__(self):
        super().__init__('movement_action_client')

        self.action_client = ActionClient(self, Move, 'movement_action')
        self.status_client = self.create_client(RobotStateSrv, 'get_robot_state')

        while not self.status_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info("waiting for robot state service")

    def send_request(self):
        monitor_msg = RobotStateSrv.Request()
        future = self.status_client.call_async(monitor_msg)
        rclpy.spin_until_future_complete(self, future)

        response = future.result()
        return response.position

    def send_goal(self, x, y):

        goal_msg = Move.Goal()
        goal_msg.target_position = [x,y]
        goal_msg.initial_position = self.send_request()
        self.action_client.wait_for_server()

        return self.action_client.send_goal_async(goal_msg)

def main(args=None):
    rclpy.init()
    action_client = MovementActionClient()
    future = action_client.send_goal(int(sys.argv[1]), int(sys.argv[2]))
    rclpy.spin_until_future_complete(action_client, future)
    
if __name__ == "__main__":
    main()