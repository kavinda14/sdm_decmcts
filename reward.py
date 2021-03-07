'''
Basic MCTS implementation
Graeme Best
Oregon State University
Jan 2020
'''

import math
from Simulator import Simulator
import sys

def reward(action_sequence, robot, map):

    unique_survivor_locs = set()

    map_before_other_robot_simulation = map
    for sequence in robot.top_10_sequences_other_robots:    
        simulator = Simulator(map, [robot])    
        other_robot_map = map_before_other_robot_simulation
        other_robot_survivor_locs = simulate_and_get_survivor_locs(robot, sequence, simulator, map)   
        other_robot_survivor_locs.add(loc for loc in other_robot_survivor_locs)
        map = map_before_other_robot_simulation

    # Now I'm finding the survivors for the current robot.
    simulator = Simulator(map, [robot])
    robot_survivor_locs = simulate_and_get_survivor_locs(robot, action_sequence, simulator, map)   

    for loc in robot_survivor_locs:
        if loc in unique_survivor_locs:
            robot_survivor_locs.remove(loc)
    
    return len(robot_survivor_locs)


def simulate_and_get_survivor_locs(robot, sequence, simulator, map):    
    robot.set_path(sequence)
    simulator = Simulator(map, [robot])
    simulator.run()
    return map.survivor_locs

# def reward(action_sequence, robot, map):
#     # path_before = robot.path
#     robot.set_path(action_sequence)
#     simulator = Simulator(map, [robot])
#     simulator.run()
#     score = simulator.get_score()

#     print(robot.top_10_sequences)
#     sys.exit(0)

#     return score


# def reward(current_action_sequence, other_action_sequence, robot, map):

#     # old_current_action_sequence = current_action_sequence
#     #How do you account for everything that the other robots found and I didn't?
#     #Try evaluating all paths separately and remove the common survivor paths.
#     #We get a list of lists for the other_action_sequences.

#     for current_action in current_action_sequence:
#         for other_action in other_action_sequence:
#             if current_action.location == other_action.location:
#                 current_action_sequence.remove(current_action)

#     # print("Length diff: ", len(old_current_action_sequence) - len(current_action_sequence))

#     robot.set_path(current_action_sequence)
#     simulator = Simulator(map, [robot])
#     simulator.run()
#     score = simulator.get_score()

#     return score

def normalize_reward(action_sequence, reward):
    # Normalise between 0 and 1
    max_reward = len(action_sequence) #-1
    if max_reward == 0:
        reward_normalised = 0
    else:
        reward_normalised = float(reward) / float(max_reward)
    return reward_normalised


# def reward_graeme(action_sequence):
#     # A simple reward function
#     # Iterate through the sequence, looking at pairs
#     reward = 0
#     for i in range(len(action_sequence)-1): # Yes, we want -1 here
        
#         # Pick out a pair
#         first = action_sequence[i]
#         second = action_sequence[i+1]

#         # Add to the reward if second is +1
#         if first.id + 1 == second.id:
#             reward += 1

#     # Also give reward for first action by itself
#     if action_sequence[0].id == 1:
#         reward += 1

#     # Normalise between 0 and 1
#     max_reward = len(action_sequence) #-1
#     if max_reward == 0:
#         reward_normalised = 0
#     else:
#         reward_normalised = float(reward) / float(max_reward)
#     return reward_normalised
