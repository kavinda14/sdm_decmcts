'''
Basic MCTS implementation
Graeme Best
Oregon State University
Jan 2020
'''

from mcts import mcts
from action import Action, printActionSequence, listActionSequence
from tree_node import countNodes
from plot_tree import plotTree
import time, sys

def mcts_planner(robot):
    # Setup the problem
    num_actions = 4  # 0 = left, 1 = right, 2 = up, 3 = down
    action_set = []
    # for i in range(num_actions):
    #     id = i
    #     action_set.append(Action(id,i))
    action_set.append(Action(1, 'left'))
    action_set.append(Action(2, 'right'))
    action_set.append(Action(3, 'forward'))
    action_set.append(Action(4, 'backward'))

    budget = 20
    # Solve it with MCTS
    exploration_exploitation_parameter = .0001 # =1.0 is recommended. <1.0 more exploitation. >1.0 more exploration.
    max_iterations = 1000
    [solution, root, list_of_all_nodes, winner] = mcts( action_set, budget, max_iterations, exploration_exploitation_parameter, robot)

    # Display the tree
    print("MCTS Solution")
    # plotTree(list_of_all_nodes, winner, action_set, False, budget, 1, exploration_exploitation_parameter)
    # plotTree(list_of_all_nodes, winner, action_set, True, budget, 2, exploration_exploitation_parameter)
    path = solution
    return path




    
    