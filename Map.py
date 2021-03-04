import math
import sys
import numpy as np

class Map:
    def __init__(self, bounds):
        """
        Inputs:
            robot: list of robot objects from Robot.py
        """
        #NOTE: These values scale the difficulty of the problem
        self.num_survivors = 25
        self.num_hotspots = 10
        self.num_damages = 5

        self.bounds = bounds
        self.invalid_locations = list()
        self.hotspots = list()
        diff = self.bounds[1]*0.05

        #Simulate damage to environment
        for i in range(self.num_damages):
            tetris_id = np.random.randint(0, 2)
            x = int(np.random.uniform(self.bounds[0]+diff, self.bounds[1], size=1))
            y = int(np.random.uniform(self.bounds[0]+diff, self.bounds[1], size=1))

            if tetris_id == 0: #Square
                self.invalid_locations.append((x, y))
                self.invalid_locations.append((x+1, y))
                self.invalid_locations.append((x, y+1))
                self.invalid_locations.append((x+1, y+1))
            else: #Straight line
                self.invalid_locations.append((x, y))
                self.invalid_locations.append((x+1, y))
                self.invalid_locations.append((x+2, y))
                self.invalid_locations.append((x+3, y))

        #Randomly place people in the environment
        rand_x = np.random.uniform(self.bounds[0]+diff, self.bounds[1]-diff, size=self.num_hotspots*3)
        rand_y = np.random.uniform(self.bounds[0]+diff, self.bounds[1]-diff, size=self.num_hotspots*3)
        counter = 0
        for i in range(self.num_hotspots):
            #Generate a hotspot
            min_dist = 0.0
            hotspot = None
            while min_dist <= 2.0:
                rand_x = np.random.uniform(self.bounds[0]+diff, self.bounds[1]-diff, size=1)
                rand_y = np.random.uniform(self.bounds[0]+diff, self.bounds[1]-diff, size=1)
                hotspot = (rand_x[counter], rand_y[counter])
                min_dist = sys.maxsize

                for loc in self.invalid_locations:
                    dist = self.euclidean_distance(hotspot, loc)
                    if dist < min_dist:
                        min_dist = dist
            self.hotspots.append(hotspot)

        self.survivor_locs = list()
        for i in range(0, self.num_survivors):
            hotspot_id = np.random.randint(0, self.num_hotspots)
            hotspot_loc = self.hotspots[hotspot_id]

            rand_diff_x = np.random.uniform(-1.0, 1.0)
            rand_diff_y = np.random.uniform(-1.0, 1.0)
            survivor_loc = (hotspot_loc[0]+rand_diff_x, hotspot_loc[1]+rand_diff_y)
            self.survivor_locs.append(survivor_loc)

    def nearby_survivors(self, robots):
        visited_states = set()
        for r in robots:
            r_loc = r.get_loc()
            for s_loc in self.survivor_locs:
                distance = self.euclidean_distance(r_loc, s_loc)
                if distance <= r.sensing_range:
                    visited_states.add(s_loc)
        return visited_states

    @staticmethod
    def euclidean_distance(p1, p2):
        x1 = p1[0]
        y1 = p1[1]
        x2 = p2[0]
        y2 = p2[1]

        return math.sqrt((y2-y1)**2 + (x2-x1)**2)