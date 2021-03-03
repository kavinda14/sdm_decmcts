'''
Basic MCTS implementation
Graeme Best
Oregon State University
Jan 2020
'''

import math
from Simulator import Simulator

def reward(action_sequence, robot, map):
    # path_before = robot.path
    robot.set_path(action_sequence)
    simulator = Simulator(map, [robot])
    simulator.run()
    score = simulator.get_score()
    return score
    
def euclidean_distance(p1, p2):
    x1 = p1[0]
    y1 = p1[1]
    x2 = p2[0]
    y2 = p2[1]

    return math.sqrt((y2-y1)**2 + (x2-x1)**2)

def normalize_reward(action_sequence, reward):
    # Normalise between 0 and 1
    max_reward = len(action_sequence) #-1
    if max_reward == 0:
        reward_normalised = 0
    else:
        reward_normalised = float(reward) / float(max_reward)
    return reward_normalised


# def reward(action_sequence, robot, map):
#     hotspots = map.hotspots
#     #It picks up an empty tuple at the start, so I just delete it.
#     reward = 0

#     for action in action_sequence:
#         if action.coords == ():
#             continue
#         rand_index = random.randint(0, len(action_sequence))
#         closest_hotspot_distance = math.inf
#         for hotspot in hotspots:
#             dist = euclidean_distance(action.coords, hotspot)
#             closest_hotspot_distance = min(closest_hotspot_distance, dist)
#         #Notice that we are calculating a negative reward here.
#         #Logic: closer euclidean distance to a hotspot means higher reward.
#         reward += -closest_hotspot_distance
#         # print(reward)
#     # sys.exit()

#     # print(reward)
#     # print(normalize_reward(action_sequence, reward))
#     # sys.exit()

#     return normalize_reward(action_sequence, reward)

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
