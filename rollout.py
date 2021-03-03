'''
Basic MCTS implementation
Graeme Best
Oregon State University
Jan 2020
'''

from cost import cost
import random
import copy
import sys
import Simulator

def rollout(subsequence, action_set, robot, map, budget):
    # Random rollout policy
    # Pick random actions until budget is exhausted
    # To Add:Robot current location is needed for each action

    location_before_rollout = robot.get_loc()
    # print("Location before rollout: ", location_before_rollout)

    num_actions = len(action_set)
    if num_actions <= 0:
        raise ValueError('rollout: num_actions is ' + str(num_actions))
    sequence = copy.deepcopy(subsequence)
    while cost(sequence) < budget:
        r = random.randint(0,num_actions-1)
        action = action_set[r]
        action_direction = action.label
        robot.move(action_direction)
        action.coords = robot.get_loc()
        sequence.append(action)

    simulator = Simulator(map, robot)
    simulator.run()

    robot.start_loc = location_before_rollout
    # print("Check if location is same as before: ", robot.start_loc)
    robot.reset_robot()

    return sequence
