'''
Basic MCTS implementation
Graeme Best
Oregon State University
Jan 2020
'''

from plot_tree import plotTree
from mcts import mcts

def mcts_planner(robot, map):
    # Solve it with MCTS
    budget = 250
    max_iterations = 10000
    exploration_exploitation_parameter = .2 # =1.0 is recommended. <1.0 more exploitation. >1.0 more exploration.
    [path, list_of_all_nodes, winner] = mcts(budget, max_iterations, exploration_exploitation_parameter, robot, map)

    # Display the tree
    print("MCTS Solution")
    # plotTree(list_of_all_nodes, winner, False, budget, 1, exploration_exploitation_parameter)
    # plotTree(list_of_all_nodes, winner, True, budget, 2, exploration_exploitation_parameter)
    return path


def dec_mcts_planner(robots, map):
    budget = 250
    exploration_exploitation_parameter = .2 # = 1.0 is recommended. <1.0 more exploitation. >1.0 more exploration.

    mcts_max_number_of_samples = 10
    max_iterations = 5
    budget_complete_robot_list = []
    robot_paths = []

    # Initialize Every Robots MCTS Tree
    for robot in robots:
        # MCTS Tree initialization
        mcts_initialize(budget, mcts_max_number_of_samples, exploration_exploitation_parameter, robot, map)

    #Start Dec-MCTS
    k = 0
    while k < 100:    #len(budget_complete_robot_list) < len(robots):  # Computational Budget

        for i in range(max_iterations):
            # Grow Tree for each Robot
            for robot in robots:
                # Robots determines their top 10 best sets of actions(sequences)
                mcts(budget, mcts_max_number_of_samples, exploration_exploitation_parameter, robot, map)

            # Communicate and Receive: Transfer of Sets of top 10 sequences for each Robot after they all grow their Tree
            for robot1 in robots:
                for robot2 in robots:
                    if robot1 != robot2:
                        robot1.list_of_each_other_robots_top_10_sequences.append(robot2.top_10_sequences)
        k += 1

    print("DEC_MCTS Solution")
    for robot in robots:
        robot.paths.append(robot.final_path)

    return robot_paths
    
    