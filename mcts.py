from tree_node import TreeNode
from reward import reward
from cost import cost
from rollout import heuristic_rollout, uniform_rollout
from random import randint
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


def generate_neighbors(current_state, state_sequence, bounds):
    neighbors = list()
    current_loc = current_state.location
    sequence = [s.location for s in state_sequence]
    if current_loc[0]-1 >= bounds[0]:  # left
        new_loc = (current_loc[0]-1, current_loc[1])
        if not new_loc in sequence:
            neighbors.append(State(1, "left", new_loc))

    if current_loc[0]+1 <= bounds[1]:  # right
        new_loc = (current_loc[0]+1, current_loc[1])
        if not new_loc in sequence:
            neighbors.append(State(2, "right", new_loc))

    if current_loc[1]+1 <= bounds[1]:  # forwards
        new_loc = (current_loc[0], current_loc[1]+1)
        if not new_loc in sequence:
            neighbors.append(State(3, "forward", new_loc))

    if current_loc[1]-1 >= bounds[0]:  # backwards
        new_loc = (current_loc[0], current_loc[1]-1)
        if not new_loc in sequence:
            neighbors.append(State(4, "backwards", new_loc))

    return neighbors


def mcts_initialize(budget, robot, world_map):
    # Setup
    # robot = copy.deepcopy(robot)
    # world_map = copy.deepcopy(input_map)
    start_sequence = list()
    start_sequence = [State(1, "root", robot.start_loc)]
    unpicked_child_actions = generate_neighbors(
        start_sequence[0], start_sequence, world_map.bounds)

    return TreeNode(parent=None, sequence=start_sequence, budget=budget, unpicked_child_actions=unpicked_child_actions,
                    node_id=0)


def dec_mcts(budget, num_samples, computational_budget, explore_exploit, robots, input_map, rollout_policy='uniform'):
    world_map = copy.deepcopy(input_map)
    robot_paths = []

    # Initialize Every Robots MCTS Tree
    for robot in robots:
        # MCTS Tree initialization
        robot.root = mcts_initialize(budget, robot, world_map)

    # Start Dec-MCTS
    k = 0
    while k < computational_budget:  # Computational Budget
        # for p in range(computational_budget):
        #      if p % 100 == 0:
        #          print("Percent Complete: {:.2f}%".format(p / float(computational_budget) * 100))

        # print("Computational Budget: ", k)
        for i in range(num_samples):
            # Grow Tree for each Robot
            for robot in robots:
                # Robots determines their top 10 best sets of actions(sequences)
                # Selection and Expansion
                # move recursively down the tree from root
                # then add a new leaf node
                # print("Selection and Expansion")
                current = robot.root
                robot.reset_robot()

                while True:
                    # Are there any children to be added here?
                    if current.unpicked_child_actions:  # if not empty
                        # Pick one of the children that haven't been added | Select a valid direction
                        num_unpicked_child_actions = len(
                            current.unpicked_child_actions)
                        child_index = random.randint(
                            0, num_unpicked_child_actions - 1)
                        child_action = current.unpicked_child_actions[child_index]

                        # Move the robot
                        # Remove the child form the unpicked list
                        del current.unpicked_child_actions[child_index]

                        # Setup the new action sequence
                        new_sequence = copy.deepcopy(current.sequence)
                        new_sequence.append(child_action)
                        new_budget_left = budget - cost(new_sequence)

                        # Setup the new child's unpicked children
                        # Remove any over budget or invalid children from this set
                        new_unpicked_child_actions = generate_neighbors(child_action, new_sequence,
                                                                        world_map.bounds)

                        def node_is_valid(a):
                            seq_copy = copy.deepcopy(current.sequence)
                            seq_copy.append(a)
                            x, y = a.location
                            over_budget = (cost(seq_copy) > budget)

                            # Check invalid_locations from map
                            for loc in world_map.invalid_locations:
                                if x == loc[0] and y == loc[1]:
                                    return False

                            return not over_budget

                        # removes any new children if from the child if they go over budget or are invalid action
                        new_unpicked_child_actions = [
                            a for a in new_unpicked_child_actions if node_is_valid(a)]

                        # EXPANSION
                        new_child_node = TreeNode(parent=current, sequence=new_sequence, budget=new_budget_left,
                                                  unpicked_child_actions=new_unpicked_child_actions,
                                                  node_id=current.node_id + 1)

                        current.children.append(new_child_node)
                        current = new_child_node
                        # list_of_all_nodes.append(new_child_node)  # for debugging only
                        break  # don't go deeper in the tree...
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
                                return average + explore_exploit * math.sqrt((2 * math.log(n_parent)) / float(n_child))

                            # Pick the child that maximises the UCB
                            if not current.children:
                                break
                            else:
                                n_parent = current.num_updates
                                best_child = -1
                                best_ucb_score = 0
                                for child_idx in range(len(current.children)):
                                    child = current.children[child_idx]
                                    ucb_score = ucb(
                                        child.average_evaluation_score, n_parent, child.num_updates)
                                    if best_child == -1 or (ucb_score > best_ucb_score):
                                        best_child = child
                                        best_ucb_score = ucb_score

                                # Recurse down the tree
                                current = best_child

                ################################
                # Communications
                # Sample Action Sequences of other Robots
                # Pick one of the 10 sequences
                other_robots_paths = []
                for bot in robots:
                    randSequence = randint(0, 9)
                    if bot != robot and computational_budget == 0:
                        sampled_action_sequence = bot.top_10_sequences[randSequence]
                        other_robots_paths.append(sampled_action_sequence)

                ################################
                # Rollout & Reward
                rollout_sequence = list()
                if rollout_policy == 'uniform':
                    rollout_sequence = uniform_rollout(current.sequence, robot, budget)
                else:
                    rollout_sequence = heuristic_rollout(current.sequence, robot, budget, world_map)
                rollout_reward = reward(rollout_sequence, other_robots_paths, robot.sensing_range, world_map)

                ################################
                # Back-propagation
                # update stats of all nodes from current back to root node
                parent = current
                while parent:  # is not None
                    # Update the average
                    parent.updateAverage(rollout_reward)
                    # Recurse up the tree
                    parent = parent.parent

        # Extract 10 Best Sequences from Current Robot
        # append each to robot.
        for robot in robots:
            list_of_top_10_nodes_sequences = []  # for troubleshooting
            list_of_top_10_nodes_ids = []
            list_of_top_10_nodes = []  # for troubleshooting
            i = 0
            while i != 10:
                current = robot.root
                # is not empty
                while current.children and all_children_nodes_are_not_in_the_list(current, list_of_top_10_nodes_ids):
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

                # # for troubleshooting
                # # Append each iteration's node with the best average evaluation score
                # list_of_top_10_nodes_ids.append(current.node_id)
                # list_of_top_10_nodes.append(current)
                #
                # Append the the node's action sequence into a list
                # solution =   [p.location for p in current.sequence]
                # list_of_top_10_nodes_sequences.append(solution)
                robot.top_10_sequences.append(current.sequence)
                i += 1
        k += 1

    ################################
    # Extract best solution from all the ROBOTS
    # calculate best solution so far
    # by recursively choosing child with highest average reward

    for robot in robots:
        current = robot.root
        while current.children:  # is not empty
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
        robot.final_path = current.sequence

    for robot in robots:
        robot_paths.append(robot.final_path)

    return robot_paths


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


def listActionSequence(action_sequence):
    action_list = []
    for action in action_sequence:
        action_list.append(action.label)
    # print("MCTS Solution as Directions: ", action_list)
    return action_list


def direction_path_to_state_path_converter(solution, starting_coor):
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
