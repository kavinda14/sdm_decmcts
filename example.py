from GreedyPlanner import GreedyPlanner
from RandomPlanner import RandomPlanner
from Map import Map
from Robot import Robot
from Simulator import Simulator


if __name__ == "__main__":
    #Create robots to interact with the environment
    bounds = (0, 25)
    world = Map(bounds)
    robot = Robot(bounds, world)
    robots = [robot]

    #Generate a path the robots (Dec-MCTS goes here)
    for r in robots:
        planner = GreedyPlanner(100)
        greed_path = planner.greedy_path(r, world)
        r.set_path(greed_path)
    print("Path from Greedy Planner", [p.location for p in greed_path])

    #Use the Simulator to evaluate the final paths
    simulator = Simulator(world, robots)
    simulator.run()

    # See the results
    simulator.visualize()
    print("Final Score: ", simulator.get_score())