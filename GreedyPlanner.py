from mcts import State
from random import randint
from cost import cost
import sys

class GreedyPlanner():
    def __init__(self, budget):
        self.budget = budget

    def greedy_path(self, robot, map):
        #Use robot to simulate a random path
        path = list()

        #Possible Actions
        action_set = list()
        action_set.append('left')
        action_set.append('right')
        action_set.append('forward')
        action_set.append('backward')

        # Pick random actions until budget is exhausted
        while cost(path) < self.budget:
            curr_loc = robot.get_loc()
            r = randint(0, len(action_set)-1)

            #Get closest hotspot
            closest_hotspot = None
            min_dist = sys.maxsize
            for h in map.hotspots:
                dist = map.euclidean_distance(curr_loc, h)
                if dist < min_dist:
                    closest_hotspot = h
                    min_dist = dist

            #Determine action that moves us towards a hotspot
            best_action = None
            min_dist = sys.maxsize
            for a in action_set:
                robot.move(a)
                dist = map.euclidean_distance(robot.get_loc(), closest_hotspot)
                if dist < min_dist and dist > 0.05:
                    best_action = a
                    min_dist = dist
                robot.set_loc(curr_loc[0], curr_loc[1])

            #Choose best action
            robot.move(best_action)
            path.append(State(0, best_action, robot.get_loc()))

        robot.reset_robot()
        return path