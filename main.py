from mcts import mcts
from Map import Map
from Robot import Robot
from Simulator import Simulator


if __name__ == "__main__":
    #Create robots to interact with the environment
    budget = 500
    bounds = (0, 10)
    max_iterations = 5000
    world = Map(bounds)
    robot = Robot(bounds, world)
    robots = [robot]

    #Generate a path the robots (Dec-MCTS goes here)
    for r in robots:
        # Solve it with MCTS
        exploration_exploitation_parameter = .1 # =1.0 is recommended. <1.0 more exploitation. >1.0 more exploration.
        [mcts_path, list_of_all_nodes, winner] = mcts(budget, max_iterations, exploration_exploitation_parameter, robot, world)

        # Display the tree
        print("MCTS Solution")
        # plotTree(list_of_all_nodes, winner, False, budget, 1, exploration_exploitation_parameter)
        # plotTree(list_of_all_nodes, winner, True, budget, 2, exploration_exploitation_parameter)

        #Display path solution
        print("Path from MCTS", [p.location for p in mcts_path])
        print("Path Length: ", len(mcts_path))
        r.set_path(mcts_path)

    #Use the Simulator to evaluate the final paths
    simulator = Simulator(world, robots)
    simulator.run()

    #See the results
    simulator.visualize()
    print(simulator.get_score())
    print("Done :)")