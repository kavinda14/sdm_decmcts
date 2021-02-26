from RandomPlanner import RandomPlanner
from Map import Map
from Robot import Robot
from Simulator import Simulator
from main import run


if __name__ == "__main__":
    #Create robots to interact with the environment
    robot = Robot(2,2) #NOTE: I start it at 2,2 so you can see it in the visualization
    robots = [robot]
    #Generate random map
    world = Map(robots)


    #Generate a path the robots (Dec-MCTS goes here)
    for r in robots:
        # planner = RandomPlanner(10000)
        # random_path = planner.random_path(r)
        path = run(robot)  # run mcts algorithm | output = a path
        print("Path from MCTS", path)
        r.set_path(path)

    # #Use the Simulator to evaluate the final paths
    simulator = Simulator(world, robots)
    simulator.run()

    # #See the results
    simulator.visualize()
    print(simulator.get_score())
    print("Done :)")