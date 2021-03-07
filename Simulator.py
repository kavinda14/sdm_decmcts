import numpy as np

import matplotlib.pyplot as plt
import matplotlib.patches as patches

class Simulator:
    def __init__(self, world_map, robots):
        """
        Inputs:
        map_gt: The map to be explored
        robot: the Robot object from RobotClass.py
        """
        self.map = world_map
        self.robots = robots

        #Container to identify, which survivors have been seen by the robots
        self.visited_survivors = set()
        self._update_map()
        self.score = 0
        self.iterations = 0
        self.found_goal = False

    def run(self):
        duration = max([len(r.path) for r in self.robots])
        for x in range(0, duration):
            end = self.tick()
            if end:
                # if self.found_goal:
                #     print("Found goal at time step: {}!".format(self.get_iteration()))
                # else:
                #     print("Simulation timed out")
                break

    def tick(self):
        self.iterations += 1

        #Update the location of the robots
        for r in self.robots:
            # Generate an action from the robot path
            # action = r.follow_direction_path()
            action = r.follow_path()
            # Move the robot
            r.move(action)

        # Update the explored map based on robot position
        self._update_map()

        # Update the score
        self.score = len(self.visited_survivors)*25

        #End when all survivors have been reached OR 1,000 iterations
        if (len(self.visited_survivors) == self.map.num_survivors) or (self.iterations == 1000):
            self.found_goal = len(self.visited_survivors) == self.map.num_survivors
            return True
        else:
            return False

    def reset_game(self):
        self.iterations = 0
        self.score = 0

    def get_score(self):
        return self.score

    def get_iteration(self):
        return self.iterations

    def _update_map(self):
        # Sanity check the robot is in bounds
        for r in self.robots:
            if not r.check_valid_loc():
                raise ValueError(f"Robot has left the map. It is at position: {r.get_loc()}, outside of the (0-100, 0-100) map boundary")
        
        visited_states = self.map.nearby_survivors(self.robots)
        # Visited states are the visited survivors.
        self.visited_survivors = self.visited_survivors.union(visited_states)

    def visualize(self):
        plt.xlim(self.map.bounds[0]-.5, self.map.bounds[1]+(self.map.bounds[1]*.05))
        plt.ylim(self.map.bounds[0]-.5, self.map.bounds[1]+(self.map.bounds[1]*.05))
        ax = plt.gca()

        survivor_x = [i[0] for i in self.map.survivor_locs]
        survivor_y = [i[1] for i in self.map.survivor_locs]
        plt.scatter(survivor_x, survivor_y, color='tab:red')


        survivor_x = [i[0] for i in self.visited_survivors]
        survivor_y = [i[1] for i in self.visited_survivors]
        plt.scatter(survivor_x, survivor_y, color='tab:green')

        hotspot_x = [i[0] for i in self.map.hotspots]
        hotspot_y = [i[1] for i in self.map.hotspots]
        plt.scatter(hotspot_x, hotspot_y, color='black', marker="x")

        for r in self.robots:
            robot_x = [p.location[0] for p in r.path]
            robot_y = [p.location[1] for p in r.path]
            plt.plot(robot_x, robot_y)

        plt.show()
