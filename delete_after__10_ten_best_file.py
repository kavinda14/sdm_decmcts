'''
Basic MCTS implementation
Graeme Best
Oregon State University
Jan 2020
'''

from tree_node import TreeNode
from reward import reward
from cost import cost
from rollout import rollout
from action import Action, printActionSequence
import copy
import random
import math

def mcts( action_set, budget, max_iterations, exploration_exploitation_parameter, robot):

    ################################
    # Setup
    start_sequence = []
    unpicked_child_actions = copy.deepcopy(action_set)
    root = TreeNode(node_id = 0, parent=None, sequence=start_sequence, budget=budget, unpicked_child_actions=unpicked_child_actions)
    list_of_top_10_nodes_sequences = []
    list_of_top_10_nodes_ids = []
    list_of_top_10_nodes = []
    list_of_all_nodes = []
    list_of_all_nodes.append(root) # for debugging only
    current_node = 0
    ################################
    # Main loop
    for iter in range(max_iterations):

        print("Current Iteration:", iter)
        print("Robot Loc: ", robot.get_loc())
        ################################
        # Selection and Expansion
        # move recursively down the tree from root
        # then add a new leaf node
        print("Selection and Expansion")
        current = root
        #Reset the Robot's Stating Point
        # robot.reset_robot()
        print("Robot Loc: ", robot.get_loc())
        # Remove invalid actions from root state - pat
        for a in current.unpicked_child_actions:
            direction = a.label
            if not robot.check_valid_move(direction):
                current.unpicked_child_actions.remove(a)

        while True:
            # Are there any children to be added here?
            if current.unpicked_child_actions: # if not empty
                # Pick one of the children that haven't been added | Select a valid direction
                # Do this at random
                num_unpicked_child_actions = len(current.unpicked_child_actions)
                if num_unpicked_child_actions == 1:
                    child_index = 0
                else:
                    child_index = random.randint(0,num_unpicked_child_actions-1)
                child_action = current.unpicked_child_actions[child_index]

                # Move the robot
                robot.move(child_action.label) # pat

                # Remove the child form the unpicked list
                del current.unpicked_child_actions[child_index]

                # Setup the new action sequence
                new_sequence = copy.deepcopy(current.sequence)
                new_sequence.append(child_action)
                new_budget_left = budget - cost(new_sequence)

                # Setup the new child's unpicked children
                # Remove any over budget or invalid children from this set
                new_unpicked_child_actions = copy.deepcopy(action_set)
                def is_overbudget_or_invalid(a): # pat
                    seq_copy = copy.deepcopy(current.sequence)
                    seq_copy.append(a)
                    result = robot.check_valid_move(a.label)
                    if cost(seq_copy) > budget:
                        return True # a will not be added to the new_unpicked_child_actions list
                    if result == False:
                        return True # a will not be added to the new_unpicked_child_actions list
                    else:
                        return False
                    # return cost(seq_copy) > budget #false

                #removes any new children if from the child if they go over budget or are invalid action
                new_unpicked_child_actions = [a for a in new_unpicked_child_actions if not is_overbudget_or_invalid(a)]

                # Create the new node and add it to the tree
                printActionSequence(new_sequence)
                current_node += 1
                new_child_node = TreeNode(node_id = current_node, parent=current, sequence=new_sequence, budget=new_budget_left, unpicked_child_actions=new_unpicked_child_actions)
                current.children.append(new_child_node)
                current = new_child_node
                list_of_all_nodes.append(new_child_node) # for debugging only
                print('---')
                break # don't go deeper in the tree...
            else:
                # All possible children already exist
                # Therefore recurse down the tree
                # using the UCT selection policy

                if not current.children:
                    # Reached planning horizon -- just do this again
                    break
                else:
                    # Define the UCB
                    def ucb(average, n_parent, n_child):
                        return average + exploration_exploitation_parameter * math.sqrt( (2*math.log(n_parent)) / float(n_child) )

                    # Pick the child that maximises the UCB
                    n_parent = current.num_updates
                    best_child = -1
                    best_ucb_score = 0
                    for child_idx in range(len(current.children)):
                        child = current.children[child_idx]
                        ucb_score = ucb(child.average_evaluation_score, n_parent, child.num_updates)
                        if best_child == -1 or (ucb_score > best_ucb_score):
                            best_child = child
                            best_ucb_score = ucb_score

                    # Recurse down the tree
                    # robot.move(best_child.sequence[0].label) # pat
                    current = best_child


        ################################
        # Rollout
        print("Rollout Phase")
        rollout_sequence = rollout(subsequence=current.sequence, action_set=action_set, budget=budget)
        rollout_reward = reward(action_sequence=rollout_sequence)

        ################################
        # Back-propagation
        # update stats of all nodes from current back to root node
        print("Back-Propagation Phase")
        parent = current
        while parent: # is not None
            # Update the average
            parent.updateAverage(rollout_reward)

            # Recurse up the tree
            parent = parent.parent
        print('====================')
        print('====================')
    ################################
    # Extract solution
    # calculate best solution so far
    # by recursively choosing child with highest average reward
    print('Extracting Solutions')
    i = 0
    while i != 10:
        current = root
        while current.children and all_children_nodes_are_not_in_the_list(current, list_of_top_10_nodes_ids) : # is not empty
            # Find the child with best score
            best_score = 0
            best_child = -1
            for child_idx in range(len(current.children)):
                child = current.children[child_idx]
                # Only consider child nodes who have not been placed in the list - pat
                if not child.node_id in list_of_top_10_nodes_ids:
                    score = child.average_evaluation_score
                    if best_child == -1 or (score > best_score):
                        best_child = child
                        best_score = score
            current = best_child

        # Append each iteration's node with the best average evaluation score
        list_of_top_10_nodes_ids.append(current.node_id)
        list_of_top_10_nodes.append(current)
        # Append the the node's action sequence into a list
        print('Node: ', current.node_id)
        solution = current.sequence
        solution = listActionSequence(solution)
        solution = direction_path_to_state_path_converter(solution, robot.start_loc)

        print('Solution: ', solution)
        list_of_top_10_nodes_sequences.append(solution)

        i += 1
    print('Top 10 Node List: ', list_of_top_10_nodes)
    print('Top 10 Node Id List: ', list_of_top_10_nodes_ids)
    print('Top 10 Sequences List: ', list_of_top_10_nodes_sequences)

    # Select the best node from the top 10 nodes list and provide it as the solution
    best_node = list_of_top_10_nodes[0] # there are still 9 other nodes to see the solutions of
    solution = best_node.sequence
    solution = listActionSequence(solution)
    solution = direction_path_to_state_path_converter(solution, robot.start_loc)
    winner = best_node
    print('length of node list: ', len(list_of_all_nodes))
    return [solution, root, list_of_all_nodes, winner]

def listActionSequence(action_sequence):
    action_list = []
    for action in action_sequence:
        action_list.append(action.label)
    print("MCTS Solution as Directions: ", action_list)
    return action_list

def direction_path_to_state_path_converter(solution,starting_coor):
    direction_list = solution

    state_list = []
    coordinate = list(starting_coor)
    state_list.append(coordinate[:])
    for a in direction_list:
        # print(a)
        if a == 'left':
            coordinate[0] = coordinate[0] - 1
        if a == 'right':
            coordinate[0] = coordinate[0] + 1
        if a == 'forward':
            coordinate[1] = coordinate[1] + 1
        if a == 'backward':
            coordinate[1] = coordinate[1] - 1
        b = []
        # print(coordinate)
        b.append(coordinate[:])
        state_list = state_list + b

    print("MCTS Solution as States: ", state_list)
    return state_list


def all_children_nodes_are_not_in_the_list(current, list_of_top_10_nodes):
    """
    Check if all the children of the current node is are already
    accounted for in the top 10 node list.
    """
    num_of_children_nodes_in_top_10_list = 1
    for child_idx in range(len(current.children)):
        child = current.children[child_idx]
        if child.node_id in list_of_top_10_nodes:
            num_of_children_nodes_in_top_10_list += 1
    if num_of_children_nodes_in_top_10_list < len(current.children):
        return True
    else:
        return False
