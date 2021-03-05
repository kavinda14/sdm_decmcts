import copy
from GreedyPlanner import GreedyPlanner
from numpy.core.records import get_remaining_size
from RandomPlanner import RandomPlanner
from mcts import mcts
from Map import Map
from Robot import Robot
from Simulator import Simulator
from plot_tree import plotTree

def run_mcts(budget, max_iterations, explore_exploit, input_robots, input_map, r_policy):
    robots = copy.deepcopy(input_robots)
    world_map = copy.deepcopy(input_map)
    #Generate a path the robots (Dec-MCTS goes here)
    for r in robots:
        # Solve it with MCTS
        [mcts_path, list_of_all_nodes, winner] = mcts(budget, max_iterations, explore_exploit, robot, world_map, r_policy)

        # Display the tree
        # print("MCTS Solution")
        # plotTree(list_of_all_nodes, winner, False, budget, 1, exploration_exploitation_parameter)
        # plotTree(list_of_all_nodes, winner, True, budget, 2, exploration_exploitation_parameter)

        #Display path solution
        # print("Path from MCTS", [p.location for p in mcts_path])
        # print("Path Length: ", len(mcts_path))
        r.set_path(mcts_path)

    #Use the Simulator to evaluate the final paths
    simulator = Simulator(world_map, robots)
    simulator.run()

    #See the results
    simulator.visualize()
    print("{} MCTS Score: {}".format(r_policy, simulator.get_score()))

    for r in robots:
        r.reset_robot()
    simulator.reset_game()

    return len(mcts_path)

def run_random_planner(budget, input_robots, input_map):
    robots = copy.deepcopy(input_robots)
    world_map = copy.deepcopy(input_map)
    for r in robots:
        r.reset_robot()

    for r in robots:
        planner = RandomPlanner(budget)
        random_path = planner.random_path(r)
        r.set_path(random_path)
        # print("Path from Random Planner", [p.location for p in random_path])

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
        r.set_path(greedy_path)
        # print("Path from Greedy Planner", [p.location for p in greedy_path])

    #Use the Simulator to evaluate the final paths
    simulator = Simulator(world_map, robots)
    simulator.run()

    #See the results
    simulator.visualize()
    print("Greedy Score: {}".format(simulator.get_score()))
    simulator.reset_game()

if __name__ == "__main__":
    #Create robots to interact with the environment
    budget = 60
    bounds = (0, 10)
    max_iterations = 5000
    exploration_exploitation_parameter = 1.0 # =1.0 is recommended. <1.0 more exploitation. >1.0 more exploration.
    world_map = Map(bounds)
    robot = Robot(bounds, world_map)
    robots = [robot]

    length_of_path = run_mcts(budget, max_iterations, exploration_exploitation_parameter, robots, world_map, 'heuristic')
    length_of_path = run_mcts(budget, max_iterations, exploration_exploitation_parameter, robots, world_map, 'uniform')
    run_random_planner(length_of_path, robots, world_map)
    run_greedy_planner(length_of_path, robots, world_map)
    
    print("Done :)")