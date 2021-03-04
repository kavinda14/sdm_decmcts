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
    # for r in robots:
    #     planner = RandomPlanner(1000)
    #     random_path = planner.random_path(r)
    #     r.set_path(random_path)
    # print("random_path: ", random_path)

    #Use the Simulator to evaluate the final paths
    simulator = Simulator(world, robots)
    simulator.run()

    # See the results
    simulator.visualize()
    print("Final Score: ", simulator.get_score())

    print('test')