'''
Basic MCTS implementation
Graeme Best
Oregon State University
Jan 2020
'''

from mcts import mcts

def mcts_planner(robot, map):
    # Solve it with MCTS
    budget = 250
    max_iterations = 2000
    exploration_exploitation_parameter = .01 # =1.0 is recommended. <1.0 more exploitation. >1.0 more exploration.
    path = mcts(budget, max_iterations, exploration_exploitation_parameter, robot, map)

    # Display the tree
    print("MCTS Solution")
    # plotTree(list_of_all_nodes, winner, action_set, False, budget, 1, exploration_exploitation_parameter)
    # plotTree(list_of_all_nodes, winner, action_set, True, budget, 2, exploration_exploitation_parameter)
    return path




    
    