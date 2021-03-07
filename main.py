import copy
from random import random
from GreedyPlanner import GreedyPlanner
from RandomPlanner import RandomPlanner
from mcts import dec_mcts
from Map import Map
from Robot import Robot
from Simulator import Simulator
from plot_tree import plotTree

def run_dec_mcts(budget, num_samples, c_budget, explore_exploit, input_robots, input_map, r_policy):
    robots = copy.deepcopy(input_robots)
    world_map = copy.deepcopy(input_map)

    #Generate a path the robots (Dec-MCTS goes here)
    dec_mcts_paths = dec_mcts(budget, num_samples, c_budget, exploration_exploitation_parameter, robots, world_map)
    for r in robots:
        r.reset_robot()

    #Use the Simulator to evaluate the final paths
    simulator = Simulator(world_map, robots)
    simulator.run()

    #See the results
    simulator.visualize()
    print("{} Dec-MCTS Score: {}".format(r_policy, simulator.get_score()))

    for r in robots:
        r.reset_robot()
    simulator.reset_game()

    #Determine longest path to guide the Random and Greedy Planners
    max_length = -1
    for path in dec_mcts_paths:
        if len(path) > max_length:
            max_length = len(path)

    return max_length

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

    #See the results
    simulator.visualize()
    print("Random Score: {}".format(simulator.get_score()))
    simulator.reset_game()

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

    #See the results
    simulator.visualize()
    print("Greedy Score: {}".format(simulator.get_score()))
    simulator.reset_game()

if __name__ == "__main__":
    #Dec-MCTS Parameters
    budget = 60
    computational_budget = 10
    num_samples = 10
    exploration_exploitation_parameter = 1.0 # =1.0 is recommended. <1.0 more exploitation. >1.0 more exploration.

    #Map Parameters
    bounds = (0, 10)
    num_survivors = 50
    num_hotspots = 10
    num_damages = 2

    world_map = Map(bounds, num_survivors, num_hotspots, num_damages)
    robot = Robot(0, 0, bounds, world_map)
    robot2 = Robot(10, 10, bounds, world_map)
    robots = [robot, robot2]

    length_of_path = run_dec_mcts(budget, num_samples, computational_budget, exploration_exploitation_parameter, robots, world_map, 'heuristic')
    length_of_path = run_dec_mcts(budget, num_samples, computational_budget, exploration_exploitation_parameter, robots, world_map, 'uniform')
    run_random_planner(length_of_path, robots, world_map)
    run_greedy_planner(length_of_path, robots, world_map)
    
    print("Done :)")