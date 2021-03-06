from RandomPlanner import RandomPlanner
from Map import Map
from Robot import Robot
from Simulator import Simulator
# from mcts_planner import mcts_planner
from mcts import dec_mcts


if __name__ == "__main__":
    #Create robots to interact with the environment
    robot = Robot(0,0) #NOTE: I start it at 2,2 so you can see it in the visualization
    robots = [robot]
    #Generate random map
    world = Map(robots)

    # #Generate a path the robots (Dec-MCTS goes here)
    # for r in robots:
    #     # planner = RandomPlanner(10000)
    #     # random_path = planner.random_path(r)
    #     mcts_path = mcts_planner(r, world)  # run mcts algorithm | output = a path
    #     print("Path from MCTS", [p.location for p in mcts_path])
    #     print("Path Length: ", len(mcts_path))
    #     r.set_path(mcts_path)
    budget = 250
    exploration_exploitation_parameter = .2 # = 1.0 is recommended. <1.0 more exploitation. >1.0 more exploration.
    mcts_max_number_of_samples = 10
    computational_budget = 2
    dec_mcts_paths = dec_mcts(budget, mcts_max_number_of_samples, computational_budget, exploration_exploitation_parameter, robots, world) # TODO
    print("Number of Robot Paths: ", len(dec_mcts_paths))
    # r.set_path(mcts_path)

    # #Use the Simulator to evaluate the final paths
    simulator = Simulator(world, robots)
    simulator.run()

    # #See the results
    simulator.visualize()
    print(simulator.get_score())
    print("Done :)")