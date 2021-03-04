from cost import cost
import random
import copy
import sys

def uniform_rollout(path, robot, budget):
    #Possible Actions
    action_set = list()
    action_set.append('left')
    action_set.append('right')
    action_set.append('forward')
    action_set.append('backward')

    # Random rollout policy
    # Pick random actions until budget is exhausted
    new_path = copy.deepcopy(path)
    robot.set_path(path)

    #Move Robot along the path
    action = "start"
    while action:
        action = robot.follow_path()
        # Move the robot
        robot.move(action)

    while cost(new_path) < budget:
        r = random.randint(0, len(action_set)-1)
        action = action_set[r]

        robot.move(action)
        new_path.append(robot.get_loc())

    return path

def heuristic_rollout(path, robot, budget, map):
    #Possible Actions
    action_set = list()
    action_set.append('left')
    action_set.append('right')
    action_set.append('forward')
    action_set.append('backward')

    # Random rollout policy
    # Pick random actions until budget is exhausted
    new_path = copy.deepcopy(path)
    robot.set_path(path)

    #Move Robot along the path
    action = "start"
    while action:
        action = robot.follow_path()
        # Move the robot
        robot.move(action)

    while cost(new_path) < budget:
        curr_loc = robot.get_loc()

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
            if dist < min_dist:
                best_action = a
                min_dist = dist
            robot.set_loc(curr_loc[0], curr_loc[1])

        #Choose best action
        robot.move(best_action)
        new_path.append(robot.get_loc())

    return path