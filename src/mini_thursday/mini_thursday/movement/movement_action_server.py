import rclpy
from rclpy.node import Node
from rclpy.action import ActionServer
from interfaces.action import Move
from interfaces.msg import Position
import time

class MovementActionServer(Node):

    def __init__(self):

        super().__init__('movement_action_server')
        self.action_server = ActionServer(self, Move, "movement_action", self.movement_callback)
        self.position_updater_publisher = self.create_publisher(Position, 'position_updater', 10)

    def movement_callback(self, goal_handle):

        feedback_msg = Move.Feedback()
        target_x, target_y = goal_handle.request.target_position[0], goal_handle.request.target_position[1]
        initial_x, initial_y = goal_handle.request.initial_position[0], goal_handle.request.initial_position[1]

        direction_x = target_x - initial_x
        if direction_x < 0:
            direction_x = "negative"
        elif direction_x > 0:
            direction_x = "positive"
        else:
            direction_x = "zero"

        while initial_x != target_x and direction_x != "zero":

            position_msg = Position()

            if direction_x == "negative":
                initial_x -= 1
            else:
                initial_x += 1

            time.sleep(1)

            feedback_msg.curr_position = [initial_x, initial_y]
            goal_handle.publish_feedback(feedback_msg)
            position_msg.position = [initial_x, initial_y]
            self.position_updater_publisher.publish(position_msg)

        direction_y = target_y - initial_y
        if direction_y < 0:
            direction_y = "negative"
        elif direction_y > 0:
            direction_y = "positive"
        else:
            direction_y = "zero"

        while initial_y != target_y and direction_y != "zero":

            position_msg = Position()

            if direction_y == "negative":
                initial_y -= 1
            else:
                initial_y += 1

            time.sleep(1)

            feedback_msg.curr_position = [initial_x, initial_y]
            goal_handle.publish_feedback(feedback_msg)
            position_msg.position = [initial_x, initial_y]
            self.position_updater_publisher.publish(position_msg)

        goal_handle.succeed()
        result = Move.Result()
        result.success = True
        return result

def main():
    rclpy.init()
    action_server = MovementActionServer()
    rclpy.spin(action_server)
    rclpy.shutdown()

if __name__ == "__main__":
    main()