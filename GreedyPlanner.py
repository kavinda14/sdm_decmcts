from mcts import State
from random import randint
from cost import cost
import sys

class GreedyPlanner():
    def __init__(self, budget):
        self.budget = budget
        self.visited_hotspots = set()

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
            hotspots = [h for h in map.hotspots if not h in self.visited_hotspots]
            for h in hotspots:
                dist = map.euclidean_distance(curr_loc, h)
                if dist < min_dist:
                    closest_hotspot = h
                    min_dist = dist

            #Determine action that moves us towards a hotspot
            if closest_hotspot:
                #If we haven't visited all the hotspots, keep visiting them
                best_action = None
                min_dist = sys.maxsize
                for a in action_set:
                    robot.move(a)
                    dist = map.euclidean_distance(robot.get_loc(), closest_hotspot)
                    if dist < min_dist:
                        best_action = a
                        min_dist = dist
                    robot.set_loc(curr_loc[0], curr_loc[1])

                #If the robot visits a hotspot, don't visit it again
                if min_dist <= robot.sensing_range:
                    self.visited_hotspots.add(closest_hotspot)
                    
                #Choose best action
                robot.move(best_action)
                path.append(State(0, best_action, robot.get_loc()))
            else:
                #Else move Randomly
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