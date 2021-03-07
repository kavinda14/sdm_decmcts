import math
from Simulator import Simulator
import sys

def reward(current_robot_paths, other_robot_paths, robot, world_map):

    survivor_locs_found_by_other_robots = set()

    for path in other_robot_paths:
        other_robot = Robot(2, 2)    
        other_robot_survivor_locs = simulate_and_get_survivor_locs(other_robot, path, world_map)   
        survivor_locs_found_by_other_robots.add(loc for loc in other_robot_survivor_locs)

    current_robot_survivor_locs = simulate_and_get_survivor_locs(robot, current_robot_paths, world_map)   

    for loc in current_robot_survivor_locs:
        if loc in survivor_locs_found_by_other_robots:
            current_robot_survivor_locs.remove(loc)

    score = len(current_robot_survivor_locs)
    
    return score


def simulate_and_get_survivor_locs(robot, path, world_map):    
    robot.set_path(path)
    simulator = Simulator(world_map, [robot])
    simulator.run()
    return simulator.visited_survivors

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

# def normalize_reward(action_sequence, reward):
#     # Normalise between 0 and 1
#     max_reward = len(action_sequence) #-1
#     if max_reward == 0:
#         reward_normalised = 0
#     else:
#         reward_normalised = float(reward) / float(max_reward)
#     return reward_normalised


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
