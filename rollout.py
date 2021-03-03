'''
Basic MCTS implementation
Graeme Best
Oregon State University
Jan 2020
'''

from cost import cost
import random
import copy

def rollout(path, robot, budget):
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