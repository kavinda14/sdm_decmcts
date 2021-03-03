'''
Basic MCTS implementation
Graeme Best
Oregon State University
Jan 2020
'''

from State import State
from tree_node import TreeNode
from reward import reward
from cost import cost
from rollout import heuristic_rollout, uniform_rollout
import copy
import random
import math
import sys

class State():
    '''Container for states in the graph'''
    def __init__(self, id, label, location):
        self.id = id
        self.label = label
        self.location = location

    def toString(self):
        return str(self.label)
    def toInt(self):
        return int(self.label)


def generate_neighbors(current_state, bounds):
    neighbors = list()
    current_loc = current_state.location
    if current_loc[0]-1 >= bounds[0]: #left
        new_loc = (current_loc[0]-1, current_loc[1])
        neighbors.append(State(1, "left", new_loc))

    if current_loc[0]+1 <= bounds[1]: #right
        new_loc = (current_loc[0]+1, current_loc[1])
        neighbors.append(State(2, "right", new_loc))

    if current_loc[1]+1 <= bounds[1]: #forwards
        new_loc = (current_loc[0], current_loc[1]+1)
        neighbors.append(State(3, "forward", new_loc))

    if current_loc[1]-1 >= bounds[0]: #backwards
        new_loc = (current_loc[0], current_loc[1]-1)
        neighbors.append(State(4, "backwards", new_loc))

    return neighbors

def mcts(budget, max_iterations, exploration_exploitation_parameter, robot, world_map):
    ################################
    # Setup
    start_sequence = list()
    start_sequence = [State(0, "root", robot.start_loc)]
    unpicked_child_actions = generate_neighbors(start_sequence[0], world_map.bounds)
    root = TreeNode(parent=None, sequence=start_sequence, budget=budget, unpicked_child_actions=unpicked_child_actions)

    list_of_all_nodes = list()
    list_of_all_nodes.append(root) # for debugging only

    visited_nodes = set()
    visited_nodes.add(robot.start_loc)
    # visited_nodes.add(root.sequence[0])

    ################################
    # Main loop
    for i in range(max_iterations):
        if i%100 == 0:
            print("Percent Complete: {:.2f}%".format(i/float(max_iterations)*100))

        # Selection and Expansion
        # move recursively down the tree from root
        # then add a new leaf node
        # print("Selection and Expansion")
        current = root
        robot.reset_robot()

        while True:
            # Are there any children to be added here?
            if current.unpicked_child_actions: # if not empty
                # Pick one of the children that haven't been added | Select a valid direction
                num_unpicked_child_actions = len(current.unpicked_child_actions)
                child_index = random.randint(0, num_unpicked_child_actions-1)
                child_action = current.unpicked_child_actions[child_index]

                # Move the robot
                if not child_action in visited_nodes:
                    # visited_nodes.add(child_action)

                    # Remove the child form the unpicked list
                    del current.unpicked_child_actions[child_index]

                    # Setup the new action sequence
                    new_sequence = copy.deepcopy(current.sequence)
                    new_sequence.append(child_action)
                    new_budget_left = budget - cost(new_sequence)

                    # Setup the new child's unpicked children
                    # Remove any over budget or invalid children from this set
                    new_unpicked_child_actions = generate_neighbors(child_action, world_map.bounds)

                    def node_is_valid(a):
                        seq_copy = copy.deepcopy(current.sequence)
                        seq_copy.append(a)
                        end_loc = seq_copy[-1]

                        # in_visited_nodes = end_loc in visited_nodes
                        over_budget = (cost(seq_copy) > budget)

                        return not over_budget

                    #removes any new children if from the child if they go over budget or are invalid action
                    new_unpicked_child_actions = [a for a in new_unpicked_child_actions if node_is_valid(a)]

                    ##EXPANSION
                    new_child_node = TreeNode(parent=current, sequence=new_sequence, budget=new_budget_left, unpicked_child_actions=new_unpicked_child_actions)
                    current.children.append(new_child_node)
                    current = new_child_node
                    list_of_all_nodes.append(new_child_node) # for debugging only
                    break # don't go deeper in the tree...
                else:
                    del current.unpicked_child_actions[child_index]
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
                    if not current.children:
                        break
                    else:
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
                        current = best_child

        ################################
        # Rollout
        # print("Rollout Phase")
        rollout_sequence = uniform_rollout(path=current.sequence, robot=robot, budget=budget)
        # rollout_sequence = heuristic_rollout(path=current.sequence, robot=robot, budget=budget, map=world_map)
        rollout_reward = reward(action_sequence=rollout_sequence, robot=robot, map=world_map)

        ################################
        # Back-propagation
        # update stats of all nodes from current back to root node
        # print("Back-Propagation Phase")
        parent = current
        while parent: # is not None
            # Update the average
            parent.updateAverage(rollout_reward)
            # Recurse up the tree
            parent = parent.parent

    ################################
    # Extract solution
    # calculate best solution so far
    # by recursively choosing child with highest average reward
    current = root
    while current.children: # is not empty
        # Find the child with best score
        best_score = 0
        best_child = -1
        for child_idx in range(len(current.children)):
            child = current.children[child_idx]
            score = child.average_evaluation_score
            if best_child == -1 or (score > best_score):
                best_child = child
                best_score = score
        current = best_child

    solution = current.sequence
    winner = current

    return [solution, list_of_all_nodes, winner]