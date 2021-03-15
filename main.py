import copy
from random import random
from GreedyPlanner import GreedyPlanner
from RandomPlanner import RandomPlanner
from mcts import dec_mcts
from Map import Map
from Robot import Robot
from Simulator import Simulator
import numpy as np
from plot_tree import plotTree

def run_dec_mcts(budget, num_samples, c_budget, explore_exploit, input_robots, input_map, r_policy):
    robots = copy.deepcopy(input_robots)
    world_map = copy.deepcopy(input_map)

    #Generate a path the robots (Dec-MCTS goes here)
    dec_mcts_paths = dec_mcts(budget, num_samples, c_budget, explore_exploit, robots, world_map, r_policy)
    for r in robots:
        r.reset_robot()

    #Use the Simulator to evaluate the final paths
    simulator = Simulator(world_map, robots)
    simulator.run()
    score = simulator.get_score()

    #See the results
    # simulator.visualize()
    # print("{} Dec-MCTS Score: {}".format(r_policy, simulator.get_score()))

    for r in robots:
        r.reset_robot()
    simulator.reset_game()

    #Determine longest path to guide the random and Greedy Planners
    max_length = -1
    for path in dec_mcts_paths:
        if len(path) > max_length:
            max_length = len(path)

    return max_length, score

def run_random_planner(budget, input_robots, input_map):
    robots = copy.deepcopy(input_robots)
    world_map = copy.deepcopy(input_map)
    for r in robots:
        r.reset_robot()

    for r in robots:
        planner = RandomPlanner(budget)
        random_path = planner.random_path(r)
        r.final_path = random_path
        
    #Use the Simulator to evaluate the final paths
    simulator = Simulator(world_map, robots)
    simulator.run()
    score = simulator.get_score()

    #See the results
    # simulator.visualize()
    # print("random Score: {}".format(simulator.get_score()))
    simulator.reset_game()

    return score

def run_greedy_planner(budget, input_robots, input_map):
    robots = copy.deepcopy(input_robots)  
    world_map = copy.deepcopy(input_map)  
    for r in robots:
        r.reset_robot()
        
    for r in robots:
        planner = GreedyPlanner(budget)
        greedy_path = planner.greedy_path(r, world_map)
        r.final_path = greedy_path
    
    #Use the Simulator to evaluate the final paths
    simulator = Simulator(world_map, robots)
    simulator.run()
    score = simulator.get_score()

    #See the results
    # simulator.visualize()
    # print("Greedy Score: {}".format(simulator.get_score()))
    simulator.reset_game()

    return score

if __name__ == "__main__":
    #Number of Trials
    num_trials = 100

    #Dec-MCTS Parameters
    budget = 1000
    computational_budget = 50
    num_samples = 20
    exploration_exploitation_parameter = 1.0 # =1.0 is recommended. <1.0 more exploitation. >1.0 more exploration.

    #Map Parameters
    bounds = (0, 20)
    num_survivors = 50
    num_hotspots = 10
    num_damages = 25

    winner_dict = dict()
    scores_dict = dict()
    scores_dict['dec-heuristic'] = list()
    scores_dict['dec-uniform'] = list()
    scores_dict['random'] = list()
    scores_dict['greedy'] = list()
    
    for i in range(num_trials):
        #Set up problem
        print("Experiment {}".format(i))
        world_map = Map(bounds, num_survivors, num_hotspots, num_damages)
        robots = list()
        robot = Robot(0, 0, bounds, world_map)
        robot2 = Robot(0, 0, bounds, world_map)
        robots = [robot, robot2]

        #Run Planners
        length_of_path, h_score = run_dec_mcts(budget, num_samples, computational_budget, exploration_exploitation_parameter, robots, world_map, 'heuristic')
        length_of_path, u_score = run_dec_mcts(budget, num_samples, computational_budget, exploration_exploitation_parameter, robots, world_map, 'uniform')
        r_score = run_random_planner(length_of_path, robots, world_map)
        g_score = run_greedy_planner(length_of_path, robots, world_map)

        #Collect Data
        scores = [h_score, u_score, r_score, g_score]
        scores_dict['dec-heuristic'].append(h_score)
        scores_dict['dec-uniform'].append(u_score)
        scores_dict['random'].append(r_score)
        scores_dict['greedy'].append(g_score)

        max_index = scores.index(max(scores))
        if max_index == 0:
            if not 'dec-heuristic' in winner_dict:
                winner_dict['dec-heuristic'] = 0
            winner_dict['dec-heuristic'] += 1
        elif max_index == 1:
            if not 'dec-uniform' in winner_dict:
                winner_dict['dec-uniform'] = 0
            winner_dict['dec-uniform'] += 1
        elif max_index == 2:
            if not 'random' in winner_dict:
                winner_dict['random'] = 0
            winner_dict['random'] += 1
        elif max_index == 3:
            if not 'greedy' in winner_dict:
                winner_dict['greedy'] = 0
            winner_dict['greedy'] += 1

    #Summary Stats
    print(scores_dict)
    for k, v in scores_dict.items():
        print('{} Avg: {}, Std: {}'.format(k, np.mean(v), np.std(v)))
    
    print("Winners dict: {}".format(winner_dict))