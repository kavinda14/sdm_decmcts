'''
Basic MCTS implementation
Graeme Best
Oregon State University
Jan 2020
'''

from mcts import mcts

def mcts_planner(robot, map):
    # Setup the problem
    action_set = []
    # for i in range(num_actions):
    #     id = i
    #     action_set.append(Action(id,i))
    # action_set.append(Action(1, 'left'))
    # action_set.append(Action(2, 'right'))
    # action_set.append(Action(3, 'forward'))
    # action_set.append(Action(4, 'backward'))

    budget = 250
    # Solve it with MCTS
    exploration_exploitation_parameter = .1 # =1.0 is recommended. <1.0 more exploitation. >1.0 more exploration.
    max_iterations = 1000
    path = mcts(budget, max_iterations, exploration_exploitation_parameter, robot, map)

    # Display the tree
    print("MCTS Solution")
    # plotTree(list_of_all_nodes, winner, action_set, False, budget, 1, exploration_exploitation_parameter)
    # plotTree(list_of_all_nodes, winner, action_set, True, budget, 2, exploration_exploitation_parameter)
    return path




    
    