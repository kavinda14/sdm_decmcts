from mcts import State
from random import randint

class RandomPlanner():
    def __init__(self, length):
        self.path_length = length

    def random_path(self, robot):
        #Use robot to simulate a random path
        path = list()

        for i in range(0, self.path_length):
            #Random direction
            randNumb = randint(0, 3)
            direction = None
            if randNumb == 0:
                direction = 'left'
            if randNumb == 1:
                direction = 'right'
            if randNumb == 2:
                direction = 'backward'
            if randNumb == 3:
                direction = 'forward'

            robot.move(direction)
            path.append(State(0, direction, robot.get_loc()))
        robot.reset_robot()
        return path